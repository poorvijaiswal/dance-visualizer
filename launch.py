"""
Dance Visualizer Launcher

Starts both the web interface and the main visualizer application.
"""

import subprocess
import sys
import time
import webbrowser
from threading import Thread

def start_web_interface():
    """Start the Streamlit web interface"""
    subprocess.run([sys.executable, "-m", "streamlit", "run", "web_interface.py"])

def start_visualizer():
    """Start the main visualizer after a delay"""
    time.sleep(3)  # Wait for web interface to start
    print("Starting main visualizer...")
    subprocess.run([sys.executable, "main.py"])

def main():
    print("🚀 Launching Dance Performance Visualizer...")
    print("📱 Starting web interface...")
    
    # Start web interface in a separate thread
    web_thread = Thread(target=start_web_interface, daemon=True)
    web_thread.start()
    
    # Wait a moment then open browser
    time.sleep(2)
    webbrowser.open("http://localhost:8501")
    
    print("🎮 Starting main application...")
    print("Use the web interface to control settings!")
    
    # Start main visualizer
    start_visualizer()

if __name__ == "__main__":
    main()
