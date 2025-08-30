@echo off
title Dance Visualizer - Stable Interface
color 0B

echo ============================================
echo      DANCE PERFORMANCE VISUALIZER
echo ============================================
echo.

REM Check if running in Anaconda
if defined CONDA_DEFAULT_ENV (
    echo [INFO] Anaconda environment detected: %CONDA_DEFAULT_ENV%
    echo [INFO] Installing dependencies via conda and pip...
    conda install -c conda-forge opencv -y
    pip install --quiet mediapipe streamlit numpy
) else (
    REM Check for venv
    if exist "venv\Scripts\activate.bat" (
        echo [INFO] Activating virtual environment...
        call venv\Scripts\activate
    ) else (
        echo [INFO] Creating virtual environment...
        python -m venv venv
        call venv\Scripts\activate
    )
    
    echo [INFO] Installing dependencies via pip...
    pip install --quiet --upgrade opencv-python mediapipe streamlit numpy
)

echo.
echo [INFO] Starting Stable Web Interface...
echo.
echo ============================================
echo  Open browser: http://localhost:8501
echo  Click START to begin visualization
echo  Use lower FPS if experiencing issues
echo  Press Ctrl+C here to stop server
echo ============================================
echo.

REM Start with optimized settings to prevent media file errors
streamlit run web_interface.py --server.headless true --server.port 8501 --server.maxUploadSize 10 --server.enableCORS false

echo.
echo [INFO] Dance Visualizer stopped.
pause
