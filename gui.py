import threading
import customtkinter
from PIL import Image, ImageTk
from Scanner.camera import stored_barcodes, scan_code  # From camera.py
from Scanner.product_finder_v1 import get_product_info  # From product_finder_v1.py
from collections import Counter  # To count barcode occurrences

# Function to animate the GIF


def animate_gif(label, frames, delay, count=[0]):
    frame = frames[count[0] % len(frames)]
    label.configure(image=frame)
    count[0] += 1
    label.after(delay, animate_gif, label, frames, delay, count)

# Function to load the GIF frames


def load_gif(file_path):
    gif = Image.open(file_path)
    frames = []
    try:
        while True:
            frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
            frames.append(frame)
            gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass  # End of the sequence
    return frames


# System settings for CustomTkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Initialize the GUI
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Troll-E")

# Add UI components
main_label = customtkinter.CTkLabel(
    app, text="WELCOME TO TROLL-E", font=("Arial", 30))
main_label.pack(pady=50)

# String variable to hold product info
value = customtkinter.StringVar(app)

# Counter to keep track of barcode occurrences
barcode_counter = Counter()


def update_gui():
    # Only update if the barcode queue has items
    if not stored_barcodes.empty():
        # Get product info for the barcode
        product_info = get_product_info()

        barcode_counter[stored_barcodes] += 1
        if product_info:
            title, symbol, price = product_info
            count = barcode_counter[stored_barcodes]
            print(f"Product info: {title}, {symbol}{price} x{count}")
            value.set(f"Product: {title}\nPrice: {symbol}{price:.2f} x{count}")
    # Schedule the next GUI update
    app.after(100, update_gui)  # Update the GUI every 100 ms


# Display product info
product_info_label = customtkinter.CTkLabel(
    app, textvariable=value, font=("Arial", 16))
product_info_label.pack(pady=20)

# Load and display the animated GIF
gif_frames = load_gif(
    "./Assets/NFC_gif/wCneoCuZt2 (1).gif")  # Path to your GIF
gif_label = customtkinter.CTkLabel(app, text="")
gif_label.pack(pady=5)
animate_gif(gif_label, gif_frames, 60)

# Product image label (optional)
product_img_label = customtkinter.CTkLabel(app, text="")
product_img_label.pack(pady=20)

# Remove items from list
remove_button = customtkinter.CTkButton(
    app, text="Remove", command=lambda: stored_barcodes.empty if not stored_barcodes.empty() else None)
remove_button.pack(pady=5)

# Start the barcode scanning in a separate thread


def start_camera_thread():
    global stop_threads
    stop_threads = False
    reader_thread = threading.Thread(target=scan_code)
    reader_thread.daemon = True  # Daemonize the thread so it exits when the program exits
    reader_thread.start()


# Start the camera thread
start_camera_thread()

# Run the GUI update function to handle barcode and product info updates


def start_gui_update_thread():
    # Update the GUI periodically without blocking the main loop
    update_gui()


# Run the GUI update in a separate thread
gui_update_thread = threading.Thread(target=start_gui_update_thread)
gui_update_thread.daemon = True  # Daemonize so it exits when the app closes
gui_update_thread.start()

# Run the app
app.mainloop()
