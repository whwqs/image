# ex2tron's blog:
# http://ex2tron.wang

import cv2

imgpath = "lena.jpg"

img = cv2.imread(imgpath)
cv2.imshow('lena', img)

k = cv2.waitKey(0)
# ord()用来获取某个字符的编码
if k == ord('s'):
    cv2.imwrite('lena_save.bmp', img)
