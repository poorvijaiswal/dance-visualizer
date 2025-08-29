@echo off
echo Starting Dance Visualizer Web Interface...

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing Streamlit...
    pip install streamlit
)

echo Starting Streamlit server...
echo Open your browser to: http://localhost:8501
echo Press Ctrl+C to stop the server

streamlit run web_interface.py --server.port 8501 --server.address localhost

pause
