import cv2
import numpy as np
from yaml import safe_load
import helper_functions as f
import os
import math
with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)

def computeEllipseAnglesFromCam(ellipses):
    """Assuming the inputted ellipses are circles viewed from an angle, calculates the angle from that circle to the camera."""
    angles = []
    for ellipse in ellipses:
        major = ellipse[1][1]
        minor = ellipse[1][0]
        angle = ellipse[2] # The clockwise angle from a horizontal line to the minor axis
        ellipseAngle = f.pixelsToRadians(minor, angle)
        minorLengthRelativeToDiameter = minor / major
        angleFromCam = (math.pi - ellipseAngle) / 2 - math.asin(minorLengthRelativeToDiameter * math.sin((math.pi + ellipseAngle) / 2))
        angles.append(angleFromCam)
    return angles

def computeNoteDistancesFromAngles(angles):
    """Uses the angle of a note from the camera to calculate its distance, assuming it is on the floor."""
    distances = []
    for angle in angles:
        distance = params["CAMERA_HEIGHT_IN"] * math.tan(angle)
        distances.append(distance)
    return distances

def computeNoteDistancesFromMajorAxes(ellipses):
    """Uses the major axis of a note to calculate its distance, assuming it is on the floor."""
    distances = []
    for ellipse in ellipses:
        major = ellipse[1][1]
        angle = ellipse[2]
        ellipseAngle = f.pixelsToRadians(major, angle - 90)
        distanceStraightOn = 6 / math.tan(ellipseAngle / 2) # tan(ellipseAngle) SHOULD not be 0 or infinity
        if distanceStraightOn < params["CAMERA_HEIGHT_IN"]: distance = 0
        else: distance = math.sqrt(distanceStraightOn ** 2 - params["CAMERA_HEIGHT_IN"] ** 2)
        distances.append(distance)
    return distances

def computeNoteDistancesFromCenters(centers):
    """Uses the center point of a note to calculate its distance based on the tilt of the camera, assuming it is on the floor and the center point is below the camera"""
    distances = []
    for center in centers:
        centerY = center[1]
        heightAboveCamCenter = params["FOV_HEIGHT_PIX"] / 2 - centerY
        angleAboveCamCenter = f.pixelsToRadians(heightAboveCamCenter, 90)
        angleAboveHorizontal = angleAboveCamCenter + math.radians(params["CAMERA_CENTER_ANGLE_DEGREES"])
        distance = params["CAMERA_HEIGHT_IN"] / math.tan(angleAboveHorizontal)
        distances.append(distance)
    return distances