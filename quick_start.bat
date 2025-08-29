@echo off
echo === Dance Visualizer Quick Start ===

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo Starting web interface in 3 seconds...
echo You can then use the web interface to start the main visualizer.
echo.
echo Open your browser to: http://localhost:8501
echo.
timeout /t 3

start "" streamlit run web_interface.py

echo Web interface started!
echo To start the main visualizer:
echo   1. Use the web interface "Start Visualizer" button, OR
echo   2. Open a new command prompt and run: python main.py
echo.
pause
