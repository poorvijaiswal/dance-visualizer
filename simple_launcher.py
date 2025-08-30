"""
Simple One-Click Launcher for Dance Visualizer
Automatically handles virtual environment and dependencies
"""

import os
import sys
import subprocess

def main():
    print("🕺 Dance Visualizer Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found!")
        print("Make sure you're in the dance_visualiser directory")
        input("Press Enter to exit...")
        return
    
    # Check if virtual environment exists
    venv_path = "venv"
    if os.path.exists(venv_path):
        print("✅ Virtual environment found")
        
        # Get python executable from venv
        if os.name == 'nt':  # Windows
            python_exe = os.path.join(venv_path, "Scripts", "python.exe")
        else:  # Linux/Mac
            python_exe = os.path.join(venv_path, "bin", "python")
    else:
        print("⚠️ No virtual environment found, using system Python")
        python_exe = sys.executable
    
    try:
        print("🚀 Starting Dance Visualizer...")
        
        # Run the main visualizer
        subprocess.run([python_exe, "main.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running visualizer: {e}")
        print("\n🔧 Try installing dependencies:")
        print(f"{python_exe} -m pip install opencv-python mediapipe pygame numpy")
    except FileNotFoundError:
        print(f"❌ Python not found at: {python_exe}")
        print("Please check your Python installation")
    except KeyboardInterrupt:
        print("\n👋 Visualizer stopped by user")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
