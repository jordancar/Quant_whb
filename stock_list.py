#coding:utf8 
import tushare  as ts  
ts.set_token('23b817c8b6e2b772f37ad6f5628ad348a0aefed07ed9b07ecc75976d')
pro = ts.pro_api()
#获取沪股通成分
df = pro.hs_const(hs_type='SH') 

#获取深股通成分
df_sz = pro.hs_const(hs_type='SZ')

def stock_all():
    all_stock=pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return all_stock 
    