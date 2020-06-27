from skimage.io import imread, imshow
import matplotlib.pyplot as plt
import os

# step 1 - read the images and apply gray scale
# note: the images are already scaled


def read_data_set(dir_name, allowed_extensions, as_gray=False):
    # create a list of file and sub directories
    # names in the given directory
    list_of_file = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_file:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + read_data_set(full_path)
        else:
            if full_path.split("/")[2].split(".")[1] in allowed_extensions:
                all_files.append(imread(full_path, as_gray))

    return all_files


def display_data_set(images_data_set):
    for category in images_data_set:
        print("displaying category " + category)
        for image in images_data_set[category]:
            plt.imshow(image)
            plt.show()


extensions = ["jpg", "jpeg"]
data_set_colored = {
    "donuts": read_data_set("dataset/donuts", extensions),
    "macarons": read_data_set("dataset/macarons", extensions),
    "pancake": read_data_set("dataset/pancake", extensions),
    "pizza": read_data_set("dataset/pizza", extensions),
    "sushi": read_data_set("dataset/sushi", extensions)
}

# pre-processing

"""
1. median filtering
2. segmentation
3. otsu threshold
4. closing
5. glcm
6. cie lab
7. euclidean distance
8. ranking
"""

