import datetime
import json
import numpy as np
import cv2
import time
import sys

from pytesseract import pytesseract
from pyzbar import pyzbar

def process(image):
        """
        形态学变换的预处理，得到可以查找矩形的图片
        :param image: 文字区域图片对象
        :return: 膨胀后的图片对象
        """
        # 1.灰度转换
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Sobel算子，x方向求梯度
        sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)

        # 3. 二值化
        ret, binary = cv2.threshold(
            sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        # 4. 膨胀和腐蚀操作的核函数
        element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 3))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 3))

        # 5. 膨胀一次，让轮廓突出
        dilation = cv2.dilate(binary, element2, iterations=1)

        # 6. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
        erosion = cv2.erode(dilation, element1, iterations=1)

        # 7. 再次膨胀，让轮廓明显一些
        dilation2 = cv2.dilate(erosion, element2, iterations=2)

        cv2.namedWindow("w1",0);
        cv2.resizeWindow("w1",300, 300);
        cv2.namedWindow("w2",0);
        cv2.resizeWindow("w2",300, 300);

        cv2.imshow("w1",image)
        cv2.imshow("w2",dilation2)
        cv2.waitKey()
        cv2.destroyWindow()

if __name__ == "__main__" :
    img = cv2.imread("img.bmp")
    img = img[758:951,825:898]
    process(img)