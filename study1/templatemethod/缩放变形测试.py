import numpy as np
import cv2

def show(img):
    cv2.imshow("test",img)
    cv2.waitKey()

img0 = np.zeros((101,101),np.uint8)

for i in range(101):
    for j in range(101):
        if (i+j)%2==1:
            img0[i,j] = 255
    

show(img0.transpose())

img1 = cv2.resize(img0, (505, 505), interpolation=cv2.INTER_NEAREST)

show(img1.transpose())

img2 = cv2.resize(img0.transpose(),(324,456),interpolation=cv2.INTER_NEAREST)

img3 = cv2.resize(img1.transpose(),(324,456),interpolation=cv2.INTER_NEAREST)

show(img2-img3)
