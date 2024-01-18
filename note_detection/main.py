import cv2
import os
import math
import helper_functions as f
from filter import *
from pos_math import *
from yaml import safe_load
with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)

cap = f.waitForCam(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

while True:
    success, image = cap.read()
    if not success:
        print("failed to get image from camid 0")
        cap.release()
        cap = f.waitForCam(0)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    
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
    cv2.waitKey(1)