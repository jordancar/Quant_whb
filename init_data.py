#coding:utf8
import tushare  as  ts  
import pandas as pd  
import  numpy as np 
import matplotlib.pyplot  as  plt  
import datetime ,time 
import pymysql 
'''
Use Tushare api to Test stock exchange  Strategy.
Author:Michael 11270907   beta
'''
today=datetime.date.today().strftime('%Y%m%d') 
stock_pool = ['603912.SH', '300666.SZ', '300618.SZ', '002049.SZ', '300672.SZ']
db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='stock', charset='utf8')
cursor = db.cursor()
print today
class Stock(object):
    def __init__(self,code,token='9479832d9c2b7719809d7a39f606172d37d27af2f1713f6814493dfc'): #init the specific stock , and tushare token 
        self.code=code
        self.token=token

    def fetch_code(self,start_date='20180101',end_date='20181127'):
        pro=ts.pro_api(self.token)
        
        df=pro.daily(ts_code=self.code,start_date=start_date,end_date=end_date)
        return df 
for code in stock_pool:
    st=Stock(code)
    data=st.fetch_code()
    print data.head(3)
    for i in range(len(data)):
        values=tuple(st.fetch_code().loc[i])
        print values
        sql="insert into stock_all ('state_dt','stock_code','open','close','high','low','vol','amount', \
            'pre_close','amt_change','pct_change','big_order_cntro','big_order_delt') \
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % values
        sql = sql.replace('nan','null').replace('None','null').replace('none','null') 
        print sql
        cursor.execute(sql)
