import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    print("Testing imports...")
    from detector import ObjectDetector
    from analyzer import ImageAnalyzer
    print("Imports successful!")
    
    print("Initializing Detector...")
    detector = ObjectDetector()
    print("Detector initialized!")
    
    print("Initializing Analyzer...")
    analyzer = ImageAnalyzer()
    print("Analyzer initialized!")
    
    print("SUCCESS: All models loaded correctly.")
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
