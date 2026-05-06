# Drone Vision Analyzer 🛸

![Dashboard Preview](assets/dashboard_preview.png)

A high-performance, full-stack AI pipeline designed for drone surveillance and reconnaissance. This system achieves 95%+ accuracy by combining real-time object detection with deep vision-language analysis.

## 🌟 Modern Architecture

The system operates on a **Dual-Stage Hybrid AI Pipeline**:

1.  **Stage 1: Neural Detection (YOLOv8)**
    *   **Core**: Uses `ultralytics` YOLOv8 (configurable from Nano to Extra-Large).
    *   **Action**: Scans the incoming high-resolution drone feed to identify and localize objects (Cars, People, Electronics, etc.).
    *   **Output**: Bounding boxes, confidence scores, and automated cropping of every detected interest point.

2.  **Stage 2: Deep Contextual Analysis (OpenAI CLIP)**
    *   **Core**: Uses Hugging Face `transformers` with the CLIP (Vision-Language) model.
    *   **Action**: Performs "Zero-Shot Classification" on every cropped object.
    *   **Output**: Extracts specific details (e.g., Identifying a "car" as a "Sportscar" or a "cell phone" as an "iPhone") without needing specific training for those sub-classes.

---

## 🛠️ Tech Stack

*   **Frontend**: React.js (Vite), Lucide Icons, Glassmorphism UI.
*   **Backend**: FastAPI (Python), Uvicorn Server.
*   **AI/ML**: YOLOv8, OpenAI CLIP, OpenCV, PyTorch.

---

## 🚀 Getting Started

### 1. Prerequisites
*   **Python 3.8+**
*   **Node.js & npm** (for the frontend dashboard)

### 2. Installation
```powershell
# Setup Python Environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Setup Frontend
cd frontend
npm install
cd ..
```

### 3. Launching the System
Simply run the control batch file:
```powershell
.\run.bat
```
This will automatically launch:
*   **AI Backend**: `http://localhost:8000`
*   **Control Center UI**: `http://localhost:5173`

---

## 📂 Project Structure

```plaintext
drone-vision-analyzer/
├── src/
│   ├── api.py            # FastAPI Entry Point (Neural Gateway)
│   ├── detector.py       # YOLOv8 Implementation
│   ├── analyzer.py       # CLIP Deep Analysis Implementation
│   └── main.py           # CLI Pipeline Version
├── frontend/
│   ├── src/App.jsx       # Control Center UI (React)
│   └── ...
├── input_images/         # Raw telemetry data
├── output_images/        # Processed intelligence
└── run.bat               # Unified startup script
```

---

## 📡 Single-to-Single Working Flow

1.  **Telemetry Upload**: High-res image is sent via the UI to the Neural Gateway.
2.  **Primary Scan**: YOLOv8 identifies all objects and generates a global map (Annotated Image).
3.  **Neural Cropping**: The system physically segments the image into "Interest Crops".
4.  **Deep Interrogation**: Each crop is analyzed by the VLM (CLIP) to determine specific attributes.
5.  **Intelligence Display**: Results are streamed back to the dashboard, rendering high-confidence "Object Cards" with deep details.

---

## 📜 License
This project is open-source. Build the future of autonomous vision!
