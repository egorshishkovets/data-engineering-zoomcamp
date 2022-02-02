select count(*) 
FROM public.yellow_taxi_data
where cast(tpep_pickup_datetime as date) between '2021-01-15' and '2021-01-15';

with t as(
select cast(tpep_pickup_datetime as date)
,cast(tpep_dropoff_datetime as date)
, max(tip_amount)
from public.yellow_taxi_data
group by cast(tpep_pickup_datetime as date)
,cast(tpep_dropoff_datetime as date)
	)
select * from t 
where max = (select max(tip_amount) from public.yellow_taxi_data);

with t as(
select tz2."Zone", count(1) as cnt
FROM public.yellow_taxi_data yd
	join public.time_zones tz1
	on yd."PULocationID" = tz1."LocationID"
	join public.time_zones tz2
	on yd."DOLocationID" = tz2."LocationID"
where cast(tpep_pickup_datetime as date) between '2021-01-14' and '2021-01-14'
group by tz2."Zone")
select * from t where cnt = (select max(cnt) as cnt  from t);


with t as(
select tz1."Zone" ,tz2."Zone", avg(total_amount) max_avg
FROM public.yellow_taxi_data yd
	join public.time_zones tz1
	on yd."PULocationID" = tz1."LocationID"
	join public.time_zones tz2
	on yd."DOLocationID" = tz2."LocationID"
group by tz1."Zone" ,tz2."Zone")
select * from t where max_avg = (select max(max_avg) as max_avg  from t);