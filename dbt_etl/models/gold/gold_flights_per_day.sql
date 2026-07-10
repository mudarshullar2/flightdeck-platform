{{ config(materialized="external", location="s3://lakehouse/gold/gold_flights_per_day.parquet", format="parquet") }}

select
    cast(last_seen as date) as flight_day,
    count(*) as num_flights
from {{ ref('silver_flights') }}
group by flight_day
order by flight_day
