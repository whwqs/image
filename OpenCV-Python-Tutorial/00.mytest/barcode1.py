import datetime
import json
import numpy as np
import cv2
import time
import sys

from pytesseract import pytesseract
from pyzbar import pyzbar

imgfile = r"D:\spmonitor\1.jpg"
(x,y,w,h) = eval("("+"1488,743,105,165"+")")
n=200
worng1 =0
worng2 =0
while n>0:
    img = cv2.imread(imgfile,0)
    
    img2 = img[y:y+h,x:x+w]


    barcodes = pyzbar.decode(img2)
    if len(barcodes)>0:
        barcode = barcodes[0]
        if barcode.data.decode("utf-8") != "6901028938433":
            print(barcode.data.decode("utf-8"))
            worng1+=1
    else:
        worng2+=1
    time.sleep(1)

print(worng1)
print(worng2)
