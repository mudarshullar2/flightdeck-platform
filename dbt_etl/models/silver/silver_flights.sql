{{ config(materialized='table', database='flightdeck_iceberg_catalog', schema='silver') }}

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
    airport
from read_json_auto('s3://bronze/arrivals/*/*/*.json')
