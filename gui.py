# from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as ttk

root = ttk.Window(themename="superhero", )
root.title("Troll-E")
root.iconbitmap("./Assets/troll-e.ico")
root.geometry("490x320")


my_label = ttk.Label(
    text="Welcome to Troll-E",
    font=("Arial", 20, "bold"),
    justify=CENTER,
)


my_label.pack(pady=100)

my_button = ttk.Button(
    text="Scan Barcode",
    default="active",
    bootstyle=(SUCCESS, "outline"),
)
my_button.pack(pady=150)

root.mainloop()
