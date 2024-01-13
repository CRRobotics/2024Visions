import cv2


cap = cv2.VideoCapture(0)

while 1:
    s, img = cap.read()
    if s:
        cv2.imshow("frame", img)
        cv2.waitKey(1)
    else:
        print("failed")