import cv2
import numpy as np
import math


# CONSTANTS

HUE = 179
SATURATION = 255
VALUE = 255

UPPER = np.array([19, 219, 197])
LOWER = np.array([7, 78, 61])
BLUR_SIZE = 4

CAMERA_CENTER_ANGLE_DEGREES = -29
CAMERA_HEIGHT_IN = -8.5

FOV_HEIGHT_DEGREES = 41
FOV_HEIGHT_PIX = 240
FOV_WIDTH_DEGREES = 54
FOV_WIDTH_PIX = 320
BUMPER_HEIGHT_PIX = 20

NOTE_OUTER_RADIUS_IN = 14
NOTE_THICKNESS_IN = 2

X_ERROR_M = 0.96
X_ERROR_B = 0.69
Z_ERROR_M = 0.92
Z_ERROR_B = 8.06

ACCEPTED_ERROR_A = 0.02675
ACCEPTED_ERROR_B = 0.0894167
ACCEPTED_ERROR_C = -2.72321
ACCEPTED_ERROR_D_MIN = -0.7
ACCEPTED_ERROR_D_MAX = 0.4


# HELPER FUNCTIONS

def polarToRectangular(r, theta):
    """Converts the given polar coordinates (r, theta) into rectangular coordinates (x, y)."""
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

def getOpticalAngle(img, orientation:int, coordinate:tuple):
    """
        Gets the angle based on the fov, orientation, and coordinate of the parabola representing the target. From 2022.
        @param img The image or frame to use
        @param orientation The orientation of the angle (0 gets horizontal angle to the coordinate, 1 gets vertical angle to the tape)
        NOTE: vertical angle is only accurate if the x-coordinate of the center coordinate is in the middle of the frame
        @param coordinate The coordinate of the center of the tape or parabola
    """
    h, w, _ = img.shape

    px = coordinate[0]
    py = coordinate[1]

    centerPixel = (int(w / 2), int(h / 2))
    if orientation == 0:
        distanceFromCenter = px - centerPixel[0]
        radiansPerPixelWidth = math.radians(FOV_WIDTH_DEGREES) / FOV_WIDTH_PIX
        angle = radiansPerPixelWidth * distanceFromCenter
    elif orientation == 1:
        distanceFromCenter = centerPixel[1] - py
        radiansPerPixelHeight = math.radians(FOV_HEIGHT_DEGREES) / FOV_HEIGHT_PIX
        angle = radiansPerPixelHeight * distanceFromCenter
    return angle

def getHorizontalDistance(angle, degrees=False, heightToTarget=CAMERA_HEIGHT_IN):
    """Determines the horizontal distance to the target based on the angle and height of the target relative to the robot. From 2022."""
    return heightToTarget / math.tan(math.radians(angle)) if degrees else heightToTarget / math.tan(angle)

def horizontalOpticalToGround(angle):
    """Converts the horizontal angle relative to the optical axis to the horizontal angle relative to the ground. From 2022."""
    return math.atan((1 / math.cos(math.radians(CAMERA_CENTER_ANGLE_DEGREES))) * math.tan(angle))

def verticalOpticalToGround(opticalHorizontalAngle, opticalVerticalAngle):
    """Converts the vertical angle relative to the optical axis to the vertical angle relative to the ground. From 2022."""
    return math.asin(math.cos(math.radians(CAMERA_CENTER_ANGLE_DEGREES)) * math.sin(opticalVerticalAngle) + \
        math.cos(opticalHorizontalAngle) * math.cos(opticalVerticalAngle) * math.sin(math.radians(CAMERA_CENTER_ANGLE_DEGREES)))

def processImage(image):
    """The main image processing function, returns the image with things drawn on it, the mask, and the X and Z coorinates of notes found."""
    convexHulls, mask = findNoteContours(image)
    ellipses, convexHulls = zip(*[fitEllipsesToNotes(convexHull) for convexHull in convexHulls])
    # If an ellipse could not be fit, ellipses and convexHulls will both contain one or more Nones
    ellipses = list(filter(lambda item: item is not None, ellipses))
    convexHulls = list(filter(lambda item: item is not None, convexHulls))
    centers = [ellipse[0] for ellipse in ellipses]

    distances2, groundAngles = zip(*[computeNoteCoordsFromCenter(center, image) for center in centers])
    convexHulls, distances2, groundAngles, ellipses = closestNote(convexHulls, distances2, groundAngles, ellipses)
    xCoords, zCoords = zip(*[polarToRectangular(distances2[i], groundAngles[i]) for i in range(len(ellipses))])

    displayText = [str(round(xCoords[i], 1)) + ", " + str(round(zCoords[i], 1)) for i in range(len(ellipses))] # X coord, Z coord
    toDisplay = drawEllipses(ellipses, displayText, image)
    toDisplay = cv2.drawContours(toDisplay, convexHulls, -1, (0, 0, 255), 2)

    # If xCoords and zCoords are empty, 0 will be pushed to NetworkTables for both
    xCoords.append(0)
    zCoords.append(0)

    return toDisplay, mask, xCoords, zCoords


# FILTER CODE

def invertedHueMask(image):
    """Returns an HSV mask with the hue range inverted, similar to what LimeLight's built-in color threshold can do. Likely won't be needed."""
    lower1 = np.array([0, LOWER[1], LOWER[2]])
    upper1 = np.array([LOWER[0], UPPER[1], UPPER[2]])
    lower2 = np.array([UPPER[0], LOWER[1], LOWER[2]])
    upper2 = np.array([HUE, UPPER[1], UPPER[2]])
    mask1 = cv2.inRange(image, lower1, upper1)
    mask2 = cv2.inRange(image, lower2, upper2)
    return cv2.bitwise_or(mask1, mask2)

def findNoteContours(image):
    """Filters the image for notes and returns a list of convexHulls where they are, plus the mask."""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blurred = cv2.medianBlur(image, BLUR_SIZE * 2 + 1)
    mask = cv2.inRange(blurred, LOWER, UPPER)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return [], mask
    convexHull = [cv2.convexHull(contour) for contour in contours]
    return convexHull, mask

def fitEllipsesToNotes(convexHull):
    """Given a list of contours, finds ellipses that represent the center circles of notes, also returns the contours that could have ellipses fit to them."""
    if len(convexHull) < 5: return None, None # fitEllipse needs at least 5 points

    ellipse = cv2.fitEllipse(convexHull)
    newMajor = ellipse[1][1] * (1 - NOTE_THICKNESS_IN / NOTE_OUTER_RADIUS_IN) # Shrink the ellipse to be at roughly the center of the torus
    newMinor = ellipse[1][0] - ellipse[1][1] * NOTE_THICKNESS_IN / NOTE_OUTER_RADIUS_IN # Removing the same amount from the minor axis as the major axis
    ellipse = list(ellipse) # Tuples must be converted to lists to edit their contents
    ellipse[1] = (newMinor, newMajor)
    ellipse = tuple(ellipse)
    return ellipse, convexHull

def drawEllipses(ellipses, textToDisplay, image):
    """Displays the inputted array of ellipses on image with textToDisplay (an array of the same length) at their centers."""
    toReturn = image.copy()
    for i in range(len(ellipses)):
        ellipse = ellipses[i]
        text = textToDisplay[i]

        try:
            ellipseCenter = tuple([int(coord) for coord in ellipse[0]])
            toReturn = cv2.circle(toReturn, ellipseCenter, 0, (0, 0, 0), 5)
            toReturn = cv2.ellipse(toReturn, ellipse, (255, 255, 0), 2)
            toReturn = cv2.putText(toReturn, str(text), ellipseCenter, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        except:
            # Errors this catches: ellipse has infinity in it, ellipse is zero size, center doesn't work for text
            print("Can't display ellipse")
    return toReturn


# POS MATH

def computeNoteCoordsFromCenter(vertex, image):
    """Uses the center point of a note to calculate its z-coordinate based on the tilt of the camera, assuming it is on the floor and the center point is below the camera."""
    # Some code from 2022
    opticalHorizontalAngle = getOpticalAngle(image, 0, vertex) # if vertex is not None else getOpticalAngle(image, 0, centers[0])
    groundHorizontalAngle = horizontalOpticalToGround(opticalHorizontalAngle)
    opticalVerticalAngle = getOpticalAngle(image, 1, vertex) # if vertex is not None else getOpticalAngle(image, 1, centers[0])
    groundVerticalAngle = verticalOpticalToGround(opticalHorizontalAngle, opticalVerticalAngle)

    horizontalDistance = getHorizontalDistance(groundVerticalAngle)
    groundHorizontalAngle = math.pi / 2 - groundHorizontalAngle # Convert from angle from center to angle from X-axis
    return horizontalDistance, groundHorizontalAngle

def undoError(givenX, givenZ):
    """Uses the given X and Z and the error of the given X and Z, adjusts for the error of the functions. We're too good for this, though ;)."""
    adjustedX = (givenX - X_ERROR_B) / X_ERROR_M
    adjustedZ = (givenZ - Z_ERROR_B) / Z_ERROR_M
    return adjustedX, adjustedZ

def closestNote(contours, distances, angles, ellipses):
    """Finds the closest and biggest contour."""
    if len(ellipses) == 0:
        return [], [], [], []
    maxNote = 0
    maxIndex = -1
    for i in range(len(ellipses)):
        contour = contours[i]
        distance = distances[i]
        
        if distance == 0: sizeDistance = 639639639
        else: sizeDistance = cv2.contourArea(contour) / distance
        if sizeDistance > maxNote:
            maxNote = sizeDistance
            maxIndex = i
    return [contours[maxIndex]], [distances[maxIndex]], [angles[maxIndex]], [ellipses[maxIndex]]


# MAIN

def runPipeline(image, llrobot):
    image = cv2.rectangle(image, (0, FOV_HEIGHT_PIX - BUMPER_HEIGHT_PIX), (FOV_WIDTH_PIX, FOV_HEIGHT_PIX), (0, 0, 0), -1) # Make the bottom of the image black to hide the red bumper
    toDisplay, mask, xCoords, zCoords = processImage(image)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    llpython = [xCoords[0], zCoords[0], 0, 0, 0, 0, 0, 0]

    return [], toDisplay, llpython