import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, PngImagePlugin

def select_source_file():
    global source_file, source_label
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select source file",
                                          filetypes=(("PNG", "*.png"),))
    if filename:
        source_label.config(text=f"{filename.split('/')[-1]}")
        source_file = filename

def select_target_file():
    global target_file, target_label
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select target file",
                                          filetypes=(("PNG", "*.png"),))
    if filename:
        target_label.config(text=f"{filename.split('/')[-1]}")
        target_file = filename

def copy_png_info():
    global source_file, target_file
    if not source_file or not target_file:
        return messagebox.showerror(title="Oops", message="Please select both a source and target image")
    try:
        with Image.open(source_file, formats=("png",)) as source:
            info = source.info.get("parameters", None)
        if not info:
            return messagebox.showerror(title="Oops", message="No PNG info found in source image.")
        target = Image.open(target_file, formats=("png",))
    except:
        return messagebox.showerror(title="Oops", message="One of the images might've been moved or is invalid.")
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", info)
    target.save(target_file, format="png", pnginfo=pnginfo)
    messagebox.showinfo(title="Success", message=f"PNG Info copied to {target_file.split('/')[-1]}")

source_file, target_file = "", ""

window = tk.Tk()
window.title("Copy PNG Info")
window.geometry("500x150")

boxtop = tk.Frame(window, width=500, height=50)
boxmiddle = tk.Frame(window, width=500, height=50)
boxbottom = tk.Frame(window, width=500, height=50)
boxtop.grid(row=0, pady=10)
boxmiddle.grid(row=1)
boxbottom.grid(row=2)
boxmiddle.grid_propagate(0)
boxmiddle.columnconfigure(0, minsize=250)
boxmiddle.columnconfigure(1, minsize=250)

tk.Label(boxtop, text="This program will copy Stable Diffusion Generation data from one image to another.").pack()
tk.Button(boxmiddle, text="Select source", command=select_source_file).grid(row=0, column=0)
tk.Button(boxmiddle, text="Select target", command=select_target_file).grid(row=0, column=1)
source_label = tk.Label(boxmiddle, text="No file selected.")
target_label = tk.Label(boxmiddle, text="No file selected.")
source_label.grid(row=1, column=0)
target_label.grid(row=1, column=1)
tk.Button(boxbottom, text="Copy", command=copy_png_info).pack(pady=(0, 10))

window.mainloop()
