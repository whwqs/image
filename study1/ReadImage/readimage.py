from globalmanager import *
import numpy as np
import cv2
from pytesseract import pytesseract
from pyzbar import pyzbar
from PIL import Image,ImageEnhance

def contrast_and_brightness(alpha, beta, img):
    blank = np.full(img.shape,0,img.dtype)
    #part = np.uint8(np.clip((alpha * part + beta), 0, 255))#改变亮度和对比度  
    # dst = alpha * img + beta * blank
    dst = cv2.addWeighted(img, alpha, blank, 1-alpha, beta)    
    return dst

def smallImage(img):
    tmp = img.copy()
    tmp = cv2.resize(tmp,(100,100), interpolation=cv2.INTER_NEAREST)
    return tmp

def getArcLength(img):
    tmpimg,contours, hierarchy = cv2.findContours(img, 3, 2)  
    return cv2.arcLength(contours[0], True)

def getContours(img):
    tmpimg,contours, hierarchy = cv2.findContours(img, 3, 2)  
    return contours

def countOfContours(img):
    tmpimg,contours, hierarchy = cv2.findContours(img, 3, 2)  
    return len(contours)

def reverseImage(img):
    tmp = img.copy()
    r,c = tmp.shape
    for r1 in range(r):
        for c1 in range(c):
            tmp[r1,c1] = 255-tmp[r1,c1]
    return tmp

def setCurrentDir():
    dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir)

def get0_255Image(img,size=3):
    img2 = cv2.blur(img,(size,size))
    _,thresh = cv2.threshold(img2, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    return thresh

def getMinImageRectangleWithWhiteEdge(img):
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
    retimg = img[r1:r2,c1:c2].copy()
    rr,cc = retimg.shape
    retimg2 = np.full((rr+2,cc+2),255,np.uint8)
    retimg2[1:rr+1,1:cc+1]=retimg
    return retimg2

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
                ret.append(getMinImageRectangleWithWhiteEdge(x2))
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

def show(img,title="test"):
    cv2.imshow(title,img)
    cv2.waitKey(0)

class BarcodeRecognizer(object):
    def __init__(self, img,resize=1,contrast=1.5,brightness=50,bfix=False):
        self.img = img
        self.resize = resize
        self.contrast = contrast#对比度1-3 
        self.brightness = brightness#亮度0-100
        self.bfix = bfix

    def getBarcode(self):
        part = self.img.copy()
        resize = self.resize
        r,c = part.shape[:2]
        if self.bfix:            
            part = cv2.resize(part,(resize*c,resize*r), interpolation=cv2.INTER_LANCZOS4) #INTER_LANCZOS4  
            #part[part>thresh]=255
            #_,part = cv2.threshold(part, thresh, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
            part = contrast_and_brightness(self.contrast,self.brightness,part)            
            #show(part)
        barcodes = pyzbar.decode(part) 
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type           
            return barcodeData,barcodeType        
        return ["",""]

class ImageSplit(object):
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
        img = get0_255Image(img,self.blursize)
        self.imglist = split(img,mincount_0)#切分后放在这个数组      
        self.count = len(self.imglist)        
        
    def check(self,isDigital=False):        
        nv = len(self.tv)        
        if nv!=self.count:
            raise Exception("图像切分数量不等于值的数量，图像数量："+str(self.count)+",值数量："+str(nv))   
        self.whrate = [x.shape[1]/x.shape[0] for x in self.imglist]        
        if isDigital:
            if nv != 10:
                raise Exception("请检查数字模板是否正确,当前配值是："+str(self.tv))   
            idx = self.tv.index("1")
            self.wh_1 = self.whrate[idx]
            self.wh_other = (np.sum(self.whrate)-self.wh_1)/(self.count-1) 
            idx = self.tv.index("3")
            self.wh_3 = self.whrate[idx]
            self.v_idx_dic = {}
            for i in range(nv):
                self.v_idx_dic[self.tv[i]] = i

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

class ImageRecognizer(object):
    def __init__(self,img,imgSplit=None):
        self.img = img
        self.imageSplit = imgSplit
        self.debug_1 = -1        

    def getCodeFromTemplate(self,resize,interpolation):
        v = None        
        sum0 = 0 
        img0 = self.img.copy()        
        h,w = img0.shape
        whrate0 = w/h
        size = (w*resize,h*resize)
        img0 = cv2.resize(img0, size, interpolation=interpolation)        
        
        for i in range(self.imageSplit.count):
            t = cv2.resize(self.imageSplit.imglist[i],size, interpolation=interpolation) 
            dimg = t-img0    
            n0 = np.sum(dimg==0)

            if n0>sum0:                
                v = self.imageSplit.tv[i]                
                sum0 = n0  

        self.v = v

    def getOneDigital(self,resize,interpolation):
        v = None        
        sum0 = 0 
        img0 = self.img.copy()        
        h,w = img0.shape
        size = (w*resize,h*resize)
        whrate0 = w/h
        count0 = countOfContours(reverseImage(self.img))        
        img0 = cv2.resize(img0, size, interpolation=interpolation)

        if debug and self.debug_1== debug_1:
            show(img0,"img0")
        
        #8
        if count0==3:
            self.v = "8"
            return
        #1
        f1 = math.fabs(whrate0-self.imageSplit.wh_1)
        f2 = math.fabs(whrate0-self.imageSplit.wh_other)
        if f1<f2:#3掉像素时也会扁，所以有可能是3            
            f2 = math.fabs(whrate0-self.imageSplit.wh_3)
            if f1<f2:
                self.v = "1"
            else:
                self.v = "3"
            return        
        
        for i in range(self.imageSplit.count):
            img1 = self.imageSplit.imglist[i]
            count1 = digital_countOfContours_dic[self.imageSplit.tv[i]]
            if count0 != count1:
                continue

            t = cv2.resize(img1,size, interpolation=interpolation) 
            dimg = t-img0    
            n0 = np.sum(dimg==0)
            
            if debug and self.debug_1== debug_1:
                dimg[dimg==1] = 255            
                show(dimg,str(i))
                print(i,n0)

            if n0>sum0:                
                v = self.imageSplit.tv[i]                
                sum0 = n0 

        self.v = v        

        if debug and self.debug_1== debug_1:
            print(self.v,self.lastv,self.sum0rate)        

    def readBinary(self,cx=3,cy=3):
        r,c = self.img.shape
        img = self.img[1:r-1,1:c-1]#去掉白边
        r2,c2 = img.shape
        dx = math.ceil(c2/cx)#小块宽
        dy = math.ceil(r2/cy)#小块高
        size = dx*dy
        binary = ""
        for i in range(cy):#从上往下
            for j in range(cx):#从左到右
                dimg = img[i*dy:(i+1)*dy,j*dx:(j+1)*dx]
                n0 = np.sum(dimg==0)
                if n0/size>0.5:
                    binary += "0"
                else:
                    binary += "1"
        self.v = binary