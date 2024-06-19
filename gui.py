from Scanner.camera import scan_code, stored_barcodes
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


value = customtkinter.StringVar(
    app,)


def on_button_click(e):
    scan_code()  # Assuming this updates `stored_barcodes`
    print(f"multi: {stored_barcodes}")
    # Clear any previous values
    value.set("")
    for multi in stored_barcodes:
        product_info = get_product_info()
        if product_info:
            title, symbol, price,  = product_info
            count = stored_barcodes.count(multi)
            item_price = count * price
            # Set the value based on product info
            # Ensure price is formatted with 2 decimal places
            formatted_price = f"{symbol}{item_price}"
            value.set(f"{title} x{count}\n{formatted_price} ")


h2 = customtkinter.CTkLabel(app, text="Scan your product", font=("Arial", 20))
h2.bind("<Button-1>", on_button_click)
h2.pack(pady=20)

# Remove items from list
remove_button = customtkinter.CTkButton(
    app, text="Remove", command=lambda: stored_barcodes.pop())

remove_button.pack(pady=5)

# Display product info
product_info_label = customtkinter.CTkLabel(
    app, textvariable=value, font=("Arial", 16))
product_info_label.pack(pady=20)

# Add GIF
gif_frames = load_gif("./Assets/NFC_gif/wCneoCuZt2 (1).gif")

# Show GIF
gif_label = customtkinter.CTkLabel(app, text="")
gif_label.pack(pady=5)
animate_gif(gif_label, gif_frames, 60)

# Product image label
product_img_label = customtkinter.CTkLabel(app, text="")
product_img_label.pack(pady=20)

# Run app
app.mainloop()
