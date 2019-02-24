import numpy as np


def imgsplit(img):
    sections_x = np.size(img, axis=0) / 8
    sections_y = np.size(img, axis=1) / 8
    split_img = np.reshape(img,(sections_x,sections_y,8,8))
    #x_split = np.split(img, sections_x, axis=0)
    #y_split = np.split(x_split, sections_y, axis=1)
    return split_img

def imgunsplit(img):
    size_x = np.size(img, axis=0) * np.size(img, axis=2)
    size_y = np.size(img, axis=1) * np.size(img, axis=3)
    unsplit_img = np.reshape(img, (size_x, size_y))
    return unsplit_img;