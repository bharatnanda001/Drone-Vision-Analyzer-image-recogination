from ultralytics import YOLO
import cv2
import os
import logging
from config import OUTPUT_DIR, DETECTION_MODEL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ObjectDetector:
    def __init__(self, model_size=DETECTION_MODEL):
        logger.info(f"Initializing YOLO detector with model: {model_size}")
        self.model = YOLO(model_size) 

    def detect_and_crop(self, image_path, output_dir=OUTPUT_DIR):
        if not os.path.isabs(image_path):
            image_path = os.path.abspath(image_path)

        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Failed to load image at: {image_path}")
            raise ValueError(f"Could not read image at {image_path}")

        logger.info(f"Running detection on {os.path.basename(image_path)}...")
        results = self.model(image, verbose=False, imgsz=320)[0]
        detected_objects = []

        os.makedirs(output_dir, exist_ok=True)

        for i, box in enumerate(results.boxes):
            # Extract coordinates and confidence
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]

            # Ensure crop coordinates are within image boundaries
            h, w, _ = image.shape
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            # Crop the detected object
            cropped_img = image[y1:y2, x1:x2]
            if cropped_img.size == 0:
                continue

            crop_filename = os.path.join(output_dir, f"crop_{i}_{class_name}.jpg")
            cv2.imwrite(crop_filename, cropped_img)

            detected_objects.append({
                "label": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
                "crop_path": crop_filename
            })

            # Draw bounding box on the original image
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{class_name} {confidence:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the full annotated image
        annotated_path = os.path.join(output_dir, "annotated_full_image.jpg")
        cv2.imwrite(annotated_path, image)
        logger.info(f"Detection complete. Found {len(detected_objects)} objects.")

        return detected_objects, annotated_path
