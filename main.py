from FooderImage import *

# step 1 - read the images and apply gray scale
# note: the images are already scaled


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
                                             auto_compute_color_moment=True)
                                 )

    return all_files


def display_data_set(images_data_set):
    for category in images_data_set:
        print("displaying category " + category)
        for image in images_data_set[category]:
            plt.imshow(image)
            plt.show()




print("Reading dataset...")
extensions = ["jpg", "jpeg"]
data_set = read_data_set("dataset/", extensions)
print("finish")

print(data_set[3].debug())
