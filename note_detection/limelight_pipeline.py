import cv2
import numpy as np
import math
from time import sleep
import os

# CONSTANTS
HUE = 179
SATURATION = 255
VALUE = 255

HSV_UPPER = [179, 255, 255]
HSV_LOWER = [169, 191, 78]
BLUR_SIZE = 0

CAMERA_CENTER_ANGLE_DEGREES = 0
CAMERA_HEIGHT_IN = 12.75

FOV_HEIGHT_DEGREES = 40
FOV_HEIGHT_PIX = 720
FOV_WIDTH_DEGREES = 70
FOV_WIDTH_PIX = 1280

NOTE_OUTER_RADIUS_IN = 14
NOTE_THICKNESS_IN = 2

# HELPER FUNCTIONS

# Returns a frame that is smaller
def shrinkFrame(frame, scale):
    kernel = np.ones((scale,scale),np.float32)/(scale ** 2)
    dst = cv2.filter2D(frame,-1,kernel)
    return dst[::scale,::scale]

'''
def waitForCam(path):
    """Waits until there is a camera available at `path`. This is to ensure that cameras that are unplugged can be plugged back in and not interrupt the script."""
    while True:
        cap = cv2.VideoCapture(path)
        cap:cv2.VideoCapture
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FOV_WIDTH_PIX)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FOV_HEIGHT_PIX)
        cap.set(cv2.CAP_PROP_FPS, 20)
        if cap.isOpened():
            print("open")
            return cap
        else:
            sleep(0.001)
            print("Waiting")
'''

def pixelsToRadians(pixelLength, angle):
    """Converts a line of pixelLength pixels rotated clockwise from a horizontal line by angle degrees into an angle in radians based on the camera's FOV."""
    radiansPerPixelHeight = math.radians(FOV_HEIGHT_DEGREES / FOV_HEIGHT_PIX)
    radiansPerPixelWidth = math.radians(FOV_WIDTH_DEGREES / FOV_WIDTH_PIX)
    lineAngleHeight = pixelLength * math.sin(math.radians(angle)) * radiansPerPixelHeight
    lineAngleWidth = pixelLength * abs(math.cos(math.radians(angle))) * radiansPerPixelWidth
    lineAngle = math.sqrt(lineAngleHeight ** 2 + lineAngleWidth ** 2)
    return lineAngle

def processImage(image):
    convexHull, mask = findNoteContours(image, True)
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
    #cv2.imshow("Frame", shrinkFrame(toDisplay, 2))
    return toDisplay, mask

# FILTER CODE
    
# Get upper and lower bounds for HSV filter
upper = np.array(HSV_UPPER)
lower = np.array(HSV_LOWER)
#print(upper)

# Read the image and convert to HSV
# sampleImage = cv2.imread(os.path.join("note_detection", "sample_images", "IMG_1559.jpeg"))

def findNoteContours(image, displayMask = False):
    """Filters the image for notes and returns a list of convexHulls where they are"""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blurred = cv2.medianBlur(image, BLUR_SIZE * 2 + 1)
    mask = cv2.inRange(blurred, lower, upper)
    if displayMask:
        #cv2.imshow("Mask", shrinkFrame(mask, 2))
        pass
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return [], mask
    largestContour = max(contours, key=lambda x: cv2.contourArea(x))
    convexHull = [cv2.convexHull(largestContour)]

    # Add in more filtering here

    return convexHull, mask

def fitEllipsesToNotes(convexHull):
    ellipses = []
    for hull in convexHull:
        if len(hull) < 5: continue # fitEllipse needs at least 5 points
        ellipse = cv2.fitEllipse(hull)
        newMajor = ellipse[1][1] * (1 - NOTE_THICKNESS_IN / NOTE_OUTER_RADIUS_IN) # Shrink the ellipse to be at roughly the center of the torus
        newMinor = ellipse[1][0] - ellipse[1][1] * NOTE_THICKNESS_IN / NOTE_OUTER_RADIUS_IN # Removing the same amount from the minor axis as the major axis
        ellipse = list(ellipse)
        ellipse[1] = (newMinor, newMajor)
        ellipse = tuple(ellipse)
        ellipses.append(ellipse)
    
    return ellipses

def drawEllipses(ellipses, textToDisplay, image):
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

# POS MATH

def computeEllipseAnglesFromCam(ellipses):
    """Assuming the inputted ellipses are circles viewed from an angle, calculates the angle from that circle to the camera."""
    angles = []
    for ellipse in ellipses:
        major = ellipse[1][1]
        minor = ellipse[1][0]
        angle = ellipse[2] # The clockwise angle from a horizontal line to the minor axis
        ellipseAngle = pixelsToRadians(minor, angle)
        minorLengthRelativeToDiameter = minor / major
        angleFromCam = (math.pi - ellipseAngle) / 2 - math.asin(minorLengthRelativeToDiameter * math.sin((math.pi + ellipseAngle) / 2))
        angles.append(angleFromCam)
    return angles

def computeNoteDistancesFromAngles(angles):
    """Uses the angle of a note from the camera to calculate its distance, assuming it is on the floor."""
    distances = []
    for angle in angles:
        distance = CAMERA_HEIGHT_IN * math.tan(angle)
        distances.append(distance)
    return distances

def computeNoteDistancesFromMajorAxes(ellipses):
    """Uses the major axis of a note to calculate its distance, assuming it is on the floor."""
    distances = []
    for ellipse in ellipses:
        major = ellipse[1][1]
        angle = ellipse[2]
        ellipseAngle = pixelsToRadians(major, angle - 90)
        distanceStraightOn = 6 / math.tan(ellipseAngle / 2) # tan(ellipseAngle) SHOULD not be 0 or infinity
        if distanceStraightOn < CAMERA_HEIGHT_IN: distance = 0
        else: distance = math.sqrt(distanceStraightOn ** 2 - CAMERA_HEIGHT_IN ** 2)
        distances.append(distance)
    return distances

def computeNoteDistancesFromCenters(centers):
    """Uses the center point of a note to calculate its distance based on the tilt of the camera, assuming it is on the floor and the center point is below the camera"""
    distances = []
    for center in centers:
        centerY = center[1]
        heightAboveCamCenter = FOV_HEIGHT_PIX / 2 - centerY
        angleAboveCamCenter = pixelsToRadians(heightAboveCamCenter, 90)
        angleAboveHorizontal = angleAboveCamCenter + math.radians(CAMERA_CENTER_ANGLE_DEGREES)
        distance = CAMERA_HEIGHT_IN / math.tan(angleAboveHorizontal)
        distances.append(distance)
    return distances

# CALIBRATION

'''
def calibrate(image):
    blurSize = 1
    blurred = cv2.medianBlur(image, blurSize * 2 + 1)
    mask = cv2.inRange(blurred, lower, upper)

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

    def updateBlurSize(value):
        global blurSize
        blurSize = value

    def saveValues(value):
        print("HSV_LOWER = " + lower.tolist())
        print("HSV_LOWER = " + upper.tolist())
        print("HSV_LOWER = " + blurSize)

    cv2.namedWindow("Filter")
    cv2.createTrackbar("Hue min", "Filter", 0, HUE, updateHueMin)
    cv2.createTrackbar("Hue max", "Filter", HUE, HUE, updateHueMax)
    cv2.createTrackbar("Saturation min", "Filter", 0, SATURATION, updateSaturationMin)
    cv2.createTrackbar("Saturation max", "Filter", SATURATION, SATURATION, updateSaturationMax)
    cv2.createTrackbar("Value min", "Filter", 0, VALUE, updateValueMin)
    cv2.createTrackbar("Value max", "Filter", VALUE, VALUE, updateValueMax)
    cv2.createTrackbar("Blur", "Filter", 0, 20, updateBlurSize)
    cv2.createTrackbar("Slide to save", "Filter", 0, 1, saveValues)

    blurred = cv2.medianBlur(image, blurSize * 2 + 1)
    toDisplay = cv2.cvtColor(blurred, cv2.COLOR_HSV2BGR)
    mask = cv2.inRange(blurred, lower, upper)
    return mask
'''

# MAIN
def runPipeline(image, llrobot):
    #print(image)
    image, mask = processImage(image)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    llpython = [0, 0, 0, 0, 0, 0, 0, 0]

    return [], image, llpython
