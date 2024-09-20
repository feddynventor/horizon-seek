import sys
import cv2

import kernel_filter
import hue_filter
import line_interpolation

image = cv2.imread( sys.argv[1] )

image_masked = hue_filter.isolate_color( image ) 

cv2.namedWindow( '1', cv2.WINDOW_NORMAL)
cv2.imshow( '1', image_masked )

binary_image, dots = kernel_filter.filter( image_masked )
y_left, y_right = line_interpolation.interpolate(binary_image)

image_marks = cv2.line( dots, (1,int(y_left)), (1919,int(y_right)), (0,255,127), 5 )

cv2.namedWindow( '2', cv2.WINDOW_NORMAL)
cv2.imshow( '2', image_marks )

cv2.waitKey(0)
cv2.destroyAllWindows()
