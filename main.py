import csv
import cv2
import pytesseract
from pytesseract import Output
from pre_proc_img import pre_proc_img
from pre_proc_img import PathToImg

custom_config = r'--oem 3 --psm 6'
path_to_img = PathToImg

image = cv2.imread(path_to_img)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


def lowlevelproc(threshold_img, custom_conf):
    return pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')


def highlevelproc(prec_proc_img):
    return pytesseract.image_to_data(prec_proc_img, output_type=Output.DICT, config=custom_config, lang='eng')


parse_text = []
word_list = []
last_word = ''

for word in lowlevelproc(threshold_img, custom_config)['text']:
    if word != '':
        word_list.append(word)
        last_word = word

    if (last_word != '' and word == '') or (word == lowlevelproc(threshold_img, custom_config)['text'][-1]):
        parse_text.append(word_list)
        word_list = []

with open('result_text.txt',  'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(parse_text)