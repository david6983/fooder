from skimage.color import rgb2gray, rgb2lab
from skimage.io import imread, imshow
from skimage.feature import greycomatrix, greycoprops
from skimage.filters import threshold_otsu
from skimage.filters import median
from sklearn.metrics.pairwise import euclidean_distances
from scipy.stats import moment, skew
from skimage.morphology import area_closing
import matplotlib.pyplot as plt
import os
import numpy as np


class FooderImage:
    def __init__(self, full_path, category="", as_pre_processed=False):
        self.full_path = full_path
        self.category = category
        self.is_grey = False
        self.img = imread(self.full_path, self.is_grey)
        if as_pre_processed:
            self.pre_process()

    def read(self):
        self.img = imread(self.full_path, self.is_grey)

    def to_gray_scale(self):
        self.img = rgb2gray(self.img)
        self.is_grey = True

    def pre_process(self):
        self.to_gray_scale()
        self.img = median(self.img)
        thresh = threshold_otsu(self.img)
        self.img = self.img > thresh
        self.img = area_closing(self.img, area_threshold=64)
        self.img = self.img.astype(np.uint8)
