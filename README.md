# 🕺 Dance Performance Visualizer

An end-to-end generative dance performance visualizer that captures dancer movements using AI-based pose estimation and generates real-time visual effects.

## 🚀 Quick Start

### Method 1: Easy Start (Windows)
```bash
# Start web interface
start_web.bat
# OR
.\start_web.ps1

# In another terminal, start the visualizer
python main.py
```

### Method 2: Manual Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start web interface
streamlit run web_interface.py

# 3. In another terminal/command prompt, start visualizer
python main.py
```

### Method 3: Alternative Port (if localhost:8501 doesn't work)
```bash
streamlit run web_interface.py --server.port 8502
```

## 🔧 Troubleshooting

### "localhost refused to connect"
1. **Check if Streamlit is running**:
   ```bash
   # Look for this output when starting:
   # Local URL: http://localhost:8501
   # Network URL: http://192.168.x.x:8501
   ```

2. **Try different port**:
   ```bash
   streamlit run web_interface.py --server.port 8502
   ```

3. **Check firewall/antivirus**: Make sure they're not blocking the connection

4. **Use network URL**: If localhost doesn't work, try the Network URL shown in the terminal

### "Module not found" errors
```bash
# Make sure you're in the right directory
cd c:\Users\Poorvi\Desktop\dance_visualiser

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Virtual Environment Issues
```bash
# Create new virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## 📱 Web Interface Features

- 🎮 **Start/Stop Controls**: Launch visualizer from web interface
- 🎨 **Visual Presets**: Calm, Energetic, and Party modes
- ⚙️ **Real-time Configuration**: Adjust settings without restarting
- 📊 **Performance Monitoring**: FPS and particle count metrics
- 📱 **Mobile Friendly**: Works on phones and tablets

## 🎯 Usage Flow

1. **Start Web Interface**: `streamlit run web_interface.py`
2. **Configure Settings**: Use the web panel to adjust visual effects
3. **Start Visualizer**: Click "Start Visualizer" or run `python main.py`
4. **Dance & Enjoy**: Move in front of your camera to see the effects!

## 📞 Support

If you're still having issues:
1. Check that you're in the correct directory
2. Ensure Python 3.10+ is installed
3. Try running commands in a new terminal/command prompt
4. Check Windows firewall settings

---

**Happy Dancing! 🕺💃**
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
