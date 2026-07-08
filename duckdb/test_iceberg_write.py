import os, duckdb
from dotenv import load_dotenv

load_dotenv()

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

conn.execute(
    """
        create secret iceberg_secret (
            type iceberg,
            token 'dummy'
        )
    """)

conn.execute(
    """
       attach 'flightdeck' as flightdeck_iceberg_catalog (
            type iceberg,
            secret iceberg_secret,
            endpoint 'http://localhost:8181/catalog'
       )
    """)

conn.execute(
    """
        create schema if not exists flightdeck_iceberg_catalog.bronze;
        use flightdeck_iceberg_catalog.bronze;
    """)

conn.execute(
    """
       create table if not exists flightdeck_iceberg_catalog.bronze.arrivals (
            icao24 varchar,
            firstSeen bigint,
            estDepartureAirport varchar,
            lastSeen bigint,
            estArrivalAirport varchar,
            callsign varchar,
            estDepartureAirportHorizDistance bigint,
            estDepartureAirportVertDistance bigint,
            estArrivalAirportHorizDistance bigint,
            estArrivalAirportVertDistance bigint,
            departureAirportCandidatesCount bigint,
            arrivalAirportCandidatesCount bigint,
            airport varchar,
            date date
       )
    """)

arrivals_table = conn.execute(
    """
        select * from flightdeck_iceberg_catalog.bronze.arrivals
    """).fetchall()

conn.execute(
    """
       create table if not exists flightdeck_iceberg_catalog.bronze.departures (
            icao24 varchar,
            firstSeen bigint,
            estDepartureAirport varchar,
            lastSeen bigint,
            estArrivalAirport varchar,
            callsign varchar,
            estDepartureAirportHorizDistance bigint,
            estDepartureAirportVertDistance bigint,
            estArrivalAirportHorizDistance bigint,
            estArrivalAirportVertDistance bigint,
            departureAirportCandidatesCount bigint,
            arrivalAirportCandidatesCount bigint,
            airport varchar,
            date date
       )
    """).fetchall()

departures_table = conn.execute(
        """
            select * from flightdeck_iceberg_catalog.bronze.departures
        """).fetchall()

print(f"arrivals table: {arrivals_table}")
print("\n")
print(f"departures table: {departures_table}")


conn.execute(
    """
        drop table flightdeck_iceberg_catalog.bronze.arrivals;
        drop table flightdeck_iceberg_catalog.bronze.departures;
    """
)
