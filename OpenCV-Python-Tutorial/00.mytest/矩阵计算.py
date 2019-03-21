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


arr2 = [[[[1,2,3,4]],[[1,2,3,4]]],[[[1,2,3,4]],[[1,2,3,4]]]]

a2 = np.array(arr2)

print(a2.shape)

#3元1次方程组
#3.45x+4.6y+8z = 300.45
#4x-5y+6z = 210.45
#9x+9y+12z = 230
A = [
    [3.45,4.6,8]
    ,[4,-5,5]
    ,[9,9,12]
]
b = [300.45,210.45,230]

c = 