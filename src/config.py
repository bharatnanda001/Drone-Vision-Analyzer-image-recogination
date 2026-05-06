import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model Settings
DETECTION_MODEL = 'yolov8n.pt'  # Options: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
ANALYSIS_MODEL = 'openai/clip-vit-base-patch32'

# Thresholds
DETECTION_CONFIDENCE = 0.3
ANALYSIS_CONFIDENCE = 0.5

# Directories
INPUT_DIR = os.path.join(BASE_DIR, 'input_images')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_images')

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Deep Analysis Labels
CANDIDATE_LABELS = {
    "cell phone": ["an iPhone", "an Android phone", "a flip phone", "a smartphone with a cracked screen"],
    "car": ["a sedan", "an SUV", "a pickup truck", "a sports car"],
    "person": ["a pilot", "a bystander", "someone waving", "someone sitting"],
    "laptop": ["a MacBook", "a Windows laptop", "a gaming laptop"],
    "truck": ["a delivery truck", "a semi-trailer", "a cement mixer", "a fire engine"],
    "motorcycle": ["a sportbike", "a cruiser", "a scooter", "a dirt bike"],
    "building": ["a skyscraper", "a residential house", "a factory", "a warehouse"],
    "dog": ["a golden retriever", "a german shepherd", "a bulldog", "a poodle"],
    "default": ["brand new", "used and old", "metallic", "plastic"]
}

# Global Theme Analysis Labels
SCENE_LABELS = [
    "an urban city street",
    "a busy highway with traffic",
    "a quiet residential neighborhood",
    "a dense forest area",
    "a shipping port or industrial zone",
    "a construction site",
    "a park or recreational area",
    "an indoor office environment",
    "a parking lot",
    "a rural farmland"
]
