import numpy as np
import pandas as pd
def data_std(price_diff,T):
#计算前T日均值和标准差
#输入参数T和待处理数据
    price_diff_mean = []
    price_diff_std = []
    for i in range(len(price_diff)):
        if(i<T):
            price_diff_mean.append(np.mean(price_diff[0:T]))
            price_diff_std.append(np.std(price_diff[0:T]))
        else:
            price_diff_mean.append(np.mean(price_diff[i-T:i]))
            price_diff_std.append(np.std(price_diff[i-T:i]))
    price_std=pd.DataFrame(price_diff)
    price_std['price_diff']=price_std['price_diff'].astype(float)
    #价差序列用前T日数据标准化
    for  i in range(len(price_diff)):
        price_std['price_diff'][i]=(float(price_std['price_diff'][i])-float(price_diff_mean[i]))/float(price_diff_std[i])
    return price_std