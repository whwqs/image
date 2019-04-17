from globalmanager import *
from readimage import *

def getBarcode(imgpath,cfgname):  
    setting = cfg.get("t_"+cfgname)
    barcodeset = setting["barcode"]
    x,y,w,h = barcodeset["loc"]
    resize = barcodeset["resize"]
    contrast = barcodeset["contrast"]
    brightness = barcodeset["brightness"]
    image = cv2.imread(imgpath,0)
    part = image[y:y+h,x:x+w]
    recog = BarcodeRecognizer(part,resize,contrast,brightness)
    return recog.getBarcode()

def getCode(imgpath,cfgname):      
    setting = cfg.get("t_"+cfgname)
    codeset = setting["code"] 
    tfile = codeset["tfile"]
    tv = codeset["tv"]
    tloc = codeset["tloc"]    
    loc = codeset["loc"]
    resize = codeset["resize"]
    interpolation = eval(codeset["interpolation"])
    blursize = codeset["blursize"]
    tminpx = codeset["tminpx"]
    minpx = codeset["minpx"]

    img1 = cv2.imread(tfile,0)
    temp1 = ImageSplit(img1,tloc,tv,blursize)
    temp1.split(tminpx)
    temp1.check(True)
    #temp1.show(10,True,"templates")

    img2 = cv2.imread(imgpath,0)    
    temp2 = ImageSplit(img2,loc,[],blursize)
    temp2.split(minpx)
    #temp2.show(8,False)
    code = ""    
    for idx in range(temp2.count):
        img3 = temp2.imglist[idx]
        recog = ImageRecognizer(img3,temp1)
        recog.debug_1 = idx
        recog.getOneDigital(resize,interpolation)             
        code += recog.v
    return code

def getCode2(imgpath,cfgname):      
    setting = cfg.get("t_"+cfgname)
    codeset = setting["code"] 
    tfile = codeset["tfile"]
    tv = codeset["tv"]
    tloc = codeset["tloc"]    
    loc = codeset["loc"]
    resize = codeset["resize"]
    interpolation = eval(codeset["interpolation"])
    blursize = codeset["blursize"]
    tminpx = codeset["tminpx"]
    minpx = codeset["minpx"]

    img1 = cv2.imread(tfile,0)
    temp1 = ImageSplit(img1,tloc,tv,blursize)
    temp1.split(tminpx)
    temp1.check()
    #temp1.show(10,True,"templates")

    img2 = cv2.imread(imgpath,0)    
    temp2 = ImageSplit(img2,loc,[],blursize)
    temp2.split(minpx)
    #temp2.show(8,False)
    code = ""    
    for idx in range(temp2.count):
        img3 = temp2.imglist[idx]        
        recog = ImageRecognizer(img3,temp1)
        recog.getCodeFromTemplate(resize,interpolation)
        code += recog.v
    return code

if __name__== '__main__':
    functype = sys.argv[1]#"code"#
    imgpath = sys.argv[2]#"20190329_150621.bmp"#
    name = sys.argv[3]# "黄鹤楼"#   
    if functype == "barcode":
        print(getBarcode(imgpath,name)[0])
    elif functype=="code":     
        code = getCode(imgpath,name)
        print(code)
    elif functype=="code2":     
        code = getCode2(imgpath,name)
        print(code)