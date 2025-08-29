"""
Dance Performance Visualizer - Web Interface

Streamlit-based web interface for configuring and controlling the dance visualizer.
Runs alongside the main pygame application.
"""

import streamlit as st
import json
import os
import subprocess
import threading
import time
from typing import Dict, Any

class VisualizerConfig:
    def __init__(self):
        self.config_file = "visualizer_config.json"
        self.default_config = {
            "particle_count": 50,
            "trail_length": 15,
            "sensitivity": 5.0,
            "color_scheme": "energetic",
            "background_effects": True,
            "gesture_detection": True,
            "fullscreen": False,
            "video_overlay": True,
            "fps_target": 30
        }
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = self.default_config.copy()
        else:
            self.config = self.default_config.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save_config()

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe', 
        'pygame': 'pygame',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
        except ImportError:
            missing_packages.append(package_name)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    missing = check_dependencies()
    if missing:
        st.warning(f"Missing dependencies: {', '.join(missing)}")
        if st.button("🔧 Install Missing Dependencies"):
            try:
                import sys
                import subprocess
                
                for package in missing:
                    st.info(f"Installing {package}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                
                st.success("✅ All dependencies installed! Try starting the visualizer again.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to install dependencies: {e}")
                st.info("Please run manually: pip install opencv-python mediapipe pygame numpy")

def main():
    st.set_page_config(
        page_title="Dance Visualizer Control",
        page_icon="🕺",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .control-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .status-running { background-color: #28a745; }
    .status-stopped { background-color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🕺 Dance Performance Visualizer</h1>
        <p>Control Panel & Configuration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize config
    config = VisualizerConfig()
    
    # Sidebar for main controls
    with st.sidebar:
        st.header("🎮 Main Controls")
        
        # Check dependencies first
        missing_deps = check_dependencies()
        if missing_deps:
            st.error(f"❌ Missing: {', '.join(missing_deps)}")
            install_dependencies()
        else:
            st.success("✅ All dependencies installed")
        
        # Visualizer status
        if st.button("🚀 Start Visualizer", type="primary"):
            start_visualizer()
        
        if st.button("⏹️ Stop Visualizer"):
            stop_visualizer()
        
        st.markdown("---")
        
        # Quick presets
        st.header("🎨 Quick Presets")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌊 Calm Mode"):
                apply_preset(config, "calm")
                st.success("Calm mode applied!")
        
        with col2:
            if st.button("🔥 Energetic Mode"):
                apply_preset(config, "energetic")
                st.success("Energetic mode applied!")
        
        if st.button("🌈 Party Mode"):
            apply_preset(config, "party")
            st.success("Party mode applied!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("⚙️ Visual Configuration")
        
        # Visual Effects Section
        with st.expander("🎨 Visual Effects", expanded=True):
            config.set("particle_count", 
                      st.slider("Particle Count", 10, 200, config.get("particle_count"), 5))
            
            config.set("trail_length", 
                      st.slider("Trail Length", 5, 50, config.get("trail_length")))
            
            config.set("sensitivity", 
                      st.slider("Movement Sensitivity", 1.0, 10.0, config.get("sensitivity"), 0.5))
            
            config.set("color_scheme", 
                      st.selectbox("Color Scheme", 
                                 ["energetic", "calm", "neutral", "rainbow"], 
                                 index=["energetic", "calm", "neutral", "rainbow"].index(config.get("color_scheme"))))
        
        # Detection Settings
        with st.expander("🤖 Detection Settings"):
            config.set("gesture_detection", 
                      st.checkbox("Enable Gesture Detection", config.get("gesture_detection")))
            
            config.set("background_effects", 
                      st.checkbox("Background Effects", config.get("background_effects")))
            
            config.set("fps_target", 
                      st.slider("Target FPS", 15, 60, config.get("fps_target")))
        
        # Display Settings
        with st.expander("🖥️ Display Settings"):
            config.set("fullscreen", 
                      st.checkbox("Fullscreen Mode", config.get("fullscreen")))
            
            config.set("video_overlay", 
                      st.checkbox("Show Video Overlay", config.get("video_overlay")))
    
    with col2:
        st.header("📊 Status & Info")
        
        # Check if visualizer files exist and show status
        required_files = ['main.py', 'pose_module.py', 'visuals.py']
        all_files_exist = all(os.path.exists(f) for f in required_files)
        
        if all_files_exist:
            status_text = "✅ Ready to Start"
            status_class = "status-running"
        else:
            status_text = "❌ Missing Files"
            status_class = "status-stopped"
        
        st.markdown(f"""
        <div class="control-section">
            <h4>📁 Project Status</h4>
            <div>
                <span class="status-indicator {status_class}"></span>
                <span>{status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show file status
        st.subheader("📁 Required Files")
        for file in required_files:
            status = "✅" if os.path.exists(file) else "❌"
            st.write(f"{status} {file}")
        
        # Current configuration
        st.subheader("📋 Current Config")
        st.json(config.config)
        
        # Performance metrics (placeholder)
        st.subheader("📈 Performance")
        col_fps, col_particles = st.columns(2)
        with col_fps:
            st.metric("FPS", "30", "0")
        with col_particles:
            st.metric("Particles", "156", "+12")
        
        # Help section
        st.subheader("❓ Help")
        st.info("""
        **Controls:**
        - V: Toggle video window
        - F: Toggle fullscreen
        - Q: Quit application
        
        **Gestures:**
        - Hands up: Explosions
        - Arms wide: Line effects
        - Jump: Fireworks
        """)

def apply_preset(config: VisualizerConfig, preset_name: str):
    """Apply predefined configuration presets"""
    presets = {
        "calm": {
            "particle_count": 30,
            "trail_length": 20,
            "sensitivity": 3.0,
            "color_scheme": "calm",
            "background_effects": True
        },
        "energetic": {
            "particle_count": 100,
            "trail_length": 10,
            "sensitivity": 8.0,
            "color_scheme": "energetic",
            "background_effects": True
        },
        "party": {
            "particle_count": 150,
            "trail_length": 15,
            "sensitivity": 10.0,
            "color_scheme": "rainbow",
            "background_effects": True
        }
    }
    
    if preset_name in presets:
        for key, value in presets[preset_name].items():
            config.set(key, value)

def start_visualizer():
    """Start the main visualizer application"""
    try:
        # Check dependencies first
        missing_deps = check_dependencies()
        if missing_deps:
            st.error(f"❌ Missing dependencies: {', '.join(missing_deps)}")
            st.info("Click 'Install Missing Dependencies' button above to fix this.")
            return
        
        # Check if required files exist
        if not os.path.exists("main.py"):
            st.error("❌ main.py not found! Make sure you're in the correct directory.")
            return
        
        # Start the process with better error handling
        import sys
        process = subprocess.Popen(
            [sys.executable, "main.py"], 
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        # Wait a moment to check if process starts successfully
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            st.success("✅ Visualizer process started!")
        else:
            # Process died, get error output
            stdout, stderr = process.communicate()
            st.error("❌ Visualizer failed to start!")
            if stderr:
                st.error(f"Error: {stderr.decode()}")
            if stdout:
                st.info(f"Output: {stdout.decode()}")
        
        st.info("🎮 **Look for a separate Pygame window** with the title 'Dance Performance Visualizer'")
        st.info("📹 **Position yourself in front of your camera** to see the dance effects!")
        
        # Add manual command option
        st.markdown("""
        ### 🔧 If window still doesn't appear, try manually:
        1. **Open a new Command Prompt/PowerShell**
        2. **Navigate to project folder:**
           ```
           cd c:\\Users\\Poorvi\\Desktop\\dance_visualiser
           ```
        3. **Activate virtual environment:**
           ```
           venv\\Scripts\\activate
           ```
        4. **Run visualizer directly:**
           ```
           python main.py
           ```
        
        ### 🎯 What to expect:
        1. **Pygame Window**: A separate black window should open showing visual effects
        2. **Camera Feed**: Small video window in the corner showing your pose detection
        3. **Real-time Effects**: Particles and colors that respond to your movements
        
        ### 🕺 Try these gestures:
        - **Raise both hands above your head** → Particle explosions
        - **Spread your arms wide** → Connecting line effects  
        - **Jump up** → Fireworks burst
        """)
        
    except Exception as e:
        st.error(f"❌ Failed to start visualizer: {e}")
        
        # Show troubleshooting steps
        st.markdown("""
        ### 🔧 Troubleshooting Steps:
        
        **Option 1: Manual Terminal Method**
        1. Open **new** Command Prompt or PowerShell
        2. `cd c:\\Users\\Poorvi\\Desktop\\dance_visualiser`
        3. `venv\\Scripts\\activate`
        4. `python main.py`
        
        **Option 2: Check for errors**
        1. Look at the terminal where Streamlit is running
        2. Check for any error messages
        
        **Option 3: Install missing dependencies**
        ```
        pip install opencv-python mediapipe pygame numpy
        ```
        """)

def stop_visualizer():
    """Stop the visualizer (placeholder - would need IPC)"""
    st.warning("Stop functionality requires implementing inter-process communication.")

if __name__ == "__main__":
    main()
