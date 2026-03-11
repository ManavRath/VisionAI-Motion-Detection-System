import cv2
import numpy as np
import os

class ObjectDetector:
    def __init__(self):
        # Using pre-trained MobileNet SSD
        self.prototxt = "models/deploy.prototxt"
        self.model = "models/mobilenet_iter_73000.caffemodel"
        self.confidence_threshold = 0.1
        
        # Labels for MobileNet SSD
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        
        self.net = None
        self._load_network()

    def _load_network(self):
        abs_prototxt = os.path.normpath(os.path.abspath(self.prototxt))
        abs_model = os.path.normpath(os.path.abspath(self.model))
        
        if not os.path.exists(abs_prototxt) or not os.path.exists(abs_model):
            return False

        try:
            # Check file sizes
            if not os.path.exists(abs_model): return False
            m_size = os.path.getsize(abs_model)
            if m_size < 1000000: # Less than 1MB is definitely wrong
                print(f"!!! WARNING: Model file seems too small ({m_size} bytes).")
                return False

            self.net = cv2.dnn.readNetFromCaffe(abs_prototxt, abs_model)
            if self.net is not None:
                print("AI: SUCCESS - Network loaded.")
                return True
        except Exception as e:
            # Print error if it's the first attempt or if it's a new error
            print(f"AI: Load attempt failed: {e}")
        return False

    def detect(self, frame):
        if self.net is None:
            # Auto-retry every 100 frames
            if not hasattr(self, '_retry_count'): self._retry_count = 0
            self._retry_count += 1
            if self._retry_count % 100 == 1:
                print("AI: Net is None. Attempting Self-Repair / Re-load...")
                if self._load_network():
                    print("AI: Self-Repair Successful!")
                else:
                    print("AI: Self-Repair failed. Will retry in 100 frames.")
            return []

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        
        self.net.setInput(blob)
        detections = self.net.forward()
        
        results = []
        raw_count = detections.shape[2]
        # Only print once every few frames to avoid flooding
        if np.random.random() < 0.1: 
            print(f"DEBUG: AI analyzing {raw_count} potential objects...")
        
        max_conf = 0
        for i in range(0, raw_count):
            confidence = detections[0, 0, i, 2]
            if confidence > max_conf:
                max_conf = confidence
            
            if confidence > self.confidence_threshold:
                idx = int(detections[0, 0, i, 1])
                label = self.CLASSES[idx]
                
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                
                results.append({
                    "label": label,
                    "confidence": confidence,
                    "box": (startX, startY, endX, endY)
                })
        if len(results) == 0 and max_conf > 0:
            if np.random.random() < 0.1:
                print(f"DEBUG: No detection above threshold. Max confidence was {max_conf:.4f}")
        return results
