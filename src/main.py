import argparse
import os
import logging
from detector import ObjectDetector
from analyzer import ImageAnalyzer
from config import INPUT_DIR, DETECTION_CONFIDENCE

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_image(image_path):
    logger.info(f"--- Pipeline Started: {os.path.basename(image_path)} ---")
    
    # 1. Initialize models
    detector = ObjectDetector()
    analyzer = ImageAnalyzer()

    # 2. Run Object Detection
    objects, annotated_img_path = detector.detect_and_crop(image_path)
    
    # 3. Run Deep Analysis on each detected object
    for obj in objects:
        if obj["confidence"] > DETECTION_CONFIDENCE: 
            logger.info(f"Analyzing {obj['label']} (Conf: {obj['confidence']:.2f})...")
            
            details = analyzer.analyze_product(obj["crop_path"], obj["label"])
            
            print(f"\n[DETAIL FOUND] Object: {obj['label']}")
            print(f"  -> Specific Detail: {details['specific_detail']}")
            print(f"  -> Detail Confidence: {details['detail_confidence']:.2f}")
        else:
            logger.warning(f"Low confidence ({obj['confidence']:.2f}) for {obj['label']}. Skipping analysis.")

    logger.info("--- Pipeline Completed ---")
    print(f"\nResults saved to output_images/ folder.")
    print(f"Annotated image: {annotated_img_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drone Vision Analyzer Pipeline")
    parser.add_argument("--image", type=str, help="Path to the image file to analyze")
    args = parser.parse_args()

    if args.image:
        test_image = args.image
    else:
        # Default to test.jpg in input_images
        test_image = os.path.join(INPUT_DIR, "test.jpg")

    if os.path.exists(test_image):
        process_image(test_image)
    else:
        logger.error(f"Image not found at {test_image}. Please provide a valid image path.")
