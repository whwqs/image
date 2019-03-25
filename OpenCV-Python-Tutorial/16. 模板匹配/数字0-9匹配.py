import cv2
import numpy as np
from matplotlib import pyplot as plt

#原图
img = cv2.imread("1234567890.jpg",0)
img0 = img[10:75,70:99]
img1 = img[10:75,115:136]
img2 = img[10:75,160:195]
img3 = img[10:75,210:245]
img4 = img[10:75,255:293]
img5 = img[10:75,305:335]
img6 = img[10:75,349:385]
img7 = img[10:75,396:430]
img8 = img[10:75,442:480]
img9 = img[10:75,495:525]

for i in range(10):
    img_ = img.copy()
    template = eval("img"+str(i))
    h, w = template.shape[:2]
    res = cv2.matchTemplate(img_, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # *号表示可选参数
        bottom_right = (pt[0] + w, pt[1] + h)
        cv2.rectangle(img_, pt, bottom_right, (0, 0, 255), 2)
    cv2.imshow('img_',img_)
    cv2.waitKey(0)
