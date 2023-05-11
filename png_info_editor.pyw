import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, PngImagePlugin

START = "1.0"
ERROR = "Oops"

def select_source_file():
    global source_label, textbox
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select source file", filetypes=(("PNG", "*.png"),))
    if filename:
        with Image.open(filename, formats=("png",)) as source:
            info = source.info.get("parameters", None)
        if not info:
            return messagebox.showerror(title="Oops", message="No PNG info found in this image.")
        source_label.config(text=f"{filename.split('/')[-1]}")
        textbox.delete(START, tk.END)
        textbox.insert(START, info)
        apply_color()

def select_target_file():
    global target_file, target_label
    filename = filedialog.askopenfilename( initialdir=os.getcwd(), title="Select target file", filetypes=(("PNG", "*.png"),))
    if filename:
        target_label.config(text=f"{filename.split('/')[-1]}")
        target_file = filename

def copy_png_info():
    global target_file, textbox
    info = textbox.get(START, tk.END).strip()
    if not info:
        return messagebox.showerror(title=ERROR, message="Please select a file to copy PNG info from, or write your own.")
    if not target_file:
        return messagebox.showerror(title=ERROR, message="Please select a target image to save the PNG info to.")
    try:
        target = Image.open(target_file, formats=("png",))
    except:
        return messagebox.showerror(title=ERROR, message="The target image might've been moved or is invalid.")
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", info)
    target.save(target_file, format="png", pnginfo=pnginfo)
    messagebox.showinfo(title="Success", message=f"PNG info copied to {target_file.split('/')[-1]}")

def apply_color(event=None):
    global textbox, tags
    for tag in tags:
        textbox.tag_remove(tag, START, tk.END)
    lines = textbox.get(START, tk.END).splitlines()
    for i, line in enumerate(lines):
        for tag, pattern in tags.items():
            for match in re.finditer(pattern, line):
                textbox.tag_add(tag, f"{i+1}.{match.start(1)}", f"{i+1}.{match.end(1)}")

tags = {
    "blue": r"(?:^|, )([\w ]+):",
    "purple": r"(<\w+:[^>]+>)",
}

target_file = ""

window = tk.Tk()
window.title("PNG Info editor")

boxtop = tk.Frame(window)
boxmiddle = tk.Frame(window)
boxbottom = tk.Frame(window)
boxtop.grid(row=0)
boxmiddle.grid(row=1)
boxbottom.grid(row=2, padx=5, pady=(0, 10))
for i in range(5):
    boxmiddle.columnconfigure(i, minsize=100)

tk.Label(boxtop, text="This program lets you copy and edit Stable Diffusion Generation data between images.").pack()
tk.Button(boxmiddle, text="Copy from image", command=select_source_file).grid(row=0, column=1)
tk.Button(boxmiddle, text="Select target image", command=select_target_file).grid(row=0, column=3)
source_label = tk.Label(boxmiddle, text="No file selected.")
target_label = tk.Label(boxmiddle, text="No file selected.")
source_label.grid(row=1, column=1)
target_label.grid(row=1, column=3)

tk.Button(boxbottom, text="Copy to target", command=copy_png_info).pack(side=tk.TOP, pady=5)
scrollbar = tk.Scrollbar(boxbottom, orient="vertical")
textbox = tk.Text(boxbottom, font=("Lucida Sans Typewriter", 10), yscrollcommand=scrollbar.set)
scrollbar.config(command=textbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
textbox.pack(expand=True, fill=tk.BOTH)

textbox.bind("<KeyRelease>", apply_color)
for tag in tags:
    textbox.tag_configure(tag, foreground=tag)

window.mainloop()
