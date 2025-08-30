"""
Dance Performance Visualizer - Web Interface

Professional Streamlit-based web interface for configuring and controlling the dance visualizer.
"""

import streamlit as st
import json
import os
import subprocess
import threading
import time
import numpy as np
from typing import Dict, Any

# Configure page settings
st.set_page_config(
    page_title="Dance Performance Visualizer",
    page_icon="🕺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    .main > div {
        padding-top: 1rem;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        color: #1f2937;
    }
    
    /* Header styles */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Card styles */
    .status-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
    }
    
    /* Button styles */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 0.5rem;
        transition: all 0.2s ease;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Sidebar styles */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Success/Error alerts */
    .success-alert {
        background: #ecfdf5;
        border: 1px solid #10b981;
        border-radius: 0.5rem;
        padding: 1rem;
        color: #065f46;
        margin: 1rem 0;
    }
    
    .error-alert {
        background: #fef2f2;
        border: 1px solid #ef4444;
        border-radius: 0.5rem;
        padding: 1rem;
        color: #991b1b;
        margin: 1rem 0;
    }
    
    /* Camera feed styles */
    .camera-container {
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border: 2px solid #e5e7eb;
    }
    
    /* Progress bar styles */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
    }
</style>
""", unsafe_allow_html=True)

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
            "show_skeleton": True,
            "effect_intensity": 0.7
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
    """Install missing dependencies with progress"""
    missing = check_dependencies()
    if missing:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            import sys
            for i, package in enumerate(missing):
                status_text.text(f"Installing {package}...")
                progress_bar.progress((i + 1) / len(missing))
                
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    st.error(f"Failed to install {package}: {result.stderr}")
                    return False
            
            st.success("✅ All dependencies installed successfully!")
            time.sleep(1)
            st.rerun()
            return True
            
        except Exception as e:
            st.error(f"Installation failed: {e}")
            st.info("Please install manually:")
            st.code("pip install opencv-python mediapipe numpy")
            return False

def main():
    # Initialize session state
    if 'visualizer_active' not in st.session_state:
        st.session_state.visualizer_active = False
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🕺 Dance Performance Visualizer</h1>
        <p class="header-subtitle">AI-Powered Real-Time Dance Analysis & Visualization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎮 Control Center")
        
        # Dependency check
        missing_deps = check_dependencies()
        if missing_deps:
            st.markdown(f"""
            <div class="error-alert">
                <strong>❌ Missing Dependencies</strong><br>
                {', '.join(missing_deps)}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔧 Auto-Install Dependencies", width="stretch"):  # Fixed
                if install_dependencies():
                    st.rerun()
        else:
            st.markdown("""
            <div class="success-alert">
                <strong>✅ All Systems Ready</strong><br>
                Camera and AI ready to go!
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Main controls with better feedback
        if not st.session_state.visualizer_active:
            if st.button("▶️ START VISUALIZER", width="stretch", type="primary"):  # Fixed
                if not missing_deps:  # Only start if all deps are available
                    st.session_state.visualizer_active = True
                    # Reset all session state
                    for key in ['frame_count', 'camera_initialized', 'pose_stats', 
                               'camera_placeholder', 'status_placeholder']:
                        if key in st.session_state:
                            del st.session_state[key]
                    # Clean up camera if exists
                    if 'camera' in st.session_state:
                        st.session_state.camera.release()
                        del st.session_state.camera
                    st.success("🎬 Starting visualizer...")
                    st.rerun()
                else:
                    st.error("Please install missing dependencies first!")
        else:
            if st.button("⏹️ STOP VISUALIZER", width="stretch", type="secondary"):  # Fixed
                st.session_state.visualizer_active = False
                # Clean up all resources
                if 'camera' in st.session_state:
                    st.session_state.camera.release()
                    del st.session_state.camera
                # Clear session state
                for key in ['frame_count', 'camera_initialized', 'pose_stats',
                           'camera_placeholder', 'status_placeholder']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.info("⏸️ Visualizer stopped")
                st.rerun()
        
        # Show simplified status
        frame_count = st.session_state.get('frame_count', 0)
        st.markdown(f"**Status:** 🟢 **LIVE** ({frame_count} frames)")
        
        st.markdown("---")
        
        # Quick presets
        st.markdown("## 🎨 Visual Presets")
        
        config = VisualizerConfig()
        
        if st.button("🌊 Calm Mode", width="stretch"):  # Fixed
            apply_preset(config, "calm")
            st.success("Calm mode activated!")
            
        if st.button("🔥 Energetic Mode", width="stretch"):  # Fixed
            apply_preset(config, "energetic")
            st.success("Energetic mode activated!")
            
        if st.button("🌈 Party Mode", width="stretch"):  # Fixed
            apply_preset(config, "party")
            st.success("Party mode activated!")
    
    # Main content
    if st.session_state.visualizer_active:
        run_web_visualizer()
    else:
        show_dashboard()

def run_web_visualizer():
    """Run the web-based visualizer with optimized refresh"""
    st.markdown("## 🎬 Live Dance Visualizer")
    
    # Check dependencies
    try:
        import cv2
        from pose_module import PoseDetector
    except ImportError as e:
        st.error(f"❌ Missing module: {e}")
        st.info("Please install: pip install opencv-python mediapipe")
        return
    
    # Initialize session state with optimization flags
    if 'frame_count' not in st.session_state:
        st.session_state.frame_count = 0
    if 'camera_initialized' not in st.session_state:
        st.session_state.camera_initialized = False
    if 'pose_stats' not in st.session_state:
        st.session_state.pose_stats = {'energy': 0, 'gestures': [], 'keypoints': 0}
    if 'last_stats_update' not in st.session_state:
        st.session_state.last_stats_update = 0
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    
    # Initialize camera once
    if not st.session_state.camera_initialized:
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ Cannot access camera")
                return
            
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 10)  # Lower FPS for stability
            
            st.session_state.camera = cap
            st.session_state.pose_detector = PoseDetector()
            st.session_state.pose_detector.set_screen_dimensions(640, 480)
            st.session_state.camera_initialized = True
            
        except Exception as e:
            st.error(f"❌ Camera failed: {e}")
            return
    
    # Create layout with persistent containers
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📹 Live Camera Feed")
        video_container = st.container()
    
    with col2:
        st.markdown("### 📊 Live Stats")
        stats_container = st.container()
        
        st.markdown("### 🎮 Controls")
        
        # Control buttons
        col_a, col_b = st.columns(2)
        with col_a:
            auto_mode = st.toggle("Auto Refresh", st.session_state.auto_refresh)
            st.session_state.auto_refresh = auto_mode
        
        with col_b:
            manual_refresh = st.button("🔄 Refresh", width="stretch")  # Fixed
        
        # FPS control
        fps_value = st.slider("FPS", 1, 15, 5, help="Lower = more stable")
        
        # Reset camera
        if st.button("🎥 Reset Camera", width="stretch"):  # Fixed
            if 'camera' in st.session_state:
                st.session_state.camera.release()
            st.session_state.camera_initialized = False
            st.rerun()
    
    # Process frame only when needed
    should_process = (
        st.session_state.auto_refresh or 
        manual_refresh or 
        st.session_state.frame_count == 0
    )
    
    if should_process:
        cap = st.session_state.camera
        pose_detector = st.session_state.pose_detector
        config = VisualizerConfig()
        
        try:
            ret, frame = cap.read()
            
            if ret:
                # Process frame
                frame = cv2.flip(frame, 1)
                pose_data = pose_detector.detect_pose(frame)
                
                # Add effects
                if config.get("show_skeleton", True) and pose_data.get('landmarks'):
                    frame = pose_detector.draw_pose(frame, pose_data)
                
                frame = add_professional_effects(frame, pose_data, config)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Update stats only if significantly changed
                new_stats = {
                    'energy': pose_data.get('movement_energy', 0),
                    'gestures': pose_data.get('gestures', []),
                    'keypoints': len(pose_data.get('keypoints', {}))
                }
                
                # Check if stats changed significantly
                old_stats = st.session_state.pose_stats
                stats_changed = (
                    abs(new_stats['energy'] - old_stats['energy']) > 0.5 or
                    new_stats['gestures'] != old_stats['gestures'] or
                    abs(new_stats['keypoints'] - old_stats['keypoints']) > 2
                )
                
                if stats_changed or st.session_state.frame_count % 10 == 0:
                    st.session_state.pose_stats = new_stats
                    st.session_state.last_stats_update = st.session_state.frame_count
                
                # Display video with fixed parameter
                with video_container:
                    st.image(
                        frame_rgb, 
                        channels="RGB", 
                        width="stretch",  # Fixed deprecated parameter
                        caption=f"Frame {st.session_state.frame_count}"
                    )
                
                st.session_state.frame_count += 1
                
            else:
                with video_container:
                    st.error("❌ Camera read failed")
                    
        except Exception as e:
            with video_container:
                st.error(f"❌ Processing error: {e}")
    else:
        # Show last frame if available
        with video_container:
            st.info("📷 Auto-refresh disabled. Click 'Refresh' for new frame.")
    
    # Always show current stats (don't refresh stats container unless needed)
    with stats_container:
        display_optimized_stats(st.session_state.pose_stats)
    
    # Controlled auto-refresh
    if st.session_state.auto_refresh and st.session_state.visualizer_active:
        refresh_delay = max(1.0 / fps_value, 0.1)  # Minimum 100ms delay
        time.sleep(refresh_delay)
        
        # Only rerun if we haven't hit limits
        if st.session_state.frame_count < 2000:  # Higher limit
            st.rerun()
        else:
            st.warning("Frame limit reached. Please refresh page or restart.")

def display_optimized_stats(pose_stats):
    """Display stats without causing unnecessary reruns"""
    energy = pose_stats.get('energy', 0)
    gestures = pose_stats.get('gestures', [])
    keypoints = pose_stats.get('keypoints', 0)
    
    # Energy display with better formatting
    st.markdown("**🔋 Energy Level**")
    energy_val = min(energy / 10.0, 1.0)
    
    # Use columns for compact display
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(energy_val)
    with col2:
        st.markdown(f"**{energy:.1f}**")
    
    # Status indicator
    if energy > 7:
        st.success("🔥 HIGH ENERGY")
    elif energy > 3:
        st.info("⚡ MEDIUM")
    else:
        st.markdown("😌 *Low energy*")
    
    # Gestures - only show if active
    if gestures:
        st.markdown("**🎭 Active Gestures**")
        for gesture in gestures:
            if gesture == 'hands_up':
                st.success("🙌 Hands Up!")
            elif gesture == 'arms_wide':
                st.info("🤸 Arms Wide!")
            elif gesture == 'jump':
                st.warning("🦘 Jump!")
    else:
        st.markdown("**🎭** *No gestures*")
    
    # Compact technical info
    st.markdown("---")
    col_kp, col_status = st.columns(2)
    with col_kp:
        st.metric("Keypoints", f"{keypoints}/33", delta=None)
    with col_status:
        if keypoints > 15:
            st.markdown("✅ **Good**")
        elif keypoints > 8:
            st.markdown("⚡ **OK**")
        else:
            st.markdown("⚠️ **Detecting**")

def apply_preset(config, preset_name):
    """Apply visual presets"""
    presets = {
        "calm": {
            "particle_count": 30,
            "trail_length": 25,
            "sensitivity": 3.0,
            "color_scheme": "calm",
            "effect_intensity": 0.5
        },
        "energetic": {
            "particle_count": 80,
            "trail_length": 12,
            "sensitivity": 7.0,
            "color_scheme": "energetic",
            "effect_intensity": 0.8
        },
        "party": {
            "particle_count": 150,
            "trail_length": 15,
            "sensitivity": 9.0,
            "color_scheme": "rainbow",
            "effect_intensity": 1.0
        }
    }
    
    if preset_name in presets:
        for key, value in presets[preset_name].items():
            config.set(key, value)

def add_professional_effects(frame, pose_data, config):
    """Add professional visual effects"""
    try:
        import cv2
    except ImportError:
        return frame
    
    keypoints = pose_data.get('keypoints', {})
    energy = pose_data.get('movement_energy', 0)
    gestures = pose_data.get('gestures', [])
    intensity = config.get('effect_intensity', 0.7)
    
    # Energy-based background - FIXED TO BE MORE SUBTLE
    if config.get('background_effects') and energy > 3:  # Higher threshold
        overlay = frame.copy()
        # Much more subtle alpha blending
        alpha = min(energy * 0.03 * intensity, 0.1)  # Reduced from 0.1 to 0.03 and max 0.1
        
        # More balanced color mixing
        if energy > 8:  # Only very high energy gets red
            overlay[:, :, 2] = np.clip(overlay[:, :, 2] + int(20 * intensity), 0, 255)  # Reduced from 50 to 20
        elif energy > 6:  # Medium-high energy gets purple/magenta
            overlay[:, :, 2] = np.clip(overlay[:, :, 2] + int(15 * intensity), 0, 255)
            overlay[:, :, 0] = np.clip(overlay[:, :, 0] + int(10 * intensity), 0, 255)
        else:  # Lower energy gets very subtle blue
            overlay[:, :, 0] = np.clip(overlay[:, :, 0] + int(10 * intensity), 0, 255)  # Reduced from 30 to 10
        
        frame = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
    
    # Hand tracking with improved visuals
    for hand in ['left_wrist', 'right_wrist']:
        if hand in keypoints:
            x, y = keypoints[hand]
            color = (0, 255, 255) if hand == 'left_wrist' else (255, 100, 255)
            
            # Pulsing effect based on energy
            radius = int(6 + energy * 1.5)  # Slightly smaller circles
            cv2.circle(frame, (x, y), radius, color, -1)
            cv2.circle(frame, (x, y), radius + 3, color, 2)  # Smaller outer ring
    
    # Gesture effects - IMPROVED TEXT POSITIONING
    text_y_offset = 30
    if 'hands_up' in gestures:
        cv2.putText(frame, "CELEBRATION!", (30, text_y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)  # Smaller text
        text_y_offset += 30
    
    if 'arms_wide' in gestures:
        cv2.putText(frame, "FREEDOM!", (30, text_y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
        text_y_offset += 30
        
        # Connection line between hands
        if 'left_wrist' in keypoints and 'right_wrist' in keypoints:
            cv2.line(frame, keypoints['left_wrist'], keypoints['right_wrist'], 
                    (255, 0, 255), max(int(2 * intensity), 1))  # Thinner line
    
    if 'jump' in gestures:
        cv2.putText(frame, "JUMP!", (30, text_y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    
    return frame

def display_live_stats_safe(pose_stats):
    """Display live statistics safely without causing rerun issues"""
    energy = pose_stats.get('energy', 0)
    gestures = pose_stats.get('gestures', [])
    keypoints = pose_stats.get('keypoints', 0)
    
    # Energy meter
    st.markdown("**🔋 Energy Level**")
    energy_normalized = min(energy / 10.0, 1.0)
    st.progress(energy_normalized, text=f"{energy:.1f}/10")
    
    # Energy status
    if energy > 7:
        st.markdown("🔥 **HIGH ENERGY**", unsafe_allow_html=True)
    elif energy > 3:
        st.markdown("⚡ **MEDIUM ENERGY**", unsafe_allow_html=True)
    else:
        st.markdown("😌 **LOW ENERGY**", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gestures
    st.markdown("**🎭 Gestures**")
    if gestures:
        for gesture in gestures:
            if gesture == 'hands_up':
                st.success("🙌 Hands Up!")
            elif gesture == 'arms_wide':
                st.info("🤸 Arms Wide!")
            elif gesture == 'jump':
                st.warning("🦘 Jump!")
    else:
        st.markdown("*Ready for gestures...*")
    
    st.markdown("---")
    
    # Technical info
    st.markdown("**📊 Detection**")
    st.markdown(f"Keypoints: **{keypoints}**/33")
    if keypoints > 15:
        st.markdown("Status: **✅ Excellent**")
    elif keypoints > 8:
        st.markdown("Status: **⚡ Good**")
    else:
        st.markdown("Status: **⚠️ Detecting...**")

def show_dashboard():
    """Show the main dashboard when visualizer is not active"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## ⚙️ Configuration Panel")
        
        config = VisualizerConfig()
        
        # Visual Effects
        with st.expander("🎨 Visual Effects", expanded=True):
            config.set("particle_count", 
                      st.slider("Particle Density", 10, 200, config.get("particle_count"), 5,
                               help="Number of particles generated per gesture"))
            
            config.set("trail_length", 
                      st.slider("Trail Duration", 5, 50, config.get("trail_length"),
                               help="How long hand trails persist"))
            
            config.set("sensitivity", 
                      st.slider("Movement Sensitivity", 1.0, 10.0, config.get("sensitivity"), 0.5,
                               help="How responsive effects are to movement"))
            
            config.set("effect_intensity", 
                      st.slider("Effect Intensity", 0.1, 1.0, config.get("effect_intensity", 0.7), 0.1,
                               help="Overall intensity of visual effects"))
        
        # Detection Settings
        with st.expander("🤖 Detection Settings"):
            config.set("gesture_detection", 
                      st.toggle("Gesture Recognition", config.get("gesture_detection"),
                               help="Enable automatic gesture detection"))
            
            config.set("show_skeleton", 
                      st.toggle("Show Pose Skeleton", config.get("show_skeleton", True),
                               help="Display pose detection overlay"))
            
            config.set("background_effects", 
                      st.toggle("Background Effects", config.get("background_effects"),
                               help="Enable dynamic background visualization"))
        
        # Color scheme
        with st.expander("🎨 Color & Style"):
            config.set("color_scheme", 
                      st.selectbox("Color Palette", 
                                 ["energetic", "calm", "neutral", "rainbow", "neon"], 
                                 index=["energetic", "calm", "neutral", "rainbow", "neon"].index(
                                     config.get("color_scheme", "energetic")),
                                 help="Choose your preferred color scheme"))
        
        # Performance Settings
        with st.expander("⚡ Performance Settings"):
            st.markdown("**Frame Rate Control**")
            refresh_rate = st.slider("Refresh Rate (FPS)", 1, 30, 10, 1,
                                   help="Lower values use less CPU but less smooth video")
            
            st.markdown("**Visual Effect Controls**")
            background_intensity = st.slider("Background Effect Intensity", 0.0, 1.0, 0.3, 0.1,
                                            help="How strong the background color effects are")
            
            st.markdown("**Stability Options**")
            frame_buffer = st.checkbox("Enable Frame Buffering", value=True,
                                     help="Reduces flickering but may add slight delay")
            
            smart_refresh = st.checkbox("Smart Refresh", value=True,
                                      help="Only refresh when motion is detected")
            
            # Option to disable background effects completely
            disable_bg_effects = st.checkbox("Disable Background Effects", value=False,
                                            help="Turn off all background color effects")
            
            # Save performance settings to config
            config.set("refresh_rate", refresh_rate)
            config.set("frame_buffer", frame_buffer)
            config.set("smart_refresh", smart_refresh)
            config.set("background_intensity", background_intensity)
            config.set("background_effects", not disable_bg_effects)
    
    with col2:
        st.markdown("## 📊 System Status")
        
        # System status
        st.markdown("""
        <div class="status-card">
            <h4>🖥️ System Health</h4>
            <div class="metric-card">
                <strong>Camera:</strong> Ready ✅<br>
                <strong>AI Model:</strong> Loaded ✅<br>
                <strong>Performance:</strong> Optimal ✅
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Sessions", "0", "Ready")
        with col_b:
            st.metric("Gestures", "3", "Available")
        
        # Help section
        st.markdown("""
        <div class="status-card">
            <h4>❓ Quick Help</h4>
            <strong>Supported Gestures:</strong><br>
            🙌 Hands Up → Particle Explosion<br>
            🤸 Arms Wide → Light Trails<br>
            🦘 Jump → Fireworks<br><br>
            
            <strong>Tips:</strong><br>
            • Ensure good lighting<br>
            • Stay 3-6 feet from camera<br>
            • Wear contrasting colors<br>
            • Use stable internet connection
        </div>
        """, unsafe_allow_html=True)
        
        # Getting Started
        st.markdown("""
        <div class="status-card">
            <h4>🚀 Getting Started</h4>
            <strong>1.</strong> Adjust settings above<br>
            <strong>2.</strong> Click "START VISUALIZER"<br>
            <strong>3.</strong> Allow camera access<br>
            <strong>4.</strong> Start dancing!<br><br>
            
            <em>The web visualizer will show real-time<br>
            pose detection and visual effects.</em>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
