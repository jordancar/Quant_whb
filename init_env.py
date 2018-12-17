#coding:utf8 
import tushare as ts
import pymysql
class get_env(object):
    def __init__(self):
        self.db=pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='stock', charset='utf8')
        self.cursor=self.db.cursor()
        ts.set_token('23b817c8b6e2b772f37ad6f5628ad348a0aefed07ed9b07ecc75976d')
        self.pro = ts.pro_api()