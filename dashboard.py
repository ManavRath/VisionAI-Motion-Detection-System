from flask import Flask, render_template, Response
import cv2
import os

app = Flask(__name__)

# This will be updated by main.py
current_frame = None

def generate_frames():
    global current_frame
    while True:
        if current_frame is not None:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', current_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            continue

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VisionAI | Secure Motion Monitoring</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #00f2fe;
                --secondary: #4facfe;
                --bg: #0a0b10;
                --card-bg: rgba(255, 255, 255, 0.05);
                --text: #ffffff;
                --accent: #ff3e3e;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: 'Outfit', sans-serif;
                background-color: var(--bg);
                background-image: 
                    radial-gradient(circle at 20% 30%, rgba(79, 172, 254, 0.15) 0%, transparent 40%),
                    radial-gradient(circle at 80% 70%, rgba(0, 242, 254, 0.1) 0%, transparent 40%);
                color: var(--text);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                overflow-x: hidden;
            }

            header {
                width: 100%;
                padding: 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
            }

            .logo {
                font-size: 1.5rem;
                font-weight: 700;
                background: linear-gradient(45deg, var(--primary), var(--secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 1px;
            }

            .status-badge {
                padding: 0.5rem 1rem;
                border-radius: 50px;
                background: var(--card-bg);
                border: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                gap: 0.75rem;
                font-size: 0.875rem;
                font-weight: 500;
                backdrop-filter: blur(10px);
            }

            .pulse {
                width: 10px;
                height: 10px;
                background: #00ff88;
                border-radius: 50%;
                box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7);
                animation: pulse 1.5s infinite;
            }

            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
            }

            main {
                width: 100%;
                max-width: 1200px;
                padding: 0 2rem 4rem;
                display: grid;
                grid-template-columns: 1fr 300px;
                gap: 2rem;
            }

            @media (max-width: 900px) {
                main { grid-template-columns: 1fr; }
            }

            .feed-container {
                background: var(--card-bg);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 1.5rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
            }

            .feed-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .feed-header h2 {
                font-size: 1.125rem;
                opacity: 0.8;
                font-weight: 500;
            }

            .video-stream {
                width: 100%;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.05);
                display: block;
            }

            .sidebar {
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
            }

            .glass-card {
                background: var(--card-bg);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 1.5rem;
                backdrop-filter: blur(10px);
            }

            .stat-label {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                opacity: 0.5;
                margin-bottom: 0.5rem;
            }

            .stat-value {
                font-size: 1.75rem;
                font-weight: 700;
            }

            .logs-container {
                flex-grow: 1;
                display: flex;
                flex-direction: column;
            }

            .log-entry {
                padding: 0.75rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                font-size: 0.8125rem;
            }

            .log-time {
                color: var(--secondary);
                margin-right: 0.5rem;
                font-weight: 600;
            }

            .controls {
                margin-top: 2rem;
                display: flex;
                gap: 1rem;
                width: 100%;
                max-width: 1200px;
                padding: 0 2rem;
            }

            .btn {
                background: var(--card-bg);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: white;
                padding: 0.75rem 1.5rem;
                border-radius: 12px;
                cursor: pointer;
                font-family: inherit;
                font-weight: 600;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .btn:hover {
                background: rgba(255, 255, 255, 0.1);
                transform: translateY(-2px);
            }

            .btn-primary {
                background: linear-gradient(45deg, var(--primary), var(--secondary));
                border: none;
                color: #000;
            }

            .btn-primary:hover {
                box-shadow: 0 10px 20px -5px rgba(79, 172, 254, 0.5);
            }
        </style>
    </head>
    <body>
        <header>
            <div class="logo">VISION.AI</div>
            <div class="status-badge">
                <div class="pulse"></div>
                SYSTEM ACTIVE
            </div>
        </header>

        <main>
            <div class="feed-container">
                <div class="feed-header">
                    <h2>Live Detection Feed</h2>
                    <span style="font-size: 0.75rem; opacity: 0.5;">FHD 1080P • 30 FPS</span>
                </div>
                <img src="/video_feed" class="video-stream">
            </div>

            <div class="sidebar">
                <div class="glass-card">
                    <div class="stat-label">Total Alerts</div>
                    <div class="stat-value">12</div>
                </div>
                
                <div class="glass-card">
                    <div class="stat-label">Storage Usage</div>
                    <div class="stat-value" style="font-size: 1.25rem;">2.4 GB / 10 GB</div>
                    <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top: 1rem; overflow: hidden;">
                        <div style="width: 24%; height: 100%; background: var(--primary);"></div>
                    </div>
                </div>

                <div class="glass-card logs-container">
                    <div class="stat-label" style="margin-bottom: 1rem;">System Logs</div>
                    <div class="log-entry">
                        <span class="log-time">19:15:22</span> Motion detected (Person)
                    </div>
                    <div class="log-entry">
                        <span class="log-time">19:12:05</span> Alert sent to Telegram
                    </div>
                    <div class="log-entry">
                        <span class="log-time">18:45:30</span> Snapshot saved
                    </div>
                    <div class="log-entry" style="border: none;">
                        <span class="log-time">18:30:12</span> System initialized
                    </div>
                </div>
            </div>
        </main>

        <div class="controls">
            <button class="btn btn-primary">Download History</button>
            <button class="btn">Settings</button>
            <button class="btn" style="color: var(--accent);">Emergency Stop</button>
        </div>
    </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_dashboard():
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True, use_reloader=False)

if __name__ == "__main__":
    run_dashboard()
