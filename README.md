# flightdeck-platform

E2E flight data platform: ingests live flight data from OpenSky API into a MinIO lakehouse, transforms it through bronze/silver/gold layers with dbt + DuckDB (Iceberg), and visualize it in Superset.
Orchestration is done via Airflow and all running on Docker.

Status: In progress 
To access the opensky endpoints, you need a client id and client secret, which are only available after creating an account.
OpenSky docs: https://openskynetwork.github.io/opensky-api/

dbt was moved into a docker container. Because of this, testing the connection to duckdb (data retrieval and transformation) requires different ports when running locally vs. images from the container.
.env.local.testing was provided in the root directory, an example of the environment variables is also provided, along with a file for connecting and running queries (/duckdb/test_duckdb_local_connection.py)

Since the open sky endpoint does not provide data for every hour, the retrieval DAG was adjusted to pull data from two days ago rather than the most recent window.
Due to limitations around update and delete operations on DuckDB, an incremental append is used. is_incremental filter is added to the silver and gold models to avoid duplicate rows on reruns.
Link to the limitations: https://duckdb.org/2025/11/28/iceberg-writes-in-duckdb


## Architecture
![architecture](docs/flightdeck-platform-draw-io.png)
