import tkinter
import customtkinter
from PIL import Image, ImageTk
import itertools
from Scanner import get_product_name, scan_code


def Main_window():

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

    # Add ui
    main_label = customtkinter.CTkLabel(
        app, text="WELCOME TO TROLL-E", font=("Gunship", 20))
    main_label.pack(
        pady=20
    )
    label = customtkinter.CTkLabel(app, text="Please tap your phone here")
    label.pack(
        pady=10, padx=10
    )

    def on_button_click(e):
        get_product_name(barcode_data=scan_code())

    label.bind("<Button-1>", on_button_click )

    # Add gif
    gif_frames = load_gif("./Assets/NFC_gif/wCneoCuZt2 (1).gif")

    # show gif
    gif_label = customtkinter.CTkLabel(app, text="")
    gif_label.pack(pady=20)
    animate_gif(gif_label, gif_frames, 60)

    # Run app
    app.mainloop()


Main_window()
