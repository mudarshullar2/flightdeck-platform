{{ config(materialized="external", location="s3://lakehouse/silver/silver_flights.parquet", format="parquet") }}

select
    icao24,
    to_timestamp(firstSeen) as first_seen,
    estDepartureAirport as departure_airport,
    to_timestamp(lastSeen) as last_seen,
    estArrivalAirport as arrival_airport,
    callsign,
    estDepartureAirportHorizDistance as departure_horiz_distance_m,
    estDepartureAirportVertDistance as departure_vert_distance_m,
    estArrivalAirportHorizDistance as arrival_horiz_distance_m,
    estArrivalAirportVertDistance as arrival_vert_distance_m,
    departureAirportCandidatesCount as departure_candidates_count,
    arrivalAirportCandidatesCount as arrival_candidates_count,
    airport,
    date,
    'arrivals' as source
from read_json_auto('s3://bronze/arrivals/*/*/*.json', hive_partitioning=True)
where estDepartureAirport is not null
and estArrivalAirport is not null
{% if is_incremental() %}
and date > (select max(date) from {{ this }})
{% endif %}
union all
select
    icao24,
    to_timestamp(firstSeen) as first_seen,
    estDepartureAirport as departure_airport,
    to_timestamp(lastSeen) as last_seen,
    estArrivalAirport as arrival_airport,
    callsign,
    estDepartureAirportHorizDistance as departure_horiz_distance_m,
    estDepartureAirportVertDistance as departure_vert_distance_m,
    estArrivalAirportHorizDistance as arrival_horiz_distance_m,
    estArrivalAirportVertDistance as arrival_vert_distance_m,
    departureAirportCandidatesCount as departure_candidates_count,
    arrivalAirportCandidatesCount as arrival_candidates_count,
    airport,
    date,
    'departures' as source
from read_json_auto('s3://bronze/departures/*/*/*.json', hive_partitioning=True)
where estDepartureAirport is not null
and estArrivalAirport is not null
{% if is_incremental() %}
and date > (select max(date) from {{ this }})
{% endif %}
