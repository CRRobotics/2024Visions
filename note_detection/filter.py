import cv2
import numpy as np
from yaml import safe_load
import helper_functions as f
import os
import math
with open(os.path.join("note_detection", "constants.yml"), "r") as fp:
    params = safe_load(fp)

# Get upper and lower bounds for HSV filter
upper = np.array(params["HSV_UPPER"])
lower = np.array(params["HSV_LOWER"])
#print(upper)

# Read the image and convert to HSV
sampleImage = cv2.imread(os.path.join("note_detection", "sample_images", "IMG_1559.jpeg"))

def findNoteContours(image = sampleImage, displayMask = False):
    """Filters the image for notes and returns a list of convexHulls where they are"""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blurred = cv2.medianBlur(image, params["BLUR_SIZE"] * 2 + 1)
    mask = cv2.inRange(blurred, lower, upper)
    if displayMask:
        cv2.imshow("Mask", f.shrinkFrame(mask, 2))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return []
    largestContour = max(contours, key=lambda x: cv2.contourArea(x))
    convexHull = [cv2.convexHull(largestContour)]

    # Add in more filtering here

    return convexHull

def fitEllipsesToNotes(convexHull):
    ellipses = []
    for hull in convexHull:
        if len(hull) < 5: continue # fitEllipse needs at least 5 points
        ellipse = cv2.fitEllipse(hull)
        newMajor = ellipse[1][1] * (1 - params["NOTE_THICKNESS_IN"] / params["NOTE_OUTER_RADIUS_IN"]) # Shrink the ellipse to be at roughly the center of the torus
        newMinor = ellipse[1][0] - ellipse[1][1] * params["NOTE_THICKNESS_IN"] / params["NOTE_OUTER_RADIUS_IN"] # Removing the same amount from the minor axis as the major axis
        ellipse = list(ellipse)
        ellipse[1] = (newMinor, newMajor)
        ellipse = tuple(ellipse)
        ellipses.append(ellipse)
    
    return ellipses

def drawEllipses(ellipses, textToDisplay, image = sampleImage):
    """Displays the inputted array of ellipses on image with textToDisplay (an array of the same length) at their centers"""
    toReturn = image.copy()
    for i in range(len(ellipses)):
        ellipse = ellipses[i]
        text = textToDisplay[i]
        try:
            ellipseCenter = tuple([int(coord) for coord in ellipse[0]])
            toReturn = cv2.ellipse(toReturn, ellipse, (255, 255, 0), 20)
            toReturn = cv2.putText(toReturn, str(text), ellipseCenter, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 5)
        except:
            # Errors this catches: ellipse has infinity in it, ellipse is zero size, center doesn't work for text
            print("Can't display ellipse")
    return toReturn

"""
cap = f.waitForCam(0)
#print("Got here")
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

while True:
    success, image = cap.read()
    if not success:
        print("failed to get image from camid 0")
        cap.release()
        cap = f.waitForCam(0)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Find orange contours
    mask = cv2.inRange(image, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        continue
    largestContour = max(contours, key=lambda x: cv2.contourArea(x))
    convexHull = [cv2.convexHull(largestContour)]
    # convexHull = [cv2.convexHull(contour) for contour in contours]
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

    # Add in more filtering here


    # Fit ellipses to contours
    ellipses = []
    for hull in convexHull:
        #print(hull)
        if len(hull) < 5: continue # fitEllipse needs at least 5 points
        #print("Found contour")
        ellipse = cv2.fitEllipse(hull)
        #print(ellipse)
        newMajor = ellipse[1][1] * (1 - params["NOTE_THICKNESS_IN"] / params["NOTE_OUTER_RADIUS_IN"]) # Shrink the ellipse to be at roughly the center of the torus
        newMinor = ellipse[1][0] - ellipse[1][1] * params["NOTE_THICKNESS_IN"] / params["NOTE_OUTER_RADIUS_IN"] # Removing the same amount from the minor axis as the major axis
        ellipse = list(ellipse)
        ellipse[1] = (newMinor, newMajor)
        ellipse = tuple(ellipse)

        # Find the angle to the ellipse
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

        try:
            ellipseCenter = tuple([int(coord) for coord in ellipse[0]])
            image = cv2.ellipse(image, ellipse, (255, 255, 0), 20)
            image = cv2.putText(image, str(round(math.degrees(angleFromCam), 1)), ellipseCenter, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 5)
            ellipses.append(ellipse)
        except:
            # Errors this catches: ellipse has infinity in it, ellipse is zero size, center doesn't work for text
            print("Can't display ellipse")

    image = cv2.drawContours(image, convexHull, -1, (0, 0, 255), 10)
    cv2.imshow("Test", f.shrinkFrame(image, 2))
    cv2.imshow("Mask", f.shrinkFrame(mask, 2))
    cv2.waitKey(1)
"""