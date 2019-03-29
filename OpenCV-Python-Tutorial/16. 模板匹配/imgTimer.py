import time
class imgTimer(object):
    def __init__(self, cfg,handleObj):
        self.handle = handleObj
        self.cfg = cfg
        self.timespan = cfg.get("imgTimer")
        self.handling = False#处理中
        self.lockFile = None#锁文件句柄
        self.lockFileDic = None

    def getLock(self):
        try:
            self.lockFile = open(self.cfg.get("lock"),"r")
            self.lockFileDic = eval(self.lockFile.read())            
        except:
            self.freeLock()
            return False
        return True

    def freeLock(self):
        if bool(self.lockFile):
            self.lockFile.close()
        self.lockFile = None

    def start(self):
        while True:            
            time.sleep(self.timespan)
            if self.handling:                
                continue
            if not bool(self.getLock()):                
                continue
            print("获得锁")
            self.handling = True
            self.handle.handle(self.lockFileDic)
            self.freeLock()
            print("释放锁")
            self.handling = False