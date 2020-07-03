from skimage.color import rgb2gray, rgb2lab
from skimage.io import imread, imshow
from skimage.feature import greycomatrix, greycoprops
from skimage.filters import threshold_otsu
from skimage.filters import median
from sklearn.metrics.pairwise import euclidean_distances
from scipy.stats import moment, skew, kurtosis
from skimage.morphology import area_closing
import matplotlib.pyplot as plt
import os
import numpy as np


class FooderImage:
    def __init__(self, full_path, category="",
                 as_gray=False,
                 as_pre_processed=False,
                 auto_compute_glcm=False,
                 auto_compute_color_moment=False):
        self.full_path = full_path
        self.category = category
        self.is_gray = as_gray
        self.img = imread(self.full_path, self.is_gray)
        self.cie_img = rgb2lab(self.img)
        self.color_moment = None
        self.glcm = None
        if as_pre_processed:
            self.pre_process()
        if auto_compute_glcm:
            self.compute_glcm(distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256)
        if auto_compute_color_moment:
            self.compute_color_moment()

    def read(self):
        self.img = imread(self.full_path, self.is_gray)

    def to_gray_scale(self):
        self.img = rgb2gray(self.img)
        self.is_gray = True

    def pre_process(self):
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
        self.to_gray_scale()
        self.img = median(self.img)
        thresh = threshold_otsu(self.img)
        self.img = self.img > thresh
        self.img = area_closing(self.img, area_threshold=64)
        self.img = self.img.astype(np.uint8)

    def compute_glcm(self, distances, angles, levels):
        self.glcm = greycomatrix(self.img, distances, angles, levels)

    def get_glcm_props(self):
        return {
            "contrast": greycoprops(self.glcm, 'contrast')[0, 0],
            "dissimilarity": greycoprops(self.glcm, 'dissimilarity')[0, 0],
            "homogeneity": greycoprops(self.glcm, 'homogeneity')[0, 0],
            "ASM": greycoprops(self.glcm, 'ASM')[0, 0],
            "energy": greycoprops(self.glcm, 'energy')[0, 0],
            "correlation": greycoprops(self.glcm, 'correlation')[0, 0],
        }

    def compute_color_moment(self):
        self.color_moment = {
            "mean": np.mean(np.mean(self.cie_img, axis=(0, 1))),
            "variance": np.var(self.cie_img),
            "skewness": skew(self.cie_img.reshape(-1))
        }

    def debug(self):
        print("image: " + self.full_path)
        print("\tcategory: " + self.category)
        print("\tis_grey: " + str(self.is_gray))
        print("\tglcm_features: ")
        print(self.get_glcm_props())
        print("\tcolor_moment: ")
        print(self.color_moment)