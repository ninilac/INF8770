# Code based on https://github.com/gabilodeau/INF8770/blob/master/Codage%20predictif%20sur%20image.ipynb
# Huffman based on https://github.com/soxofaan/dahuffman/blob/master/dahuffman/huffmancodec.py

import numpy as np
import matplotlib.pyplot as py
import collections


def rgb2gray(rgb):
    return np.dot(rgb[:,:], [0.299, 0.587, 0.114])

def imfloat2uint8(image):
    return (image*255).astype('uint8')

fig1 = py.figure(figsize=(10,10))
imagelue = py.imread('gradient.png')
image = imagelue.astype('float')
image = rgb2gray(image)
image = imfloat2uint8(image)  #conversion en uint pour compression plus facile, on va considerer que l'image est en uint au depart.
py.imshow(image, cmap=py.get_cmap('gray'))
py.show()

hist, intervalles = np.histogram(image, bins=256)
py.bar(intervalles[:-1], hist, width=2)
py.xlim(min(intervalles)-1, max(intervalles))
#py.show()

erreur = np.zeros((len(image), len(image[0])-1))
imagepred = np.zeros((len(image), len(image[0])-1))

# image predite equivalente a l'image sans la derniere colonne
for i in range(0, len(image)):
    for j in range(0, len(image[0])-1):
        imagepred[i][j] = image[i][j] # on copie l'image sans la derniere colonne
        erreur[i][j] = imagepred[i][j]-image[i][j+1] # on fait un shift de 1 de l'image et on compare

hist, intervalles = np.histogram(erreur, bins=100)
py.bar(intervalles[:-1], hist, width=2)
py.xlim(min(intervalles)-1, max(intervalles))
py.show()

fig2 = py.figure(figsize=(10, 10))
py.imshow(imagepred, cmap=py.get_cmap('gray'))
py.show()

fig3 = py.figure(figsize=(10, 10))
py.imshow(erreur, cmap=py.get_cmap('gray'))
py.show()

# encodage de l'erreur avec la premiere colonne etant les pixels eux-memes
encodeErreur = np.column_stack([image[:, 0], erreur])
py.imshow(encodeErreur, cmap=py.get_cmap('gray'))
py.show()
