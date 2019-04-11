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

print(A[2].count(-9))

print(A[2].index(12))


C = [[255,255,255],[255,0,255],[0,255,0],[255,0,255],[255,255,255]]
C = np.array(C)

print("255的数量:"+str(np.sum(C==255)))

rows,cols = C.shape[:2]

C=C.tolist()



ret = []
r1,c1,r2,c2 = -1,-1,-1,-1
print("====",rows,cols)
for r in range(rows):
    if r1==-1:
        try:
            C[r].index(0)
            r1=r
        except ValueError:
            continue
    elif r2==-1:
        n=C[r].count(255)
        
        if n==cols:            
            r2=r-1   
print(r1,r2)


r1,c1,r2,c2 = -1,-1,-1,-1

for r in range(rows):
    try:        
        C[r].index(0)
        r1=r
        break
    except ValueError:
        continue   
        

for r in range(rows-1,r1,-1):
    try:        
        C[r].index(0)
        r2=r
        break
    except ValueError:
        continue   
print(r1,r2)

C = np.transpose(C).tolist()

for c in range(cols):
    try:        
        C[c].index(0)
        c1=c
        break
    except ValueError:
        continue   
        

for c in range(cols-1,c1,-1):
    try:        
        C[c].index(0)
        c2=c
        break
    except ValueError:
        continue   
print("col:",c1,c2)