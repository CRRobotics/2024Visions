import cv2
import numpy as np
from time import sleep
import math
from yaml import safe_load
import os
from pos_math import *
from filter import *
with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)

# Returns a frame that is smaller
def shrinkFrame(frame, scale):
    kernel = np.ones((scale,scale),np.float32)/(scale ** 2)
    dst = cv2.filter2D(frame,-1,kernel)
    return dst[::scale,::scale]

def waitForCam(path):
    """Waits until there is a camera available at `path`. This is to ensure that cameras that are unplugged can be plugged back in and not interrupt the script."""
    while True:
        cap = cv2.VideoCapture(path)
        cap:cv2.VideoCapture
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, params["FOV_WIDTH_PIX"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, params["FOV_HEIGHT_PIX"])
        cap.set(cv2.CAP_PROP_FPS, 20)
        if cap.isOpened():
            print("open")
            return cap
        else:
            sleep(0.001)
            print("Waiting")

def pixelsToRadians(pixelLength, angle):
    """Converts a line of pixelLength pixels rotated clockwise from a horizontal line by angle degrees into an angle in radians based on the camera's FOV."""
    radiansPerPixelHeight = math.radians(params["FOV_HEIGHT_DEGREES"] / params["FOV_HEIGHT_PIX"])
    radiansPerPixelWidth = math.radians(params["FOV_WIDTH_DEGREES"] / params["FOV_WIDTH_PIX"])
    lineAngleHeight = pixelLength * math.sin(math.radians(angle)) * radiansPerPixelHeight
    lineAngleWidth = pixelLength * abs(math.cos(math.radians(angle))) * radiansPerPixelWidth
    lineAngle = math.sqrt(lineAngleHeight ** 2 + lineAngleWidth ** 2)
    return lineAngle

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
    toDisplay = drawEllipses(ellipses, displayText, image)
    # print(image)

    toDisplay = cv2.drawContours(toDisplay, convexHull, -1, (0, 0, 255), 10)
    cv2.imshow("Frame", f.shrinkFrame(toDisplay, 2))