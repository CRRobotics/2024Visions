import cv2 as cv
import constants
from functions import *
import numpy as np
import threading
from time import sleep
import sys
import os
from datetime import datetime
import time
print("We out")



def process_frame(cameraid, path, nt, headless = False, show_select = False, mainThreadLog:dict = {}):
    cap = waitForCam(path)

    detector = getDetector()

    cammat = constants.CAMERA_CONSTANTS[cameraid]["matrix"]
    distco = constants.CAMERA_CONSTANTS[cameraid]["distortion"]

    pose_calc = None
    prev_time = datetime.now().timestamp()
    framecount = 0
    while True:
        current_time = datetime.now().timestamp()
        delta = current_time - prev_time
        fps = framecount / delta
        success, frame1 = cap.read()
        framecount += 1
        
        if framecount % 100 ==0 :
            framecount = 0
            prev_time = current_time
        if not success:
            robotheta = 63900
            rx = 63900
            ry = 63900
            tags = 0
            logPose(cameraid, rx, ry, math.degrees(robotheta), fps, current_time, constants.ALT_LOG_PATH)
            pushval(nt, f"{cameraid}", robotheta, rx, ry, tags, current_time)
            mainThreadLog[cameraid] = [rx, ry, robotheta, tags]
            print("failed to get image from camid ", cameraid)
            cap.release()
            cap = waitForCam(path)
            continue

        pose_calc = getFullPose(frame1, cammat, distco, detector, cameraid)
        if pose_calc:
            robotheta = pose_calc["angle"]
            rx, ry, _ = pose_calc["pos"]
            tags = pose_calc["tags"]
            logPose(cameraid, rx, ry,  math.degrees(robotheta), fps, current_time, constants.ALT_LOG_PATH)
            pushval(nt, f"{cameraid}", robotheta, rx, ry, tags, current_time)
            mainThreadLog[cameraid] = [rx, ry, robotheta, tags]
            cv.imwrite(f"frames/cam{cameraid}/{current_time}.png", frame1)


        if (not headless) and show_select: 
            cv.putText(frame1, "fps:%.2f"%(fps), (1200, 600), cv.FONT_HERSHEY_SIMPLEX, .5, (255,0, 255))
            cv.imshow(f"CAMID{cameraid}:", frame1)
        cv.waitKey(1)

        
    

        

if __name__ == "__main__":

    time.sleep(10)

    headless = "-h" in sys.argv

    #nt = networkConnect()
    
    
    print("Connected to networktables")
    log("connected to apriltags")

    valueLog = {}

    t1 = threading.Thread(target=process_frame, args=[0, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usbv2-0:1.3:1.0-video-index0"),nt,headless, True, valueLog])
    t2 = threading.Thread(target=process_frame, args=[2, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usbv2-0:1.4:1.0-video-index0"),nt,headless, True, valueLog])
    t3 = threading.Thread(target=process_frame, args=[4, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usbv2-0:1.2:1.0-video-index0"),nt,headless, True, valueLog])
    t4 = threading.Thread(target=process_frame, args=[6, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usbv2-0:1.1:1.0-video-index0"),nt,headless, True, valueLog])
    t5 = threading.Thread(target=process_frame, args=[8, os.path.realpath("/dev/v4l/by-path/pci-0000:06:00.4-usbv2-0:2:1.0-video-index0"),nt,headless, True, valueLog])
    t6 = threading.Thread(target=process_frame, args=[10, os.path.realpath("/dev/v4l/by-path/pci-0000:06:00.3-usbv2-0:2:1.0-video-index0"),nt,headless, True, valueLog])
    # left port: /dev/v4l/by-path/pci-0000:06:00.4-usbv2-0:2:1.0-video-index0
    # right port: /dev/v4l/by-path/pci-0000:06:00.3-usbv2-0:2:1.0-video-index0 

    cam_lst = [
        #t1,
        #t2,
        #t3,
        #t4,
        #t5,
        t6
    ]

    print("starting cams")
    for cam in cam_lst:
        cam.start()


    # cam.join() NEVER DO THIS!
        
    print("Done!")
    log("Done")

    # if not headless:
    #     while True:
    #         print(valueLog)
    #         cv.waitKey(1)
