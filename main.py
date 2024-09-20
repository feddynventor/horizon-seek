import sys
import cv2
import math

import kernel_filter
import hue_filter
import line_interpolation

cap = cv2.VideoCapture(sys.argv[1])
ret, frame = cap.read()

cv2.namedWindow( 'hue_filter', cv2.WINDOW_NORMAL)
cv2.namedWindow( 'interpolation', cv2.WINDOW_NORMAL)

while('cap' in globals() and cap.isOpened()):

    image_masked = hue_filter.isolate_color( frame ) 

    cv2.imshow( 'hue_filter', image_masked )

    binary_image = kernel_filter.filter( image_masked )
    y_left, y_right = line_interpolation.interpolate(binary_image)

    print( math.atan2( abs(y_left-y_right), 1920 )*180/math.pi, ' deg' )

    image_marks = cv2.line( frame, (1,int(y_left)), (1919,int(y_right)), (0,255,127), 5 )
    cv2.imshow( 'interpolation', image_marks)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(20)

    ret, frame = cap.read()