import cv2
from pyzbar.pyzbar import decode
import webbrowser
import numpy as np
import time

# Initialize the camera (you can also use a pre-recorded video file)
cap = cv2.VideoCapture(0)
scanned = False

while not scanned:
    ret, frame = cap.read()

    if not ret:
        continue

    # Detect and decode QR codes and barcodes
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        # Extract the data from the QR code or barcode
        data = obj.data.decode('utf-8')
        print(f"Type: {obj.type}, Data: {data}")

        # Check if the data looks like a URL
        if data.startswith("http://") or data.startswith("https://"):
            print("Opening URL:", data)
            webbrowser.open(data)          
            scanned = True

        # Draw a rectangle around the detected code
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        cv2.putText(frame, data, (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with detected codes
    cv2.imshow('QR/Barcode Scanner', frame)

    # Exit the loop and close the application when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and clos
