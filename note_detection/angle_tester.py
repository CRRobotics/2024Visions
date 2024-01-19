import cv2
import os
import math
import helper_functions as f
from filter import *
from pos_math import *
from yaml import safe_load
with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)

angleImages = os.path.join("note_detection", "angle_images")
for name in os.listdir(angleImages):
    name = os.path.join(angleImages, name)
    print(name)
    if os.path.isfile(name):
        image = cv2.imread(name)
        f.processImage(image)
cv2.waitKey(0)
