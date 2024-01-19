import cv2
import os
import math
import helper_functions as f
from filter import *
from pos_math import *
from yaml import safe_load
with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)

image = cv2.imread(os.path.join("note_detection", "sample_images", "IMG_1555.jpeg"))
savedImages = 0

def saveImage(value):
    global savedImages
    savedImages += 1
    fileName = "image" + str(savedImages) + ".jpg"
    path = os.path.join("note_detection", "angle_images", fileName)
    cv2.imwrite(path, image)

cv2.namedWindow("Slide to save image")
cv2.createTrackbar("Save", "Slide to save image", 0, 1, saveImage)

cap = f.waitForCam(1)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

while True:
    success, image = cap.read()
    if not success:
        print("failed to get image from camid 0")
        cap.release()
        cap = f.waitForCam(0)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    print(image)
    f.processImage(image)
    cv2.waitKey(1)