@echo off
echo Activating virtual environment and starting Dance Visualizer...

REM Activate virtual environment
call venv\Scripts\activate

REM Run the application
python main.py

pause
