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



def process_frame(cameraid, path, nt, headless = False):
    cap = waitForCam(path)

    detector = getDetector()
    print("got thread for ", cameraid)

    while 1:
        _, img = cap.read()

        if _:
            print(f'{cameraid}yesworks')
            


        

if __name__ == "__main__":

    headless = "-h" in sys.argv

    #nt = networkConnect()
    nt = None
    print("Connected to networktables")

    """t1 = threading.Thread(target=process_frame, args=[0, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usb-0:1.3:1.0-video-index0"),nt,headless])
    t2 = threading.Thread(target=process_frame, args=[2, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usb-0:1.4:1.0-video-index0"),nt,headless])"""
    t3 = threading.Thread(target=process_frame, args=[4, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usb-0:1.2:1.0-video-index0"),nt,headless])
    t4 = threading.Thread(target=process_frame, args=[6, os.path.realpath("/dev/v4l/by-path/pci-0000:05:00.0-usb-0:1.1:1.0-video-index0"),nt,headless])

    """t1.start()
    t1.join()
    t2.start()
    t2.join()"""
    t3.start()
    t3.join()
    t4.start()

    t4.join()
    

    # cam.join() NEVER DO THIS!
        
    print("Done!")
    
