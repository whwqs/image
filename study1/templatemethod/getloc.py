# -*- coding: utf-8 -*-

# @Time    : 2019/2/27 11:08
# @File    : getloc.py
# @Date    : 2019-02-27
# @Author  : Yuwenjun

import cv2

global img
global point1, point2


def on_mouse(event, x, y, flags, param):
    global img, point1, point2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
        cv2.rectangle(img2, point1, (x, y), (255, 0, 0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
        point2 = (x, y)
        cv2.rectangle(img2, point1, point2, (0, 0, 255), 5)
        cv2.imshow('image', img2)
        min_x = min(point1[0], point2[0])
        min_y = min(point1[1], point2[1])
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] - point2[1])
        print(min_x, min_y, width, height)
        # cut_img = img[min_y:min_y + height, min_x:min_x + width]
        # cv2.imwrite('lena3.jpg', cut_img)


def main():
    global img
    img = cv2.imread(r"d:/spmonitor/1.jpg")
    # img = cv2.imread(r"c.jpg")
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("image", 640, 480)
    cv2.setMouseCallback('image', on_mouse)
    cv2.imshow('image', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
