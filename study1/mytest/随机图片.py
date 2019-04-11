import cv2
import numpy as np
from matplotlib import pyplot as plt
from pyzbar import pyzbar
import TextEncoder 
from hubarcode.datamatrix import DataMatrixEncoder


encoder = DataMatrixEncoder("hello")
encoder.save("test.png")
print (encoder.get_ascii())

img1 = np.full((100,100,4),127,np.uint8)


for i in range(0,100):
    for j in range(0,100):
        img1[i,j][3] = 100


plt.imshow(img1)
plt.show()

img2 = np.full((300,300,1),127,np.uint8)

img2 = cv2.imread("cli-DATAMATRIX_321kk.png",0)

print(img2)
img3 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
plt.imshow(img3)
plt.show()

barcode = pyzbar.decode(img2)[0]


print(barcode)

p1 = (barcode.rect.left,barcode.rect.top)

p2 = (barcode.rect.left+barcode.rect.width,barcode.rect.top+barcode.rect.height)
cv2.rectangle(img2,p1,p2,255,3)

polyline = np.array(barcode.polygon)

print(polyline)

cv2.polylines(img2,[polyline],True,0)

img3 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
plt.imshow(img3)
plt.show()



