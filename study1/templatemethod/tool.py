import datetime
import json
import numpy as np
import cv2
import time
import sys
import math

def get0_255img(img,size):
    img2 = cv2.blur(img,(size,size))
    return cv2.threshold(img2, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

def getjustimg(img):
    if img is None:
        return None
    rows,cols = img.shape[:2]
    (r1,c1,r2,c2)=(-1,-1,-1,-1)
    old2 = img.copy()
    for r in range(rows):
        if np.sum(old2[r]==0)>0:
            r1=r
            break              

    for r in range(rows-1,r1,-1):
        if np.sum(old2[r]==0)>0:
            r2=r
            break 
    
    old3 = np.transpose(img)
    for r in range(cols):
        if np.sum(old3[r]==0)>0:
            c1 = r
            break                 

    for r in range(cols-1,c1,-1):
        if np.sum(old3[r]==0)>0:
            c2=r
            break  
    if r1>=r2 or c1>=c2:
        return None
    return img[r1:r2,c1:c2]

def split_row(img):
    if img is None:
        return []
    img2 = img.copy()
    rows,cols = img2.shape[:2]    
    ret = []
    lastrow = 0
    lastrow2 = 0
    for r in range(1,rows,1):
        has0 = np.sum(img2[lastrow2]==0)>0               
        all255 = np.sum(img2[r]==255)==cols
        if has0 and (all255 or r==rows-1):
            img_ = img2[lastrow:r]            
            ret.append(img2[lastrow:r])
            lastrow = r
        lastrow2 +=1
    return ret

def split_col(img): 
    if img is None:
        return None
    ret = split_row(img.transpose())
    return [x.transpose() for x in ret]

def split(img,mincount_0):
    ret = []
    arr_row = split_row(img)
    for x in arr_row:
        arr_col = split_col(x)
        for x2 in arr_col:
            if np.sum(x2==0)>=mincount_0:
                ret.append(getjustimg(x2))
    return ret
    

def split_row_getmaximg(old):    
    ret = split_row(old)
    n0 = 0
    img2 = None
    for img in ret:            
        n = np.sum(img==0)   
        if n>n0:
            img2 = img        
            n0 = n 
    return img2

def split_col_getmaximg(old): 
    if old is None:
        return None
    ret = split_row(old.transpose())
    n0 = 0
    img2 = None
    for img in ret:            
        n = np.sum(img==0)   
        if n>n0:
            img2 = img        
            n0 = n 
    if img2 is None:
        return None
    return img2.transpose()

def show(img):
    cv2.imshow("test",img)
    cv2.waitKey(0)

class tool(object):
    """description of class"""
    @staticmethod
    def isNullOrEmpty(strValue):
        return not bool(strValue) or  not bool(str.strip(strValue))

    @staticmethod
    def toJson(obj:object):        
        return json.dumps(obj,ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=2)   

    @staticmethod
    def fromJson(strJson:str):   
        if strJson.startswith(u'\ufeff'): 
                strJson = strJson.encode('utf8')[3:].decode('utf8')
        return json.loads(strJson)

class config(object):
    """json文件转对象"""
    def __init__(self, jsonFilePath):
        try:            
            f = open(jsonFilePath, mode="r", encoding="utf8")             
        except: 
            if bool(f):
                f.close()
            return
        lst = f.readlines() 
        f.close()
        json = ""
        for s in lst:             
            json += s
        self.obj = tool.fromJson(json)   

    def get(self,name):
        return self.obj[name]

    def getobj(self):
        return self.obj

class template(object):
    def __init__(self, img, tloc,tv,blursize=3):   
        if len(img.shape)<3:
            self.img = img
        else:
            self.img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        
        self.tloc = tloc
        self.tv = tv
        self.blursize = blursize

    def split(self,mincount_0):
        img = self.img
        x,y,w,h = self.tloc
        img = img[y:y+h,x:x+w]        
        img = get0_255img(img,self.blursize)
        self.imglist = split(img,mincount_0)
        
    def check(self):
        nimg = len(self.imglist)
        nv = len(self.tv)
        if nv!=nimg:
            raise Exception("图像切分数量不等于值的数量，图像数量："+str(nimg)+",值数量："+str(nv))

    def getv(self,img,resize,interpolation):
        v = None
        ntemp = 0
        p2 = img.copy()        
        p2 = cv2.resize(p2, (resize, resize), interpolation=interpolation)
        for i in range(len(self.imglist)):
            t = cv2.resize(self.imglist[i],(resize,resize), interpolation=interpolation) 
            dimg = p2 - t
            #show(dimg)
            n0 = np.sum(dimg==0)
            if n0>ntemp:
                ntemp = n0
                v = self.tv[i]
        return v

    def show(self,cols,showv=False,title="test"):
        maxr = 0
        maxc = 0
        for x in self.imglist:
            s = x.shape[:2]
            if maxr<s[0]:
                maxr = s[0]
            if maxc<s[1]:
                maxc = s[1]       
        
        rows = math.ceil(len(self.imglist)/cols)
        dr = 20
        dc = 10
        img = np.full(((maxr+dr)*rows, (maxc+dc)*cols),255, np.uint8)        
        for i in range(rows):
            for j in range(cols):
                z = i*cols+j
                if z>= len(self.imglist):
                    break
                img2 = self.imglist[z]
                shape = img2.shape[:2]
                x,y,w,h = j*(maxc+dc),i*(maxr+dr),shape[1],shape[0]                
                img[y:y+h,x:x+w] = img2
                if showv:
                    v = self.tv[z]
                    left = x
                    bottom=y+maxr+dr-3
                    cv2.putText(img, text=v, org=(left, bottom), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=1,bottomLeftOrigin=False)

        cv2.imshow(title,img)
        cv2.waitKey()
        