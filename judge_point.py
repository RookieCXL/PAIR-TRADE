import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
def judge_point(std_price,scale):
#逐点判断函数，将当前节点t前5个交易日进行比较，如果前五个交易日的标准化数据的最大值偏离3，
#并且目前标准化数据t品偏离五日内的极值点scale以上，那么对两只股票分别进行做多做空300手
#策略重点关注标准化数据冲高回落作为买入卖出点
#参数设置：五日内极值点（或多日），偏离程度
#初始化信号0
    sign_point=0
    if(std_price[-1]>=1):
        max_num=np.max(std_price)
        if(std_price[-1]<(1-scale)*max_num):
            if(max_num>=4):
                sign_point=4
            elif(max_num>=3):
                sign_point = 3
            elif (max_num >= 2):
                sign_point = 2
            elif (max_num >= 1):
                sign_point = 1
    elif((std_price[-1])<=-1):
        min_num = np.min(std_price)
        if (std_price[-1] >(1-scale) * min_num):
            if (min_num <= -4):
                sign_point = -4
            elif (min_num <= -3):
                sign_point = -3
            elif (min_num <= -2):
                sign_point = -2
            elif (min_num <= -1):
                sign_point = -1
    return sign_point