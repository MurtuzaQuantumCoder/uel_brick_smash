# Head gesture tracking using OpenCV
# Uses face detection to track head position for paddle control

import cv2
import threading
import time
import numpy as np

class HeadTracker:
    """Tracks head position using webcam for paddle control."""
    
    def __init__(self):
        self.cap = None
        self.face_cascade = None
        self.running = False
        self.thread = None
        self.head_position = 0.5  # 0.0 (left) to 1.0 (right)
        self.center_x = 0.5
        self.smoothed_x = 0.5
        self.alpha = 0.3  # Smoothing factor
        self.detection_active = False
        
    def start(self):
        """Start the head tracking thread."""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Warning: Could not open camera for head tracking")
                return False
            
            # Load face cascade
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                print("Warning: Could not load face cascade")
                return False
            
            self.running = True
            self.thread = threading.Thread(target=self._track_loop, daemon=True)
            self.thread.start()
            self.detection_active = True
            print("Head tracking started - position face in camera frame")
            return True
            
        except Exception as e:
            print(f"Head tracking initialization failed: {e}")
            return False
    
    def stop(self):
        """Stop the head tracking thread."""
        self.running = False
        if self.cap:
            self.cap.release()
        self.detection_active = False
    
    def _track_loop(self):
        """Main tracking loop running in separate thread."""
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Flip for mirror effect
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )
                
                if len(faces) > 0:
                    # Use the largest face
                    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
                    
                    # Calculate relative position (0.0 to 1.0)
                    frame_width = frame.shape[1]
                    center_x = (x + w // 2) / frame_width
                    
                    # Smooth the position
                    self.smoothed_x = self.alpha * center_x + (1 - self.alpha) * self.smoothed_x
                    self.head_position = self.smoothed_x
                else:
                    # No face detected - slowly return to center
                    self.smoothed_x = 0.95 * self.smoothed_x + 0.05 * 0.5
                    self.head_position = self.smoothed_x
                
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Head tracking error: {e}")
                time.sleep(0.1)
    
    def get_position(self):
        """Get the current head position (0.0 to 1.0)."""
        if not self.detection_active:
            return 0.5
        return self.head_position
    
    def is_active(self):
        """Check if head tracking is active and working."""
        return self.detection_active and self.running

# Global head tracker instance
head_tracker = None

def init_head_tracking():
    """Initialize head tracking system."""
    global head_tracker
    head_tracker = HeadTracker()
    return head_tracker.start()

def get_head_position():
    """Get current head position for paddle control."""
    global head_tracker
    if head_tracker and head_tracker.is_active():
        return head_tracker.get_position()
    return 0.5  # Default center position

def stop_head_tracking():
    """Stop head tracking."""
    global head_tracker
    if head_tracker:
        head_tracker.stop()