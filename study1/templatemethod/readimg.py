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

def getBarcode(imgpath,cfgname):  
    setting = cfg.get("t_"+cfgname)
    barcodeset = setting["barcode"]
    x,y,w,h = barcodeset["loc"]
    resize = barcodeset["resize"]
    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]
    r,c = part.shape[:2]
    if resize > 1:
        part = cv2.resize(part,(resize*c,resize*r), interpolation=cv2.INTER_LANCZOS4)
    #show(part)
    barcodes = pyzbar.decode(part)        
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type           
        return barcodeData,barcodeType
    return [""]

def getCode(imgpath,cfgname):      
    setting = cfg.get("t_"+cfgname)
    codeset = setting["code"] 
    tfile = codeset["tfile"]
    tv = codeset["tv"]
    tloc = codeset["tloc"]    
    loc = codeset["loc"]
    resize = codeset["resize"]
    interpolation = eval(codeset["interpolation"])
    blursize = codeset["blursize"]
    tminpx = codeset["tminpx"]
    minpx = codeset["minpx"]

    img1 = cv2.imread(tfile,0)
    temp1 = template(img1,tloc,tv,blursize)
    temp1.split(tminpx)
    temp1.check()
    #temp1.show(10,True,"templates")

    img2 = cv2.imread(imgpath,0)    
    temp2 = template(img2,loc,[],blursize)
    temp2.split(minpx)
    #temp2.show(8,False)
    code = ""    
    for idx in range(len(temp2.imglist)):
        img3 = temp2.imglist[idx]
        realrate = temp2.imgwhratelist[idx] 
        v = temp1.getv(img3,resize,interpolation)
        v = temp1.modifybyrate(v,realrate) 
        code += v
    return code

def getCode2(imgpath,cfgname):      
    setting = cfg.get("t_"+cfgname)
    codeset = setting["code"] 
    tfile = codeset["tfile"]
    tv = codeset["tv"]
    tloc = codeset["tloc"]    
    loc = codeset["loc"]
    resize = codeset["resize"]
    interpolation = eval(codeset["interpolation"])
    blursize = codeset["blursize"]
    tminpx = codeset["tminpx"]
    minpx = codeset["minpx"]

    img1 = cv2.imread(tfile,0)
    temp1 = template(img1,tloc,tv,blursize)
    temp1.split(tminpx)
    temp1.check()
    #temp1.show(10,True,"templates")

    img2 = cv2.imread(imgpath,0)    
    temp2 = template(img2,loc,[],blursize)
    temp2.split(minpx)
    #temp2.show(8,False)
    code = ""    
    for idx in range(len(temp2.imglist)):
        img3 = temp2.imglist[idx]        
        v = temp1.getv(img3,resize,interpolation)        
        code += v
    return code

if __name__== '__main__':
    functype = sys.argv[1]#"code"#
    imgpath = sys.argv[2]#"20190329_150621.bmp"#
    name = sys.argv[3]# "黄鹤楼"#   
    if functype == "barcode":
        print(getBarcode(imgpath,name)[0])
    elif functype=="code":     
        code = getCode(imgpath,name)
        print(code)
    elif functype=="code2":     
        code = getCode2(imgpath,name)
        print(code)