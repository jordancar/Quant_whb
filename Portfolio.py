#coding:utf8
import numpy as np
import datetime
import pymysql
import copy
import tushare as ts
import pandas as pd 
from init_env import get_env

# 返回的resu中 特征值按由小到大排列，对应的是其特征向量
def get_portfolio(stock_list,state_dt,para_window):
    print "stock_list,state_dt,para_window: ",stock_list,state_dt,para_window
    # 建数据库连接，设置Tushare的token
    ##################################################
    # 建立数据库连接,设置tushare的token,定义一些初始化参数
    env=get_env()
    db,cursor,pro=env.db,env.cursor,env.pro
    ##################################################

    portfilio = stock_list

    # 建评估时间序列, para_window参数代表回测窗口长度
    model_test_date_start = (datetime.datetime.strptime(state_dt, '%Y-%m-%d') - datetime.timedelta(days=para_window)).strftime(
        '%Y-%m-%d')
    model_test_date_end = (datetime.datetime.strptime(state_dt, "%Y-%m-%d")).strftime('%Y-%m-%d')
    # df = pro.trade_cal(exchange_id='', is_open=1, start_date=model_test_date_start, end_date=model_test_date_end) #此处切换为本地获取，防止回测日期天数过多导致调用接口崩溃 2018.12.13 12:06
    # print df 
    sql_trade="select * from trade_day where cal_date>='%s' and cal_date<='%s'" % (model_test_date_start,model_test_date_end)
    cursor.execute(sql_trade)
    db.commit()
    df=pd.DataFrame(list(cursor.fetchall())) 
    print (df)
    date_temp = list(df.iloc[:, 1])
    
    model_test_date_seq = [(datetime.datetime.strptime(x, "%Y-%m-%d")).strftime('%Y-%m-%d') for x in date_temp]

    list_return = []
    for i in range(len(model_test_date_seq)-4):
        ti = model_test_date_seq[i]
        ri = []
        for j in range(len(portfilio)):
            sql_select = "select * from stock_all_plus a where a.stock_code = '%s' and a.state_dt >= '%s' and a.state_dt <= '%s' order by state_dt asc" % (portfilio[j], model_test_date_seq[i], model_test_date_seq[i + 4])
            cursor.execute(sql_select)
            done_set = cursor.fetchall()
            db.commit()
            temp = [x[3] for x in done_set]
            base_price = 0.00
            after_mean_price = 0.00
            if len(temp) <= 1:
                r = 0.00
            else:
                base_price = temp[0]
                after_mean_price = np.array(temp[1:]).mean()
                r = (float(after_mean_price/base_price)-1.00)*100.00
            ri.append(r)
            del done_set
            del temp
            del base_price
            del after_mean_price
        list_return.append(ri)

    # 求协方差矩阵
    cov = np.cov(np.array(list_return).T)
    # 求特征值和其对应的特征向量
    ans = np.linalg.eig(cov)
    # 排序，特征向量中负数置0，非负数归一
    ans_index = copy.copy(ans[0])
    ans_index.sort()
    resu = []
    # print ans 
    for k in range(len(ans_index)):
        con_temp = []
        con_temp.append(ans_index[k])
        content_temp1 = ans[1][np.argwhere(ans[0] == ans_index[k])[0][0]]
        content_temp2 = []
        content_sum = np.array([x for x in content_temp1 if x >= 0.00]).sum()
        for m in range(len(content_temp1)):
            if content_temp1[m] >= 0 and content_sum > 0:
                content_temp2.append(content_temp1[m]/content_sum)
            else:
                content_temp2.append(0.00)
        con_temp.append(content_temp2)
        # 计算夏普率
        sharp_temp = np.array(copy.copy(list_return)) * content_temp2
        sharp_exp = sharp_temp.mean()
        sharp_base = 0.04
        sharp_std = np.std(sharp_temp)
        if sharp_std == 0.00:
            sharp = 0.00
        else:
            sharp = (sharp_exp - sharp_base) / sharp_std

        con_temp.append(sharp)
        resu.append(con_temp)

    return resu

if __name__ == '__main__':
    # pf = ['603912.SH', '300666.SZ', '300618.SZ', '002049.SZ', '300672.SZ']
    pf=['601398.SH','601857.SH','601288.SH','601988.SH','601318.SH','600036.SH','600028.SH','601628.SH','601088.SH']
    pf=['603156.SH', '603180.SH', '603196.SH', '603389.SH', '603630.SH', '603693.SH', '603711.SH', '603776.SH', '603787.SH', '603789.SH', '603799.SH', '603933.SH', \
        '300285.SZ', '300324.SZ', '300343.SZ', '300409.SZ', '300441.SZ', '300674.SZ', '300750.SZ', '300760.SZ', '600004.SH', '600009.SH']

    ans = get_portfolio(pf,'2016-11-06',90)
    print "eigz num:",len(ans)
    print('**************  Market Trend  ****************')
    print('Risk : ' + str(round(ans[0][0], 2)))
    print('Sharp ratio : ' + str(round(ans[0][2], 2)))

    for i in range(len(pf)):
        print('----------------------------------------------')
        print('Stock_code : ' + str(pf[i]) + '  Position : ' + str(round(ans[0][1][i] * 100, 2)) + '%')
    print('----------------------------------------------')

    print('**************  Best Return  *****************')
    print('Risk : ' + str(round(ans[1][0], 2)))
    print('Sharp ratio : ' + str(round(ans[1][2], 2)))
    for j in range(len(pf)):
        print('----------------------------------------------')
        print('Stock_code : ' + str(pf[j]) + '  Position : ' + str(
            round(ans[1][1][j] * 100, 2)) + '%')
    print('----------------------------------------------')
