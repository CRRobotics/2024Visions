import cv2
import numpy as np
from yaml import safe_load
import helper_functions as f
import os
import math
with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)

def computeEllipseAnglesFromCam(ellipses):
    """Assuming the inputted ellipses are circles viewed from an angle, calculates the angle from that circle to the camera"""
    angles = []
    for ellipse in ellipses:
        major = ellipse[1][1]
        minor = ellipse[1][0]
        angle = ellipse[2] # The clockwise angle from a horizontal line to the minor axis
        radiansPerPixelHeight = math.radians(params["FOV_HEIGHT_DEGREES"] / params["FOV_HEIGHT_PIX"])
        radiansPerPixelWidth = math.radians(params["FOV_WIDTH_DEGREES"] / params["FOV_WIDTH_PIX"])
        ellipseAngleHeight = minor * math.sin(math.radians(angle)) * radiansPerPixelHeight
        ellipseAngleWidth = minor * abs(math.cos(math.radians(angle))) * radiansPerPixelWidth
        ellipseAngle = math.sqrt(ellipseAngleHeight ** 2 + ellipseAngleWidth ** 2)
        minorLengthRelativeToDiameter = minor / major
        angleFromCam = (math.pi - ellipseAngle) / 2 - math.asin(minorLengthRelativeToDiameter * math.sin((math.pi + ellipseAngle) / 2))
        angles.append(angleFromCam)
    return angles

def computeNoteDistancesFromCam(angles):
    """Uses the angle of a note from the camera to calculate its distance, assuming it is on the floor"""
    distances = []
    for angle in angles:
        distance = params["CAMERA_HEIGHT_IN"] * math.tan(angle)
        distances.append(distance)
    return distances