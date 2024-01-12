import cv2
import numpy as np
from time import sleep

# Returns a frame that is smaller
def shrinkFrame(frame, scale):
    kernel = np.ones((scale,scale),np.float32)/(scale ** 2)
    dst = cv2.filter2D(frame,-1,kernel)
    return dst[::scale,::scale]

def waitForCam(path):
    """Waits until there is a camera available at `path`. This is to ensure that cameras that are unplugged can be plugged back in and not interrupt the script."""
    while True:
        cap = cv2.VideoCapture(path)
        cap:cv2.VideoCapture
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 20)
        if cap.isOpened():
            print("open")
            return cap
        else:
            sleep(0.001)
            print("Waiting")