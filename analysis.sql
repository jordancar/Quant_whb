--profit sql
select year(state_dt) 年度 ,sum(profit) 收益 from my_capital  group by  year(state_dt)
select year(state_dt) 年度,month(state_dt) 月份,sum(profit) 收益 from my_capital  group by  year(state_dt),month(state_dt)
select bz 操作类型,sum(profit) 收益 from my_capital group by  bz -- group by operate type 
select year(state_dt) 年度,stock_code,sum(profit) 收益 from my_capital group by  year(state_dt)  ,stock_code;

select * from my_capital where capital>=(select max(capital) from my_capital)
union all 
select * from my_capital where capital<=(select min(capital) from my_capital)

select * from model_macd_resu where stock_code in ('603156.SH', '603180.SH', '603196.SH', '603389.SH', '603630.SH', '603693.SH', '603711.SH', '603776.SH', '603787.SH', '603789.SH', '603799.SH', '603933.SH',
'300285.SZ', '300324.SZ', '300343.SZ', '300409.SZ', '300441.SZ', '300674.SZ', '300750.SZ', '300760.SZ', '600004.SH', '600009.SH')  and predict=1;

--连续下跌
set @a:=1,@b:=1,@c:=0;
select cum_lose_day,count(1) days from 
(
select state_dt,case when rise=1 then @c:=@c+rise else @c:=0 end as  cum_lose_day  from 
(select a.state_dt,b.state_dt dt,a.capital,b.capital cp,case when b.capital-a.capital >0 then 0 else 1 end rise from 
(select a.*,@a:=@a+1 id from my_capital a join  (select max(seq) seq,state_dt from my_capital group by state_dt) b  on a.seq=b.seq order by state_dt asc ) a 
join 
(select a.*,@b:=@b+1 id  from my_capital a join  (select max(seq) seq,state_dt from my_capital group by state_dt) b  on a.seq=b.seq order by state_dt asc) b 
 where a.id-b.id=-1) c) d  group by cum_lose_day;

--连续上涨 
set @a:=1,@b:=1,@c:=0;
select cum_rise_day,count(1) days from 
(
select state_dt,case when rise=0 then @c:=@c+1 else @c:=0 end as  cum_rise_day  from 
(select a.state_dt,b.state_dt dt,a.capital,b.capital cp,case when b.capital-a.capital >0 then 0 else 1 end rise from 
(select a.*,@a:=@a+1 id from my_capital a join  (select max(seq) seq,state_dt from my_capital group by state_dt) b  on a.seq=b.seq order by state_dt asc ) a 
join 
(select a.*,@b:=@b+1 id  from my_capital a join  (select max(seq) seq,state_dt from my_capital group by state_dt) b  on a.seq=b.seq order by state_dt asc) b 
 where a.id-b.id=-1) c
 ) d  group by cum_rise_day;
--获取各板块涨幅最高top3 
select * from stock_all_plus a where state_dt='2018-08-17' and  1=(select count(*) top_1 from  stock_all_plus b where  state_dt='2018-08-17' and a.industry=b.industry and a.pct_change>=b.pct_change) and pct_change>-8 and pct_change<-5;

--stock_pool choose 
select distinct  stock_code from (select * from stock_all_plus a  where state_dt='2018-12-04' and 1>=(select count(distinct stock_code) num from stock_all_plus b where state_dt='2018-12-04' and  b.amount>a.amount and b.industry=a.industry)) c
into outfile '/Users/wanghongbo8/fonts_whb/stock_list.csv' character set utf8 
 fields terminated by ',' optionally enclosed by '"' 
 lines terminated by '\n';

select * from btc_5min 
into outfile '/Users/wanghongbo8/fonts_whb/btc_5min.csv' character set utf8 
 fields terminated by ',' optionally enclosed by '"' 
 lines terminated by '\n';
--创建参数表，写入本地分析待用
create table backtest_paraset(
        back_test_turn int(11)   AUTO_INCREMENT,
        start_dt varchar(50) NOT NULL DEFAULT '',
        end_dt  varchar(50) NOT NULL DEFAULT '',
        para_window int(11) DEFAULT NULL,
        strategy  varchar(50) NOT NULL DEFAULT 'mkwz',
        hold_days int(11) DEFAULT NULL,
        torlence_lost decimal(20,4) DEFAULT NULL,
        torlence_profit decimal(20,4) DEFAULT NULL,
        operate_days int(11) DEFAULT NULL,
        backtest_tm varchar(50) DEFAULT NULL,
        PRIMARY KEY (`back_test_turn`)
        )ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=gbk;

CREATE TABLE `model_macd_resu` (
  `state_dt` varchar(50) NOT NULL DEFAULT '',
  `stock_code` varchar(45) NOT NULL DEFAULT '',
  `predict` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`state_dt`,`stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
create table `trade_day` (
        exchange varchar(10) not null default '',
        cal_date varchar(50) not null default '',
        is_open int(11) not null default 0,
        PRIMARY KEY(`cal_date`,`exchange`)
) ENGINE=InnoDB default CHARSET=gbk;

create table `top_list`(
        `trade_date` varchar(20) not null,
        `ts_code` varchar(20) not null, 
        `name` varchar(20) default null, 
        `close` decimal(20,4) not null, 
        `pct_change` decimal(20,4) not null,
        `turnover_rate` decimal(20,4) not null, 
        `amount` decimal(20,4) not null, 
        `l_sell` decimal(20,4) not null, 
        `l_buy` decimal(20,4) not null, 
        `l_amount` decimal(20,4) not null,
        `net_amount` decimal(20,4) not null, 
        `net_rate` decimal(20,4) not null, 
        `amount_rate` decimal(20,4) not null, 
        `float_values` decimal(20,4) not null, 
        `reason` varchar(200) default null,
        PRIMARY KEY(`trade_date`,`ts_code`)
)ENGINE=InnoDB default CHARSET=gbk;

create table `stock_fmac`(
        `trade_date` varchar(20) not null,
        `ts_code` varchar(20) not null, 
        `close` decimal(20,4) not null, 
        `turnover_rate` decimal(20,4) not null,
        `turnover_rate_f` decimal(20,4) not null, 
        `volume_ratio` decimal(20,4) not null, 
        `pe` decimal(20,4) not null, 
        `pe_ttm` decimal(20,4) not null, 
        `pb` decimal(20,4) not null,
        `ps` decimal(20,4) not null, 
        `ps_ttm` decimal(20,4) not null, 
        `total_share` decimal(20,4) not null, 
        `float_share` decimal(20,4) not null,
        `free_share` decimal(20,4) not null, 
        `total_mv` decimal(20,4) not null, 
        `circ_mv` decimal(20,4) not null, 
        PRIMARY KEY(`trade_date`,`ts_code`)
)ENGINE=InnoDB default CHARSET=gbk;

--创建BTC库，5分钟级别
create table btc_5min(
        symbol varchar(50) not null,
        date varchar(50) not null, 
        open decimal(20,4) not null, 
        high decimal(20,4) not null,
        low decimal(20,4) not null,
        close decimal(20,4) not null, 
        vol  decimal(20,4) not null,
        PRIMARY KEY(symbol,date)
) ENGINE=InnoDB default CHARSET=gbk;