from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
import uuid
import logging
from detector import ObjectDetector
from analyzer import ImageAnalyzer
from config import OUTPUT_DIR, DETECTION_CONFIDENCE

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Drone Vision API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models once
logger.info("Loading AI models...")
detector = ObjectDetector()
analyzer = ImageAnalyzer()

# Ensure directories exist
TEMP_INPUT_DIR = os.path.join(os.path.dirname(OUTPUT_DIR), "temp_input")
os.makedirs(TEMP_INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static files to serve images
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Receives an image, runs detection and analysis, and returns the results.
    """
    try:
        # 1. Save uploaded file
        file_extension = os.path.splitext(file.filename)[1]
        unique_id = str(uuid.uuid4())
        input_path = os.path.join(TEMP_INPUT_DIR, f"{unique_id}{file_extension}")
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Processing uploaded image: {file.filename}")

        # 2. Run Object Detection
        # We'll use a unique output sub-dir for this request to avoid collisions
        request_output_dir = os.path.join(OUTPUT_DIR, unique_id)
        os.makedirs(request_output_dir, exist_ok=True)
        
        objects, annotated_img_path = detector.detect_and_crop(input_path, output_dir=request_output_dir)
        
        # 3. Run Global Scene Analysis
        scene_analysis = analyzer.analyze_scene(input_path)
        
        # 4. Run Deep Analysis on Objects
        results = []
        for obj in objects:
            if obj["confidence"] > DETECTION_CONFIDENCE:
                details = analyzer.analyze_product(obj["crop_path"], obj["label"])
                obj.update(details)
                # Convert absolute paths to relative URLs for the frontend
                obj["crop_url"] = f"/outputs/{unique_id}/{os.path.basename(obj['crop_path'])}"
            else:
                obj["specific_detail"] = "skipped (low confidence)"
                obj["detail_confidence"] = 0.0
                obj["crop_url"] = f"/outputs/{unique_id}/{os.path.basename(obj['crop_path'])}"
            
            results.append(obj)

        return {
            "id": unique_id,
            "filename": file.filename,
            "annotated_url": f"/outputs/{unique_id}/{os.path.basename(annotated_img_path)}",
            "scene": scene_analysis,
            "objects": results
        }

    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
