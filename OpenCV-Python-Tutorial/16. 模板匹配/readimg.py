from tool import *
import datetime
import json
import numpy as np
import cv2
import time
import sys
from pytesseract import pytesseract
from pyzbar import pyzbar

def getBarcode(imgpath,x,y,w,h):
    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]
    barcodes = pyzbar.decode(part)        
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type           
        return barcodeData,barcodeType
    return [""]

def getCode(imgpath,x,y,w,h,template):
    cfg = config("jsoncfg.txt")
    threshold = cfg.get("threshold")[template]    
    t = cv2.imread(cfg.get("t"),0)
    templateArr = cfg.get(template)  
    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]
    pts = []    
    for i in range(10):  
        try:
            t_ = eval(templateArr[i])  
        except:
            continue
        res = cv2.matchTemplate(part, t_ , cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for p in zip(*loc[::-1]):
            closed = False
            for p2 in pts:
                if abs(p[0]-p2["p"][0])+abs(p[1]-p2["p"][1])<20:
                    closed = True
                    break
            if not closed:
                pts.append({"p":p,"i":i})
    key = eval(cfg.get(template+"_sort"))
    pts.sort(key=key)
    code = ""
    for p in pts:
        code += str(p["i"])
    return code

if __name__== '__main__':
    functype = sys.argv[1]
    imgpath = sys.argv[2]
    loc = sys.argv[3]    
    (x,y,w,h) = eval("("+loc+")")
    if functype == "barcode":
        print(getBarcode(imgpath,x,y,w,h)[0])
    else:
        template = sys.argv[4]
        print(getCode(imgpath,x,y,w,h,template))
