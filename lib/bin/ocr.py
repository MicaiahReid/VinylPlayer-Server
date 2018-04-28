# pylint: skip-file
import sys
import segmentation_v2 as s
from network import test
import dataset as D
import cv2
from PIL import Image
import base64 
import io
import numpy as np

seg_img_width = 1024
seg_img_height = 512

def ocr(img, img_height, img_width):
    letters = []
    # segment image into word(s) 
    # segment word(s) into letters
    lines = s.segment_image_v2(img, img_width, img_height)
    print("Segmenting Lines")
    for line in lines:
        print("New Line!")
        segments = s.segment_line_v2(line, img_width, img_height)
        if segments is None:
            continue
        letters.extend(segments)    
    query = test(letters)
    return query

def rotate_image(img, angle):
    img_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(img_center, angle, 1.0)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

file = sys.argv[1]
img = cv2.imread(file)

if img is None:
    print("Saved image file could not be opened")
    query = '{"query": ""}'
else:
    query = ocr(img, seg_img_height, seg_img_width)

print(query)
sys.stdout.flush()