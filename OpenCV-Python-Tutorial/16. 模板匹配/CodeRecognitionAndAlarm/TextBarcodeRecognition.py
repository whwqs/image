# -*- coding: utf-8 -*-

# @Time    : 2019/3/14 17:54
# @File    : TextBarcodeRecognition.py
# @Date    : 2019-03-14
# @Author  : Yuwenjun
import datetime
import json
import numpy as np
import cv2
import time
import sys

from pytesseract import pytesseract
from pyzbar import pyzbar


class TextBarcodeRecognition(object):
    def __init__(self, img_path, save_path):
        """
        初始化
        :param img_path: 图片路径
        :param save_path: json保存路径
        :param lock_path: 锁文件路径
        """
        self.img_path = img_path
        self.save_path = save_path
        # 计数和检测变量
        self.count = 0
        self.pre_img = None
        self.pre_barcode = None
        self.pre_text = None

    def zbarDecoder(self, image):
        """
        调用zbar解析条码
        :param image: 条码对象
        :return: 条码值和类型
        """
        barcodes = pyzbar.decode(image)
        # 循环检测到的条形码
        for barcode in barcodes:
            # 转换成字符串
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # 拼接条形码数据和类型
            code = "{} ({})".format(barcodeData, barcodeType)
            return code

    def zbarDecoder2(self, image):
        """
        调用zbar解析条码
        :param image: 条码对象
        :return: 条码值和类型
        """
        barcodes = pyzbar.decode(image)
        # 循环检测到的条形码
        for barcode in barcodes:
            # 转换成字符串
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type           
            return barcodeData,barcodeType
        return [""]

    def getQRInBinImg(self, thresh):
        """
        开运算处理后继续识别条码
        :param thresh: 二值化条码对象
        :return: 识别结果
        """
        res = self.zbarDecoder(thresh)
        if res is None:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            res = self.zbarDecoder(opened)
        return res

    def getBarcode(self, image):
        """
        条码解析主函数
        :param image: 条码对象
        :return: 识别结果
        """
        if image is None:
            return
        ret = self.zbarDecoder(image)
        if ret is None:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thre, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            ret = self.zbarDecoder(thresh)
            if ret is None:
                thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                ret = self.zbarDecoder(thresh)

            # 设定初始累加阀值
            thre = int(thre / 2)

            while (not ret) and (thre < 230):
                # 二值化
                thresh = cv2.threshold(gray, thre, 255, cv2.THRESH_BINARY)[1]
                ret = self.getQRInBinImg(thresh)
                thre += 15        
        return ret    

    def getCode(self,roi_text):
        img_binary = self.pretreatment(roi_text)
        text = self.img2string(img_binary).replace(" ", "")        
        return text

    def saveJson(self, barcode, text):
        """
        写入json文件
        :param barcode: 条码值
        :param text: 产品编号值
        :return:
        """
        while True:
            try:
                f = open(self.save_path, "w")
            except: 
                try:
                    f.close()
                except:
                    pass
                time.sleep(0.1)
                continue
            else:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dic = {
                    "code": text,
                    "barcode": barcode,
                    "count": self.count,
                    "savetime": now
                }
                # 设置不转换成ascii  json字符串首缩进
                f.write(json.dumps(dic, ensure_ascii=False, indent=2))
                f.close()
                break

    def pretreatment(self, img):
        """
        图片预处理，暂仅做滤波二值化
        :param img: 图片对象
        :return: 二值化图片对象
        """
        # 图片边缘有黑线或者其它杂色时使用
        roi_text = self.clearBorder(img)

        # 倾斜角度矫正
        roi_text = np.rot90(roi_text)
        # 计算角度
        angle = self.getMinAreaRect(roi_text)[-1]
        # 校正文本
        rotated = self.rotateBound(roi_text, angle)

        # 形态学筛选出文字矩形区域，细化文字识别区域
        dilation, roi_text = self.process(rotated)
        cv2.imwrite("close.jpg", dilation)
        # 裁剪出文字区域
        cropImg = self.findRegion(dilation, roi_text)

        # 图片二值化处理
        # 实验场景图片文字笔划过细，二值化自适应阈值和大津法容易导致文字笔划断点，导致识别错误，暂不做二值化
        gray = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # 双边过滤
        # blurred = cv2.bilateralFilter(gray, 3, 100, 15)
        # 全局二值化
        # _, thresh = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)
        # ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 4)

        # 适当对图片进行放大
        th, tw = blurred.shape[:2]
        # 局部像素的重采样填充
        img_binary = cv2.resize(blurred, (int(tw * 2), int(th * 2)), interpolation=cv2.INTER_AREA)
        return img_binary    

    def rotateBound(self, image, angle):
        """
        图片旋转
        :param image: 图片对象
        :param angle: 角度
        :return: 旋转后的图片对象
        """
        # 获取宽高
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # 提取旋转矩阵 sin cos
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # 计算图像的新边界尺寸
        nW = int((h * sin) + (w * cos))
        #     nH = int((h * cos) + (w * sin))
        nH = h

        # 调整旋转矩阵
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        return cv2.warpAffine(image, M, (nW, nH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def getMinAreaRect(self, image):
        """
        获取图片旋转角度
        :param image: 图片对象
        :return: 图片旋转角度
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        coords = np.column_stack(np.where(thresh > 0))
        return cv2.minAreaRect(coords)

    def clearBorder(self, img):
        """
        擦除边框
        :param img: 图片对象
        :return: 去除边缘两个像素的图片对象
        """
        h, w = img.shape[:2]
        for y in range(0, w):
            for x in range(0, h):
                if y < 2 or y > w - 2:
                    img[x, y] = 255
                if x < 2 or x > h - 2:
                    img[x, y] = 255
        return img

    def process(self, image):
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
        element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 9))

        # 5. 膨胀一次，让轮廓突出
        dilation = cv2.dilate(binary, element2, iterations=1)

        # 6. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
        erosion = cv2.erode(dilation, element1, iterations=1)

        # 7. 再次膨胀，让轮廓明显一些
        dilation2 = cv2.dilate(erosion, element2, iterations=2)

        return dilation2, image

    def findRegion(self, dilation, image):
        """
        查找过滤出需要识别的文本区域
        :param dilation: 膨胀后的图片对象
        :param image: 原图片对象
        :return: 细化后的文字区域对象
        """
        # 1.查找轮廓
        contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 2.筛选轮廓，未查到轮廓返回原图片区域
        if not len(contours):
            return image
        else:
            # 获取最大轮廓边界
            max_area = sorted(contours, key=cv2.contourArea, reverse=True)[0]

            # 判断获取的边界是否为三维数组
            if len(max_area.shape) != 3:
                return image

            # 如果文本区域截取过小，返回原图片
            if cv2.contourArea(max_area) < 3000:
                return image

            # 轮廓近似，作用很小
            epsilon = 0.001 * cv2.arcLength(max_area, True)
            approx = cv2.approxPolyDP(max_area, epsilon, True)

            # 找到最小的矩形，该矩形可能有方向
            rect = cv2.minAreaRect(max_area)

            # box是四个点的坐标
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # box X轴坐标
            Xs = [i[0] for i in box]
            Ys = [i[1] for i in box]
            x1 = min(Xs)
            x2 = max(Xs)
            y1 = min(Ys)
            y2 = max(Ys)

            # box 水平宽高
            height = y2 - y1
            width = x2 - x1

            # 截取符合的box区域
            cropImg = image[y1:y1 + height, x1:x1 + width]
            # cv2.imwrite("cropImg.jpg", cropImg)
            return cropImg

    def img2string(self, roi):
        """
        识别roi文本
        :param roi_dic: roi
        :return: 识别结果
        """
        # 设置 Tesseract config 参数（语言、LSTM神经网络和单行文本）。
        config = ("-l chi_sim --oem 1 --psm 7 digits")
        result = pytesseract.image_to_string(roi, config=config)

        return result

    def getBarcodeAndText(self, roi_code, roi_text, image):
        """
        获取条码值和产品编号值
        :param roi_code: 条码对象
        :param roi_text: 文本识别对象
        :return: 条码和文本区结果
        """
        # save_path = r"D:\spmonitor\log"
        # now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # f = open(save_path + "\\" + "1.txt", "a")
        # cv2.imwrite(save_path + "\\" + "{}1.jpg".format(now), image)
        # cv2.imwrite(save_path + "\\" + "{}2.jpg".format(now), roi_text)
        # 1.解析条码
        barcode = self.getBarcode(roi_code)
        # 2.识别文本
        text = self.getCode(roi_text)
        # cv2.imwrite(save_path + "\\" + "{}3.jpg".format(now), img_binary)
        # f.write(now + ":" + text.replace(" ", "") + ":" + "\n")
        # f.close()
        print(barcode)
        print(text)
        return barcode, text

    def handle(self, loc_conf):
        """
        主函数
        :return:
        """
        image = cv2.imread(self.img_path)
        if image is None:
            print("image is Nonetype")
            return

        # 获取文本和条码区域
        loc_code = loc_conf["loc_code"]
        loc_text = loc_conf["loc_text"]

        (x1, y1, w1, h1) = loc_code
        roi_code = image[y1:y1 + h1, x1:x1 + w1]
        (x2, y2, w2, h2) = loc_text
        roi_text = image[y2:y2 + h2, x2:x2 + w2]

        # 转灰度图
        gray_lwpCV = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 运动检测部分，通过判断图片差值、条码和文本识别结果进行相应的计数
        gray_lwpCV = cv2.resize(gray_lwpCV, (300, 300))  # 重置窗口大小
        # 用高斯滤波进行模糊处理
        gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (3, 3), 0)

        # 如果没有背景图像就将当前帧当作背景图片
        if self.pre_img is None:
            self.pre_img = gray_lwpCV
        else:
            # absdiff把两幅图的差的绝对值输出到另一幅图上面来
            img_delta = cv2.absdiff(self.pre_img, gray_lwpCV)
            # threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）阈值时应该被赋予的新的像素值,阈值方法)
            thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
            # 膨胀图像
            thresh = cv2.dilate(thresh, None, iterations=2)
            # findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 当未检测到轮廓或最大轮廓的面积小于设定值时认为物体禁止，否则认为物体运动
            if not len(contours):
                if not all([self.pre_barcode, self.pre_text]):
                    barcode, text = self.getBarcodeAndText(roi_code, roi_text, image)
                    if all([barcode, text]):
                        self.pre_barcode, self.pre_text = barcode, text
                        self.count += 1
                        self.saveJson(barcode, text)
                else:
                    barcode, text = self.getBarcodeAndText(roi_code, roi_text, image)
                    if barcode and self.pre_text != text:
                        self.pre_barcode, self.pre_text = barcode, text
                        self.count += 1
                        self.saveJson(barcode, text)
            else:
                # 获取最大轮廓边界
                max_area = sorted(contours, key=cv2.contourArea, reverse=True)[0]
                # 设置敏感度，contourArea计算轮廓面积
                if cv2.contourArea(max_area) < 2200:
                    barcode, text = self.getBarcodeAndText(roi_code, roi_text, image)
                    if barcode and self.pre_text != text:
                        self.pre_barcode, self.pre_text = barcode, text
                        self.count += 1
                        self.saveJson(barcode, text)
                else:
                    print("Object Moving!")
                    pass

            # 将当图片设置为背景
            self.pre_img = gray_lwpCV


if __name__ == '__main__':    
    functype = sys.argv[1]# "code"# 
    imgpath = sys.argv[2]#r"D:\spmonitor\1.jpg"#
    image = cv2.imread(imgpath)        
    loc = sys.argv[3]#"583,808,71,164"#
    (x,y,w,h) = eval("("+loc+")")
    roi = image[y:y + h, x:x + w]
    rec = TextBarcodeRecognition(imgpath,"")
    if functype == "barcode":  
        print(rec.zbarDecoder2(roi)[0])
    else: 
        ret = rec.getCode(roi)
        if bool(ret):
            print(ret)
        else:
            print("")