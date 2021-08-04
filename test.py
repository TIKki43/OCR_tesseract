import cv2
import numpy as np

img = cv2.imread('/home/timur/Downloads/teXT.png', 0)
kernel = np.ones((2, 2), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=1)
opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
cv2.imwrite('gs.png', opening)
