from Scanner.camera import scan_code
from Scanner.product_finder_v1 import get_product_info
import tkinter
import customtkinter
from PIL import Image, ImageTk
import itertools
import io
import requests

# Function to animate GIF


def animate_gif(label, frames, delay, count=[0]):
    frame = frames[count[0] % len(frames)]
    label.configure(image=frame)
    count[0] += 1
    label.after(delay, animate_gif, label, frames, delay, count)

# Function to load GIF frames


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


# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Troll-E")

# Add UI
main_label = customtkinter.CTkLabel(
    app, text="WELCOME TO TROLL-E", font=("Arial", 30))
main_label.pack(pady=50)

value = customtkinter.StringVar()

# Function to handle button click


item_counter = 0


def on_button_click(e):
    barcode_data = scan_code()
    global item_counter

    multi_barcode_data = list(barcode_data)
    print(f"multi: {multi_barcode_data}")
    for multi in multi_barcode_data:
        if barcode_data:
            item_counter += 1
            product_info = get_product_info(barcode_data)
            for _ in product_info:
                value.set(f"{product_info} x{multi_barcode_data.count(multi)}")


h2 = customtkinter.CTkLabel(app, text="Scan your product", font=("Arial", 20))
h2.bind("<Button-1>", on_button_click)
h2.pack(pady=20)

# Display product info
product_info_label = customtkinter.CTkLabel(
    app, textvariable=value, font=("Arial", 16))
product_info_label.pack(pady=20)

# Add GIF
gif_frames = load_gif("./Assets/NFC_gif/wCneoCuZt2 (1).gif")

# Show GIF
gif_label = customtkinter.CTkLabel(app, text="")
gif_label.pack(pady=20)
animate_gif(gif_label, gif_frames, 60)

# Product image label
product_img_label = customtkinter.CTkLabel(app, text="")
product_img_label.pack(pady=20)

# Run app
app.mainloop()
