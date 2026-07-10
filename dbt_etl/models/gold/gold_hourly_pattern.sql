{{ config(materialized="external", location="s3://lakehouse/gold/gold_hourly_pattern.parquet", format="parquet") }}

select
    case when source = 'arrivals' then extract(hour from last_seen)
        else extract(hour from first_seen) end as hour_of_day,
    source,
    count(*) as num_flight,
    date
from {{ ref('silver_flights') }}
where (
    (source = 'arrivals' and last_seen is not null)
    or (source = 'departures' and first_seen is not null)
)
group by hour_of_day, source, date
