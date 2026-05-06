import sys
import os

# Ensure the root and src are in path for both the script and the IDE
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, 'src'))

try:
    print("--- Drone Vision: System Health Check ---")
    
    print("[1/3] Verifying Module Imports...")
    # These imports are now easily resolvable by the IDE when the script is in the root
    from detector import ObjectDetector
    from analyzer import ImageAnalyzer
    print("      ✓ Modules imported successfully.")
    
    print("[2/3] Initializing YOLOv8 Detector...")
    detector = ObjectDetector()
    print("      ✓ Detector initialized and weights loaded.")
    
    print("[3/3] Initializing CLIP Analyzer...")
    analyzer = ImageAnalyzer()
    print("      ✓ Analyzer initialized.")
    
    print("\n[RESULT] System is HEALTHY. All AI models are operational.")
    
except Exception as e:
    print(f"\n[ERROR] System check failed: {e}")
    sys.exit(1)
