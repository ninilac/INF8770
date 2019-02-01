# Code based on https://github.com/gabilodeau/INF8770/blob/master/Codage%20predictif%20sur%20image.ipynb

# Some parts of the Huffman code were inspired by
# https://github.com/soxofaan/dahuffman/blob/master/dahuffman/huffmancodec.py

# numpy library: http://www.numpy.org/
# matplotlib library: https://matplotlib.org/
# collections library: https://github.com/python/cpython/blob/2.7/Lib/collections.py
# sys library: built in
# bitarray library: https://pypi.org/project/bitarray/
# uuid library: https://github.com/python/cpython/blob/2.7/Lib/uuid.py

#Node class from https://www.tutorialspoint.com/python/python_binary_tree.htm

import numpy as np
import matplotlib.pyplot as py
import collections
import sys
import bitarray
import uuid

class Node:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data


    def printTree(self):
        print(self.data)

    def isLeaf(self):
        return self.left is None and self.right is None

def assignbit(substitutions, node, bits):
    if node.isLeaf():
        substitutions[node.data[0]] = bits
    else:
        bitsleft = bits.copy()
        bitsleft.append(True)
        assignbit(substitutions, node.left, bitsleft)
        bitsright = bits.copy()
        bitsright.append(False)
        assignbit(substitutions, node.right, bitsright)
    return substitutions

def rgb2gray(rgb):
    return np.dot(rgb[:,:], [0.299, 0.587, 0.114])

def imfloat2uint8(image):
    return (image*255).astype('uint8')

fig1 = py.figure(figsize=(10,10))
imagelue = py.imread('louvre.jpeg')
image = imagelue.astype('float')
image = rgb2gray(image)
image = imfloat2uint8(image)  #conversion en uint pour compression plus facile, on va considerer que l'image est en uint au depart.
py.imshow(image, cmap=py.get_cmap('gray'))
#py.show()

bytesize = 8 #size of a uint8
#originalSize = sys.getsizeof(image)*bytesize
originalSize = sys.getsizeof(image.tobytes()) * bytesize # get the size of the corresponding byte array to remove any extra data

hist, intervalles = np.histogram(image, bins=256)
py.bar(intervalles[:-1], hist, width=2)
py.xlim(min(intervalles)-1, max(intervalles))
#py.show()

erreur = np.zeros((len(image), len(image[0])-1), dtype=np.int8)
imagepred = np.zeros((len(image), len(image[0])-1), dtype=np.int8)

# image predite equivalente a l'image sans la derniere colonne
for i in range(0, len(image)):
    for j in range(0, len(image[0])-1):
        imagepred[i][j] = image[i][j] # on copie l'image sans la derniere colonne
        erreur[i][j] = imagepred[i][j]-image[i][j+1] # on fait un shift de 1 de l'image et on compare

hist, intervalles = np.histogram(erreur, bins=100)
py.bar(intervalles[:-1], hist, width=2)
py.xlim(min(intervalles)-1, max(intervalles))
#py.show()

fig2 = py.figure(figsize=(10, 10))
py.imshow(imagepred, cmap=py.get_cmap('gray'))
#py.show()

fig3 = py.figure(figsize=(10, 10))
py.imshow(erreur, cmap=py.get_cmap('gray'))
#py.show()

# encodage de l'erreur avec la premiere colonne etant les pixels eux-memes
encodedErreur = np.column_stack([image[:, 0], erreur])
py.imshow(encodedErreur, cmap=py.get_cmap('gray'))
#py.show()

#Huffman
c = collections.Counter()
encodedErreur = encodedErreur.ravel()

for value in encodedErreur:
    c[value] += 1

ccopy = c.copy()

#Keeps all the subtree roots for building the Huffman tree
Roots = dict()

#Build the Huffman tree
while(len(c) > 1):

    #get first min
    min1 = min(c, key=c.get)
    min1Count = c[min1]
    del c[min1]

    #get second min
    min2 = min(c, key=c.get)
    min2Count = c[min2]
    del c[min2]

    #build new tree node
    nodeId = uuid.uuid1() #generates a unique uuid
    count = min1Count + min2Count
    root = Node((nodeId, count))

    #get children, if the children node doesn't exist, create it
    if min1 in Roots.keys():
        root.right = Roots[min1]
        del Roots[min1]
    else:
        root.right = Node((min1, min1Count))
    if min2 in Roots.keys():
        root.left = Roots[min2]
        del Roots[min2]
    else:
        root.left = Node((min2, min2Count))

    Roots[nodeId] = root
    c[nodeId] = count

if len(Roots) != 1:
    print "Error: more than 1 root node or no root node found..."
    print "quitting program..."
    quit()

substitutions = dict()
bits = bitarray.bitarray()

# Find the substitution codes based on the Huffman tree
substitutions = assignbit(substitutions, Roots.values()[0], bits)

encodedImg = bitarray.bitarray()
for pixel in encodedErreur:
    encodedImg += substitutions[pixel]

finalSize = encodedImg.count()

for i in range(0, len(substitutions)):
    finalSize += 8 # size of the pixel values, which are between 0 and 255, which fits in a uint8
    finalSize += substitutions.values()[i].count()

compressionRate = 100.0 * (1-(float(finalSize)/float(originalSize)))

print "original size (bits): ", originalSize
print "final size (bits): ", finalSize
print "compression rate (%): ", compressionRate

