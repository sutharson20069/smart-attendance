import cv2
import numpy as np
import os

class FaceRecognition:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.known_faces_dir = "known_faces"
        self.labels = {}
        self.current_id = 0
        
        # Create known faces directory if it doesn't exist
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            
    def capture_face(self, id_data):
        """Capture face image and save it with the ID data"""
        cap = cv2.VideoCapture(0)
        
        print(f"Capturing face for ID: {id_data}")
        print("Press 'c' to capture or 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break
                
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            # Draw rectangle around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                
            cv2.imshow('Face Capture', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            # Capture face when 'c' is pressed
            if key == ord('c') and len(faces) > 0:
                # Save the face image
                face_filename = os.path.join(self.known_faces_dir, f"{id_data}.jpg")
                cv2.imwrite(face_filename, frame)
                
                # Store the label
                self.labels[id_data] = self.current_id
                self.current_id += 1
                
                print(f"Face captured and saved as {face_filename}")
                cap.release()
                cv2.destroyAllWindows()
                return True
                
            # Quit when 'q' is pressed
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return False
                
        cap.release()
        cv2.destroyAllWindows()
        return False
        
    def recognize_face(self):
        """Recognize face from camera"""
        cap = cv2.VideoCapture(0)
        
        # Load known faces and train recognizer
        self._train_recognizer()
        
        print("Face recognition started. Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                # Predict the face
                label, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                
                # Find the ID associated with this label
                recognized_id = None
                for id_data, lid in self.labels.items():
                    if lid == label:
                        recognized_id = id_data
                        break
                        
                # Draw rectangle and display recognition info
                color = (0, 255, 0) if confidence < 70 else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                
                if recognized_id:
                    text = f"ID: {recognized_id} ({confidence:.2f}%)"
                else:
                    text = f"Unknown ({confidence:.2f}%)"
                    
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                if recognized_id:
                    print(f"Recognized: {recognized_id}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return recognized_id
                    
            cv2.imshow('Face Recognition', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        return None
        
    def _train_recognizer(self):
        """Train the face recognizer with known faces"""
        faces = []
        labels = []
        
        # Load known faces
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(".jpg"):
                id_data = filename.split(".")[0]
                if id_data in self.labels:
                    img_path = os.path.join(self.known_faces_dir, filename)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    
                    if img is not None:
                        faces.append(img)
                        labels.append(self.labels[id_data])
                        
        # Train the recognizer
        if len(faces) > 0:
            self.recognizer.train(faces, np.array(labels))
            print(f"Trained recognizer with {len(faces)} faces")

if __name__ == "__main__":
    fr = FaceRecognition()
    
    # Example usage:
    # First capture a face with an ID
    # id_data = "STUDENT123"  # This would come from ID card scanner
    # fr.capture_face(id_data)
    
    # Then recognize faces
    recognized_id = fr.recognize_face()
    if recognized_id:
        print(f"Successfully recognized: {recognized_id}")