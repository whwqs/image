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
            #print(i)#定位出错代码
            t_ = cv2.resize(t_, None, fx=fx[i], fy=fy[i], interpolation=cv2.INTER_CUBIC)
            #print(i)#定位出错代码
        except:
            return "模板出错，请检查配置文件"        
                
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

if __name__== '__main__':
    functype = sys.argv[1]
    imgpath = sys.argv[2]
    name = sys.argv[3]    
    if functype == "barcode":
        print(getBarcode(imgpath,name)[0])
    else:        
        print(getCode(imgpath,name))
