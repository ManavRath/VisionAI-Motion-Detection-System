# VisionAI | Smart Motion Detection System

VisionAI is a modern, AI-powered security monitoring system that combines real-time computer vision with a sleek web-based dashboard. It is specifically designed to detect and track human activity while filtering out false positives like pets or moving furniture.

![VisionAI Dashboard Preview](https://via.placeholder.com/800x450.png?text=VisionAI+Dashboard+Preview)

## 🚀 Features

- **AI-Powered Person Detection**: Uses MobileNet-SSD to specifically identify human figures with high confidence.
- **Smart Logic Filtering**: Ignores pets, vehicles, and other non-human objects to reduce alert fatigue.
- **Real-time Web Dashboard**: A premium, Glassmorphism-inspired UI to monitor your feed from any device.
- **Sci-Fi Alert System**: High-pitched distinctive audio notifications upon detection.
- **Auto-Recording**: Automatically saves snapshots and video clips when motion is verified by AI.
- **Self-Repairing Core**: Intelligent re-initialization logic to ensure stable AI performance.

## 🛠️ Technology Stack

### Backend
- **Core**: Python 3.x
- **Computer Vision**: OpenCV (DNN Module)
- **AI Model**: Caffe-based MobileNet-SSD
- **Networking**: Requests (for Telegram/External triggers)

### Frontend
- **Web Framework**: Flask
- **UI Design**: Modern CSS (Glassmorphism, Animations)
- **Streaming**: Multipart M-JPEG video stream

## 🏗️ Architecture

### 1. The Processing Pipeline (Backend)
The system captures raw video frames and runs two stages of processing:
- **Stage 1 (Motion)**: Identifies pixel-level changes to detect movement.
- **Stage 2 (AI Verification)**: The AI Detector scans the frame specifically for a `person`. If both stages trigger, an alert is fired.

### 2. Telegram Integration (Alerts)
VisionAI goes beyond local monitoring by sending instant photo alerts to your phone. 
- **Auto-Snapshot**: When a person is verified, the system takes a high-res snapshot.
- **Bot Delivery**: The snapshot is securely sent via the Telegram Bot API directly to your private chat.

### 3. The Dashboard (Frontend)
The Flask server runs in a dedicated thread, allowing the video processing to stay at 30+ FPS. It serves a responsive HTML5 page that pulls the live frame buffer directly from the AI loop.

## 📦 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ManavRath/VisionAI-Motion-Detection-System.git
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Telegram (Optional)
To receive alerts on your phone:
1. Message [@BotFather](https://t.me/botfather) on Telegram to create a bot and get your **Token**.
2. Message [@userinfobot](https://t.me/userinfobot) to get your **Chat ID**.
3. Open `telegram_bot.py` and enter your credentials:
   ```python
   BOT_TOKEN = "your_token_here"
   CHAT_ID = "your_chat_id_here"
   ```

### 4. Initialize the AI "Brain"
You must download the pre-trained weights before running the system:
```bash
python download_models.py
```

### 4. Launch the System
```bash
python main.py
```

## 🌐 Usage
- **Local Feed**: The application will open a window on your desktop.
- **Web Dashboard**: Open `http://localhost:5000` in any browser on your network.
- **Controls**: Press `q` in the camera window to exit safely.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

