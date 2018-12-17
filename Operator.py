#coding:utf8
import pymysql.cursors
import Deal
from para_set import back_test
from init_env import get_env
bt=back_test() #初始化回测参数

def buy(stock_code,opdate,buy_money):
    ##################################################
    # 建立数据库连接,设置tushare的token,定义一些初始化参数
    env=get_env()
    db,cursor,pro=env.db,env.cursor,env.pro
    ##################################################
    deal_buy = Deal.Deal(opdate)
    print "deal_buy info:deal_buy.rest:%s,deal_buy.cur_capital:%s" %(str(deal_buy.cur_money_rest),str(deal_buy.cur_capital))
    print 'buy_money: ',buy_money
    #后买入
    if deal_buy.cur_money_rest+1 >= buy_money:
        print "deal_buy.cur_money_rest+1  : ",deal_buy.cur_money_rest+1 ,   "    buy_money: ",buy_money
        sql_buy = "select * from stock_info a where a.state_dt = '%s' and a.stock_code = '%s'" % (opdate, stock_code)
        cursor.execute(sql_buy)
        done_set_buy = cursor.fetchall()
        print done_set_buy,'donesetbuy'
        if len(done_set_buy) == 0:
            return -1
        #剔除涨跌停因素
        if  done_set_buy[0][10]>9.9:
            print "涨停无法买入:%s" % str(done_set_buy)
            return -1 
        buy_price = float(done_set_buy[0][3])
        print "buy_price",buy_price
        if buy_price >= 195:
            return 0
        vol, rest = divmod(min(deal_buy.cur_money_rest, buy_money), buy_price * 100)
        print "vol, rest:",vol,rest
        vol = vol * 100
        if vol == 0:
            return 0
        new_capital = deal_buy.cur_capital - vol * buy_price * 0.0005
        new_money_lock = deal_buy.cur_money_lock + vol * buy_price
        new_money_rest = deal_buy.cur_money_rest - vol * buy_price * 1.0005
        sql_buy_update2 = "insert into my_capital(capital,money_lock,money_rest,deal_action,stock_code,stock_vol,state_dt,deal_price)VALUES ('%.2f', '%.2f', '%.2f','%s','%s','%i','%s','%.2f')" % (new_capital, new_money_lock,new_money_rest, 'buy', stock_code, vol, opdate, buy_price)
        print "sql_buy_update2: ",sql_buy_update2
        cursor.execute(sql_buy_update2)
        db.commit()
        if stock_code in deal_buy.stock_all:
            new_buy_price = (deal_buy.stock_map1[stock_code] * deal_buy.stock_map2[stock_code] + vol * buy_price) / (deal_buy.stock_map2[stock_code] + vol)
            new_vol = deal_buy.stock_map2[stock_code] + vol
            sql_buy_update3 = "update my_stock_pool w set w.buy_price = (select '%.2f' from dual) where w.stock_code = '%s'" % (new_buy_price, stock_code)
            sql_buy_update3b = "update my_stock_pool w set w.hold_vol = (select '%i' from dual) where w.stock_code = '%s'" % (new_vol, stock_code)
            sql_buy_update3c = "update my_stock_pool w set w.hold_days = (select '%i' from dual) where w.stock_code = '%s'" % (1, stock_code)
            cursor.execute(sql_buy_update3)
            cursor.execute(sql_buy_update3b)
            cursor.execute(sql_buy_update3c)
            db.commit()
        else:
            sql_buy_update3 = "insert into my_stock_pool(stock_code,buy_price,hold_vol,hold_days) VALUES ('%s','%.2f','%i','%i')" % (stock_code, buy_price, vol, int(1))
            cursor.execute(sql_buy_update3)
            db.commit()
        db.close()
        return 1
    db.close()
    return 0

def sell(stock_code,opdate,predict):
    ##################################################
    # 建立数据库连接,设置tushare的token,定义一些初始化参数
    env=get_env()
    db,cursor,pro=env.db,env.cursor,env.pro
    ##################################################
    deal = Deal.Deal(opdate)
    init_price = deal.stock_map1[stock_code]
    hold_vol = deal.stock_map2[stock_code]
    hold_days = deal.stock_map3[stock_code]
    sql_sell_select = "select * from stock_info a where a.state_dt = '%s' and a.stock_code = '%s'" % (opdate, stock_code)
    cursor.execute(sql_sell_select)
    done_set_sell_select = cursor.fetchall()
    if len(done_set_sell_select) == 0:
        return -1
    sell_price = float(done_set_sell_select[0][3])
    #跌停无法卖出
    if done_set_sell_select[0][10]<-9.9:
            print "跌停无法卖出:%s" % str(done_set_sell_select)
            return -1 
    if sell_price > init_price*(1+bt.torlence_profit) and hold_vol > 0:
        new_money_lock = deal.cur_money_lock - sell_price*hold_vol
        if new_money_lock<0:
            print "deal.cur_money_lock:%f,new_money_lock:%f,sell_price:%f,hold_vol:%d" %(deal.cur_money_lock,new_money_lock,sell_price,hold_vol)
            x=raw_input('profit error....')
        new_money_rest = deal.cur_money_rest + sell_price*hold_vol
        new_capital = deal.cur_capital + (sell_price-init_price)*hold_vol
        new_profit = (sell_price-init_price)*hold_vol
        new_profit_rate = sell_price/init_price
        sql_sell_insert = "insert into my_capital(capital,money_lock,money_rest,deal_action,stock_code,stock_vol,profit,profit_rate,bz,state_dt,deal_price)values('%.2f','%.2f','%.2f','%s','%s','%.2f','%.2f','%.2f','%s','%s','%.2f')" %(new_capital,new_money_lock,new_money_rest,'SELL',stock_code,hold_vol,new_profit,new_profit_rate,'GOODSELL',opdate,sell_price)
        cursor.execute(sql_sell_insert)
        db.commit()
        sql_sell_update = "delete from my_stock_pool where stock_code = '%s'" % (stock_code)
        cursor.execute(sql_sell_update)
        db.commit()
        db.close()
        return 1

    elif sell_price < init_price*(1-bt.torlence_lost) and hold_vol > 0:
        new_money_lock = deal.cur_money_lock - sell_price*hold_vol
        if new_money_lock<0:
            print "deal.cur_money_lock:%f,new_money_lock:%f,sell_price:%f,hold_vol:%d" %(deal.cur_money_lock,new_money_lock,sell_price,hold_vol)
            x=raw_input('lost error....')
        new_money_rest = deal.cur_money_rest + sell_price*hold_vol
        new_capital = deal.cur_capital + (sell_price-init_price)*hold_vol
        new_profit = (sell_price-init_price)*hold_vol
        new_profit_rate = sell_price/init_price
        sql_sell_insert2 = "insert into my_capital(capital,money_lock,money_rest,deal_action,stock_code,stock_vol,profit,profit_rate,bz,state_dt,deal_price)values('%.2f','%.2f','%.2f','%s','%s','%.2f','%.2f','%.2f','%s','%s','%.2f')" %(new_capital,new_money_lock,new_money_rest,'SELL',stock_code,hold_vol,new_profit,new_profit_rate,'BADSELL',opdate,sell_price)
        cursor.execute(sql_sell_insert2)
        db.commit()
        sql_sell_update2 = "delete from my_stock_pool where stock_code = '%s'" % (stock_code)
        cursor.execute(sql_sell_update2)
        db.commit()
        # sql_ban_insert = "insert into ban_list(stock_code) values ('%s')" %(stock_code)
        # cursor.execute(sql_ban_insert)
        # db.commit()
        db.close()
        return 1

    elif hold_days >= bt.hold_days and hold_vol > 0:
        new_money_lock = deal.cur_money_lock - sell_price * hold_vol
        if new_money_lock<0:
            print "deal.cur_money_lock:%f,new_money_lock:%f,sell_price:%f,hold_vol:%d" %(deal.cur_money_lock,new_money_lock,sell_price,hold_vol)
            x=raw_input('hold days  error....')
        new_money_rest = deal.cur_money_rest + sell_price * hold_vol
        new_capital = deal.cur_capital + (sell_price - init_price) * hold_vol
        new_profit = (sell_price - init_price) * hold_vol
        new_profit_rate = sell_price / init_price
        sql_sell_insert3 = "insert into my_capital(capital,money_lock,money_rest,deal_action,stock_code,stock_vol,profit,profit_rate,bz,state_dt,deal_price)values('%.2f','%.2f','%.2f','%s','%s','%.2f','%.2f','%.2f','%s','%s','%.2f')" % (new_capital, new_money_lock, new_money_rest, 'OVERTIME', stock_code, hold_vol, new_profit, new_profit_rate,'OVERTIMESELL', opdate,sell_price)
        cursor.execute(sql_sell_insert3)
        db.commit()
        sql_sell_update3 = "delete from my_stock_pool where stock_code = '%s'" % (stock_code)
        cursor.execute(sql_sell_update3)
        db.commit()
        db.close()
        return 1

    elif predict == -1:
        new_money_lock = deal.cur_money_lock - sell_price * hold_vol
        new_money_rest = deal.cur_money_rest + sell_price * hold_vol
        new_capital = deal.cur_capital + (sell_price - init_price) * hold_vol
        new_profit = (sell_price - init_price) * hold_vol
        new_profit_rate = sell_price / init_price
        sql_sell_insert4 = "insert into my_capital(capital,money_lock,money_rest,deal_action,stock_code,stock_vol,profit,profit_rate,bz,state_dt,deal_price)values('%.2f','%.2f','%.2f','%s','%s','%.2f','%.2f','%.2f','%s','%s','%.2f')" % (
        new_capital, new_money_lock, new_money_rest, 'Predict', stock_code, hold_vol, new_profit, new_profit_rate,
        'PredictSell', opdate, sell_price)
        cursor.execute(sql_sell_insert4)
        db.commit()
        sql_sell_update3 = "delete from my_stock_pool where stock_code = '%s'" % (stock_code)
        cursor.execute(sql_sell_update3)
        db.commit()
        db.close()
        return 1
    db.close()
    return 0

