# code to import an image with consistent type: https://stackoverflow.com/questions/46013594/matplotlib-reads-jpg-into-int8-and-png-into-normalized-float

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import rgb2ycbcr
import imgsplit
import DCT
import zigzag

img = np.asarray(Image.open("Lena_512.png"))
img_no_alpha = img[:,:,:3]
plt.figure()
plt.imshow(img_no_alpha, cmap=plt.get_cmap('gray'))
plt.draw()

# conversion to YCbCr
immod = rgb2ycbcr.rgb2ycbcr(img_no_alpha)
plt.figure()
plt.imshow(immod, cmap=plt.get_cmap('gray'))
plt.draw()

# Split into 8x8 regions
Y = immod[:,:,0]
Cb = immod[:,:,1]
Cr = immod[:,:,2]

Ysplit = imgsplit.imgsplit(Y)
Cbsplit = imgsplit.imgsplit(Cb)
Crsplit = imgsplit.imgsplit(Cr)

# DCT
YDCT = DCT.dctloop(Ysplit)
CbDCT = DCT.dctloop(Cbsplit)
CrDCT = DCT.dctloop(Crsplit)

#zigzag
Yz = zigzag.zigzag(YDCT)
Cbz = zigzag.zigzag(CbDCT)
Crz = zigzag.zigzag(CrDCT)

# convert back

#reverse zigzag
YDCT = zigzag.zagzig(Yz)
CbDCT = zigzag.zagzig(Cbz)
CrDCT = zigzag.zagzig(Crz)

# inverse DCT
Ysplit = DCT.idctloop(YDCT)
Cbsplit = DCT.idctloop(CbDCT)
Crsplit = DCT.idctloop(CrDCT)

# recombine the 8x8 regions
Yunsplit = imgsplit.imgunsplit(Ysplit)
Cbunsplit = imgsplit.imgunsplit(Cbsplit)
Crunsplit = imgsplit.imgunsplit(Crsplit)

im_recombine = np.dstack((Yunsplit, Cbunsplit, Crunsplit))

# convert back to RGB
immod = rgb2ycbcr.ycbcr2rgb(im_recombine)
plt.figure()
plt.imshow(immod, cmap=plt.get_cmap('gray'))
plt.draw()
plt.show()