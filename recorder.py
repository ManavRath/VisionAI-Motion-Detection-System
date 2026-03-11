import cv2
import os
import time

# Ensure output directory exists
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def save_snapshot(frame):
    """
    Saves the current frame as a timestamped JPEG image.
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"motion_{timestamp}.jpg")
    cv2.imwrite(filename, frame)
    print(f"Snapshot saved: {filename}")
    return filename

def start_video_recording(frame_width, frame_height, fps=20.0):
    """
    Initializes a VideoWriter object for recording a clip.
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"motion_{timestamp}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
    print(f"Started recording: {filename}")
    return out, filename
