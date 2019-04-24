import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import judge_point
import data_std

#风险控制参数：每个阶段亏损达到percentage强制平仓
percentage=0.3
#读取数据
data_cu = pd.read_csv('cu.csv')[['Date (GMT)','Last']]
data_zn = pd.read_csv('zn.csv')['Last']
stocks_pair = ['Data','cu', 'zn']
# 按行拼接收盘价
data= pd.concat([data_cu, data_zn], axis=1)
#绘制加个变化曲线和价差图
data.columns = stocks_pair
plt.figure(1)
data.plot(figsize= (8,6))
plt.title('Price for Cu and Zn')
price_diff= pd.concat([data['Data'], data['cu']-data['zn']], axis=1)
price_diff.columns=['Date','price_diff']
plt.figure(2)
price_diff.plot(figsize=(8,6))
plt.title('Price-Diff')

##数据的标准化处理
T=100#前T日数据对数据做标准化
price_std=data_std.data_std(price_diff,T)


#生成交易信号序列
sell_point=np.zeros(len(price_diff))#平仓信号初始化
sign_point=np.zeros(len(price_diff))#交易信号初始化
record_sign=np.zeros(len(price_diff))#判断每个时刻是否需要记录资金信号
hold_point=0 #取-1，0，1。记录目前持仓的做多做空状态
price_std_list=list(price_std['price_diff'])
for i in range(len(price_diff)):
    if(i<5):
        sign_point[i]=0
    else:
        sign_point[i]=judge_point.judge_point(price_std_list[i-5:i],0.03)#用前5日数据判断时间t的交易信号
        if(hold_point>=1 and price_std_list[i]<=0):
            hold_point=0
            sell_point[i]=1#平仓节点的设定
        if(hold_point<=-1and price_std_list[i]>=0):
            hold_point=0
            sell_point[i]=-1#平仓节点的设定
        if(sign_point[i]>=1):
            if(sign_point[i]>hold_point):#当前时刻信号大于之前阶段的信号，记录信号点，否则抹去
                if(hold_point==0):
                    record_sign[i]=1
                hold_point=sign_point[i]
            else:
                sign_point[i]=0
        elif(sign_point[i]<=-1):
            if(sign_point[i]<hold_point):#当前时刻信号大于之前阶段的信号，记录信号点，否则抹去
                if(hold_point==0):
                    record_sign[i]=-1
                hold_point=sign_point[i]
            else:
                sign_point[i]=0

##回测过程，模拟持仓
#注意根据买入卖出信号实现补仓操作
stock_cu=0#cu的持仓
stock_zn=0#zn的持仓
money=0#初始资金
record_money=-1e10;
asset=np.zeros(len(price_diff))#收益数组初始化
#根据设定的交易信号进行回测，模拟持仓
for i in range(len(price_diff)):
    if sign_point[i]>=1:
        stock_cu=stock_cu-100
        stock_zn=stock_zn+100
        money=money+data['cu'][i]*100-data['zn'][i]*100
    elif sign_point[i]<=-1:
        stock_cu=stock_cu+100
        stock_zn=stock_zn-100
        money = money - data['cu'][i] * 100 + data['zn'][i] * 100
    if(np.abs(sell_point[i])==1):
        money=money+stock_cu*data['cu'][i]+stock_zn*data['zn'][i]
        stock_cu=0
        stock_zn=0
    asset[i]=money+stock_zn*data['zn'][i]+stock_cu*data['cu'][i]
    if(record_sign[i]!=0):
        record_money=asset[i]
    if(asset[i]<record_money*(1-percentage)):
        money=asset[i]
        stock_cu=0
        stock_zn=0
        record_money=-1e10
        if(hold_point==-1):
            sell_point[i]=-1
        elif(hold_point==1):
            sell_point[i]=1

##提取信号点，用作绘图
duo_point_collect=[] #做多节点收集
duo_point_collect_price=[]
kong_point_collect=[]#做空节点收集
kong_point_collect_price=[]
sell_point_collect=[] #平仓点收集
sell_point_collect_price=[]
for i in range(len(price_diff)):
    if(np.abs(sell_point[i])==1):
        sell_point_collect.append(i)
        sell_point_collect_price.append(price_std['price_diff'][i])
    if(sign_point[i]>=1):
        duo_point_collect.append(i)
        duo_point_collect_price.append(price_std['price_diff'][i])
    elif(sign_point[i]<=-1):
        kong_point_collect.append(i)
        kong_point_collect_price.append(price_std['price_diff'][i])

##绘制标准化价差变化曲线和交易点标注
plt.figure(3)
price_std.plot(figsize=(8,6))
plt.plot(duo_point_collect,list(duo_point_collect_price),'r*',kong_point_collect,list(kong_point_collect_price),'g*',sell_point_collect,list(sell_point_collect_price),'k*')
plt.title('Standard Price Diff')
plt.show()

##绘制盈利曲线
plt.figure(4)
plt.plot(range(len(price_diff)),asset)
plt.title('PROFIT-LINE')
plt.show()