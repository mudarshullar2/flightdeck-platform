{{ config(materialized="incremental", unique_key="icao24" ,database="flightdeck_iceberg_catalog", schema="silver") }}

select
    icao24,
    to_timestamp(firstSeen) as first_seen,
    estDepartureAirport,
    to_timestamp(lastSeen) as last_seen,
    estArrivalAirport,
    callsign,
    estDepartureAirportHorizDistance,
    estDepartureAirportVertDistance,
    estArrivalAirportHorizDistance,
    estArrivalAirportVertDistance,
    departureAirportCandidatesCount,
    arrivalAirportCandidatesCount,
    airport,
    date,
    'arrivals' as source
from read_json_auto('s3://bronze/arrivals/*/*/*.json', hive_partitioning=True)
union all
select
    icao24,
    to_timestamp(firstSeen) as first_seen,
    estDepartureAirport,
    to_timestamp(lastSeen) as last_seen,
    estArrivalAirport,
    callsign,
    estDepartureAirportHorizDistance,
    estDepartureAirportVertDistance,
    estArrivalAirportHorizDistance,
    estArrivalAirportVertDistance,
    departureAirportCandidatesCount,
    arrivalAirportCandidatesCount,
    airport,
    date,
    'departures' as source
from read_json_auto('s3://bronze/departures/*/*/*.json', hive_partitioning=True)
