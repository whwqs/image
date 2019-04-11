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
    tloc = codeset["tloc"]    
    loc = codeset["loc"]
    resize = codeset["resize"]
    blursize = codeset["blursize"]
    tminpx = codeset["tminpx"]
    minpx = codeset["minpx"]

    img1 = cv2.imread(tfile,0)
    temp1 = template(img1,tloc,tv,blursize)
    temp1.split(tminpx)
    temp1.check()
    #temp1.show(3,True)

    img2 = cv2.imread(imgpath,0)    
    temp2 = template(img2,loc,[],blursize)
    temp2.split(minpx)
    #temp2.show(14,False)
    code = ""    
    for p in temp2.imglist:  
        code += temp1.getv(p,resize)
    return code

if __name__== '__main__':
    functype = sys.argv[1]#"code"#
    imgpath = sys.argv[2]#"20190329_150621.bmp"#
    name = sys.argv[3]# "黄鹤楼"#   
    if functype == "barcode":
        print(getBarcode(imgpath,name)[0])
    else:     
        code = getCode(imgpath,name)
        print(code)