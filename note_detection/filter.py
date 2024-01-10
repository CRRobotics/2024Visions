import cv2
import numpy as np
from yaml import safe_load
import helper_functions as f
import os

with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)

upper = np.array(params["HSV_UPPER"])
lower = np.array(params["HSV_LOWER"])
#print(upper)

image = cv2.imread(os.path.join("note_detection", "sample_images", "IMG_1555.jpeg"))
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(image, lower, upper)
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
image = cv2.drawContours(image, contours, -1, (255, 0, 255), 10)
cv2.imshow("Test", f.shrinkFrame(image, 3))
cv2.imshow("Mask", f.shrinkFrame(mask, 3))
cv2.waitKey(0)