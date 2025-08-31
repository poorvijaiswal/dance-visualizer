# 🕺 Dance Performance Visualizer

An AI-powered real-time dance visualization system that captures dancer movements using MediaPipe pose estimation and generates stunning visual effects with Pygame. Features a professional web interface built with Streamlit for easy configuration and control.

![Dance Visualizer Demo](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎯 Core Functionality
- **Real-time Pose Detection**: Uses MediaPipe for accurate body tracking
- **Dynamic Visual Effects**: Particle systems, trails, and gesture-based animations
- **Gesture Recognition**: Detects hands up, arms wide, jumping, and more
- **Energy-based Visualization**: Effects intensity responds to movement energy
- **Professional Web Interface**: Streamlit-based control panel

### 🎨 Visual Effects
- **Particle Systems**: Explosions, trails, and ambient particles
- **Hand Tracking**: Colorful wrist indicators with pulsing effects
- **Gesture Animations**: 
  - 🙌 Hands Up → Particle explosions
  - 🤸 Arms Wide → Connecting light trails  
  - 🦘 Jump → Fireworks burst
- **Dynamic Backgrounds**: Energy-responsive color schemes
- **Multiple Color Palettes**: Calm, Energetic, Neutral, Rainbow, Neon

### ⚙️ Configuration Options
- **Visual Presets**: One-click Calm/Energetic/Party modes
- **Real-time Adjustment**: Particle density, trail duration, sensitivity
- **Performance Controls**: FPS limiting, frame buffering, smart refresh
- **Effect Intensity**: Customizable visual effect strength
- **Background Effects**: Toggle and adjust background visualizations

## 🚀 Quick Start

### Option 1: One-Click Launch (Windows)
```bash
# Download and run
run.bat
```

### Option 2: Web Interface First
```bash
# Start web interface
streamlit run web_interface.py

# Then click "START VISUALIZER" in the web interface
```

### Option 3: Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start web interface
streamlit run web_interface.py

# 5. Start visualizer (in another terminal)
python main.py
```

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **Camera**: USB webcam or built-in camera
- **OS**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **RAM**: 4GB minimum, 8GB recommended
- **GPU**: Optional (improves performance)

### Python Dependencies
```txt
mediapipe>=0.10.0      # AI pose detection
opencv-python>=4.8.0   # Computer vision
pygame>=2.5.0          # Graphics rendering
streamlit>=1.28.0      # Web interface
numpy>=1.24.0          # Mathematical operations
```

## 🎮 Usage

### Web Interface Controls
1. **Start/Stop**: Launch and control the visualizer
2. **Visual Presets**: Quick setup for different moods
3. **Real-time Config**: Adjust effects while running
4. **Performance Monitor**: Track FPS and system health

### Keyboard Controls (Main Visualizer)
- `V` - Toggle video overlay
- `F` - Toggle fullscreen mode  
- `Q` - Quit application

### Gesture Controls
- **Raise both hands above head** → Particle explosions
- **Spread arms wide** → Light trail connections
- **Jump up** → Fireworks burst effect
- **General movement** → Ambient particle generation

## 📁 Project Structure

```
dance_visualiser/
├── main.py                 # Main visualizer application
├── web_interface.py        # Streamlit web interface
├── pose_module.py          # MediaPipe pose detection
├── visuals.py             # Visual effects engine
├── requirements.txt        # Python dependencies
├── run.bat                # Windows launcher
├── start_web.bat          # Web interface launcher
├── start_web.ps1          # PowerShell launcher
├── quick_start.bat        # Quick setup script
├── simple_launcher.py     # Python launcher
└── README.md              # This file
```

## 🔧 Configuration

### Web Interface Settings

**Visual Effects**
- Particle Density: 10-200 particles
- Trail Duration: 5-50 frames
- Movement Sensitivity: 1.0-10.0
- Effect Intensity: 0.1-1.0

**Detection Settings**
- Gesture Recognition: Enable/Disable
- Pose Skeleton: Show/Hide overlay
- Background Effects: Dynamic backgrounds

**Performance Settings**
- Refresh Rate: 1-30 FPS
- Frame Buffering: Stability option
- Smart Refresh: Motion-based updates

### Configuration File
Settings are automatically saved to `visualizer_config.json`:

```json
{
  "particle_count": 50,
  "trail_length": 15,
  "sensitivity": 5.0,
  "color_scheme": "energetic",
  "background_effects": true,
  "gesture_detection": true,
  "show_skeleton": true,
  "effect_intensity": 0.7
}
```

## 🎨 Visual Presets

### 🌊 Calm Mode
- Fewer particles (30)
- Longer trails (25 frames)
- Lower sensitivity (3.0)
- Soft blue color scheme
- Subtle effects (0.5 intensity)

### 🔥 Energetic Mode  
- More particles (80)
- Shorter trails (12 frames)
- Higher sensitivity (7.0)
- Red/orange color scheme
- Strong effects (0.8 intensity)

### 🌈 Party Mode
- Maximum particles (150)
- Medium trails (15 frames)
- Highest sensitivity (9.0)
- Rainbow color scheme
- Full intensity (1.0)

## 🛠️ Troubleshooting

### Common Issues

**Camera not detected**
```bash
# Check camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"

# Try different camera index
# Edit main.py line: cv2.VideoCapture(1)  # Try 1, 2, etc.
```

**Import errors**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

**Performance issues**
- Close other camera applications (Zoom, Teams, etc.)
- Reduce FPS in web interface (5-10 FPS)
- Disable background effects
- Lower particle density (10-30)

**Web interface won't load**
```bash
# Try different port
streamlit run web_interface.py --server.port 8502

# Check firewall settings
# Disable antivirus temporarily
```

**Pose detection not working**
- Ensure good lighting
- Stay 3-6 feet from camera
- Wear contrasting colors
- Check camera positioning

### Error Messages

**"MediaPipe not found"**
```bash
pip install mediapipe
```

**"No module named 'streamlit'"**
```bash
pip install streamlit
```

**"Camera index out of range"**
- Try different camera indices (0, 1, 2)
- Check if camera is in use by another app

## 🔬 Technical Details

### Architecture
- **Pose Detection**: MediaPipe Pose with smooth landmark tracking
- **Visual Rendering**: Pygame with optimized particle systems  
- **Web Interface**: Streamlit with real-time configuration
- **Gesture Recognition**: Custom algorithm using pose history
- **Energy Calculation**: Movement-based intensity mapping

### Performance Optimizations
- Efficient particle lifecycle management
- Smart frame rate limiting
- Conditional effect rendering
- Memory-optimized trail systems
- Configurable quality settings

### AI/ML Components
- **MediaPipe Pose**: 33-point body landmark detection
- **Gesture Classification**: Rule-based movement analysis
- **Energy Mapping**: Mathematical movement quantification
- **Smoothing Algorithms**: Temporal landmark filtering

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests if applicable**
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/dance-visualizer.git
cd dance-visualizer

# Setup development environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start development server
streamlit run web_interface.py
```

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where applicable
- Add docstrings to all functions
- Keep functions focused and modular

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Dance Visualizer Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- **[MediaPipe](https://mediapipe.dev/)** - Google's ML framework for pose detection
- **[Pygame](https://www.pygame.org/)** - Python game development library for graphics
- **[OpenCV](https://opencv.org/)** - Computer vision and image processing
- **[Streamlit](https://streamlit.io/)** - Web app framework for ML applications
- **[NumPy](https://numpy.org/)** - Scientific computing with Python

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/dance-visualizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/dance-visualizer/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/dance-visualizer/wiki)

## 🔮 Future Features

- [ ] Music synchronization and beat detection
- [ ] Multiple dancer support
- [ ] 3D visual effects
- [ ] Custom gesture training
- [ ] Video recording and export
- [ ] Social sharing integration
- [ ] Mobile app companion
- [ ] VR/AR visualization modes

---

**Made with ❤️ for dancers and creative technologists**

*Start dancing, start creating! 🕺💃*
