import os
def SetCurrentDir(file):
    dir = os.path.dirname(file)
    os.chdir(dir)
    