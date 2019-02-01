# numpy library: http://www.numpy.org/
# matplotlib library: https://matplotlib.org/

import numpy as np
import matplotlib.pyplot as py
import collections

def rgb2gray(rgb):
    return np.dot(rgb[:,:], [0.299, 0.587, 0.114])

def imfloat2uint8(image):
    return (image*255).astype('uint8')

fig1 = py.figure(figsize=(10,10))
imagelue = py.imread('black.png')
image = imagelue.astype('float')
image = rgb2gray(image)

#print(image)

Message = []

for i in range(0, len(image)):
    for j in range(0, len(image[i])):
        Message.append(imfloat2uint8(image[i][j]))

tailleOriginale = len(Message)




remplacementpossible = True
while remplacementpossible == True:

    Pairs = []
    for i in range(0, len(Message) - 1):
        Pairs.append((Message[i], Message[i + 1]))

    c = collections.Counter()

    for pair in Pairs:
        c[pair] += 1

    remplacementpossible = False
    for pair in c:
        if c[pair] > 3:
            remplacementpossible = True

    max = 0
    maxKey = 0
    for pair in c:
        if c[pair] > max:
            maxKey = pair
            max = c[pair]

    s = set(Message)
    freeUint = -1
    for i in range(0, 255):
        if i not in s:
            freeUint = i
            break

    if freeUint == -1:
        print("not enough free uint")
        break

    newMessage = []
    skip = False
    for i in range(0,len(Message)):
        if not skip:
            if Message[i] == maxKey[0]:
                if i+1 >= len(Message) or Message[i + 1] == maxKey[1]:
                    skip = True
                else:
                    newMessage.append(Message[i])
            else:
                newMessage.append(Message[i])
        elif skip:
            newMessage.append(freeUint)
            skip = False

    tailleNow = len(newMessage)

    print("taille now")
    print(tailleNow)

    Message = newMessage

tailleCompresse = len(Message)

print("taille originale")
print(tailleOriginale)
print("taille compresse")
print(tailleCompresse)

compressionRate = 100.0 * (1-(float(tailleCompresse)/float(tailleOriginale)))
print "compression rate (%): ", compressionRate
