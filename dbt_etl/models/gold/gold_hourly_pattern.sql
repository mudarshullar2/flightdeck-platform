{{ config(materialized="incremental", incremental_strategy="append", unique_key=["hour_of_day", "source", "date"] ,database="flightdeck_iceberg_catalog", schema="gold") }}

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
{% if is_incremental() %}
and date > (select max(date) from {{ this }})
{% endif %}
group by hour_of_day, source, date
