import cv2
from pyzbar.pyzbar import decode
from queue import Queue
from sound import beep
from time import sleep


# Initialize the video capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 480)  # Set width
cap.set(4, 480)  # Set height

# Queue to store scanned barcodes
stored_barcodes = Queue()
stop_threads = False  # Thread control flag


def scan_code():
    """Reads barcodes using the webcam."""
    global stop_threads
    while not stop_threads:
        success, frame = cap.read()
        if not success:
            print("Failed to capture image")
            continue

        # Decode barcodes from the frame
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            stored_barcodes.put(barcode_data)

            beep()  # Play a beep sound for a new barcode
            sleep(2)
        # Display the video frame with the barcode overlay
        cv2.imshow("Barcode Scanner", frame)

        # Exit when 'Esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            stop_threads = True
            break

    cap.release()
    cv2.destroyAllWindows()  # Close OpenCV window when done
