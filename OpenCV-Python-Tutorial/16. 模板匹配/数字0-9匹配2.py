import cv2
import numpy as np
from matplotlib import pyplot as plt

#原图
img = cv2.imread("img.bmp",0)
img0 = img[775:800,838:888]
img1 = img[859:874,234:285]
img2 = img[768:795,531:581]
img3 = img[10:75,210:245]
img4 = img[10:75,255:293]
img5 = img[10:75,305:335]
img6 = img[10:75,349:385]
img7 = img[899:927,836:883]
img8 = img[10:75,442:480]
img9 = img[10:75,495:525]
pts = []
img_ = img.copy()
for template in [img0,img1,img2,img7]:        
    h, w = template.shape[:2]
    res = cv2.matchTemplate(img_, template, cv2.TM_CCOEFF_NORMED)
    print("====")
    print(res)
    print("******")
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # *号表示可选参数
        bottom_right = (pt[0] + w, pt[1] + h)
        cv2.rectangle(img_, pt, bottom_right, (0, 0, 255), 2)
        pts.append(pt)
print(len(pts))
cv2.imshow('img_',img_)
cv2.waitKey(0)
