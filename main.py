import cv2
import threading
import time
from id_card_scanner import IDCardScanner
from face_recognition_module import FaceRecognition
from database import AttendanceDatabase
from report_generator import ReportGenerator

class SmartAttendanceSystem:
    def __init__(self):
        self.id_scanner = IDCardScanner()
        self.face_recognizer = FaceRecognition()
        self.database = AttendanceDatabase()
        self.report_generator = ReportGenerator(self.database)
        self.running = True
        
    def scan_id_thread(self):
        """Thread function for ID card scanning"""
        print("ID Card Scanner started...")
        while self.running:
            id_data = self.id_scanner.scan_id_card()
            if id_data:
                print(f"ID Scanned: {id_data}")
                # Store ID data for face recognition
                self.current_id = id_data
                
    def recognize_face_thread(self):
        """Thread function for face recognition"""
        print("Face Recognition started...")
        while self.running:
            if hasattr(self, 'current_id'):
                # Capture face with the current ID
                if self.face_recognizer.capture_face(self.current_id):
                    print(f"Face captured for ID: {self.current_id}")
                    
                    # Try to recognize the face
                    recognized_id = self.face_recognizer.recognize_face()
                    if recognized_id:
                        print(f"Face recognized: {recognized_id}")
                        
                        # Check if ID matches face recognition
                        if recognized_id == self.current_id:
                            print("ID and Face match! Attendance marked.")
                            self.mark_attendance(self.current_id)
                        else:
                            print("ID and Face do not match!")
                            
    def mark_attendance(self, student_id):
        """Mark attendance for the student"""
        # Use database to mark attendance
        if self.database.mark_attendance(student_id):
            print(f"Attendance marked for: {student_id}")
            # Generate report after marking attendance
            self.report_generator.generate_attendance_report()
        else:
            print(f"Failed to mark attendance for: {student_id}")
        
    def start_system(self):
        """Start the smart attendance system"""
        # Create threads for ID scanning and face recognition
        id_thread = threading.Thread(target=self.scan_id_thread)
        face_thread = threading.Thread(target=self.recognize_face_thread)
        
        # Start threads
        id_thread.start()
        face_thread.start()
        
        print("Smart Attendance System running...")
        print("Press 'q' in any window to quit.")
        
        # Wait for threads to complete
        id_thread.join()
        face_thread.join()
        
    def stop_system(self):
        """Stop the system"""
        self.running = False

if __name__ == "__main__":
    system = SmartAttendanceSystem()
    
    try:
        system.start_system()
    except KeyboardInterrupt:
        print("\nStopping system...")
        system.stop_system()
    
    print("System stopped.")