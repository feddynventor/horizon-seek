import numpy as np
import cv2
import math
import sys

from color_filter import filter_green
from detect_horizon import detect_horizon_line

value = 130

def on_trackbar(val):
    global value
    value = val
    cv2.imshow('mask', pipeline())

def pipeline():
    global value
    global frame
    frame = frame[0:540, 0:]
    [mask,hsv] = filter_green(frame, value)
    [x1,x2,y1,y2] = detect_horizon_line(mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # per applicare la linea rossa
    print(x1,x2,y1,y2)
    cv2.line(mask, (x1, y1), (x2, y2), (0,0,255), 6)
    return mask

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