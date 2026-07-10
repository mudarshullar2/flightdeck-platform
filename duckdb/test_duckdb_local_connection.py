import os, duckdb
from dotenv import load_dotenv

load_dotenv(".env.local.testing")

s3_region = os.getenv("S3_REGION")
s3_endpoint = os.getenv("S3_ENDPOINT")
s3_access_key_id = os.getenv("MINIO_ROOT_USER")
s3_secret_access_key = os.getenv("MINIO_ROOT_PASSWORD")
s3_url_style = os.getenv("S3_URL_SSL_STYLE")
s3_use_ssl = os.getenv("S3_USE_SSL")

conn = duckdb.connect(":memory:")
conn.execute("install httpfs;")
conn.execute("load httpfs;")
conn.execute(f"set s3_endpoint='{s3_endpoint}';")
conn.execute(f"set s3_access_key_id='{s3_access_key_id}';")
conn.execute(f"set s3_secret_access_key='{s3_secret_access_key}';")
conn.execute(f"set s3_use_ssl='{s3_use_ssl}';")
conn.execute(f"set s3_url_style='{s3_url_style}';")
conn.execute(f"set s3_region='{s3_region}';")

view = conn.execute(
    """
        create or replace view silver as 
        (
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
                from read_json_auto('s3://bronze/arrivals/*/*/*.json')
                where departure_airport is not null
                and arrival_airport is not null
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
                from read_json_auto('s3://bronze/departures/*/*/*.json')
                where departure_airport is not null
                and arrival_airport is not null
        )
    """
).df()

full_view = conn.sql(
    """
    select * 
    from silver 
    """).df()

busiest_routes_df = conn.sql(
    """
        select 
            departure_airport,
            arrival_airport,
            count(*) as flights
        from silver
        group by departure_airport, arrival_airport
        order by flights desc
    """).df()

flights_per_day_df = conn.sql(
    """
        select 
            cast(last_seen as date) as flight_day,
            count(*) as num_flights
        from silver
        group by flight_day
        order by flight_day
    """).df()

most_frequent_arrival_airport = conn.sql(
    """
        select departure_airport
        from silver
        where source = 'arrivals' is not null
        group by departure_airport
        order by count(*) desc
        limit 1
    """).df()

hourly_pattern_arrivals_df = conn.sql(
    """
        select
            extract(hour from last_seen) as hour_of_day,
            count(*) as num_arrival_flights
        from silver
        where source = 'arrivals' and last_seen is not null
        group by hour_of_day
        order by hour_of_day
    """).df()

hourly_pattern_departures_df = conn.sql(
    """
        select
            extract(hour from first_seen) as hour_of_day,
            count(*) as num_departure_flights
        from silver
        where source = 'departures' and first_seen is not null
        group by hour_of_day
        order by hour_of_day
    """).df()

merged_hourly_pattern_df = conn.sql(
    """
        select
            case when source = 'arrivals' then extract(hour from last_seen)
                else extract(hour from first_seen) end as hour_of_day,
            source,
            count(*) as num_flights
        from silver
        where (source = 'arrivals' and last_seen is not null)
            or (source = 'departures' and first_seen is not null)
        group by hour_of_day, source
        order by hour_of_day, source
    """).df()

num_arrival_flights_df = conn.sql(
    """
    select 
        count(*) num_arrival_flights
    from silver 
    where source = 'arrivals' is not null
    """).df()

num_departure_flights_df = conn.sql(
    """
        select 
            count(*) as num_departure_flights
        from silver
        where source = 'departures' is not null
    """).df()
