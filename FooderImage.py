from skimage.color import rgb2gray, rgb2lab
from skimage.io import imread
from skimage.feature import greycomatrix, greycoprops
from skimage.filters import threshold_otsu
from skimage.filters import median
from scipy.stats import skew
from skimage.morphology import area_closing
import numpy as np


class FooderImage:
    """
    This class represent an image in the dataset and it feature vector associated.
    """

    # count the number of instance of the class FooderImage. This is to give an id for each images
    count = 0

    def __init__(self, full_path, category="",
                 as_gray=False,
                 as_pre_processed=False,
                 auto_compute_glcm=False,
                 auto_compute_color_moment=False):
        """
        Constructor.

        :param full_path: full path of the jpeg image on the computer
        :param category: the food category of the image if known from the data set
        :param as_gray: is the image should be grey scale processed ?
        :param as_pre_processed: Should the image being pre-processed ?
        :param auto_compute_glcm: Do you want to compute the glcm once the image is read ?
        :param auto_compute_color_moment: Do you want to compute the color moment once the image is read ?
        """
        self.full_path = full_path
        self.img_id = FooderImage.count
        self.category = category
        self.is_gray = as_gray
        # read the image using skimage, the result is a nd-array depending on the color space
        # one 2D-array per channel for rgb image or one 2D-array for gray scale image
        self.img = imread(self.full_path, self.is_gray)
        # translate the rgb image to cie lab color space
        self.cie_img = rgb2lab(self.img)

        self.color_moment = None
        self.glcm = None

        # update next index
        FooderImage.count += 1

        if as_pre_processed:
            self.pre_process()
        if auto_compute_glcm:
            # the glcm distance is 1 and we are using the 4 angles for better precision
            self.compute_glcm(distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256)
        if auto_compute_color_moment:
            self.compute_color_moment()

    def read(self):
        """
        Read an image using skimage module

        :return: img_array ndarray The different color bands/channels are stored in the third dimension,
        such that a gray-image is MxN, an RGB-image MxNx3 and an RGBA-image MxNx4.
        """
        self.img = imread(self.full_path, self.is_gray)

    def to_gray_scale(self):
        """
        Translate the image from rgb color space to gray scale color space.

        :return: one 2D-array for gray scale image
        """
        self.img = rgb2gray(self.img)
        self.is_gray = True

    def pre_process(self):
        """
        Pre-processing algorithm to reduce noise of images

        :return: 2d-array of pixels
        """
        # translate to gray scale the rgb image
        self.to_gray_scale()
        # median filtering
        self.img = median(self.img)
        # otsu threshold
        thresh = threshold_otsu(self.img)
        self.img = self.img > thresh
        # closing
        self.img = area_closing(self.img, area_threshold=64)
        # the image pixel are considered as unsigned integer, not float
        self.img = self.img.astype(np.uint8)

    def compute_glcm(self, distances, angles, levels):
        """
        Compute the glcm using greycomatrix from skimage

        :param distances: List of pixel pair distance offsets. (array)
        :param angles: List of pixel pair angles in radians. (array)
        :param levels: number of grey-levels counted, 256 for a 8-bits image
        :return: 4-D ndarray The grey-level co-occurrence histogram. The value P[i,j,d,theta] is the number of times
        that grey-level j occurs at a distance d and at an angle theta from grey-level i.
        If normed is False, the output is of type uint32, otherwise it is float64
        """
        self.glcm = greycomatrix(self.img, distances, angles, levels)

    def get_glcm_props(self):
        """
        Extract the glcm props from the glcm histogram

        :return: dictionary that contains the 6 props of the glcm feature
        """
        return {
            "contrast": greycoprops(self.glcm, 'contrast')[0, 0],
            "dissimilarity": greycoprops(self.glcm, 'dissimilarity')[0, 0],
            "homogeneity": greycoprops(self.glcm, 'homogeneity')[0, 0],
            "ASM": greycoprops(self.glcm, 'ASM')[0, 0],
            "energy": greycoprops(self.glcm, 'energy')[0, 0],
            "correlation": greycoprops(self.glcm, 'correlation')[0, 0],
        }

    def compute_color_moment(self):
        """
        Compute the color moment feature of the image (the mean, variance and skewness).
        Concerning the mean, we compute the mean of the 3 means for each channel.

        :return: dictionary that contains the 3 props of the color moment feature
        """
        self.color_moment = {
            "mean": np.mean(np.mean(self.cie_img, axis=(0, 1))),
            "variance": np.var(self.cie_img),
            "skewness": skew(self.cie_img.reshape(-1))
        }

    def debug(self):
        """
        Terminal-based helping method to display the image characteristics and it feature vector.

        :return:
        """
        print("image" + str(self.img_id) + ": " + self.full_path)
        print("\tcategory: " + self.category)
        print("\tis_grey: " + str(self.is_gray))
        print("\tglcm_features: ")
        print(self.get_glcm_props())
        print("\tcolor_moment: ")
        print(self.color_moment)

    def get_feature_vector(self):
        """
        concatenate the glcm props and the color moment props

        :return:
        """
        return {**self.color_moment, **self.get_glcm_props()}