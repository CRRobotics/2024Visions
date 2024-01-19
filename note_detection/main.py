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

def processImage(image):
    convexHull = findNoteContours(image, True)
    ellipses = fitEllipsesToNotes(convexHull)
    angles = computeEllipseAnglesFromCam(ellipses)
    centers = [ellipse[0] for ellipse in ellipses]
    distances0 = computeNoteDistancesFromAngles(angles)
    distances1 = computeNoteDistancesFromMajorAxes(ellipses)
    distances2 = computeNoteDistancesFromCenters(centers)
    displayText = [str(round(distances0[i], 1)) + ", " + str(round(distances1[i], 1)) + ", " + str(round(distances2[i], 1)) for i in range(len(ellipses))]
    # displayText = [str(ellipse[0]) for ellipse in ellipses]
    image = drawEllipses(ellipses, displayText, image)
    # print(image)

    image = cv2.drawContours(image, convexHull, -1, (0, 0, 255), 10)
    cv2.imshow("Frame", f.shrinkFrame(image, 2))

cap = f.waitForCam(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

while True:
    success, image = cap.read()
    if not success:
        print("failed to get image from camid 0")
        cap.release()
        cap = f.waitForCam(0)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    print(image)
    processImage(image)
    cv2.waitKey(1)