import cv2
import time
from pyzbar.pyzbar import decode
import os
from sound import beep

stored_barcodes = ['8714100597347', '8714100597347',
                   '8714100597347', '8714100597347']


def scan_code():

    global stored_barcodes
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1080)  # width
    cap.set(4, 480)  # height

    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # mp3_file_path = os.path.join(
    #     current_directory, "Barcode_scanner_beep_sound.mp3")

    # scanner_beep = AudioSegment.from_mp3(
    #     mp3_file_path)

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
                # Play sound when a new barcode is detected
                # play(scanner_beep)
                beep()
                time.sleep(2)
                # print(stored_barcodes)

        cv2.imshow('Testing-code-scan', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows

    return stored_barcodes
