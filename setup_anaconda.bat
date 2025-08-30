@echo off
title Dance Visualizer - Anaconda Setup
color 0A

echo ================================================
echo    DANCE VISUALIZER - ANACONDA SETUP
echo ================================================
echo.

echo [INFO] Installing dependencies in Anaconda environment...
conda install -c conda-forge opencv -y
conda install -c conda-forge mediapipe -y
pip install streamlit numpy

echo.
echo [INFO] Starting Dance Visualizer...
echo [INFO] Open browser: http://localhost:8501
echo.

streamlit run web_interface.py --server.port 8501

pause
