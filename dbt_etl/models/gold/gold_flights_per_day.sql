{{ config(materialized="incremental", incremental_strategy = "append", unique_key=["flight_day"] ,database="flightdeck_iceberg_catalog", schema="gold") }}

select
    cast(last_seen as date) as flight_day,
    count(*) as num_flights
from {{ ref('silver_flights') }}
{% if is_incremental() %}
where cast(last_seen as date) > (select max(cast(last_seen as date)) from {{ this }} )
{% endif %}
group by flight_day
order by flight_day
