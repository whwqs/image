import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = np.full((100,100,4),127,np.uint8)


for i in range(0,100):
    for j in range(0,100):
        img1[i,j][3] = 100


plt.imshow(img1)
plt.show()