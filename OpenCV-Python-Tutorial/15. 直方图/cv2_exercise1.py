# More: http://ex2tron.wang

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)
img = cv2.imread('hist.jpg', 0)
cv2.imshow("t",img)
# 只计算左上角200*200的区域
mask = np.zeros(img.shape, dtype=np.uint8)
mask[:200, :200] = 255

hist_mask = cv2.calcHist([img], [0], mask, [256], [0, 256])

plt.plot(hist_mask)
plt.show()
