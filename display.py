import tkinter as tk
import tkinter.ttk as ttk
import logging
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image
from resizeimage import resizeimage
import os

"""
This code is deprecated and no longer used !
"""

root = tk.Tk()
root.title("Fooder (CBIR Food Image Retrieval) by Haioum David and Boillot Mathias")

#center(root, width=625, height=300)
style = ttk.Style(root)
style.theme_use("clam")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_view = Frame(root)
main_view.grid(row=0, column=0)

# top n images in a scrollable window on the left
main_window = Canvas(main_view)
main_window.grid(row=0, column=0, sticky='nswe')

# query information on the right
query_view = Canvas(main_view)
query_view.grid(row=0, column=2, sticky='nswe')

# the frame goes inside the canvas without grid system

top_n_view_frame = Frame(main_window)
top_n_view_frame.grid(row=0, column=0)

query_view_frame = Frame(query_view)
query_view_frame.grid(row=0, column=1)


def open_image_callback():
    # clear the view
    for widget in main_window.winfo_children():
        widget.grid_forget()

    # open a file dialog that can open only .jpeg or .jpg images
    rep = filedialog.askopenfilenames(
        parent=root,
        initialdir='/',
        initialfile='tmp',
        filetypes=[
            ("JPEG", "*.jpg"),
            ("JPEG", "*.jpeg")
        ])
    try:
        #center(root, width=1000, height=500)
        # rep[0] is the file path of the image selected
        query_image_loaded = Image.open(rep[0])
        # resize the image for the display only
        query_image_loaded = resizeimage.resize_width(query_image_loaded, 200)
        # render the image as tkinter canvas and place it in the main window
        query_image_render = ImageTk.PhotoImage(query_image_loaded)
        img = Label(query_view_frame, image=query_image_render)
        img.image = query_image_render
        img.grid(row=1, column=1, padx=50, pady=3, sticky='ew')

        # Display query image information
        Label(query_view_frame, text="Query", font=("none", 20)).grid(row=0, column=1, padx=4, pady=30, sticky='ew')
        Label(main_view, text="Category: ").grid(row=2, column=2, padx=50, pady=5)
        # TODO Command for button precision
        Button(query_view_frame,
               text="display p/r curve",
               command=open_image_callback
               ).grid(row=1, column=2, padx=50, pady=10)
        # Label for the top 10 similarity window
        Label(top_n_view_frame, text="Top 10 similarity", font=("none", 20)).grid(row=0, column=0, padx=5, pady=30)

        # get the top_n similarity images here
        # TODO merge back-end here
        top_images = get_all_images("dataset/macarons/", "jpg")

        # ranking start from top 1
        ranking = 1

        for retrieved_image in top_images:
            # open the image and resize it for the display only
            image = Image.open(retrieved_image)
            image = resizeimage.resize_width(image, 200)
            # render it as tkinter component
            tk_image = ImageTk.PhotoImage(image)
            tk_image_label = Label(top_n_view_frame, image=tk_image)
            tk_image_label.image = tk_image
            tk_image_label.grid(row=ranking, column=0, padx=4, pady=0, sticky='ew')
            # TODO print distance here
            image_detail = "distance: " + str("0.345") + " \n category: " + "pancake" + "\n"
            # display the rank
            Label(top_n_view_frame, text=image_detail).grid(row=ranking, column=1)
            # increase the rank number displayed
            ranking += 1

        # update the frame
        top_n_view_frame.update()
        main_window.create_window(0, 0, window=top_n_view_frame, anchor=NW)
        # add scrollbars
        h_scroll = Scrollbar(main_view, orient=HORIZONTAL, command=main_window.xview)
        h_scroll.grid(row=1, column=0, sticky='we')
        v_scroll = Scrollbar(main_view, orient=VERTICAL, command=main_window.yview)
        v_scroll.grid(row=0, column=1, sticky='ns')
        main_window.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        main_window.configure(scrollregion=main_window.bbox(ALL))
        Button(main_view, text="New Query", command=open_image_callback).grid(row=2, column=1, padx=50, pady=10)

    except IndexError:
        # if we don't select any image, re-render the first view and display an error message
        main_view_start("No file selected")
        logging.warning("No file selected")


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


def main_view_start(error_message):
    title = Label(main_window, text="Fooder (CBIR Food Image Retrieval)", font=("none", 40))
    title.grid(row=1, column=0, padx=4, pady=4)

    subtitle = Label(main_window,
                     text="type of food available : donuts, sushis, pizzas, pancakes, macarons",
                     font=("none", 20))
    subtitle.grid(row=2, column=0, padx=4, pady=4)

    Button(main_window,
           text="Open Query Image",
           font=('Helvetica', '20'),
           command=open_image_callback,
           padx=50
           ).grid(row=3, column=0, padx=0, pady=50)
    # display error message
    Label(main_window, text=error_message, font=("none", 20), fg="red")


main_view_start("")

root.mainloop()
