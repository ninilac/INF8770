import numpy as np

def imgsplit(img):
    split_img = np.empty([0])
    sections_x = np.size(img, axis=0) / 8
    sections_y = np.size(img, axis=1) / 8
    x_split = np.split(img, sections_x, axis=0)
    for im in x_split:
        np.split(im, sections_y, axis=1)
        split_img[]