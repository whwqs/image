import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = np.zeros((300,300,3),np.uint8)#300*300黑图片
cv2.imshow("窗口标题",img1)#标题乱码，先放一下
cv2.waitKey()

print(img1.shape)

#画31根水平红线
for i in range(0,300,10):    
    for j in range(0,300):
        mod = j%10
        if mod != 5:
            img1[i,j] = (0,0,255)
for i in range(0,300):
    img1[299,i] = (0,0,255)

cv2.imshow("title",img1)
cv2.waitKey()

#matplotlib 是rgb
img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
plt.imshow(img2)
plt.show()

sobelx = cv2.Sobel(img1,-1,1,0,ksize=3)
cv2.imshow("title",sobelx)
cv2.waitKey()

sobely = cv2.Sobel(img1,-1,0,1)
cv2.imshow("title",sobely)
cv2.waitKey()