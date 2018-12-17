#coding:utf8
'''
This module used for back_test parament settings 
author:michael 2018.12.05
'''
from init_env import get_env
stock_pool=['000002.SZ', '000007.SZ', '000040.SZ', '000056.SZ', '000063.SZ', '000069.SZ', '000333.SZ', '000401.SZ', '000507.SZ',  \
     '000576.SZ', '000582.SZ', '000592.SZ', '000603.SZ', '000610.SZ', '000622.SZ', '000638.SZ', '000651.SZ', '000666.SZ', '000722.SZ',  \
     '000725.SZ', '000735.SZ', '000768.SZ', '000778.SZ', '000786.SZ', '000793.SZ', '000830.SZ', '000856.SZ', '000858.SZ', '000876.SZ', \
      '000887.SZ', '000895.SZ', '000913.SZ', '000917.SZ', '000936.SZ', '000975.SZ', '000977.SZ', '000979.SZ', '000996.SZ','002007.SZ',  \
      '002011.SZ', '002024.SZ', '002027.SZ', '002075.SZ', '002086.SZ', '002094.SZ', '002103.SZ', '002108.SZ', '002110.SZ', '002210.SZ',  \
      '002221.SZ', '002236.SZ', '002264.SZ', '002271.SZ', '002285.SZ', '002288.SZ', '002320.SZ', '002337.SZ', '002344.SZ', '002353.SZ',  \
      '002366.SZ', '002367.SZ', '002371.SZ', '002400.SZ', '002415.SZ', '002416.SZ', '002440.SZ', '002441.SZ', '002450.SZ', '002451.SZ',  \
      '002466.SZ', '002472.SZ', '002504.SZ', '002549.SZ', '002568.SZ', '002575.SZ', '002594.SZ','002607.SZ', '002611.SZ', '002679.SZ',  \
      '002696.SZ', '002708.SZ', '002711.SZ', '002714.SZ', '002719.SZ', '002761.SZ', '002856.SZ', '002903.SZ', '300003.SZ', '300017.SZ',  \
      '300059.SZ', '300084.SZ', '300104.SZ', '300122.SZ', '300144.SZ', '300146.SZ', '300159.SZ', '300173.SZ', '300181.SZ', '300221.SZ',  \
      '300285.SZ', '300324.SZ', '300343.SZ', '300409.SZ', '300441.SZ', '300674.SZ', '300750.SZ', '300760.SZ', '600004.SH', '600009.SH',  \
      '600011.SH', '600019.SH', '600020.SH', '600026.SH', '600027.SH','600028.SH', '600029.SH', '600030.SH', '600031.SH', '600036.SH',  \
      '600048.SH', '600050.SH', '600053.SH', '600056.SH', '600107.SH', '600122.SH', '600125.SH', '600128.SH', '600132.SH', '600150.SH',  \
      '600165.SH', '600171.SH', '600176.SH', '600187.SH', '600196.SH', '600210.SH', '600219.SH', '600226.SH', '600235.SH', '600271.SH', \
       '600276.SH', '600283.SH', '600309.SH', '600339.SH', '600340.SH', '600352.SH', '600362.SH', '600365.SH', '600368.SH', '600387.SH',  \
       '600438.SH', '600487.SH', '600490.SH','600506.SH', '600507.SH', '600516.SH', '600518.SH', '600519.SH', '600538.SH', '600547.SH',  \
       '600552.SH', '600585.SH', '600598.SH', '600600.SH', '600604.SH', '600624.SH', '600635.SH', '600662.SH', '600689.SH', '600695.SH',  \
       '600729.SH', '600733.SH', '600740.SH', '600754.SH', '600755.SH', '600760.SH', '600783.SH', '600790.SH', '600825.SH', '600874.SH',  \
       '600884.SH', '600887.SH', '600895.SH', '600900.SH', '600903.SH', '601006.SH', '601011.SH', '601012.SH', '601088.SH', '601111.SH',  \
       '601118.SH','601155.SH', '601166.SH', '601186.SH', '601225.SH', '601233.SH', '601318.SH', '601319.SH', '601600.SH', '601668.SH',  \
       '601766.SH', '601828.SH', '601857.SH', '601888.SH', '601899.SH', '601933.SH', '601989.SH', '603032.SH', '603069.SH', '603101.SH', \
        '603156.SH', '603180.SH', '603196.SH', '603389.SH', '603630.SH', '603693.SH', '603711.SH', '603776.SH', '603787.SH', '603789.SH', '603799.SH', '603933.SH']
stock_pool_9=['601398.SH','601857.SH','601288.SH','601988.SH','601318.SH','600036.SH','600028.SH','601628.SH','601088.SH']
# stock_pool_9=['600729.SH', '600733.SH', '600740.SH', '600754.SH', '600755.SH', '600760.SH', '600783.SH', '600790.SH', '600825.SH', '600874.SH','000576.SZ', '000582.SZ', '000592.SZ', '000603.SZ',  '000622.SZ', '000638.SZ', '000651.SZ', '000666.SZ', '000722.SZ']
env=get_env()
db,cursor,pro=env.db,env.cursor,env.pro
class back_test(object):
    def __init__(self,para_window=90,start_time='2018-01-01',end_time='2018-12-01',hold_days=30,strategy='',torlence_profit=0.05,torlence_lost=0.10,operate_days=5,operate_tm=''):
        self.para_window=para_window
        self.start_time=start_time
        self.end_time=end_time
        self.hold_days=hold_days
        self.strategy=strategy
        self.torlence_lost=torlence_lost
        self.torlence_profit=torlence_profit
        self.operate_days=operate_days
        self.operate_tm=operate_tm
        self.stock_pool=self.get_stock_list('2018-06-01',15)
    def get_stock_list(self,dt,n):
        stock_list=[]
        sql="select ts_code from stock_fmac where trade_date='%s' order by circ_mv desc limit %d;" % (dt,n)
        cursor.execute(sql)
        db.commit()
        for x in cursor.fetchall():
            stock_list.append(x[0])
        return stock_list
import matplotlib.pyplot as plt  
stock_pool=back_test().stock_pool 
def draw_stock_curve(code):
    sql_stock = "select * from stock_all a where a.stock_code = '%s' and a.state_dt >= '%s' and a.state_dt <= '%s' order by state_dt asc"%(code,'2016-01-01','2018-12-07')
    cursor.execute(sql_stock)
    stock_value = cursor.fetchall()
    x_t = [x[0] for x in stock_value]
    y_v=[x[3] / stock_value[0][3] for x in stock_value]
    return x_t,y_v
profit_list=[]
for code in stock_pool:
    x_t,y_v=draw_stock_curve(code)
    profit_list.append({code:x_t})
    profit_list.append({code:y_v})

    # x_tf=[x for x in range(len(x_t))]
    # x_lb=[]
    # for i in x_tf:
    #     if i%7==0:
    #         x_lb.append(x_t[i])
    #     else:
    #         x_lb.append("")    
    # print x_t[:10],y_v[0:10]
    # plt.plot(x_t, y_v,label=code)
import pandas as pd 
print profit_list[0:3]
df=pd.DataFrame(profit_list)
print df.head()
# plt.legend()
# plt.xticks(x_tf,(x_lb),rotation=85)
# plt.show()