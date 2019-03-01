import numpy as np

def quantify(img, Qmat):
    (a,b,x,y) = img.shape
    newImg = np.zeros(img.shape)
    for m in range(0,a):
        for n in range(0,b):
            newImg[m][n] = img[m][n]/ Qmat
    return newImg

def dequantify(img, Qmat):
    (a,b,x,y) = img.shape
    newImg = np.zeros(img.shape)
    for m in range(0,a):
        for n in range(0,b):
            newImg[m][n] = img[m][n]* Qmat
    return newImg
