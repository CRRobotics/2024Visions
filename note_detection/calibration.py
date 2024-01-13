import cv2
import numpy as np
from yaml import safe_load, safe_dump
import os
import helper_functions as f
with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)
print(params)

cap = f.waitForCam(0)
#print("Got here")
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

#cammat = params["CAMERA_CONSTANTS"][0][0]["MATRIX"]
#distco = params["CAMERA_CONSTANTS"][0][0]["DISTORTION"]

image = cv2.imread(os.path.join("note_detection", "sample_images", "IMG_1555.jpeg"))

#image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])
upper = np.array([params["HUE"], params["SATURATION"], params["VALUE"]])
mask = cv2.inRange(image, lower, upper)

def updateHueMin(value):
    lower[0] = value

def updateHueMax(value):
    upper[0] = value

def updateSaturationMin(value):
    lower[1] = value

def updateSaturationMax(value):
    upper[1] = value

def updateValueMin(value):
    lower[2] = value

def updateValueMax(value):
    upper[2] = value

def saveValues(value):
    params["HSV_LOWER"] = lower.tolist()
    params["HSV_UPPER"] = upper.tolist()
    with open(os.path.join("note_detection", "constants.yml"), "w") as fp:
        safe_dump(params, fp)

cv2.namedWindow("Filter")
cv2.createTrackbar("Hue min", "Filter", 0, params["HUE"], updateHueMin)
cv2.createTrackbar("Hue max", "Filter", params["HUE"], params["HUE"], updateHueMax)
cv2.createTrackbar("Saturation min", "Filter", 0, params["SATURATION"], updateSaturationMin)
cv2.createTrackbar("Saturation max", "Filter", params["SATURATION"], params["SATURATION"], updateSaturationMax)
cv2.createTrackbar("Value min", "Filter", 0, params["VALUE"], updateValueMin)
cv2.createTrackbar("Value max", "Filter", params["VALUE"], params["VALUE"], updateValueMax)
cv2.createTrackbar("Slide to save", "Filter", 0, 1, saveValues)

while True:
    success, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    if not success:
        print("failed to get image from camid 0")
        cap.release()
        cap = f.waitForCam(0)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    toDisplay = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("Test", f.shrinkFrame(toDisplay, 2))
    cv2.imshow("Mask", f.shrinkFrame(mask, 2))
    cv2.waitKey(1)
