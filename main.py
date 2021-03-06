from matplotlib import pyplot
from sklearn.metrics import precision_recall_curve
import tkinter as tk
import tkinter.ttk as ttk
import logging
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from FooderImage import *
import math
import os


def center(win, width, height):
    """
    Center any graphical window.

    :param win: window to center
    :param width: width
    :param height: height
    :return: Void
    """
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Graphical interface setttings
root = tk.Tk()
# title
root.title("Fooder (CBIR Food Image Retrieval) by Haioum David and Boillot Mathias")
# center and set a width and a height
center(root, width=625, height=300)
# same gap on the left and on the right
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# grid system
main_view = Frame(root)
main_view.grid(row=0, column=0)
main_window = Canvas(main_view)
main_window.grid(row=0, column=0, sticky='nswe')

# gui style
style = ttk.Style(root)
style.theme_use("clam")


def simple_query(full_path, as_gray=False):
    # simplify the creation of a query
    return FooderImage(full_path,
                       as_gray=as_gray,
                       as_pre_processed=True,
                       auto_compute_glcm=True,
                       auto_compute_color_moment=True)


def read_data_set(dir_name, allowed_extensions, as_gray=False):
    # create a list of file and sub directories
    # names in the given directory
    list_of_file = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_file:
        if entry is ".DS_Store":
            break
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + read_data_set(full_path, allowed_extensions, as_gray)
        else:
            if entry.split(".")[1] in allowed_extensions:
                all_files.append(FooderImage(full_path,
                                             category=full_path.split("/")[1],
                                             as_gray=as_gray,
                                             as_pre_processed=True,
                                             auto_compute_glcm=True,
                                             auto_compute_color_moment=True))

    return all_files


def get_image_by_id(data_set, img_id):
    """
    get an image from the dataset by giving the id in the dataset
    """
    for image in data_set:
        if image.img_id is img_id:
            return image


def display_data_set(images_data_set):
    for image in images_data_set:
        image.debug()


def abs2(src, target):
    """
    compute the square absolute value of two number.

    :param src: first value
    :param target: second value
    :return: square absolute value
    """
    return abs(src - target) ** 2


def euclidean_distance(i1, i2, round_value):
    """
    Compute the euclidean distance and normalize it between [0, 1]

    :param i1: first image
    :param i2: second image
    :param round_value: how many digits ?
    :return: normalized euclidean distance of the to images
    """
    f1 = i1.get_feature_vector()
    f2 = i2.get_feature_vector()
    d = 0
    for v, v2 in zip(f1.values(), f2.values()):
        d += abs2(v, v2)

    return round(math.sqrt(d) / 100, round_value)


def generate_euclidean_set(data_set, query_image, round_value):
    """
    Get a sorted list of (id of the image, euclidean distance generated)

    :param data_set:
    :param query_image:
    :param round_value:
    :return:
    """
    row = []
    for image in data_set:
        row.append((image.img_id, euclidean_distance(image, query_image, round_value)))

    return sorted(row, key=lambda x: x[1])


def top_n_similarity(n, euclidean_distance_set):
    top_n = []
    for i in range(0, n):
        top_n.append(euclidean_distance_set[i])
    return top_n


def estimate_relevant_images_by_user_input(data_set, top_n):
    """
    The user is asked to rate each images retrieved using terminal

    1: the image is relevant
    0: the image is not relevant

    :param data_set:
    :param top_n:
    :return:
    """
    relevant_images = []
    relevant_scores = []
    for image in top_n:
        print(get_image_by_id(data_set, image[0]).debug())
        print("distance: " + str(image[1]))
        relevant = int(input("Is this image relevant ? (1: yes, 0: no): "))
        relevant_images.append(relevant)
        relevant_scores.append(image[1])
    return relevant_images, relevant_scores


def pr_curve(relevant_images, relevant_scores):
    # use sklearn and matplotlib to display the curve
    precision, recall, threshold = precision_recall_curve(relevant_images, relevant_scores)
    return precision, recall


def display_pr_curve(precision, recall):
    pyplot.plot(recall, precision, marker='.', label='Colour-Texture')
    # axis labels
    pyplot.xlabel('Recall')
    pyplot.ylabel('Precision')
    # show the legend
    pyplot.legend()
    # show the plot
    pyplot.show()


def open_query_window(root, image_path):
    # create a new window to display the query image selected
    query_window = tk.Toplevel(root)
    query_window.title("Query characteristics")
    query_window.grid_columnconfigure(0, weight=1)
    center(query_window, width=500, height=700)
    # title of the window
    Label(query_window, text="Query", font=("none", 20)).grid(row=0, column=0, sticky='nsew')
    # display the image
    query_image_loaded = Image.open(image_path)
    # render the image as tkinter canvas and place it in the main window
    query_image_render = ImageTk.PhotoImage(query_image_loaded)
    img = Label(query_window, image=query_image_render)
    img.image = query_image_render
    img.grid(row=1, column=0, sticky='nsew')
    # display characteristics
    Label(query_window, text="path: " + image_path).grid(row=2, column=0)
    return query_window


def open_image_callback():
    # open a file dialog that can open only .jpeg or .jpg images
    out = filedialog.askopenfilenames(
        parent=root,
        initialdir='/',
        initialfile='tmp',
        filetypes=[
            ("JPEG", "*.jpg"),
            ("JPEG", "*.jpeg")
        ])
    try:
        # The processing can start here
        print("Reading dataset...")
        extensions = ["jpg", "jpeg"]
        data_set = read_data_set("dataset/", extensions)
        print("data set successfully read")
        # create the query window
        open_query_window(root, out[0])
        # create the top 10 similarity window
        # simple query
        q = simple_query(out[0])
        print("top 10 similarity: ")
        # compute top n similarity
        top_n = top_n_similarity(10, generate_euclidean_set(data_set, q, 5))
        # get the relevant images and their scores
        relevant_images, relevant_scores = estimate_relevant_images_by_user_input(data_set, top_n)
        # generate precision and recall values
        precision, recall = pr_curve(relevant_images, relevant_scores)
        # display the p/r curve
        display_pr_curve(precision, recall)

    except IndexError:
        # if we don't select any image, re-render the first view and display an error message
        simple_query_gui("No file selected")
        logging.warning("No file selected")


def simple_query_gui(error_message):
    # insert a title
    title = Label(main_window, text="Fooder (CBIR Food Image Retrieval)", font=("none", 40))
    title.grid(row=1, column=0, padx=4, pady=4)
    # insert a subtitle
    subtitle = Label(main_window,
                     text="type of food available : donuts, sushis, pizzas, pancakes, macarons",
                     font=("none", 20))
    subtitle.grid(row=2, column=0, padx=4, pady=4)
    # generate a button that call the function open_image_callback()
    Button(main_window,
           text="Open Query Image",
           font=('Helvetica', '20'),
           command=open_image_callback,
           padx=50
           ).grid(row=3, column=0, padx=0, pady=50)
    # display error message if any
    Label(main_window, text=error_message, font=("none", 20), fg="red")


def main():
    # launch the gui to open an image
    simple_query_gui("")
    root.mainloop()


if __name__ == '__main__':
    main()
