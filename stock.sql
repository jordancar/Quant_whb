
select m.dt,m.code,m.name,m.max_price max_price_1031,m.low_price low_price_1031,m.pre_end end_price_1031, m.rise_rate, x.dt,x.rise_rate rise_1101,
m.done_volume_rate done_ring_1031,
n.done_volume_rate done_ring_month_avg from 
(select b.*,(b.done_volume-a.done_volume)/a.done_volume done_volume_rate,
(b.done_money-a.done_money)/a.done_money done_money_rate

  from stock_sh a  left join  (select * from stock_sh where dt='2018-10-31' and rise_rate>=9.9)  b on a.code=b.code 
 where datediff(b.dt,a.dt)=1 ) m
 join 

(select code,avg(done_volume_rate) done_volume_rate ,avg(done_money_rate) done_money_rate from (
select c.*,(c.done_volume-d.done_volume)/d.done_volume done_volume_rate, (c.done_money-d.done_money)/d.done_money done_money_rate from 
(select * from stock_sh where code in (select code from stock_sh where dt='2018-10-31' and rise_rate>=9.9 group by code)  and dt>='2018-10-01') c 
join  
(select * from stock_sh where code in (select code from stock_sh where dt='2018-10-31' and rise_rate>=9.9 group by code)  and dt>='2018-10-01') d 
on c.code= d.code 
where  
datediff(c.dt,d.dt)=1 ) e
group by code )  n 

on m.code = n.code 
left join 
(select * from stock_sh where code in (select code from stock_sh where dt='2018-10-31' and rise_rate>=9.9 group by code) and dt='2018-11-01')x
on  m.code =x.code

order by done_volume_rate desc
 ;

  select * from stock_sh limit 10 into outfile '/Users/wanghongbo8/fonts_whb/stock_sh.csv' character set gbk 
 fields terminated by ',' optionally enclosed by '"' 
 lines terminated by '\n';


 select
	m.dt,
	m.code,
	m.name,
	m.max_price max_price_1031,
	m.low_price low_price_1031,
	m.pre_end end_price_1031,
	m.rise_rate,
	x.dt,
	x.rise_rate rise_1101,
	m.done_volume_rate done_ring_1031,
	n.done_volume_rate done_ring_month_avg
from
	(
		select
			b.*,
			(b.done_volume - a.done_volume) / a.done_volume done_volume_rate,
			(b.done_money - a.done_money) / a.done_money done_money_rate
		from
			stock_sh a
		left join
			(
				select * from stock_sh where dt = '2018-10-31' and rise_rate >= 9.9
			)
			b
		on
			a.code = b.code
		where
			datediff(b.dt, a.dt) = 1
	)
	m
join
	(
		select
			code,
			avg(done_volume_rate) done_volume_rate,
			avg(done_money_rate) done_money_rate
		from
			(
				select
					c.*,
					(c.done_volume - d.done_volume) / d.done_volume done_volume_rate,
					(c.done_money - d.done_money) / d.done_money done_money_rate
				from
					(
						select
							*
						from
							stock_sh
						where
							code in
							(
								select
									code
								from
									stock_sh
								where
									dt = '2018-10-31'
									and rise_rate >= 9.9
								group by
									code
							)
							and dt >= '2018-10-01'
					)
					c
				join
					(
						select
							*
						from
							stock_sh
						where
							code in
							(
								select
									code
								from
									stock_sh
								where
									dt = '2018-10-31'
									and rise_rate >= 9.9
								group by
									code
							)
							and dt >= '2018-10-01'
					)
					d
				on
					c.code = d.code
				where
					datediff(c.dt, d.dt) = 1
			)
			e
		group by
			code
	)
	n on m.code = n.code
left join
	(
		select
			*
		from
			stock_sh
		where
			code in
			(
				select
					code
				from
					stock_sh
				where
					dt = '2018-10-31'
					and rise_rate >= 9.9
				group by
					code
			)
			and dt = '2018-11-01'
	)
	x
on
	m.code = x.code
order by
	done_volume_rate desc ;


