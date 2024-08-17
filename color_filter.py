import cv2 as cv
import numpy as np

def on_trackbar(val):
    mask, hsv = filter_green(img, val)
    cv.imshow("mask", mask)

def filter_green(img, value=0):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #set the lower and upper bounds for the green hue
    lower_green = np.array([0,0,value])
    upper_green = np.array([255,255,255])

    #create a mask for green colour using inRange function
    mask = cv.inRange(hsv, lower_green, upper_green)
    return mask, hsv

# import sys

# if (".jpg" in sys.argv[1]):
#     img = cv.imread(sys.argv[1])
#     mask, hsv = filter_green(img)

#     cv.namedWindow("mask", cv.WINDOW_NORMAL)
#     cv.createTrackbar("min_value", "mask" , 0, 255, on_trackbar)
#     cv.imshow("mask", mask)

#     if cv.waitKey(0):
#         cv.destroyAllWindows()