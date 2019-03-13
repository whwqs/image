import numpy as np
arr = [[1,2,3],[4,5,5],[4,5,5]]
a = np.array(arr)

len = a.shape[0] #多维数组的行数
print(a.dtype) #输出元素类型
#另外也还可以使用切片方式来处理数组

print(a)
b = np.add(arr,10)
print(b.shape)

c = np.multiply(arr,arr)
print(c)

d = np.sum(c,axis=1)

print(d)