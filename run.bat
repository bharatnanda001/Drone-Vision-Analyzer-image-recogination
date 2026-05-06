@echo off
echo ===================================================
echo   DRONE VISION ANALYZER - CONTROL CENTER
echo ===================================================

:: 1. Start Backend (FastAPI)
echo [1/2] Starting AI Backend (FastAPI)...
start "Drone AI Backend" cmd /k "cd /d %~dp0 && .\venv\Scripts\python.exe src\api.py"

:: 2. Start Frontend (Vite)
echo [2/2] Starting Control Center UI (Vite)...
cd /d %~dp0\frontend
start "Drone UI Frontend" cmd /k "npm run dev"

echo.
echo ---------------------------------------------------
echo   SERVICES STARTING...
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:5173
echo ---------------------------------------------------
echo.
echo Keep both windows open for the application to function.
pause
