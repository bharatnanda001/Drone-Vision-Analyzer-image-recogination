from transformers import pipeline
from PIL import Image
import logging
from config import ANALYSIS_MODEL, CANDIDATE_LABELS, SCENE_LABELS

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    def __init__(self, model_name=ANALYSIS_MODEL):
        logger.info(f"Initializing deep analyzer with model: {model_name}")
        self.classifier = pipeline("zero-shot-image-classification", model=model_name)

    def analyze_scene(self, image_path):
        """
        Analyzes the entire image to determine the overall theme/scene.
        """
        try:
            image = Image.open(image_path)
            logger.info("Performing global scene analysis...")
            results = self.classifier(image, candidate_labels=SCENE_LABELS)
            
            best_match = results[0]
            return {
                "theme": best_match['label'],
                "theme_confidence": best_match['score']
            }
        except Exception as e:
            logger.error(f"Scene analysis failed: {e}")
            return {"theme": "unknown", "theme_confidence": 0.0}

    def analyze_product(self, image_path, base_label):
        """
        Takes the cropped image and tries to extract deeper details based on what it is.
        """
        try:
            image = Image.open(image_path)
            
            # Map base labels to candidate labels from config
            candidate_labels = CANDIDATE_LABELS.get(base_label, CANDIDATE_LABELS["default"])

            logger.info(f"Performing deep analysis for '{base_label}'...")
            results = self.classifier(image, candidate_labels=candidate_labels)
            
            best_match = results[0]
            return {
                "specific_detail": best_match['label'],
                "detail_confidence": best_match['score']
            }
        except Exception as e:
            logger.error(f"Analysis failed for {image_path}: {e}")
            return {
                "specific_detail": "unknown",
                "detail_confidence": 0.0
            }
