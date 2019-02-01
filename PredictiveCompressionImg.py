# Code based on https://github.com/gabilodeau/INF8770/blob/master/Codage%20predictif%20sur%20image.ipynb
# Huffman based on https://github.com/soxofaan/dahuffman/blob/master/dahuffman/huffmancodec.py
# bitarray library: https://pypi.org/project/bitarray/

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
        return self.left is None & self.right is None

def assignbit(substitutions, node, bits):
    if node.isLeaf:
        substitutions[node.data] = bits
    else:
        assignbit(substitutions, node.left, bits.append(True))
        assignbit(substitutions, node.right, bits.append(False))
    return substitutions

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
#py.show()

originalSize = image.size*sys.getsizeof(image[0][0])

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
#py.show()

fig2 = py.figure(figsize=(10, 10))
py.imshow(imagepred, cmap=py.get_cmap('gray'))
#py.show()

fig3 = py.figure(figsize=(10, 10))
py.imshow(erreur, cmap=py.get_cmap('gray'))
#py.show()

# encodage de l'erreur avec la premiere colonne etant les pixels eux-memes
encodeErreur = np.column_stack([image[:, 0], erreur])
py.imshow(encodeErreur, cmap=py.get_cmap('gray'))
#py.show()

#Huffman
c = collections.Counter()
encodeErreur = encodeErreur.ravel()

for value in encodeErreur:
    c[value] += 1

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

if len(Roots) == 1:
    print "good"
else:
    print "what"


