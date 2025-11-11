# Object Detection using Ultralytics YOLO11

Real-time object detection demonstrating Edge AI concepts: model size trade-offs, performance constraints, and local inference.

This demo uses [Ultralytics](https://ultralytics.com/) YOLO11 model. Ultralytics is a world leader in creating state-of-the-art computer vision tools for AI applications. Their YOLO (You Only Look Once) models set the standard for real-time object detection, balancing speed and accuracy at every scale. 

## 🎬 Demo

> ⏱️ **Time to Complete**: 10-15 minutes from setup to running the example.

![YOLO11 Object Detection Demo](images/demo.gif)

---

### 💻 Can I Run This Without a Raspberry Pi?

**Yes! This demo runs perfectly on just your laptop.**

- ✅ **Laptop Only**: Works great with MacOS, Linux, or Windows using your built-in webcam
- ✅ **Raspberry Pi (Optional but Recommended)**: Experience true edge deployment and performance constraints

> **The Raspberry Pi is completely optional.** It's recommended for learning about real-world edge AI deployment constraints, but all features work identically on your laptop.

### Prerequisites

- **Python 3.8+**: This demo requires Python 3.8 or later installed on your system.

---

###  Hardware Requirements

### Laptop/Desktop Only (No Raspberry Pi Needed!)
- **Computer**: MacOS, Linux, or Windows
- **Camera**: Built-in webcam or USB camera
- **RAM**: 4GB minimum (8GB recommended)
- **That's it!** You're ready to explore Edge AI concepts

> **⚠️ Note:** WSL (Windows Subsystem for Linux) is **not supported** because this demo requires direct camera access, which WSL does not provide. Windows users should run this demo in native Windows with Python installed.

### For Raspberry Pi Deployment (Optional - Recommended for Edge Experience)
Deploy the **exact same code** to experience real edge AI constraints:

- **Board**: Raspberry Pi 4 or 5 (4GB+ RAM recommended)
- **OS**: Raspberry Pi OS (64-bit, Full Desktop)
  
  <img src="../images/RPi_OS.png" width="400" alt="Raspberry Pi OS Selection">
  
- **Camera**: Pi Camera Module 2/3
  - For Pi Camera setup instructions, see [Raspberry Pi Camera Installation Guide](https://www.raspberrypi.com/documentation/accessories/camera.html#install-a-raspberry-pi-camera)
  - Once connected properly, the installation steps in the next section will install the required software
- **Storage**: 16GB+ microSD card

> **Why try Raspberry Pi?** Experience authentic edge computing constraints: limited CPU/RAM, thermal throttling, and power efficiency challenges—all while running the exact same code!

---

### 🚀 Quick Start (3 Steps)

### 1. Install Dependencies


**Only execute on Raspberry Pi:**
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv python3-opencv libcap-dev
```
**For all (including RPi):**
```bash
# Create virtual environment (recommended)
python -m venv edge-ai-env
source edge-ai-env/bin/activate  # Windows: edge-ai-env\Scripts\activate
```
For MacOS, Linux, Windows:
```bash
# Install requirements
pip install -r requirements.txt
```
For RPi:
```bash
pip install -r requirements_pi.txt
```

### 2. Launch the App
```bash
streamlit run YOLO11_Example.py
```

> **Note:** When launching the app for the first time, Streamlit may ask for your email address. Arm is not collecting any data or expecting your email. Feel free to leave this blank and press Enter to continue.

### 3. Start Experimenting!
Your browser will open automatically at `http://localhost:8501`. Start detecting objects, segmenting scenes, or tracking poses immediately!

---

### 🎯 How to Use the App

### Choose Your Input Source
- **📹 Video File**: Upload MP4/AVI files to analyze pre-recorded footage
- **📷 Camera**: Live feed from your webcam (desktop) or Pi Camera (Raspberry Pi)

### Select a Vision Task

| Task | What It Does | Use Cases |
|------|-------------|-----------|
| **Detection** | Draws boxes around objects | Security, counting, tracking |
| **Segmentation** | Precise pixel-level masks | Scene understanding, robotics |
| **Pose Estimation** | Detects human body keypoints | Fitness, sports analysis, HCI |

### Pick Your Model Size

The app automatically detects your platform and shows appropriate options:

**Nano**
- ⚡ Fastest inference
- 💾 Lowest memory usage
- ✅ Best for: Real-time on Raspberry Pi, battery devices
- 📊 Accuracy: Good for most applications

**Small**
- ⚖️ Balanced performance
- ✅ Best for: General purpose edge deployment
- 📊 Accuracy: Better than nano, still efficient

**Medium**
- 🎯 Higher accuracy
- 💪 More processing power needed
- ✅ Best for: Desktop testing, when accuracy matters most
- 📊 Accuracy: Excellent detection quality

### Monitor Performance
Real-time metrics show you:
- **Overall FPS**: AI model speed + Streamlit UI overhead
- **Inference FPS**: Pure AI model speed
- **Inference Time**: Milliseconds per frame

---

### 🎓 Learning Objectives

### 1. Edge AI Fundamentals
- **Local Processing**: All AI runs on your device—no cloud needed
- **Privacy**: Video never leaves your machine
- **Latency**: Instant responses vs. cloud round-trips
- **Reliability**: Works offline, no internet dependency

### 2. Performance Constraints
- See how model size impacts speed in real-time
- Understand FPS requirements for different applications
- Learn when "smaller and faster" beats "larger and more accurate"

### 3. Vision AI Capabilities
- Experiment with detection, segmentation, and pose estimation
- Understand which task fits which application
- See how task complexity affects performance

### 4. Deployment Workflow
- Test rapidly on development machine
- Deploy seamlessly to edge hardware
- Monitor performance metrics in production
---

### 🛠️ Technical Details

**Auto-Platform Detection**: The app detects if it's running on Raspberry Pi and automatically:

**Model Auto-Download**: First time you select a model, it downloads automatically. Subsequent runs use cached models.
