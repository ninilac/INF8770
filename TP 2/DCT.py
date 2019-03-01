#code from moodle: https://github.com/gabilodeau/INF8770/blob/master/Transform%C3%A9e%20DCT%20et%20quantification.ipynb

import numpy as np
import scipy.fftpack as dctpack


def dctloop(img):
    DCTimg = np.zeros((np.size(img,axis=0),np.size(img,axis=1),np.size(img, axis=2),np.size(img, axis=3)),dtype=np.int64)
    for i in range(0, np.size(img, axis=0)):
        for j in range(0, np.size(img, axis=1)):
            DCTimg[i][j] = dct(img[i][j])
    return DCTimg


def dct(blocimg):
    blocimg = blocimg.astype(int)-128
    BlocDCT = dctpack.dct(dctpack.dct(blocimg, axis=0, norm='ortho'), axis=1, norm='ortho')
    return BlocDCT


def idctloop(DCTimg):
    img = np.zeros((np.size(DCTimg,axis=0),np.size(DCTimg,axis=1),np.size(DCTimg, axis=2),np.size(DCTimg, axis=3)),dtype=np.int64)
    for i in range(0, np.size(DCTimg, axis=0)):
        for j in range(0, np.size(DCTimg, axis=1)):
            img[i][j] = idct(DCTimg[i][j])
    return img


def idct(blocDCTimg):
    Blocimg = dctpack.idct(dctpack.idct(blocDCTimg, axis=0, norm='ortho'), axis=1, norm='ortho')+128
    return Blocimg