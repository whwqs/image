from tool import *
import datetime
import json
import numpy as np
import cv2
import time
import sys
import os


#os.chdir("/home/xx/projects/LSTM_Qi_v27/py")   #修改当前工作目录

#print(os.getcwd() )   #获取当前工作目录
#print(__file__)
#print(__name__)
dir1 = os.path.dirname(os.path.abspath(__file__))
#print(dir1)
os.chdir(dir1)


img = cv2.imread("0_9.jpg",0)
print(img.shape)
img = get0_255img(img,3)
print(img.shape)
cv2.imwrite("09test3.jpg",img)