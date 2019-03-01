# ex2tron's blog:
# http://ex2tron.wang

import cv2
imgpath = "lena.jpg"

# 1.灰度图加载一张彩色图
img = cv2.imread(imgpath, 0)


# 2.显示图片
cv2.imshow('lena', img)
cv2.waitKey(0)

# 先定义窗口，后显示图片
cv2.namedWindow('lena2', cv2.WINDOW_NORMAL)
cv2.imshow('lena2', img)
cv2.waitKey(0)


# 3.保存图片
cv2.imwrite('lena_gray.jpg', img)
