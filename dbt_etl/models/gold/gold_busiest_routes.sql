{{ config(materialized="incremental", incremental_strategy="append", unique_key=["departure_airport", "arrival_airport", "date"] ,database="flightdeck_iceberg_catalog", schema="gold") }}

select
    departure_airport,
    arrival_airport,
    count(*) as flights,
    date
from {{ ref('silver_flights') }}
{% if is_incremental() %}
where date > (select max(date) from {{ this }} )
{% endif %}
group by departure_airport, arrival_airport, date
order by flights desc
