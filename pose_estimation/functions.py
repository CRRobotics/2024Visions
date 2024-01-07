"""Functions that help make the pipeline more readable"""
from apriltag import apriltag
import cv2 as cv
import numpy as np
import constants
from networktables import NetworkTables as nt
import threading
import math
from time import sleep
import csv


"""CAMERA FUNCTIONS-----------------------------------------------"""
def waitForCam(path):
    """Waits until there is a camera available at `path`. This is to ensure that cameras that are unplugged can be plugged back in and not interrupt the script."""
    while True:
        cap = cv.VideoCapture(path)
        cap:cv.VideoCapture
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv.CAP_PROP_FPS, 20)
        if cap.isOpened():
            print("open")
            return cap
        else:
            sleep(0.001)

def shrinkFrame(frame):
    """Returns a frame that is shrinked. Only works when NON-HEADLESS"""
    kernel = np.ones((2,2),np.float32)/2
    dst = cv.filter2D(frame,-1,kernel)
    return dst[::2,::2]



"""NETWORK TABLES AND LOGGING FUNCTIONS-----------------------------"""
def networkConnect() -> any:
    """Copied from documentation. Establishes a connection to 10.6.39.2"""
    cond = threading.Condition()
    notified = [False]

    def connectionListener(connected, info):
        print(info, '; Connected=%s' % connected)
        with cond:
            notified[0] = True
            cond.notify()

    nt.initialize(server=constants.SERVER)
    nt.addConnectionListener(connectionListener, immediateNotify=True)

    with cond:
        print("Waiting")
        if not notified[0]:
            cond.wait()
    return nt

def pushval(networkinstance, tablename:str, theta, rx, ry, ntags, time):
    """Pushes theta, rx, ry, ntags, and time values to the networktable. TableName should be the CameraID"""
    table = networkinstance.getTable(tablename)
    table.putNumber("theta", theta)
    table.putNumber("rx", rx)
    table.putNumber("ry", ry)
    table.putNumber("ntags", ntags)
    table.putNumber("time", time)

def logPose(camid, rx, ry, rt, time):
    """Logs camid, rx, ry, rt, and time of a pose."""
    with open("/home/crr/2024Visions/pose_estimation/log.csv", "a+", newline="") as log:
        c = csv.writer(log)
        c.writerow(
            [camid, rx, ry, rt, time]
        )








"""APRILTAG FUNTIONS -----------------------------------"""
def getDetector():
    """Returns an Apriltag Detector"""
    aprilobj = apriltag(constants.TAG_FAMILY, maxhamming=0, blur = 0.1)
    return aprilobj


def getDetections(detector, frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return detector.detect(gray)


def allGoodCorners(l:list, framewidth:int, frameheight:int, margin:int) -> bool:
    """Detects corner clipping at the corner of a frame. Invalidates corners that are `margin` pixels away from the corner."""
    for corner in l:
        x, y = corner
        print(x, y)
        if x < margin or x > framewidth - margin or y < margin or y > frameheight - margin:
            return False
    return True

def getPose(frame, cmtx, dist, detector, cameraid):
    """Calculates and returns the pose given an intrinsiz camera matrix, distortion coefficients, a frame, detector, and camera ID. """
    detections = getDetections(detector,frame)

    h, w, _ = frame.shape

    toreturn = {
    }

    if detections:
        objectpoints = []
        cornerpoints = []
        tagcounter = 0
        margins = []

        for detection in detections:
            if detection["id"] in range(1, 16) and len(detection["lb-rb-rt-lt"]) == 4 and detection["margin"] > constants.MARGIN_THRESHOLD and allGoodCorners(detection["lb-rb-rt-lt"], w, h, constants.PIXEL_MARGIN):
                tagcounter += 1

                corner_counter = 1
                for x, y in detection["lb-rb-rt-lt"]:
                    corner = (int(x), int(y))
                    cv.putText(frame, f"{corner_counter}", corner, cv.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0))
                    cv.circle(frame, corner, 5, (255,0,0), -1)
                    corner_counter += 1

                """Drawing corners"""
                cx, cy = detection["center"]
                cv.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
                cv.putText(frame, "id: %s"%(detection["id"]), (int(cx), int(cy) + 20), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255, 0))
                

                """Updating objectpoints and cornerpoints lists."""
                for coord in constants.ID_POS[detection["id"]]:
                    objectpoints.append(coord)

                for corner in detection["lb-rb-rt-lt"]:
                    cornerpoints.append(corner)
                
                margins.append(detection["margin"])

        if objectpoints and cornerpoints:
            objectpoints = np.array(objectpoints)
            cornerpoints = np.array(cornerpoints)

            mmat, rvec, tvec = cv.solvePnP(
                objectpoints, 
                cornerpoints,
                cmtx,
                dist,  
                )

            tvec = (np.array(tvec))
            rvec = (np.array(rvec))   

            rotationmatrix, _ = cv.Rodrigues(rvec)

            "GETTING THE COORDINATES OF CAMERA"
            final_coords = np.dot(-rotationmatrix.T, tvec)#Multiply the negative inverse of the rotations to the translation vector. 


            "GETTING THE ZTHETA (yaw of CAMERA on ground)"
            pointCoords = np.dot(rotationmatrix.T, np.array([[1],[0],[0]])) # Get coordinates of rotated point on unit sphere. We want to project it onto the x-y axis
            pointX, pointY = [pointCoords[0][0], pointCoords[1][0]]

            # Signs of x and y coordinates on unit circle
            sx = 1 if pointX <= 0 else -1
            sy = 1 if pointY <= 0 else -1
            # # Modify theta based on coordinate quadrant to compensate for arctan only going from -90 to 90
            ztheta = math.degrees(math.atan(pointCoords[1][0]/pointCoords[0][0])) + (180*sy)*(sx - 1)/(-2)
            ztheta -= 90
            if ztheta < 0: ztheta += 360


            px, py, pz = final_coords

            robocoords, robotheta = getRobotVals(ztheta, cameraid, px, py)#Transform back to pose of robot

            toreturn["pos"] = robocoords
            toreturn["angle"] = robotheta
            toreturn["tags"] = tagcounter
            toreturn["margins"] = margins
            rx, ry, _ = robocoords

            cv.putText(frame, " PX: %.4f  PY: %.4f  PZ: %.4f"%(px, py, pz), (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255))
            cv.putText(frame, " ZTHETA: %.4f"%(ztheta), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255))
            cv.putText(frame, " RX: %.4f  RY: %.4f RTHETA: %.4f"%(rx, ry, math.degrees(robotheta)), (50, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255))
            return toreturn

    """IF DOES NOT DETECT ANYTHING, RETURN PLACEHOLDER"""
    return {
        "pos": (63900,63900,63900),
        "angle":63900,
        "tags":0,
        "margins":0
    }

def getRobotVals(ay, cameraid, px, py):
    """Return positioning data of the robot. (rx, ry )"""
    robotheta = math.radians(ay - constants.CAMERA_CONSTANTS[cameraid]["thetar"])
    if robotheta > math.pi: robotheta -= math.tau
    xr = constants.CAMERA_CONSTANTS[cameraid]["xc"]
    yr = constants.CAMERA_CONSTANTS[cameraid]["yc"]

    transformationmatrix = np.array([
            [math.cos(math.radians(ay)), -math.sin(math.radians(ay)), px],
            [math.sin(math.radians(ay)), math.cos(math.radians(ay)), py],
            [0, 0, 1]
        ],
        dtype=object
    )
    robotcoordsRelativetocam = np.array(
        [
            [xr],
            [yr],
            [1]
        ],
        dtype=object
    )
    robocoords = np.dot(transformationmatrix, robotcoordsRelativetocam) #what we learned in visions training
    return robocoords, robotheta


