import cv2 as cv
import constants
from functions import *
import numpy as np
import threading
from time import sleep
import sys
import os
from datetime import datetime
print("We out")



def process_frame(cameraid, path, nt, headless = False, show_select = False):
    cap = waitForCam(path)

    detector = getDetector()
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    cammat = constants.CAMERA_CONSTANTS[cameraid]["matrix"]
    distco = constants.CAMERA_CONSTANTS[cameraid]["distortion"]

    while True:
        current_time = datetime.now().timestamp()
        success, frame1 = cap.read()
        frame1 = cv.blur(frame1, (5,5))

        if not success:
            robotheta = 63900
            rx = 63900
            ry = 63900
            logPose(cameraid, rx, ry, math.degrees(robotheta), current_time)
            pushval(nt, f"{cameraid}", robotheta, rx, ry, tags, current_time)

            print("failed to get image from camid ", cameraid)
            cap.release()
            cap = waitForCam(path)
            cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            continue

        pose_calc = getPose(frame1, cammat, distco, detector, cameraid)
        if pose_calc:
            robotheta = pose_calc["angle"]
            rx, ry, _ = pose_calc["pos"]
            tags = pose_calc["tags"]
            logPose(cameraid, rx, ry,  math.degrees(robotheta), current_time)
            pushval(nt, f"{cameraid}", robotheta, rx, ry, tags, current_time)

        if (not headless) and show_select: cv.imshow(f"CAMID{cameraid}:", frame1)
        



        cv.waitKey(1)

        

if __name__ == "__main__":

    headless = "-h" in sys.argv

    nt = networkConnect()
    # nt = None
    print("Connected to networktables")

    t1 = threading.Thread(target=process_frame, args=[0, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usb-0:1.3:1.0-video-index0"),nt,headless, False])
    t2 = threading.Thread(target=process_frame, args=[2, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usb-0:1.4:1.0-video-index0"),nt,headless, False])
    t3 = threading.Thread(target=process_frame, args=[4, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usb-0:1.2:1.0-video-index0"),nt,headless, False])
    t4 = threading.Thread(target=process_frame, args=[6, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usb-0:1.1:1.0-video-index0"),nt,headless, True])

    cam_lst = [
        #t1,
        #t2,
        #t3,
        t4,
    ]

    for cam in cam_lst:
        cam.start()


    # cam.join() NEVER DO THIS!
        
    print("Done!")