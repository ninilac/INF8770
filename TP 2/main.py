# code to import an image with consistent type: https://stackoverflow.com/questions/46013594/matplotlib-reads-jpg-into-int8-and-png-into-normalized-float
# quantification matrix: https://www.researchgate.net/figure/Recommended-JPEG-quantization-matrix_fig2_5566221

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import rgb2ycbcr
import imgsplit
import DCT
import quantification
import zigzag
import Huffman

def jpgPipeline(im, Qmat):
    # conversion to YCbCr
    immod = rgb2ycbcr.rgb2ycbcr(im)
    plt.figure()
    plt.imshow(immod, cmap=plt.get_cmap('gray'))
    plt.draw()

    # separation of each channel
    Y = immod[:,:,0]
    Cb = immod[:,:,1]
    Cr = immod[:,:,2]

    #subsampling of Cb and Cr
    Cbsub = Cb[0::2, 0::2]
    Crsub = Cr[0::2, 0::2]

    # Split into 8x8 regions
    Ysplit = imgsplit.imgsplit(Y)
    Cbsplit = imgsplit.imgsplit(Cbsub)
    Crsplit = imgsplit.imgsplit(Crsub)

    # DCT
    YDCT = DCT.dctloop(Ysplit)
    CbDCT = DCT.dctloop(Cbsplit)
    CrDCT = DCT.dctloop(Crsplit)

    # quantification
    Yq = quantification.quantify(YDCT, Qmat)
    Cbq = quantification.quantify(CbDCT, Qmat)
    Crq = quantification.quantify(CrDCT, Qmat)

    #zigzag
    Yz = zigzag.zigzag(Yq)
    Cbz = zigzag.zigzag(Cbq)
    Crz = zigzag.zigzag(Crq)

    # Huffman
    YH = Huffman.huffman_encoding(Yz)
    CbH = Huffman.huffman_encoding(Cbz)
    CrH = Huffman.huffman_encoding(Crz)

    # size calculation
    finalSize = YH.getSize()
    finalSize += CbH.getSize()
    finalSize += CrH.getSize()

    # convert back

    # Huffman decoding
    # skipped, as we were told we could skip it


    #reverse zigzag
    Yq = zigzag.zagzig(Yz)
    Cbq = zigzag.zagzig(Cbz)
    Crq = zigzag.zagzig(Crz)

    # quantification inverse
    YDCT = quantification.dequantify(Yq, Qmat)
    CbDCT = quantification.dequantify(Cbq, Qmat)
    CrDCT = quantification.dequantify(Crq, Qmat)

    # inverse DCT
    Ysplit = DCT.idctloop(YDCT)
    Cbsplit = DCT.idctloop(CbDCT)
    Crsplit = DCT.idctloop(CrDCT)

    # recombine the 8x8 regions
    Yunsplit = imgsplit.imgunsplit(Ysplit)
    Cbunsplit = imgsplit.imgunsplit(Cbsplit)
    Crunsplit = imgsplit.imgunsplit(Crsplit)

    # unsubsampling of Cb and Cr
    Cbunsubx = np.repeat(Cbunsplit, 2, axis=0)
    Cbunsub = np.repeat(Cbunsubx, 2, axis=1)
    Crunsubx = np.repeat(Crunsplit, 2, axis=0)
    Crunsub = np.repeat(Crunsubx, 2, axis=1)

    im_recombine = np.dstack((Yunsplit, Cbunsub, Crunsub))

    # convert back to RGB
    imfinal = rgb2ycbcr.ycbcr2rgb(im_recombine)
    plt.figure()
    plt.imshow(imfinal, cmap=plt.get_cmap('gray'))
    plt.draw()
    plt.show()

    compression = 1-(float(finalSize)/float(originalSize))

    print "original size: " + str(originalSize)
    print "final size: " + str(finalSize)
    print "compression rate: " + str(compression)

    return imfinal

img = np.asarray(Image.open("Lena_512.png"))
if(len(img.shape) == 2):
    img = np.dstack((img, img, img))
img_no_alpha = img[:,:,:3]
plt.figure()
plt.imshow(img_no_alpha, cmap=plt.get_cmap('gray'))
plt.draw()
originalSize = img_no_alpha.size*8 # number of bits used per value in the image

mat50 = np.ones((8, 8))
mat50.fill(50)

matQ = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                 [12, 12, 14, 19, 26, 58, 60, 55],
                 [14, 13, 16, 24, 40, 57, 69, 56],
                 [14, 17, 22, 29, 51, 87, 80, 62],
                 [18, 22, 37, 56, 68, 109, 103, 77],
                 [24, 35, 55, 64, 81, 104, 113, 92],
                 [49, 64, 78, 87, 103, 121, 120, 101],
                 [72, 92, 95, 98, 112, 100, 103, 99]]).astype(np.float64)

matQ2 = np.array([[1, 1, 15, 15, 40, 40, 70, 70],
                  [1, 1, 15, 15, 40, 40, 70, 70],
                  [1, 1, 15, 15, 40, 40, 70, 70],
                  [1, 1, 15, 15, 40, 40, 70, 70],
                  [1, 1, 15, 15, 40, 40, 70, 70],
                  [1, 1, 15, 15, 40, 40, 70, 70],
                  [1, 1, 15, 15, 40, 40, 70, 70],
                  [1, 1, 15, 15, 40, 40, 70, 70],]).astype(np.float64)

img1 = jpgPipeline(img, matQ)
img2 = jpgPipeline(img1, matQ2)
img3 = jpgPipeline(img2, mat50)
