from msilib.schema import RadioButton

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
positionRight = int(root.winfo_screenwidth() / 4 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 4 - windowHeight / 2)

# Positions the window in the center of the page.
root.geometry("1280x720+{}+{}".format(positionRight, positionDown))
style = ttk.Style(root)
style.theme_use("clam")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


frm = Frame(root)
frm.grid(row=0, column=0)
## Le canvas
cnv = Canvas(frm)
cnv.grid(row=0, column=0, sticky='nswe')



## Le canvas
cnv2 = Canvas(frm)
cnv2.grid(row=0, column=2, sticky='nswe')

## Les scrollbars
hScroll = Scrollbar(frm, orient=HORIZONTAL, command=cnv.xview)
hScroll.grid(row=1, column=0, sticky='we')

vScroll = Scrollbar(frm, orient=VERTICAL, command=cnv.yview)
vScroll.grid(row=0, column=1, sticky='ns')

cnv.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)

## Le Frame, dans le Canvas, mais sans pack ou grid

frm1 = Frame(cnv)
frm1.grid(row=0, column=0)

frm2 = Frame(cnv2)
frm2.grid(row=0, column=1)



def c_open_file_old():
    for widget in cnv.winfo_children():
        ## CHOIX 1:
        widget.grid_forget()


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
        load = resizeimage.resize_width(load, 380)
        render = ImageTk.PhotoImage(load)
        img = Label(frm2, image=render)
        img.image = render
        img.grid(row=1, column=1, padx=50, pady=3, sticky='ew')
        queryLabel = Label(frm2, text="Query",font=("none", 20)).grid(row=0, column=1, padx=4, pady=30,sticky='ew')
        categoryLabel= Label(frm, text="Category = ").grid(row=2, column= 2, padx=50, pady=5)
        #TODO Command for button precision
        precisionLabel=  Button(frm2, text="Precision", command=c_open_file_old).grid(row=1, column= 2, padx=50,pady=10)
        rank = Label(frm1, text="Top 10 Similarity",font=("none", 20)).grid(row=0, column=0, padx=5, pady=30)

        data = get_all_images("dataset/macarons/", "jpg")
        ranking = 1

        for imgToRank in data:
            loadRank = Image.open(imgToRank)
            loadRank = resizeimage.resize_width(loadRank, 200)
            renderRank = ImageTk.PhotoImage(loadRank)
            imgRank = Label(frm1, image=renderRank)
            imgRank.image = renderRank
            imgRank.grid(row=ranking, column=0, padx=4, pady=0, sticky='ew')
            my_details = "d = " + str("num_d") + " \n category = " + "category_detected" + "\n"
            Label(frm1, text=my_details).grid(row = ranking, column = 1);
            ranking += 1

        frm1.update()
        cnv.create_window(0, 0, window=frm1, anchor=NW)
        cnv.configure(scrollregion=cnv.bbox(ALL))
        categoryLabel=  Button(frm, text="New Query", command=c_open_file_old).grid(row=2, column= 1, padx=50,pady=10)
        categoryLabel=  Button(frm, text="New Query", command=c_open_file_old).grid(row=2, column= 1, padx=50,pady=10)





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


def frame_start():
    title = Label(cnv, text="Fooder (Food Image Retrieval)", font=("none", 40))
    title.grid(row=1, column=0, padx=4, pady=4)
    subtitle = Label(cnv, text="type of food available : donuts, sushis, pizzas, pancakes, macarons", font=("none", 20))
    subtitle.grid(row=2, column=0, padx=4, pady=4)

    Button(cnv, text="Open files", command=c_open_file_old).grid(row=3, column=0, padx=4, pady=100)

frame_start()

root.mainloop()
