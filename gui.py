import threading
import customtkinter
from PIL import Image, ImageTk
from Scanner.camera import stored_barcodes, scan_code  # From camera.py
from Scanner.product_finder_v1 import get_product_info  # From product_finder_v1.py
from collections import Counter  # To count barcode occurrences
import requests
from io import BytesIO

# Function to animate the GIF


# def animate_gif(label, frames, delay, count=[0]):
#     frame = frames[count[0] % len(frames)]
#     label.configure(image=frame)
#     count[0] += 1
#     label.after(delay, animate_gif, label, frames, delay, count)

# # Function to load the GIF frames


# def load_gif(file_path):
#     gif = Image.open(file_path)
#     frames = []
#     try:
#         while True:
#             frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
#             frames.append(frame)
#             gif.seek(len(frames))  # Move to the next frame
#     except EOFError:
#         pass  # End of the sequence
#     return frames


# System settings for CustomTkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Initialize the GUI
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Troll-E")

id = 1
# Add UI components
main_label = customtkinter.CTkLabel(
    app, text=f"TROLL-E {id}", font=("Arial", 30))
main_label.pack(pady=50)

# String variable to hold product info
value = customtkinter.StringVar(app)

# Counter to keep track of barcode occurrences
barcode_counter = Counter()


def remove_background(image):
    """Remove the background of the image (make white background transparent)."""
    image = image.convert(
        "RGBA")  # Ensure it's in RGBA mode (with alpha channel)
    datas = image.getdata()

    new_data = []
    for item in datas:
        # Change all white (also shades of whites) pixels to transparent
        if item[0] in range(200, 256) and item[1] in range(200, 256) and item[2] in range(200, 256):
            new_data.append((255, 255, 255, 0))  # Add a transparent pixel
        else:
            new_data.append(item)  # Keep the other pixels unchanged

    image.putdata(new_data)  # Apply the new pixel data
    return image


def update_gui():
    global needs_update
    if not stored_barcodes.empty():  # Only update if there are barcodes to display
        # Peek at the first barcode in the queue
        barcode = stored_barcodes.queue[0]
        # Get product info for that barcode
        product_info = get_product_info()

        barcode_counter[barcode] += 1
        if product_info:
            title, symbol, price, product_image = product_info
            count = barcode_counter[barcode]
            full_price = count * price
            print(f"Product info: {title}, {symbol}{full_price} x{count}")
            value.set(f"Product: {title}\nPrice: {
                      symbol}{full_price:.2f} x{count}")

            # Check if product_image is a URL or a local file path
            try:
                if product_image.startswith('http://') or product_image.startswith('https://'):
                    # Download image if it's a URL
                    response = requests.get(product_image)
                    # Open the image from bytes
                    image = Image.open(BytesIO(response.content))
                else:
                    # Open the image directly if it's a file path
                    image = Image.open(product_image)

                # Remove the background if possible
                image = remove_background(image)

                # Resize image to fit the GUI
                image = image.resize((50, 50))
                image_tk = ImageTk.PhotoImage(image)

                # Update image on the label (assuming image_label exists)
                product_img_label.configure(image=image_tk)
                product_img_label.image = image_tk  # Keep a reference to the image
            except Exception as e:
                print(f"Error loading image: {e}")
                # Optionally, set a placeholder image or handle the error

    # Schedule the next GUI update
    app.after(100, update_gui)  # Update the GUI every 100 ms


# Display product info
product_info_label = customtkinter.CTkLabel(
    app, textvariable=value, font=("Arial", 16))
product_info_label.pack(pady=20)

product_img_label = customtkinter.CTkLabel(app, text="")
product_img_label.pack(pady=20)


# Load and display the animated GIF
# gif_frames = load_gif(
#     "./Assets/NFC_gif/wCneoCuZt2 (1).gif")  # Path to your GIF
# gif_label = customtkinter.CTkLabel(app, text="")
# gif_label.pack(pady=5)
# animate_gif(gif_label, gif_frames, 60)

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
