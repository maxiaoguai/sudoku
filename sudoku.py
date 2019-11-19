import numpy as np
import time
data =      "0 0 0 6 0 0 0 5 0 \
             8 0 4 0 0 0 6 0 0 \
             0 2 0 0 8 0 0 3 0 \
             0 0 0 7 0 3 0 0 4 \
             0 0 6 0 5 0 1 0 0 \
             3 0 0 1 0 8 0 0 0 \
             0 7 0 0 1 0 0 2 0 \
             0 0 2 0 0 0 3 0 1 \
             0 9 0 0 0 7 0 0 0 "
data=np.array(data.split(),dtype=int).reshape((9,9))

"""算法思路：
1.对于一个数独，每一个空格填入的候选值应该是确定的，首先计算每个空格可填入的候选值，并按照候选值的个数升序排列，
（首先选择确定性较大的空格填入）;
2.在填入候选值后，刷新数独矩阵，并重新计算空格位置的可选值;
3.当空格位置的候选值个数为0时，说明在前面某一步候选值填的有错，需要回溯，回溯错误上一步时，如果候选值个数为1，
说明错误还在前面，但需要将此处值重新置为0；
4.按照步骤3依次回溯，当回溯到候选值个数大于1时，（说明错误有可能是在此处发生），将指针指向此位置的下一个候选值填入，
在重新刷新记录插入位置和值的字典，并重复进行步骤1,2；
5.当记录步骤1的字典（空格位置及候选值）为空时，说明所有空格均已填完，则跳出所有循环
"""
def nine(data): #将数据划分成3*3的矩阵
    nine_data=np.zeros((3,3,3,3))
    for i in range(3):
        for j in range(3):
            nine_data[i,j]=data[i*3:(i*3)+3,j*3:(j*3)+3]
    return nine_data

def fill_value(data,nine_data): #输出每个空格中能够填的数字
    dict_data={} #建立一个空字典
    for i in range(9):
        for j in range(9):
            if data[i,j]==0:
                dict_data[str(i)+str(j)]=set(range(10))-set(data[i,:])-set(data[:,j])\
                -set(nine_data[i//3,j//3].flatten()) #通过减法找出每个空格可选填的数字
    dict_data=sorted(dict_data.items(),key=lambda x:len(x[1])) #输出结果按照可选填数字个数升序排序
    return dict_data

def insert_data(data):
    start_time=time.time() #开始时间
    insert_data=[] #建立空字典用来记录插入顺序
    while True:
        dict_data=fill_value(data,nine(data)) #生成每个空格中能够填的数字
        if len(dict_data) == 0: break #如果可选填的空格为0（表示所有空格以全部填完），则跳出while循环
        fisrt_values=dict_data[0] #取候选字典中第一个值（已排序）        
        key=fisrt_values[0]
        value=list(fisrt_values[1])
        insert_data.append((key,value)) #记录插入位置和插入值
        if len(value)!=0: #判断插入值是否为空
            data[int(key[0]),int(key[1])]=value[0]
        else: #（如果插入值为空，则说明在前面某一步选值出现问题，需要回溯）
            insert_data.pop() #将插入值为空的位置和值从记录字典中删除
            for i in range(len(insert_data)): #此循环的目的是往上回溯i步，不一定需要回溯len(insert_data)步
                recall=insert_data.pop() #取出出错位置的上一步
                if len(recall[1])==1: #如果出错位置的上一步可选值为1，说明可能出错的地方还在前面
                    data[int(recall[0][0]),int(recall[0][1])]=0 #将出错位置的上一步处的值置为0
                else:
                    data[int(recall[0][0]),int(recall[0][1])]=recall[1][1] #否则找到当初可能出错位置，在该位置处填入下一个候选值
                    insert_data.append((recall[0],recall[1][1:])) #重新记录填入位置和候选值
                    break #此处跳出的是上面的for循环，并非while循环
    end_time=time.time() #结束时间
    return data,end_time-start_time

insert_data(data)      