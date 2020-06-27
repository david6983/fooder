try:
    import os
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
    from tkinter import *
    from PIL import ImageTk, Image
    from resizeimage import resizeimage
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog

root = tk.Tk()

style = ttk.Style(root)
style.theme_use("clam")


def c_open_file_old():
    rep = filedialog.askopenfilenames(
        parent=root,
        initialdir='/',
        initialfile='tmp',
        filetypes=[
            ("JPEG", "*.jpg"),
            ("PNG", "*.png"),
            ("All files", "*")])
    try:
        print(rep[0])

        load = Image.open(rep[0])
        render = ImageTk.PhotoImage(load)
        img = Label(root, image=render)
        img.image = render
        img.grid(row=2, column=0, padx=4, pady=30, sticky='ew')
        rank = Label(root, text="Top 10").grid(row=3, column=0, padx=4, pady=30, sticky='ew')
        data = []
        data = get_all_images("dataset/macarons/", "jpg")
        ranking = 0
        for imgToRank in data:
            loadRank = Image.open(imgToRank)
            loadRank = resizeimage.resize_width(loadRank, 150)
            renderRank = ImageTk.PhotoImage(loadRank)
            imgRank = Label(root, image=renderRank)
            imgRank.image = renderRank
            imgRank.grid(row=4, column=ranking, padx=4, pady=4, sticky='ew')
            ranking += 1
        print(data)

    except IndexError:
        print("No file selected")


def get_all_images(folder, ext):
    all_files = []
    # Iterate through all files in folder
    for file in os.listdir(folder):
        # Get the file extension
        _, file_ext = os.path.splitext(file)

        # If file is of given extension, get it's full path and append to list
        if ext in file_ext:
            full_file_path = os.path.join(folder, file)
            all_files.append(full_file_path)

    # Get list of all files
    return all_files


ttk.Button(root, text="Open files", command=c_open_file_old).grid(row=1, column=0, padx=4, pady=4, sticky='ew')


root.mainloop()
