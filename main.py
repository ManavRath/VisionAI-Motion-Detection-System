import cv2
import numpy as np
import time
import threading
from alerts import trigger_alert
from recorder import save_snapshot, start_video_recording
from detector import ObjectDetector
from telegram_bot import send_telegram_alert
import dashboard

def main():
    # Initialize components
    print("\n" + "="*50)
    print("      MOTION SENSOR AI SYSTEM STARTUP")
    print("="*50)
    import os
    print(f"Current Directory: {os.getcwd()}")
    print("Initializing AI Detector...")
    detector = ObjectDetector()
    
    if detector.net is not None:
        print("AI Status: [  READY  ]")
    else:
        print("AI Status: [ FAILED  ]")
        print("\n" + "!"*50)
        print("CRITICAL ERROR: AI Detector failed to initialize!")
        print("The system will continue with motion detection only,")
        print("but NO bounding boxes will be shown.")
        print("!"*50)
    print("="*50 + "\n")
    
    # Start dashboard in a separate thread
    db_thread = threading.Thread(target=dashboard.run_dashboard, daemon=True)
    db_thread.start()

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Give the camera time to warm up
    time.sleep(2)

    # Variables for motion detection
    static_back = None
    motion_counter = 0
    recording = False
    video_writer = None
    
    # AI Filtering - Only alert if person is detected
    FILTER_CLASSES = ["person"]
    
    # Motion detection sensitivity
    MIN_AREA = 1000  
    
    print(f"AI Motion detection restricted to: {', '.join(FILTER_CLASSES)}")
    print("Dashboard available at http://localhost:5000")
    print("Press 'q' to exit.")

    last_detected_label = None

    while True:
        check, frame = cap.read()
        if not check:
            break

        motion_detected = False
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if static_back is None:
            static_back = gray
            continue

        diff_frame = cv2.absdiff(static_back, gray)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        cnts, _ = cv2.findContours(thresh_frame.copy(), 
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < MIN_AREA:
                continue
            motion_detected = True
            break

        # AI Stage: Run detection on every frame for visual feedback
        detections = detector.detect(frame)
        if len(detections) > 0:
            print(f"AI: Found {len(detections)} objects.")
        
        verified_motion = False
        current_frame_label = None
        
        for d in detections:
            label = d["label"]
            conf = d["confidence"]
            (startX, startY, endX, endY) = d["box"]
            
            # ONLY handle persons
            if label == "person":
                if conf >= 0.3:
                    color = (0, 255, 0) # Green for verified person
                    verified_motion = True
                    current_frame_label = label
                    text = f"PERSON: {conf:.2f}"
                    
                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                    cv2.putText(frame, text, (startX, startY - 5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                else:
                    # Optional: show low confidence person in yellow
                    color = (0, 255, 255)
                    text = f"PERSON? ({conf:.2f})"
                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 1)

        # Alert Logic: Only trigger if BOTH AI sees something AND motion was detected
        if verified_motion and motion_detected:
            motion_counter += 1
            if motion_counter == 5: # Trigger on 5th consecutive frame of motion + AI
                trigger_alert()
                img_path = save_snapshot(frame)
                send_telegram_alert(f"⚠️ AI detected a {current_frame_label}!", img_path)
                
                h, w = frame.shape[:2]
                video_writer, _ = start_video_recording(w, h)
                recording = True
                last_detected_label = current_frame_label
        else:
            # If recording is active, we check if we should stop
            if not motion_detected and recording:
                recording = False
                if video_writer:
                    video_writer.release()
                    print(f"Recording stopped for {last_detected_label or 'motion'}.")
            motion_counter = 0

        # Share frame with dashboard AFTER drawing bounding boxes
        dashboard.current_frame = frame.copy()

        cv2.imshow("AI Motion Sensor Feed", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Cleanup
    if video_writer:
        video_writer.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
