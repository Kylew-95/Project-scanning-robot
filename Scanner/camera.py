import cv2
import time
from pyzbar.pyzbar import decode


def scan_code():
    stored_barcodes = []

    cap = cv2.VideoCapture(0)
    cap.set(3, 1080)  # width
    cap.set(4, 480)  # height

    while True:
        success, frame = cap.read()

        if not success:
            print("Failed to capture image")
            continue

        barcodes = decode(frame)
        if barcodes:
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                stored_barcodes.append(barcode_data)
                # Call the callback function with new barcode data
                time.sleep(2)
                print(stored_barcodes)

        cv2.imshow('Testing-code-scan', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break
    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows

    return stored_barcodes
