import cv2
import numpy as np

# Returns a frame that is smaller
def shrinkFrame(frame, scale):
    kernel = np.ones((scale,scale),np.float32)/(scale ** 2)
    dst = cv2.filter2D(frame,-1,kernel)
    return dst[::scale,::scale]