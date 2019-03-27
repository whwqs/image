import cv2
import numpy as np
from matplotlib import pyplot as plt

#原图
img = cv2.imread("img.bmp")
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
h,w = img.shape[:2]
#print(round(w/2),round(h/2))
for template in [img0,img1,img2,img7]:        
    h, w = template.shape[:2]
    res = cv2.matchTemplate(img_, template, cv2.TM_CCOEFF_NORMED)

    print("img"+str(img.shape))
    print("res"+str(res.shape))
    print("t"+str(template.shape))

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)
    
    cv2.rectangle(img_, max_loc, (max_loc[0]+w,max_loc[1]+h), (255,0,0), 1)

    #print("====")
    #print(res)
    #print("******")
    threshold = 0.8
    loc = np.where(res >= threshold)
    #print(res)
    #print(loc)
    add = 0
    print(loc[::-1])
    for pt in zip(*loc[::-1]):  # *号表示可选参数
        bottom_right = (pt[0] + w, pt[1] + h)
        cv2.rectangle(img_, pt, bottom_right, (0,0,255), 1)
        closed = False
        for pt2 in pts:
                if abs(pt[0]-pt2[0])+abs(pt[1]-pt2[1]) < 20:
                        closed = True
        if not closed:
                pts.append(pt)
        if add==0:
                
                add+=1
print((pts))
cv2.namedWindow("img_1",0);
cv2.resizeWindow("img_1",960, 540);
cv2.imshow('img_1',img_)
cv2.waitKey(0)
cv2.destroyAllWindows()
