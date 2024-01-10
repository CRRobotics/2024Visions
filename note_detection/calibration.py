import cv2
import numpy as np
from yaml import safe_load, safe_dump
import os
import helper_functions as f

image = cv2.imread(os.path.join("note_detection", "sample_images", "IMG_1555.jpeg"))

image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
with open("note_detection\\constants.yml", "r") as fp:
    params = safe_load(fp)
print(params)
lower = np.array([0, 0, 0])
upper = np.array([params["HUE"], params["SATURATION"], params["VALUE"]])

def updateHueMin(value):
    lower[0] = value
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("Mask", f.shrinkFrame(mask, 3))

def updateHueMax(value):
    upper[0] = value
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("Mask", f.shrinkFrame(mask, 3))

def updateSaturationMin(value):
    lower[1] = value
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("Mask", f.shrinkFrame(mask, 3))

def updateSaturationMax(value):
    upper[1] = value
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("Mask", f.shrinkFrame(mask, 3))

def updateValueMin(value):
    lower[2] = value
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("Mask", f.shrinkFrame(mask, 3))

def updateValueMax(value):
    upper[2] = value
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("Mask", f.shrinkFrame(mask, 3))

image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
cv2.imshow("Test", f.shrinkFrame(image, 3))
cv2.namedWindow("Filter")
cv2.createTrackbar("Hue min", "Filter", 0, params["HUE"], updateHueMin)
cv2.createTrackbar("Hue max", "Filter", params["HUE"], params["HUE"], updateHueMax)
cv2.createTrackbar("Saturation min", "Filter", 0, params["SATURATION"], updateSaturationMin)
cv2.createTrackbar("Saturation max", "Filter", params["SATURATION"], params["SATURATION"], updateSaturationMax)
cv2.createTrackbar("Value min", "Filter", 0, params["VALUE"], updateValueMin)
cv2.createTrackbar("Value max", "Filter", params["VALUE"], params["VALUE"], updateValueMax)
cv2.waitKey(0)

save = input("Save values? (y/n) ")
if save == "y":
    params["HSV_LOWER"] = lower.tolist()
    params["HSV_UPPER"] = upper.tolist()
    with open("note_detection\\constants.yml", "w") as fp:
        safe_dump(params, fp)
