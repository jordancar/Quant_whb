#coding:utf8 
import logging 
logger=logging.getLogger("Michael&XB's logger")
logger.setLevel(logging.DEBUG)
LOG_FORMAT=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
st=logging.StreamHandler()
st.setFormatter(LOG_FORMAT)
# st.setLevel(logging.CRITICAL) #日志不输出
logger.addHandler(st)

