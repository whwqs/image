import cv2
img = cv2.imread("0.png")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imwrite("0_1.png",gray)