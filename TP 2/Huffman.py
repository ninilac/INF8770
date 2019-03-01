# code for the huffman encoding taken from TP 1
# modified according to this website: https://www.impulseadventure.com/photo/jpeg-huffman-coding.html

import numpy as np
import collections
import uuid
import bitarray


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


def huffmantree(c):
    # Keeps all the subtree roots for building the Huffman tree
    Roots = dict()

    # Build the Huffman tree
    while (len(c) > 1):

        # get first min
        min1 = min(c, key=c.get)
        min1Count = c[min1]
        del c[min1]

        # get second min
        min2 = min(c, key=c.get)
        min2Count = c[min2]
        del c[min2]

        # build new tree node
        nodeId = uuid.uuid1()  # generates a unique uuid
        count = min1Count + min2Count
        root = Node((nodeId, count))

        # get children, if the children node doesn't exist, create it
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

        if len(c) == 1:
            print "a"

        Roots[nodeId] = root
        c[nodeId] = count

    if len(Roots) != 1:
        print "Error: more than 1 root node or no root node found..."
        print "quitting program..."
        quit()

    substitutions = dict()
    bits = bitarray.bitarray()

    # Find the substitution codes based on the Huffman tree
    return assignbit(substitutions, Roots.values()[0], bits)


def huffman_encoding(img):
    (a,b,x) = img.shape
    # Huffman
    # counts the first value of each block
    DC_counter = collections.Counter()
    # counts the rest of the values of blocks
    AC_counter = collections.Counter()

    for m in range(0, a):
        for n in range(0, b):
            for i in range(0, x):
                pixel = img[m][n][i]
                if i == 0:
                    DC_counter[pixel] += 1
                else:
                    AC_counter[pixel] += 1

    DC_substitutions = huffmantree(DC_counter)
    AC_substitutions = huffmantree(AC_counter)

    encodedImg = bitarray.bitarray()
    for m in range(0, a):
        for n in range(0, b):
            for i in range(0, x):
                if i == 0:
                    encodedImg += DC_substitutions[img[m][n][i]]
                else:
                    encodedImg += AC_substitutions[img[m][n][i]]

    return Huffmancode(DC_substitutions, AC_substitutions, encodedImg, a*8, b*8)


class Huffmancode:
    def __init__(self, dctable, actable, code, x, y):
        self.DCtable = dctable
        self.ACtable = actable
        self.code = code
        self.x = x
        self.y = y

    def getSize(self):
        finalSize = self.code.count()
        for i in range(0, len(self.ACtable)):
            finalSize += 8  # size of the pixel values, which are between 0 and 255, which fits in a uint8
            finalSize += self.ACtable.values()[i].count()
        for i in range(0, len(self.DCtable)):
            finalSize += 8  # size of the pixel values, which are between 0 and 255, which fits in a uint8
            finalSize += self.DCtable.values()[i].count()
        return finalSize
