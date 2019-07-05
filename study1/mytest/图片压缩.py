import sys
import os

sys.path.append(os.getcwd())
from mytool import *
SetCurrentDir(__file__)


import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("1.png")
img = cv2.resize(img,(0,0),fx=1,fy=1,interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite("2.png",img)