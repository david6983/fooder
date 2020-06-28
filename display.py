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

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
print("Width", windowWidth, "Height", windowHeight)

# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth() /4 - windowWidth / 2)
positionDown = int(root.winfo_screenheight()/4 - windowHeight/2)

# Positions the window in the center of the page.
root.geometry("1280x720+{}+{}".format(positionRight, positionDown))
style = ttk.Style(root)
style.theme_use("clam")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

## Le canvas
cnv = Canvas(root)
cnv.grid(row=0, column=0, sticky='nswe')

## Les scrollbars
hScroll = Scrollbar(root, orient=HORIZONTAL, command=cnv.xview)
hScroll.grid(row=1, column=0, sticky='we')

vScroll = Scrollbar(root, orient=VERTICAL, command=cnv.yview)
vScroll.grid(row=0, column=1, sticky='ns')

cnv.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)

## Le Frame, dans le Canvas, mais sans pack ou grid
frm = Frame(cnv)

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
        img = Label(frm, image=render)
        img.image = render
        img.grid(row=2, column=0, padx=5, pady=50, sticky='ew')
        rank = Label(frm, text="Top 10").grid(row=1, column=1, padx=4, pady=30, sticky='ew')
        data = []
        data = get_all_images("dataset/macarons/", "jpg")
        ranking = 1
        for imgToRank in data:
            loadRank = Image.open(imgToRank)
            loadRank = resizeimage.resize_width(loadRank, 200)
            renderRank = ImageTk.PhotoImage(loadRank)
            imgRank = Label(frm, image=renderRank)
            imgRank.image = renderRank
            imgRank.grid(row=2, column=ranking, padx=10, pady=0, sticky='ew')
            ranking += 1
        frm.update()
        cnv.create_window(0, 0, window=frm, anchor=NW)
        cnv.configure(scrollregion=cnv.bbox(ALL))

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

ttk.Button(cnv, text="Open files", command=c_open_file_old).grid(row=1, column=0, padx=4, pady=4, sticky='ew')


root.mainloop()
