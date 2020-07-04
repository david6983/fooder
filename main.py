from matplotlib import pyplot
from sklearn.metrics import precision_recall_curve

from FooderImage import *
import math


def simple_query(full_path, as_gray=False):
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
    for image in data_set:
        if image.img_id is img_id:
            return image


def display_data_set(images_data_set):
    for image in images_data_set:
        image.debug()


def abs2(src, target):
    return abs(src - target) ** 2


def euclidean_distance(i1, i2, round_value):
    f1 = i1.get_feature_vector()
    f2 = i2.get_feature_vector()
    d = 0
    for v, v2 in zip(f1.values(), f2.values()):
        d += abs2(v, v2)

    return round(math.sqrt(d) / 100, round_value)


def generate_euclidean_set(data_set, query_image, round_value):
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
    relevant_images = []
    relevant_scores = []
    for image in top_n:
        print(get_image_by_id(data_set, image[0]).debug())
        relevant = int(input("Is this image relevant ? (1: yes, 0: no): "))
        relevant_images.append(relevant)
        relevant_scores.append(image[1])
    return relevant_images, relevant_scores


def pr_curve(relevant_images, relevant_scores):
    precision, recall, _ = precision_recall_curve(relevant_images, relevant_scores)
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


def main():
    print("Reading dataset...")
    extensions = ["jpg", "jpeg"]
    data_set = read_data_set("dataset/", extensions)
    #display_data_set(data_set)
    print("finish")

    print(data_set[3].get_feature_vector())

    # simple query
    q = simple_query("querry/1332510.jpg")
    print(q.debug())
    print("top: ")
    top_n = top_n_similarity(10, generate_euclidean_set(data_set, q, 5))
    relevant_images, relevant_scores = estimate_relevant_images_by_user_input(data_set, top_n)
    precision, recall = pr_curve(relevant_images, relevant_scores)
    display_pr_curve(precision, recall)


if __name__ == '__main__':
    main()
