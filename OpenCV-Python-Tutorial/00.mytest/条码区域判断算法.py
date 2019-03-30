import cv2
import numpy as np
from matplotlib import pyplot as plt

arr = np.arange(start=1,stop=10,step=1)
arr = np.reshape(arr,(3,3))
arr = np.where(arr>4)
arr = zip(arr)
print(arr)
    
    