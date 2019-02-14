# code to import an image with consistent type: https://stackoverflow.com/questions/46013594/matplotlib-reads-jpg-into-int8-and-png-into-normalized-float

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import rgb2ycbcr

img = np.asarray(Image.open("Lena_512.png"))
img_no_alpha = img[:,:,:3]
plt.figure()
plt.imshow(img_no_alpha, cmap=plt.get_cmap('gray'))
plt.draw()

immod = rgb2ycbcr.rgb2ycbcr(img_no_alpha)
plt.figure()
plt.imshow(immod, cmap=plt.get_cmap('gray'))
plt.draw()


Y = immod[:,:,0]
Cb = immod[:,:,1]
Cr = immod[:,:,2]





# convert back



immod = rgb2ycbcr.ycbcr2rgb(immod)
plt.figure()
plt.imshow(immod, cmap=plt.get_cmap('gray'))
plt.draw()
plt.show()