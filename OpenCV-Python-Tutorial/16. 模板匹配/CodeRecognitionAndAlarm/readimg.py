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
    tfile = codeset["tfile"]
    tv = codeset["tv"]
    xt,yt,wt,ht = codeset["tloc"]    
    x,y,w,h = codeset["loc"]
    size = codeset["resize"]

    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]    
    part =  get0_255img(part)
    parts = split_row(part) 
    parts2 = []
    for p in parts:
        p2 = split_row_getmaximg(p)
        if p2 is None:
            continue
        p2 = split_col_getmaximg(p2)
        if p2 is None:
            continue
        p2 = getjustimg(p2)
        if p2 is None:
            continue
        parts2.append(p2)
    
    
    template = cv2.imread(tfile,0)   
    template = template[yt:yt+ht,xt:xt+wt]
    template = get0_255img(template)
    templates = split_row(template)
    templates2 = []
    for p in templates:
        p2 = split_row_getmaximg(p)
        if p2 is None:
            continue
        p2 = split_col_getmaximg(p2)
        if p2 is None:
            continue
        p2 = getjustimg(p2)
        if p2 is None:
            continue
        templates2.append(p2)  
   
    code = ""    

    for p in parts2:  
        number = ""
        ntemp = 0
        p2 = p.copy()        
        p2 = cv2.resize(p2, (size, size), interpolation=cv2.INTER_CUBIC)
        for i in range(len(templates2)):
            t = cv2.resize(templates2[i],(size,size), interpolation=cv2.INTER_CUBIC) 
            dimg = p2 - t
            n0 = np.sum(dimg==0)
            if n0>ntemp:
                ntemp = n0
                number = tv[i]
            
        code += number
    return code

def show(img):
    cv2.imshow("test",img)
    cv2.waitKey(0)

def get0_255img(old):
    img = cv2.blur(old,(5,5))
    return cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

def getjustimg(old):
    if old is None:
        return None
    rows,cols = old.shape[:2]
    (r1,c1,r2,c2)=(-1,-1,-1,-1)
    old2 = old.copy()
    for r in range(rows):
        if np.sum(old2[r]==0)>0:
            r1=r
            break              

    for r in range(rows-1,r1,-1):
        if np.sum(old2[r]==0)>0:
            r2=r
            break 
    
    old3 = np.transpose(old)
    for r in range(cols):
        if np.sum(old3[r]==0)>0:
            c1 = r
            break                 

    for r in range(cols-1,c1,-1):
        if np.sum(old3[r]==0)>0:
            c2=r
            break  
    if r1>=r2 or c1>=c2:
        return None
    return old[r1:r2,c1:c2]

def split_row(old):
    if old is None:
        return []
    img = old.copy()
    rows,cols = img.shape[:2]    
    ret = []
    lastrow = 0
    lastrow2 = 0
    for r in range(1,rows,1):
        has0 = np.sum(img[lastrow2]==0)>0               
        all255 = np.sum(img[r]==255)==cols
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
    if old is None:
        return None
    ret = split_row(old.transpose())
    n0 = 0
    img2 = None
    for img in ret:            
        n = np.sum(img==0)   
        if n>n0:
            img2 = img        
            n0 = n 
    if img2 is None:
        return None
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