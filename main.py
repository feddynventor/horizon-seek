import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
import sys

from color_filter import filter_green
from hough_transform import draw_lines, find_lines

value = 130

def on_trackbar(val):
    global value
    value = val
    cv2.imshow('mask', pipeline())

def pipeline():
    global value
    global frame
    [mask,hsv] = filter_green(frame, value)
    lines = find_lines(mask)
    return draw_lines(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), lines)

if (".jpg" in sys.argv[1] or ".png" in sys.argv[1]):
    frame = cv2.imread(sys.argv[1])
    cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
    cv2.createTrackbar("min_value", 'mask' , 0, 255, on_trackbar)
    cv2.imshow('mask', pipeline())
    while(cv2.waitKey(1) != 113):
        pass

elif (".mp4" in sys.argv[1]):
    cap = cv2.VideoCapture(sys.argv[1])
    ret, frame = cap.read()

while('cap' in globals() and cap.isOpened()):
    cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
    cv2.imshow('mask', pipeline())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(20)

    ret, frame = cap.read()