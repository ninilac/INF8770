import numpy as np
import cv2

cap = cv2.VideoCapture('julia.avi')
ret, lastFrame = cap.read()

while cap.isOpened():
    ret, frame = cap.read()
    if ~ret:
        break
    sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)

