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

result_arrivals = conn.execute(
    "select count(*) from read_json_auto('s3://bronze/arrivals/*/*/*.json')"
).fetchall()

result_departures = conn.execute(
    "select count(*) from read_json_auto('s3://bronze/departures/*/*/*.json')"
).fetchall()

print(f"result_arrivals: {result_arrivals}\n")
print(f"result_departures: {result_departures}\n")

# check the type of data I'm getting from the endpoint
print(conn.execute("describe select * from read_json_auto('s3://bronze/arrivals/*/*/*.json')\n").fetchall())
print("\n")
print(conn.execute("describe select * from read_json_auto('s3://bronze/departures/*/*/*.json')\n").fetchall())

'''
[('icao24', 'VARCHAR', 'YES', None, None, None), 
('firstSeen', 'BIGINT', 'YES', None, None, None), 
('estDepartureAirport', 'VARCHAR', 'YES', None, None, None), 
('lastSeen', 'BIGINT', 'YES', None, None, None), 
('estArrivalAirport', 'VARCHAR', 'YES', None, None, None), 
('callsign', 'VARCHAR', 'YES', None, None, None), 
('estDepartureAirportHorizDistance', 'BIGINT', 'YES', None, None, None), 
('estDepartureAirportVertDistance', 'BIGINT', 'YES', None, None, None), 
('estArrivalAirportHorizDistance', 'BIGINT', 'YES', None, None, None), 
('estArrivalAirportVertDistance', 'BIGINT', 'YES', None, None, None), 
('departureAirportCandidatesCount', 'BIGINT', 'YES', None, None, None), 
('arrivalAirportCandidatesCount', 'BIGINT', 'YES', None, None, None), 
('airport', 'VARCHAR', 'YES', None, None, None), 
('date', 'DATE', 'YES', None, None, None)]


[('icao24', 'VARCHAR', 'YES', None, None, None), 
('firstSeen', 'BIGINT', 'YES', None, None, None), 
('estDepartureAirport', 'VARCHAR', 'YES', None, None, None), 
('lastSeen', 'BIGINT', 'YES', None, None, None), 
('estArrivalAirport', 'VARCHAR', 'YES', None, None, None), 
('callsign', 'VARCHAR', 'YES', None, None, None), 
('estDepartureAirportHorizDistance', 'BIGINT', 'YES', None, None, None), 
('estDepartureAirportVertDistance', 'BIGINT', 'YES', None, None, None), 
('estArrivalAirportHorizDistance', 'BIGINT', 'YES', None, None, None), 
('estArrivalAirportVertDistance', 'BIGINT', 'YES', None, None, None), 
('departureAirportCandidatesCount', 'BIGINT', 'YES', None, None, None), 
('arrivalAirportCandidatesCount', 'BIGINT', 'YES', None, None, None), 
('airport', 'VARCHAR', 'YES', None, None, None), 
('date', 'DATE', 'YES', None, None, None)]
'''