import cv2

img = cv2.imread("pose_estimation/IMG_1555.jpeg")


cv2.imshow("frame", img)
cv2.waitKey(0) 