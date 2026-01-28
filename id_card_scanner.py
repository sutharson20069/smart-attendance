import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

class IDCardScanner:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
    def scan_id_card(self):
        """Scan ID card and extract information from barcode/QR code"""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break
                
            # Convert frame to grayscale for better barcode detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect barcodes in the frame
            barcodes = pyzbar.decode(gray)
            
            # Draw rectangle around detected barcodes
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Extract barcode data
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type
                
                # Display barcode information
                text = f"{barcode_type}: {barcode_data}"
                cv2.putText(frame, text, (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                print(f"ID Card Data: {barcode_data}")
                return barcode_data
                
            # Display the resulting frame
            cv2.imshow('ID Card Scanner', frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        # Release the capture and close windows
        self.cap.release()
        cv2.destroyAllWindows()
        return None

if __name__ == "__main__":
    scanner = IDCardScanner()
    id_data = scanner.scan_id_card()
    if id_data:
        print(f"Successfully scanned ID: {id_data}")