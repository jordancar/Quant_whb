#coding:utf8
import pymysql.cursors
import Deal
import Operator
from init_env import get_env
def filter_main(stock_new,state_dt,predict_dt,poz):
    # 建立数据库连接
    ##################################################
    # 建立数据库连接,设置tushare的token,定义一些初始化参数
    env=get_env()
    db,cursor,pro=env.db,env.cursor,env.pro
    ##################################################

    #先更新持股天数
    sql_update_hold_days = 'update my_stock_pool w set w.hold_days = w.hold_days + 1'
    cursor.execute(sql_update_hold_days)
    db.commit()

    #先卖出
    deal = Deal.Deal(state_dt)
    stock_pool_local = deal.stock_pool

    for stock in stock_pool_local:
        sql_predict = "select predict from model_ev_resu a where a.state_dt = '%s' and a.stock_code = '%s'"%(predict_dt,stock)
        cursor.execute(sql_predict)
        done_set_predict = cursor.fetchall()
        predict = 0
        if len(done_set_predict) > 0:
            predict = int(done_set_predict[0][0])
            print  "predict: %s,predictvalue: %d " % (stock ,predict)  
        ans = Operator.sell(stock,state_dt,predict)
        print "sell: %s" % stock  

    #后买入
    for stock_index in range(len(stock_new)):
        deal_buy = Deal.Deal(state_dt)
        # # 如果模型f1分值低于50则不买入
        # sql_f1_check = "select * from model_ev_resu a where a.stock_code = '%s' and a.state_dt < '%s' order by a.state_dt desc limit 1"%(stock_new[stock_index],state_dt)
        # cursor.execute(sql_f1_check)
        # done_check = cursor.fetchall()
        # db.commit()
        # if len(done_check) > 0:
        #     if float(done_check[0][4]) < 0.5:
        #         print('F1 Warning !!')
        #         continue
        # macd模型，如果预测值为1则买入
        # sql_macd_check="select * from model_macd_resu where stock_code= '%s' and state_dt= '%s' " % (stock_new[stock_index],state_dt)
        # cursor.execute(sql_macd_check)
        # done_check = cursor.fetchall()
        # print done_check
        # db.commit()
        # if len(done_check) > 0:
        #     if done_check[0][2] <> '1': # 不可买
        #         print(state_dt,': ',stock_new[stock_index],'macd forbidden !')
        #         continue
        ans = Operator.buy(stock_new[stock_index],state_dt,float(poz[stock_index])*deal_buy.cur_money_rest)
        print "stock_new[stock_index],state_dt,poz[stock_index]*deal_buy.cur_money_rest", stock_new[stock_index],state_dt,poz[stock_index]*deal_buy.cur_money_rest
        del deal_buy
 
    db.close()
