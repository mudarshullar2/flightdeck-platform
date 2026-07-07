# flightdeck-platform

E2E flight data platform: ingests live flight data from OpenSky API into a MinIO lakehouse, transforms it through bronze/silver/gold layers with dbt + DuckDB (Iceberg), and visualize it in Superset.
Orchestration is done via Airflow and all running on Docker.

Still in progress

## Architecture
![architecture](docs/flightdeck-platform-draw-io.png)
