@echo off
echo Setting up Dance Visualizer environment...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

echo.
echo Setup complete! To run the visualizer:
echo 1. venv\Scripts\activate
echo 2. python main.py
pause
