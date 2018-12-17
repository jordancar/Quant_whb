#coding:utf8
from add_log import logger #日志打印
from init_env import get_env
import datetime
import tushare as ts
import pandas as pd 
import pymysql
import stock_list
from para_set import back_test as bt 
import sys,time 
import numpy as np 
import functools
reload(sys)
sys.setdefaultencoding('utf8')
logger.info("into {} module ".format('init_stock_all'))
env=get_env()
db,cursor,pro=env.db,env.cursor,env.pro
# 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
start_dt = '20100106'
time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
end_dt = time_temp.strftime('%Y%m%d')
def time_used(bak):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args,**kwargs):
                start_tm=time.time()
                func(*args,**kwargs)
                end_tm=time.time()
                print "time used:{}s".format(end_tm-start_tm)
            return wrapper
        return decorator
    
@time_used(200)
def init_top_list(start_dt,end_dt):#龙虎榜
    date_list=pd.date_range(start_dt,end_dt,freq='D')
    time_control=1
    start_time=time.time() #调用api初始时间
    for day in date_list:
        #频率控制模块
        time_control+=1
        sleep_time=time.time()-start_time
        logger.info("sleep_time:{},start_time:{},api_times:{}".format(sleep_time,start_time,time_control))
        if time_control %80 ==0 and sleep_time<=60:
            time.sleep(60-sleep_time+3)
            start_time=time.time()
            time_control=1
            logger.info("sleeping...{}s".format(60-sleep_time+3))
        elif sleep_time>=60:
            time_control=1
            start_time=time.time() #初始化starttime
        #获取数据
        day=datetime.datetime.strftime(day,"%Y%m%d")
        df = pro.top_list(trade_date=day)
        insert_list=np.array(df).tolist()
        for resu in insert_list:
            resu[0]=datetime.datetime.strptime(resu[0],'%Y%m%d').strftime('%Y-%m-%d')
            try:
                sql="insert into top_list(trade_date, ts_code, name, close, pct_change,turnover_rate, amount, l_sell, l_buy, l_amount, \
                    net_amount, net_rate, amount_rate, float_values, reason) values ('%s','%s','%s','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%s')" \
                    % (resu[0],resu[1],resu[2],resu[3],resu[4],resu[5],resu[6],resu[7],resu[8],resu[9],resu[10],resu[11],resu[12],resu[13],resu[14])
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                pass
    return 'top_list  initialized.'

def stock_fmac(start_dt,end_dt):#各股票市值
    dt_list=pd.date_range(start_dt,end_dt).tolist()
    dt_list=[dt.strftime("%Y%m%d") for dt in dt_list]
    time_control=1
    start_time=time.time() #调用api初始时间
    seq=1
    for dt in dt_list:
        logger.debug("Seq[{}] of {}".format(seq,len(dt_list)))
        seq+=1 #计数
        #频率控制模块
        time_control+=1
        sleep_time=time.time()-start_time
        logger.info("sleep_time:{},start_time:{},api_times:{}".format(sleep_time,start_time,time_control))
        if time_control %80 ==0 and sleep_time<=60:
            time.sleep(60-sleep_time+3)
            start_time=time.time()
            time_control=1
            logger.info("sleeping...{}s".format(60-sleep_time+3))
        elif sleep_time>=60:
            time_control=1
            start_time=time.time() #初始化starttime
        df = pro.daily_basic(ts_code='', trade_date=dt, fields='trade_date,ts_code,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb, \
        ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv')
        df.fillna(0,inplace=True)
        df=df[['trade_date','ts_code','close','turnover_rate','turnover_rate_f','volume_ratio','pe','pe_ttm','pb', \
        'ps','ps_ttm','total_share','float_share','free_share','total_mv','circ_mv']]
        

        data=np.array(df).tolist()
        for resu in data:
            try:
                resu[0]=datetime.datetime.strptime(resu[0],"%Y%m%d").strftime("%Y-%m-%d")
                sql="insert into stock_fmac (trade_date,ts_code,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb, \
                ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv) values ('%s','%s','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f', '%.2f',\
                '%.2f','%.2f','%.2f','%.2f','%.2f','%.2f', '%.2f')" % (resu[0],resu[1],resu[2],resu[3],resu[4],resu[5],resu[6],resu[7],resu[8],resu[9],resu[10],resu[11],resu[12],resu[13],resu[14],resu[15])
                # logger.debug(sql)
                cursor.execute(sql)
                db.commit()
            except Exception  as e :
                logger.debug(e)    
    
def trade_cal(start_date='19990101',end_date=end_dt): #返回指定日期区间的交易日
    df_trade = pro.trade_cal(exchange_id='', is_open=1, start_date='19990101', end_date=end_dt)
    insert_list=np.array(df_trade).tolist()
    for r in insert_list:
        sql="insert into trade_day(exchange,cal_date,is_open) values('%s','%s','%i')" %(r[0],r[1],r[2])
        cursor.execute(sql)
        db.commit()
    logger.info('trade cal done.')
@time_used(b'timeuse')
def init_stock_index():
    index_pool=['000001.SH'] #初始化指数池子
    #直接获取指数行情 
    df_index=pro.index_daily(ts_code='000001.SH', start_date='20100101', end_date=end_dt)
    df_index['code']='sh'
    df=df_index[['trade_date','code','open', 'close','high', 'low','vol','amount','pct_chg']]
    sql_init='truncate stock_index;'
    cursor.execute(sql_init)
    c_len=df.shape[0]
    for j in range(c_len):
            resu0 = list(df.ix[c_len-1-j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
#             state_dt = (datetime.datetime.strptime(resu[0], "%Y%m%d")).strftime('%Y-%m-%d')
            # state_dt=resu[0]
            state_dt = (datetime.datetime.strptime(resu[0], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO stock_index(state_dt,stock_code,open,close,high,low,vol,amount,p_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f')" % (state_dt,str(resu[1]),float(resu[2]),float(resu[3]),float(resu[4]),float(resu[5]),float(resu[6]),float(resu[7]),float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print err
                continue
    logger.info("initialized {} index".format(index_pool[0]))


def init_stock_all_plus():
    start_dt='20181204'
    df_dim=stock_list.stock_all()  #获取上证股票维表
    stock_big_pool=list(df_dim.ts_code) #A 股票 3565 股票 list
    stock_pool=stock_big_pool
    start_time=time.time()
    total = len(stock_pool)
    time_control=1
    for i in range(len(stock_pool)):
        try:
            #频率控制模块
            time_control+=1
            sleep_time=time.time()-start_time
            logger.info("sleep_time:{},start_time:{},api_times:{}".format(sleep_time,start_time,time_control))
            if time_control %198 ==0 and sleep_time<=60:
                time.sleep(60-sleep_time+3)
                start_time=time.time()
                time_control=1
                logger.info("sleeping...{}s".format(60-sleep_time+3))
            elif sleep_time>=60:
                time_control=1
                start_time=time.time() #初始化starttime
            df=ts.pro_bar(pro_api=pro, ts_code=stock_pool[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            df_new=df.merge(df_dim,on='ts_code')
            df=df_new
            print('Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
        for j in range(c_len):
            resu0 = list(df.ix[c_len-1-j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO stock_all_plus(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change,name,area,industry) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f','%s','%s','%s')" \
                    % (state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3]),float(resu[4]),float(resu[9]),float(resu[10]),float(resu[6]),float(resu[7]),float(resu[8]),str(resu[12]),str(resu[13]),str(resu[14]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                # print err
                # print 'already exists!'
                continue

def init_stock_all(stock_pool):
    total = len(stock_pool)
    # 循环获取单个股票的日线行情
    for i in range(len(stock_pool)):
        try:
            # df = pro.daily(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)
            #使用前复权数据插入
            df=ts.pro_bar(pro_api=pro, ts_code=stock_pool[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            print('Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
        for j in range(c_len):
            resu0 = list(df.ix[c_len-1-j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO stock_all(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3]),float(resu[4]),float(resu[9]),float(resu[10]),float(resu[6]),float(resu[7]),float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                # print 'already exists!'
                continue
if __name__ == '__main__':

    # 建立数据库连接,剔除已入库的部分
    # 设定需要获取数据的股票池
    bt=bt()
    stock_pool=bt.stock_pool #从 paraset 获取
    logger.info(stock_pool)
    # stock_fmac(start_dt='20180601',end_dt=end_dt)
    # init_top_list(start_dt,end_dt)
    # trade_cal() #初始化交易日期
    # init_stock_index() # 初始化上证指数
    # init_stock_all_plus() #拉取全部3556支股票前复权数据到本地
    init_stock_all(stock_pool)#初始化stock_all用于量化分析
    cursor.close()
    db.close()
    print('All Finished!')

