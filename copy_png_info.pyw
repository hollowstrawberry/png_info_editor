import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, PngImagePlugin

def select_source_file():
    global source_label, textbox
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select source file",
                                          filetypes=(("PNG", "*.png"),))
    if filename:
        with Image.open(filename, formats=("png",)) as source:
            info = source.info.get("parameters", None)
        if not info:
            return messagebox.showerror(title="Oops", message="No PNG info found in this image.")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", info)
        apply_color(None)

def select_target_file():
    global target_file, target_label
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select target file",
                                          filetypes=(("PNG", "*.png"),))
    if filename:
        target_label.config(text=f"{filename.split('/')[-1]}")
        target_file = filename

def copy_png_info():
    global target_file, textbox
    info = textbox.get("1.0",'end-1c').strip()
    if not info:
        return messagebox.showerror(title="Oops", message="Please select a file to copy PNG info from, or write your own.")
    if not target_file:
        return messagebox.showerror(title="Oops", message="Please select a target image to save the PNG info to.")
    try:
        target = Image.open(target_file, formats=("png",))
    except:
        return messagebox.showerror(title="Oops", message="The target image might've been moved or is invalid.")
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", info)
    target.save(target_file, format="png", pnginfo=pnginfo)
    messagebox.showinfo(title="Success", message=f"PNG info copied to {target_file.split('/')[-1]}")

def apply_color(event):
    global textbox
    textbox.tag_remove("blue", "1.0", "end")
    lines = textbox.get(1.0, "end").splitlines()
    for i, line in enumerate(lines):
        for match in re.finditer(r"(^|, )([\w ]+):", line):
            textbox.tag_add("blue", f"{i+1}.{match.start(2)}", f"{i+1}.{match.end(2)}")


WIDTH = 700
HEIGHT = 400

target_file = ""

window = tk.Tk()
window.title("Copy PNG Info")
window.geometry(f"{WIDTH}x{HEIGHT}")

boxtop = tk.Frame(window, width=WIDTH, height=50)
boxmiddle = tk.Frame(window, width=WIDTH, height=100)
boxbottom = tk.Frame(window, width=WIDTH, height=250)
window.columnconfigure(0, minsize=WIDTH)
boxtop.grid(row=0, pady=10)
boxmiddle.grid(row=1)
boxbottom.grid(row=2)
boxmiddle.grid_propagate(0)
boxmiddle.columnconfigure(0, minsize=WIDTH//2-40)
boxmiddle.columnconfigure(2, minsize=WIDTH//2-40)

tk.Label(boxtop, text="This program lets you copy and edit Stable Diffusion Generation data between images.").pack()
tk.Button(boxmiddle, text="Copy from image", command=select_source_file).grid(row=0, column=0)
tk.Button(boxmiddle, text="Select target image", command=select_target_file).grid(row=0, column=2)
tk.Button(boxmiddle, text="Copy to target", command=copy_png_info).grid(row=2, column=1)
source_label = tk.Label(boxmiddle, text="No file selected.")
target_label = tk.Label(boxmiddle, text="No file selected.")
source_label.grid(row=1, column=0)
target_label.grid(row=1, column=2)
scrollbar = tk.Scrollbar(boxbottom, orient='vertical')
scrollbar.pack(side="right", fill='y')
textbox = tk.Text(boxbottom, width=80, height=15, font=("Lucida Sans Typewriter",10), yscrollcommand=scrollbar.set)
scrollbar.config(command=textbox.yview)
textbox.pack()
textbox.bind("<KeyRelease>", apply_color)
textbox.tag_configure("blue", foreground="blue")

window.mainloop()
