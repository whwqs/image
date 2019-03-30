from tool import *
import datetime
import json
import numpy as np
import cv2
import time
import sys
from pytesseract import pytesseract
from pyzbar import pyzbar

cfg = config("config.json")

def getBarcode(imgpath,name):  
    setting = cfg.get("t_"+name)
    barcodeset = setting["barcode"]
    x,y,w,h = barcodeset["loc"]
    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]
    barcodes = pyzbar.decode(part)        
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type           
        return barcodeData,barcodeType
    return [""]

def getCode(imgpath,name):      
    setting = cfg.get("t_"+name)
    codeset = setting["code"] 
    t = cv2.imread(codeset["tfile"],0)    
    tloc = codeset["tloc"]
    fx = codeset["fx"]
    fy = codeset["fy"]
    x,y,w,h = codeset["loc"]
    threshold = codeset["threshold"]
    sort = codeset["sort"]
    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]
    pts = []    
    for i in range(10):  
        try:
            
            t_ = eval("t["+tloc[i]+"]") 
            
            t_ = cv2.resize(t_, None, fx=fx[i], fy=fy[i], interpolation=cv2.INTER_CUBIC)
            
        except:
            return "模板出错，请检查配置文件:"+ str(i)       
                
        res = cv2.matchTemplate(part, t_ , cv2.TM_CCOEFF_NORMED)        
        loc = np.where(res >= threshold[i]) 
        for p in zip(*loc[::-1]):            
            closed = False
            for p2 in pts:
                if abs(p[0]-p2["p"][0])+abs(p[1]-p2["p"][1])<20:
                    closed = True
                    break
            if not closed:                
                pts.append({"p":p,"i":i})
    
    if sort=="x":
        key = lambda o:o['p'][0]
    else:
        key = lambda o:o['p'][1]
    pts.sort(key=key)
    
    code = ""
    for p in pts:
        code += str(p["i"])
    return code

def getCode2(imgpath,name):      
    setting = cfg.get("t_"+name)
    codeset = setting["code"] 
    t = cv2.imread(codeset["tfile"],0)    
    tloc = codeset["tloc"]
    fx = codeset["fx"]
    fy = codeset["fy"]
    x,y,w,h = codeset["loc"]
    threshold = codeset["threshold"]
    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]    
    part_reginos = get_number_region(part)    
    code = ""
    templateDic = {}
    
    for region in part_reginos:    
        maxv = -100
        number = ""
        for i in range(10):
            key = "t"+str(i)
            if not( key in templateDic):
                try:            
                    t_ = eval("t["+tloc[i]+"]")             
                    #t_ = cv2.resize(t_, None, fx=fx[i], fy=fy[i], interpolation=cv2.INTER_CUBIC)  
                    (_, t_) = cv2.threshold(t_, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
                    #t_ = cv2.erode(t_, None, iterations=1)  # 闭运算：迭代5次
                    #t_ = get_number_region(t_)[0]
                    #show(t_)
                    templateDic[key] = t_
                except:
                    return "模板出错，请检查配置文件:"+ str(i) 
            t_ = templateDic[key]           
                
            h1,w1 = t_.shape[:2]
            h2,w2 = region.shape[:2]
            h3 = max([h1,h2])
            w3 = max([w1,w2])
            region2 = np.full((h3,w3),255,np.uint8)
            region2[:h2,:w2] = region            
           
            res = cv2.matchTemplate(region2, t_ , cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val>maxv:
                number = str(i)
                maxv = max_val
        code += number
    return code

def show(img):
    cv2.imshow("test"+str(time.time()),img)
    cv2.waitKey(0)

def get_number_region(img):    

    img = cv2.blur(img, (3, 3))
    
    (_, thresh) = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)  

    h,w = thresh.shape[:2]

    xfound = 0

    for x in range(h):
        if xfound %2==0:
            y0 = 0
        for y in range(y0,w):






    
    
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 形态学处理:定义矩形结构
    #closed = cv2.erode(thresh, None, iterations=1)  # 闭运算：迭代5次

    closed = thresh
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

if __name__== '__main__':
    functype = sys.argv[1]#"code"#
    imgpath = sys.argv[2]#"20190329_150621.bmp"#
    name = sys.argv[3]#"黄鹤楼"#    
    if functype == "barcode":
        print(getBarcode(imgpath,name)[0])
    else:     
        code = getCode2(imgpath,name)
        print(code+" "+str(len(code)))