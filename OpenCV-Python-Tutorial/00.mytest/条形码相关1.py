import cv2
import numpy as np
from matplotlib import pyplot as plt

path = "1.jpg"

img = cv2.imread('1.jpg',0)
edges = cv2.Canny(img, 100, 200)

print(edges)

cv2.imshow('Edges',edges)
cv2.waitKey(0)


img = cv2.imread(path)

img2 = cv2.imread(path, 0)

h = len(img)
w = len(img[0])

img3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def compareGray():   
    n = 0
    arr = []
    for i in range(h):
        for j in range(w):
            p1 = img2[i, j]
            p2 = img3[i,j]
            if p1!=p2:
                n+=1
                arr.append([i,j])
                img[i,j]=[255,0,0]

    print(n)

    print(h*w)

    #print(arr)

compareGray()

cv2.imshow("img3", img3)
cv2.waitKey(0)
cv2.imshow("img2", img)
cv2.waitKey(0)


# img = cv2.flip(img,1)


#cv2.imwrite("1.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])


def fun1():

    print(w, h)

    cv2.imshow("显示图片", img)
    cv2.waitKey()

    ret, thresh1 = cv2.threshold(img, 86, 255, cv2.THRESH_BINARY)
    cv2.imshow("显示图片", thresh1)
    cv2.waitKey()

    cv2.rectangle(img, (56, 228), (938, 466), (0, 255, 0), 3)
    cv2.imshow("显示图片", img)
    cv2.waitKey()
