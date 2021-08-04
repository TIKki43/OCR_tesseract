import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image as im
from scipy.ndimage import interpolation as inter

PathToImg = input('Please, enter full path to scan image: ')

img = im.open(PathToImg)
w, h = img.size
pix = np.array(img.convert('1').getdata(), np.uint8)
bin_img = 1 - (pix.reshape((h, w)) / 255.0)


def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score


delta = 1
limit = 5
angles = np.arange(-limit, limit + delta, delta)
scores = []

for angle in angles:
    hist, score = find_score(bin_img, angle)
    scores.append(score)

max_sc = max(scores)
max_agl = angles[scores.index(max_sc)]
data = inter.rotate(bin_img, max_agl, reshape=False, order=0)
img = im.fromarray((255 * data).astype("uint8")).convert("RGB")
# print(type(img))

cvImg = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
pre_proc_img = cv2.fastNlMeansDenoisingColored(cvImg, None, 10, 10, 7, 15)
# cv2.imwrite('pre-processed_img.png', pre_proc_img)
