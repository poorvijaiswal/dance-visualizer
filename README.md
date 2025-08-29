# 🕺 Dance Performance Visualizer

An end-to-end generative dance performance visualizer that captures dancer movements using AI-based pose estimation and generates real-time visual effects.

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Features

- **Real-time Pose Detection**: Uses MediaPipe for accurate body keypoint tracking
- **Gesture Recognition**: Detects specific dance moves (hands up, arms wide, jumping)
- **Dynamic Visual Effects**: Particle systems, trails, and animations that respond to movement
- **Energy-based Responses**: Visuals adapt to movement intensity (calm vs energetic)
- **Interactive Controls**: Toggle video, fullscreen mode, and debug info
- **Optimized Performance**: 30fps real-time processing

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Webcam
- Windows/Linux/macOS

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dance-visualizer.git
   cd dance-visualizer
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Quick Setup Scripts

**Windows PowerShell:**
```powershell
.\setup.ps1  # First time setup
.\run.ps1    # Run the application
```

**Windows Command Prompt:**
```cmd
run.bat
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `V` | Toggle video debug window |
| `F` | Toggle fullscreen mode |
| `Q` | Quit application |

## 🏗️ Project Structure

```
dance_visualiser/
├── main.py              # Main application entry point
├── pose_module.py       # MediaPipe pose detection logic
├── visuals.py          # Generative visual effects
├── requirements.txt    # Python dependencies
├── setup.ps1          # PowerShell setup script
├── run.ps1            # PowerShell run script
├── run.bat            # Windows batch run script
├── README.md          # This file
└── .gitignore         # Git ignore file
```

## 🎨 Visual Effects

### Gesture-based Effects
- **Hands Up**: Particle explosions from both hands
- **Arms Wide**: Connecting line particles between hands
- **Jump**: Fireworks burst effect

### Movement-based Effects
- **Hand Trails**: Colorful trails following hand movements
- **Ambient Particles**: Energy-responsive particle generation
- **Background Patterns**: Pulsing circles based on movement intensity
- **Dynamic Colors**: Color palettes change with energy levels

## 🔧 Technical Details

### Core Technologies
- **MediaPipe**: Real-time pose estimation
- **OpenCV**: Video capture and processing
- **Pygame**: Graphics rendering and visualization
- **NumPy**: Mathematical operations and data processing

### Performance Optimizations
- Efficient particle system management
- Smooth keypoint filtering
- Real-time coordinate normalization
- Memory-efficient trail rendering

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for pose estimation
- [Pygame](https://www.pygame.org/) for graphics rendering
- [OpenCV](https://opencv.org/) for computer vision capabilities

## 🐛 Troubleshooting

### Common Issues

**Camera not detected:**
- Ensure your webcam is connected and not in use by other applications
- Try changing the camera index in `main.py` (line with `cv2.VideoCapture(0)`)

**Performance issues:**
- Close other applications using the camera
- Reduce video resolution in camera settings
- Check if your system meets minimum requirements

**Import errors:**
- Make sure you activated the virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Enjoy creating beautiful dance visualizations! 💃🕺**
