import numpy as np

def zigzag(img):
    (a, b, x, y) = img.shape
    if x != y:
        print "block sizes are not equal!"
    newImg = np.zeros((a, b, x * y))
    for i in range(0, a):
        for j in range(0, b):
            newImg[i][j] = diagonal(img[i][j])
    return newImg

def zagzig(img):
    (a, b, x) = img.shape
    if np.rint(np.sqrt(x)) != np.sqrt(x):
        raise ValueError("array is not squarable")
    block_size = np.rint(np.sqrt(x)).astype(np.int64)
    newImg = np.zeros((a, b, block_size, block_size))
    for i in range(0, a):
        for j in range(0, b):
            newImg[i][j] = square(img[i][j])
    return newImg

def diagonal(img):
    (x, y) = img.shape
    if x != y:
        raise ValueError("block dimensions are not equal!")
    newImg = np.zeros(x*y)
    i = 0
    j = 0
    n = 0
    for k in range(0, x+y):
        if k % 2 == 0:
            while i >= 0 and j < x:
                newImg[n] = img[i][j]
                j = j + 1
                i = i - 1
                n = n + 1
            if j >= x and i < 0:
                i = 1
                j = x - 1
            elif i < 0:
                i = 0
                j = k + 1
            elif j >= x:
                j = x - 1
                i = k + 1 - x + 1
        else:
            while j >= 0 and i < x:
                newImg[n] = img[i][j]
                j = j - 1
                i = i + 1
                n = n + 1
            if i >= x and j < 0:
                j = 1
                i = x - 1
            elif j < 0:
                j = 0
                i = k + 1
            elif i >= x:
                i = x - 1
                j = k + 1 - x + 1
    return newImg

def square(array):
    x = array.size
    if np.rint(np.sqrt(x)) != np.sqrt(x):
        raise ValueError("array is not squarable")
    block_size = np.rint(np.sqrt(x)).astype(np.int64)
    newImg = np.zeros((block_size, block_size))
    i = 0
    j = 0
    n = 0
    for k in range(0, block_size*2):
        if k % 2 == 0:
            while j >= 0 and i < block_size:
                newImg[j][i] = array[n]
                j = j - 1
                i = i + 1
                n = n + 1
            if i >= block_size and j < 0:
                j = 1
                i = block_size - 1
            elif i >= block_size:
                i = block_size - 1
                j = k + 1 - block_size + 1
            elif j < 0:
                j = 0
                i = k + 1

        else:
            while i >= 0 and j < block_size:
                newImg[j][i] = array[n]
                j = j + 1
                i = i - 1
                n = n + 1
            if j >= block_size and i < 0:
                i = 1
                j = block_size - 1
            elif j >= block_size:
                j = block_size - 1
                i = k + 1 - block_size + 1
            elif i < 0:
                i = 0
                j = k + 1


    return newImg
