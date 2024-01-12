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
image = cv2.imread(os.path.join("note_detection", "sample_images", "IMG_1559.jpeg"))

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
    convexHull = [cv2.convexHull(contour) for contour in contours]
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

    # Add in more filtering here

    # Fit ellipses to contours
    ellipses = []
    for hull in convexHull:
        #print(hull)
        if len(hull) < 5: continue # fitEllipse needs at least 5 points
        #print("Found contour")
        ellipse = cv2.fitEllipse(hull)
        print(ellipse)
        newMajor = ellipse[1][1] * 10 / 12 # Shrink the ellipse to be at roughly the center of the torus
        newMinor = ellipse[1][0] - ellipse[1][1] * 2 / 12 # Removing the same amount from the minor axis as the major axis
        ellipse = list(ellipse)
        ellipse[1] = (newMinor, newMajor)
        ellipse = tuple(ellipse)

        # Find the angle to the ellipse
        major = ellipse[1][1]
        minor = ellipse[1][0]
        radiansPerPixelHeight = math.radians(params["FOV_HEIGHT_DEGREES"] / params["FOV_HEIGHT_PIX"])
        ellipseAngle = minor * radiansPerPixelHeight
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