#!/usr/bin/python
# -*-coding: UTF-8 -*-

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt


"""
 坐标类
"""
class Point:
    
    address = ''
    lon = 0.00 # 经度
    lat = 0.00   # 纬度
    

    def __init__(self,address,lon,lat):
        self.address =str(address)
        self.lon = float(lon)
        self.lat = float(lat)
              

    def printvar(self):
        print ("address=%s lon=%.6f lat=%.6f" % (self.address,self.lon,self.lat)) 

#p = Point('新金桥路2222号',121.636715,31.268303)
#p.printvar()



#sys.path.append(r'/home/python')
#sys.path.append(os.path.abspath("."))
#from Point import Point

from random import choice,shuffle,sample,uniform
"""
  本程序用于实现模拟退火算法计算
  最短路径问题
"""
print(os.path.abspath("."))
parent_dir = os.path.abspath(".");

filename = parent_dir+"\ControlGroup.txt"
print(filename)
lines = open(filename).readlines();
list=[]


## 读取数据
for line in lines[0:len(lines)]:
    params = line.strip().split(',')
    print(line)
   # print(params[1])
   #  print(params[2])
   #  print(params[3])
    point = Point(params[1],params[2],params[3])
    list.append(point)
    #print(len(list))

    

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

## 计算任意两点间的距离
num = len(list)
arr = [[ col for col in range(num)] for row in range(num)]

valstr = ""
for row in range(num):
    for col in range(num):
        if col == row:arr[row][col] = 0
        else:
            p1 = list[row]
            p2 = list[col]
            arr[row][col] = haversine(p1.lon,p1.lat,p2.lon,p2.lat)
            #print(arr[row][col])
            
## print the matrix for check
'''
for row in range(num):
    for col in range(num):
        print(valstr + "\n")
        valstr = ""
        valstr += str(arr[row][col]) + ","
'''   

print ("模拟退火算法查找最短路径：")

### 参数：最小路径的最后一个节点和邻域
def valSimulateAnnealSum(curnode,nextnodeList,t):
    if nextnodeList == None or len(nextnodeList) < 1 :
        print "empty"
        return 0

    maxcost = sys.maxint
    retnode = 0

    for node in nextnodeList:
       # print "curnode : ",curnode ," node: " ,node ," mincost : ",mincost 
       t *= 50000  ## 退火因子
        if arr[curnode][node] < maxcost :
            maxcost = arr[curnode][node]
            retnode = node
            ## 以一定的概率接受较差的解
        else:
            r = uniform(0,1)
            if arr[curnode][node] > maxcost and t > t_min and math.exp(( arr[curnode][node] - maxcost ) / t) > r:
                #print " t = " ,t , "maxcost = ", maxcost , " arr = " ,arr[curnode][node],   "  exp = ",math.exp((arr[curnode][node] - maxcost)/t)  ,  " r = ",r , "t_min = " ,t_min
                retnode = node
                maxcost = arr[curnode][node]
               return (retnode,maxcost,t) 
    return (retnode,maxcost,t)



indexList = [ i for i in range(num)]  ### 原始的节点序列
selectedList = []  ## 选择好的元素

### 具体思想是： 从剩余的元素中随机选择十分之一的元素，作为邻域。然后从邻域中选择一个元素作为已经构建好的最小路径的下一个节点，使得该路径
mincost = sys.maxint    ###最小的花费

count = 0  ### 计数器
t = 100  ## 初始温度
t_min = 50  ## 最小温度
while count < num:
    count += 1
  ### 构建一个邻域: 如果indexList中元素个数大于10个，则取样的个数为剩余元素个数的十分之一。否则为剩余元素个数对10的取余数
  leftItemNum = len(indexList)
#  print "leftItemNum:" ,leftItemNum
  nextnum = leftItemNum//10  
    if leftItemNum >= 10 
    else leftItemNum%10
    nextnodeList = sample(indexList,nextnum) ### 从剩余的节点中选出nextnum个节点
  
  if len(selectedList) == 0 :
      item = choice(nextnodeList)
      selectedList.append(item)
      indexList.remove(item)
      mincost = 0
      continue
  
  curnode = selectedList[len(selectedList) - 1]
  # print "nextnodeList:" ,nextnodeList
  nextnode, maxcost ,t = valSimulateAnnealSum(curnode,nextnodeList,t)   ### 对待选的序列路径求和
  
  ### 将返回的路径值添加到原来的路径值上，同时，在剩余的节点序列中，删除nextnode节点
  mincost += maxcost
  indexList.remove(nextnode)
  selectedList.append(nextnode) 

print "最合适的路径为：" ,selectedList 
print "路径节点个数：" ,len(selectedList)
print "最小花费为：" , mincost
print "尝试次数:", count

#### 画图 #####
#plt.figure(1)
x = []
y = []
for i in selectedList :
    x.append(list[i].x)
    y.append(list[i].y)
#plt.plot(x,y)
#plt.show()
print "x: ",x
print "y: " ,y


