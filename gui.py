from Scanner.camera import scan_code
from Scanner.product_finder_v1 import get_product_info
import tkinter
import customtkinter
from PIL import Image, ImageTk
import itertools


def animate_gif(label, frames, delay, count=[0]):
    frame = frames[count[0] % len(frames)]
    label.configure(image=frame)
    count[0] += 1
    label.after(delay, animate_gif, label, frames, delay, count)


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

# Label to display product information
p = customtkinter.CTkLabel(app, text="", font=("Arial", 15))
p.pack(pady=10)

# Function to update product information and image

# Add ui
main_label = customtkinter.CTkLabel(
    app, text="WELCOME TO TROLL-E", font=("Arial", 30))
main_label.pack(
    pady=50
)


def on_button_click(e):
    # print("clicked")
    get_product_info(barcode_data=scan_code())


h2 = customtkinter.CTkLabel(app, text="Scan your product", font=("Arial", 20))
h2.bind("<Button-1>", on_button_click)
h2.pack(pady=20)

# Add gif
gif_frames = load_gif("./Assets/NFC_gif/wCneoCuZt2 (1).gif")

# show gif
gif_label = customtkinter.CTkLabel(app, text="")
gif_label.pack(pady=20)
animate_gif(gif_label, gif_frames, 60)

# Run app
app.mainloop()
