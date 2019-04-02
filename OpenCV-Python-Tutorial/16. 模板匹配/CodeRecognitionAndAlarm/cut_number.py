# -*- coding: utf-8 -*-

# @Time    : 2019/3/29 17:43
# @File    : cut_number.py
# @Date    : 2019-03-29
# @Author  : Yuwenjun
import cv2
import numpy as np


def get_number_region(img):
    
    img = cv2.blur(img, (3, 3))
    (_, thresh) = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 形态学处理:定义矩形结构
    closed = cv2.erode(thresh, None, iterations=1)  # 闭运算：迭代5次

    height, width = closed.shape[:2]
    z = [0] * height
    # 垂直投影：统计并存储每一列的黑点数
    lst_x = list()
    for x in range(0, width):
        for y in range(0, height):
            if closed[y, x] == 0:
                lst_x.append(x)
            else:
                continue

    # 水平投影  #统计每一行的黑点数
    a = 0
    emptyImage1 = np.zeros((height, width), np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            if closed[y, x] == 0:
                a = a + 1
            else:
                continue
        z[y] = a
        a = 0

    # 绘制水平投影图
    for y in range(0, height):
        for x in range(0, z[y]):
            b = 255
            emptyImage1[y, x] = b

    # 获取y轴坐标
    lst_y = list()
    start = 0
    for y in range(0, height):
        if emptyImage1[y, 0] == 255:
            if not start:
                start = y
        else:
            if emptyImage1[y, 0] == 0:
                if start:
                    lst_y.append((start, y))
                    start = 0
            continue

    #print(lst_x[0], lst_x[-1])
    #print(lst_y)
    region = []
    for i in lst_y:
        corp_img = img[i[0]:i[1], 0:width]
        region.append(corp_img)
        #cv2.imwrite("{}.jpg".format(lst_y.index(i)), corp_img)
    
    return region


if __name__ == '__main__':
    img = cv2.imread(r"qie.png", 0)
    x, y, w, h = (0, 0, 98, 525)
    img = img[y:y + h, x:x + w]
    print (len(get_number_region(img)))