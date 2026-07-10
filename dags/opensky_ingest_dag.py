from opensky import TokenManager, OpenSkyClient, FlightExtractor, BronzeLoader
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
import logging, os

airport = os.getenv("AIRPORT")

def ingest_flights(**context):
    logical = context["logical_date"]
    target = logical - timedelta(days=2)
    end = int(target.timestamp())
    begin = int((target - timedelta(hours=1)).timestamp())

    tokenManager = TokenManager()
    client = OpenSkyClient(tokenManager)
    extractor = FlightExtractor(client, airport)
    loader = BronzeLoader(
        endpoint=os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ROOT_USER"),
        secret_key=os.getenv("MINIO_ROOT_PASSWORD")
    )

    bundle = extractor.extract_day(begin, end)
    arr_key = loader.land(bundle["arrivals"], "arrivals", airport)
    dep_key = loader.land(bundle["departures"], "departures", airport)
    logging.info(f"Landed {arr_key} and {dep_key}")

def alert_on_failure(context):
    logging.error(
        f"Alert {context['dag'].dag_id} {context['task_instance'].task_id} failed"
    )

default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 7, 7),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": alert_on_failure
}

with DAG(
    dag_id="opensky_ingest",
    default_args=default_args,
    schedule="@hourly",
    catchup=False
) as dag:
    ingest = PythonOperator(
        task_id="ingest_flights",
        python_callable=ingest_flights
    )
