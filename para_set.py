#coding:utf8
'''
This module used for back_test parament settings 
author:michael 2018.12.05
'''
from init_env import get_env
# stock_pool_9=['600729.SH', '600733.SH', '600740.SH', '600754.SH', '600755.SH', '600760.SH', '600783.SH', '600790.SH', '600825.SH', '600874.SH','000576.SZ', '000582.SZ', '000592.SZ', '000603.SZ',  '000622.SZ', '000638.SZ', '000651.SZ', '000666.SZ', '000722.SZ']
env=get_env()
db,cursor,pro=env.db,env.cursor,env.pro
class back_test(object):
    def __init__(self,para_window=90,start_time='2018-08-01',end_time='2018-12-01',hold_days=7,strategy='',torlence_profit=0.05,torlence_lost=0.10,operate_days=5,operate_tm=''):
        self.para_window=para_window
        self.start_time=start_time
        self.end_time=end_time
        self.hold_days=hold_days
        self.strategy=strategy
        self.torlence_lost=torlence_lost
        self.torlence_profit=torlence_profit
        self.operate_days=operate_days
        self.operate_tm=operate_tm
        # self.stock_pool=self.get_stock_list('2018-06-01',15)
        # self.stock_pool=['601857.SH','601988.SH','601628.SH','601166.SH','600000.SH']
    def get_stock_list(self,dt,n=1):
        stock_list=[]
        sql="select stock_code from stock_all_plus a where state_dt='%s' and   \
        %d=(select count(*) top_1 from  stock_all_plus b where  \
         state_dt='%s' and a.industry=b.industry and a.pct_change>=b.pct_change) and pct_change>-8 and pct_change<-5;" % (dt,n,dt)
        cursor.execute(sql)
        db.commit()
        for x in cursor.fetchall():
            stock_list.append(x[0])
        return stock_list

#########look over all stock profit
# import matplotlib.pyplot as plt  
# stock_pool=back_test().stock_pool 
# def draw_stock_curve(code):
#     sql_stock = "select * from stock_all a where a.stock_code = '%s' and a.state_dt >= '%s' and a.state_dt <= '%s' order by state_dt asc"%(code,'2016-01-01','2018-12-07')
#     cursor.execute(sql_stock)
#     stock_value = cursor.fetchall()
#     x_t = [x[0] for x in stock_value]
#     y_v=[x[3] / stock_value[0][3] for x in stock_value]
#     return x_t,y_v
# profit_list={}
# for code in stock_pool:
#     x_t,y_v=draw_stock_curve(code)
# #     profit_list[code+'_x']=x_t
# #     profit_list[code+'_y']=y_v

# # for  i,j in profit_list.iteritems():
# #     print "i:{},j:{}".format(i,len(j))
#     x_tf=[x for x in range(len(x_t))]
#     x_lb=[]
#     for i in x_tf:
#         if i%7==0:
#             x_lb.append(x_t[i])
#         else:
#             x_lb.append("")    
#     print x_t[:10],y_v[0:10]
#     if y_v[-1]<=1.2:
#         plt.plot(x_t, y_v,label=code)
# # import pandas as pd 
# # # print profit_list[0:10]
# # df=pd.DataFrame(profit_list)
# # print df.head()
# plt.legend()
# plt.xticks(x_tf,(x_lb),rotation=85)
# plt.show()