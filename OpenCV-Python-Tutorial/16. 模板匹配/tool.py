import json
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