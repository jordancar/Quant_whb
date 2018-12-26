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
# df = pro.query('coinbar', exchange='huobi', symbol='btcusdt', freq='15min', start_date='20181217', end_date='20181225')
#linux
# df=pd.read_csv('/Users/wanghongbo8/fonts_whb/btc_5min.csv') #2018.9.1-today
#windows
df=pd.read_csv(r'd:\btc_5min.csv') #2018.9.1-today
df.columns=[u'symbol', u'date', u'open', u'high', u'low', u'close', u'vol']
df=df[(df.date>'2018-11-27')&(df.date<='2018-12-28')]
df['dt']=df.date.apply(lambda x: str(x)[0:10])
df=df.sort_values('date',ascending=True)
df=df.reset_index(drop=True)

# print df.head()

df['predict']=0
df['profit']=0        

ma_list = [('fast',4), ('mid',10), ('slow',20)]
for ma in ma_list:
    df['ma_'+str(ma[0])]=df.close.rolling(ma[1]).mean()
    df['shift_ma_'+str(ma[0])]=df.close.rolling(ma[1]).mean().shift(-1)

df.loc[(df.ma_fast<df.ma_slow)&(df.shift_ma_fast>=df.shift_ma_slow),'predict']=1 #买入
df.loc[(df.ma_fast>=df.ma_slow)&(df.shift_ma_fast<df.shift_ma_slow),'predict']=-1 #卖出
df['profit']=df.predict.shift(1) #真实买卖点错向后错15分钟
df.profit=df.profit.fillna(0)
df.profit=df.profit.astype(int)
print df[['date','profit','predict','close']].head(100)

idx= df[(df.profit==1)].index
y=df[(df.profit==1)].close.tolist()
idx_sold=df[(df.profit==-1)].index
y_sold=df[(df.profit==-1)].close.tolist()
# aaa=raw_input('wait')


origin_x=[x for x in range(len(df.close))]
origin_xlabel=[]
for x in range(len(df.close)):
    if x%2==0:
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
# plt.plot(df.close)
# plt.xticks(origin_x,(origin_xlabel),rotation=85)
# plt.plot(df.ma_fast)
# # plt.plot(df.ma_mid)
# plt.plot(df.ma_slow)
# # plt.savefig(r"D:\ma.png")
# plt.show()

def cal_profit(df):
    print df.dtypes
    df=df[(df.profit==1) | (df.profit==-1)] #取出所有买点和卖点
    df=df.sort_values('date',ascending=True) #按时间升序
    #取出最近的买点和卖点pair,忽略中间的买点日期
    poi=[] 
    pivot=1
    ind=0 #定义poi索引，用于计算上一次有效存入poi的买入价
    for  i in range(df.shape[0]):
        if df.profit.iloc[i]==pivot: #初始，寻找买点
            if pivot==-1 and df.close.iloc[i]<poi[ind-1][1]:
                if df.close.iloc[i]/poi[ind-1][1] -1 <-0.55: #如果亏损超过5% 止损 
                    poi.append([df.date.iloc[i],df.close.iloc[i],df.profit.iloc[i]]) 
                    ind+=1
                    pivot=(-pivot) #买卖点切换
                    continue #继续寻找卖点
                else:    
                    print "放弃在{}-{}亏损卖出".format(df.date.iloc[i],df.close.iloc[i])
                    continue #放弃本次卖点
            poi.append([df.date.iloc[i],df.close.iloc[i],df.profit.iloc[i]]) 
            ind+=1
            pivot=(-pivot) #买卖点切换
    for e in poi:
        print e
    profit_resu=[]
    profit=0
    while 1:
        if len(poi)>1:
            try:
                profit=poi[1][1]-poi[0][1]
                # print profit
                profit_resu.append([poi[0][0],poi[1][0],poi[0][1],poi[1][1],profit,poi[1][1]*0.002]) #收益和手续费
                poi.pop(0)
                poi.pop(0)
            except Exception as e :
                print e 
        else:
            break
    # for ele in profit_resu:
    #     print "dateBuy:{},dateSold:{},profit:{}".format(ele[0],ele[1],profit_resu)      
    return profit_resu
total_profit=0
total_spend=0
profit_detail=cal_profit(df)
for ele in profit_detail:
    print "dateBuy:{},price:{},  dateSold:{},price:{},profit:{},spend_ex:{}".format(ele[0],ele[2],ele[1],ele[3],ele[4],ele[5])
    total_profit+=ele[4]
    total_spend+=ele[5]

print "区间总收益:{},交易次数:{},手续费:{}$,纯收益:{}$".format(total_profit,len(profit_detail),total_spend,total_profit-total_spend)


    
    


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