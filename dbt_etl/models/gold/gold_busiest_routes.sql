{{ config(materialized="external", location="s3://lakehouse/gold/gold_busiest_routes.parquet", format="parquet") }}

select
    departure_airport,
    arrival_airport,
    count(*) as flights,
    date
from {{ ref('silver_flights') }}
group by departure_airport, arrival_airport, date
order by flights desc
