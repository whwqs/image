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
    x,y,w,h = codeset["loc"]
    size = codeset["resize"]
    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]    
    part =  get0_255img(part)
    parts = split_row(part) 
    parts = [getjustimg(split_col_getmaximg(x)) for x in parts]
    code = ""
    templateDic = {}    
    for region in parts:  
        number = ""
        ntemp = 0
        region2 = region.copy()
        region2 = cv2.resize(region2, (size, size), interpolation=cv2.INTER_CUBIC)
        for i in range(10):
            key = "t"+str(i)
            if not( key in templateDic):
                try:            
                    t_ = eval("t["+tloc[i]+"]")    
                    t_ = get0_255img(t_)  
                    t_ = split_row_getmaximg(t_)
                    t_ = split_col_getmaximg(t_)
                    t_ = getjustimg(t_)  
                    templateDic[key] = t_
                except:
                    return "模板出错，请检查配置文件:"+ str(i) 
            t_ = templateDic[key]  
            rows,cols = t_.shape[:2]            
            
            t_2 = cv2.resize(t_,(size,size), interpolation=cv2.INTER_CUBIC)           
            
            dimg = region2-t_2
            n0 = np.sum(dimg==0)
            if n0>ntemp:
                ntemp = n0
                number = str(i)          
               
            
        code += number
    return code

def show(img):
    cv2.imshow("test"+str(time.time()),img)
    cv2.waitKey(0)

def get0_255img(old):
    img = cv2.blur(old,(5,5))
    return cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

def getjustimg(old):
    rows,cols = old.shape[:2]
    (r1,c1,r2,c2)=(-1,-1,-1,-1)
    arr = old.tolist()
    for r in range(rows):
        try:        
            arr[r].index(0)
            r1=r
            break
        except ValueError:
            continue           

    for r in range(rows-1,r1,-1):
        try:        
            arr[r].index(0)
            r2=r
            break
        except ValueError:
            continue   
    
    arr = np.transpose(old).tolist()
    for r in range(cols):
        try:        
            arr[r].index(0)
            c1=r
            break
        except ValueError:
            continue           

    for r in range(cols-1,r1,-1):
        try:        
            arr[r].index(0)
            c2=r
            break
        except ValueError:
            continue 
    return old[r1:r2,c1:c2]

def split_row(old):
    img = old.copy()
    rows,cols = img.shape[:2]
    arr = img.tolist()
    ret = []
    lastrow = 0
    lastrow2 = 0
    for r in range(1,rows,1):
        try:
            arr[lastrow2].index(0)
            has0 = True
        except ValueError:
            has0 = False
        all255 = arr[r].count(255)==cols
        if has0 and (all255 or r==rows-1):
            img_ = img[lastrow:r]            
            ret.append(img[lastrow:r])
            lastrow = r
        lastrow2 +=1
    return ret

def split_row_getmaximg(old):    
    ret = split_row(old)
    n0 = 0
    img2 = None
    for img in ret:            
        n = np.sum(img==0)   
        if n>n0:
            img2 = img        
            n0 = n 
    return img2

def split_col_getmaximg(old):    
    ret = split_row(old.transpose())
    n0 = 0
    img2 = None
    for img in ret:            
        n = np.sum(img==0)   
        if n>n0:
            img2 = img        
            n0 = n 
    return img2.transpose()

if __name__== '__main__':
    functype = sys.argv[1]#"code"#
    imgpath = sys.argv[2]#"20190329_150621.bmp"#
    name = sys.argv[3]# "黄鹤楼"#   
    if functype == "barcode":
        print(getBarcode(imgpath,name)[0])
    else:     
        code = getCode(imgpath,name)
        print(code)