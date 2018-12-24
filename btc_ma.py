#coding:utf8 
import tushare as ts
import pymysql
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
class get_env(object):
    def __init__(self):
        self.db=pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='stock', charset='utf8')
        self.cursor=self.db.cursor()
        ts.set_token('23b817c8b6e2b772f37ad6f5628ad348a0aefed07ed9b07ecc75976d')
        self.pro = ts.pro_api()
env=get_env()
pro=env.pro 
df = pro.query('coinbar', exchange='huobi', symbol='btcusdt', freq='15min', start_date='20181001', end_date='20181223')
df['dt']=df.date.apply(lambda x: str(x)[0:10])
df=df.sort_values('date',ascending=True)
df=df.reset_index(drop=True)

# print df.head()

        

ma_list = [5, 10, 30]
for ma in ma_list:
    df['ma_'+str(ma)]=df.close.rolling(ma).mean()
    df['shift_ma_'+str(ma)]=df.close.rolling(ma).mean().shift(-1)
idx= df[(df.ma_5<=df.ma_30)&(df.shift_ma_5>df.shift_ma_30)].index
y=df[(df.ma_5<df.ma_30)&(df.shift_ma_5>=df.shift_ma_30)].ma_5.tolist()
idx_sold=df[(df.ma_5>=df.ma_30)&(df.shift_ma_5<df.shift_ma_30)].index
y_sold=df[(df.ma_5>=df.ma_30)&(df.shift_ma_5<df.shift_ma_30)].ma_5.tolist()

origin_x=[x for x in range(len(df.close))]
origin_xlabel=[]
for x in range(len(df.close)):
    if x%7==0:
        origin_xlabel.append(df.date.iloc[x])
    else:
        origin_xlabel.append("")


plt.figure(figsize=(36, 12.5))
plt.scatter(idx,y,color='r')
plt.scatter(idx_sold,y_sold,color='c')
cd=0
print (np.random.randint(cd+10,180),np.random.randint(cd+10,150))
for xy in zip(idx,y):
    cd+=1
    plt.annotate("(buy: %s)"%xy[1],xy=xy,xytext=(0,-50*(-1)**cd),textcoords='offset points',arrowprops=dict(alpha=0.8,facecolor='red',edgecolor='r',connectionstyle="arc3,rad=0.2",arrowstyle="->"))
for xy in zip(idx_sold,y_sold):
    cd+=1
    plt.annotate("(sold: %s)"%xy[1],xy=xy,xytext=(50,60*(-1)**cd),textcoords='offset points',arrowprops=dict(alpha=0.8,facecolor='c',edgecolor='c',connectionstyle="arc3,rad=0.3",arrowstyle="->"))
plt.plot(df.close)
plt.xticks(origin_x,(origin_xlabel),rotation=85)
plt.plot(df.ma_5)
plt.plot(df.ma_10)
plt.plot(df.ma_30)

plt.savefig(r"D:\ma.png")
plt.show()



# print df
# openList= df[df.date.isin(df.groupby('dt').date.min())][['dt','open']].sort_values('dt',ascending=True)['open'].tolist()


# df_g=pd.DataFrame()

# df_g['maxHigh']=df.groupby('dt')['high'].max()
# df_g['minLow']=df.groupby('dt')['low'].min()
# df_g=df_g.reset_index()
# df_g['open']=openList
# df_g['minGap']=(df_g.minLow/df_g.open-1)*100
# df_g['maxGap']=(df_g.maxHigh/df_g.open-1)*100
# df_g.sort_values('minGap')