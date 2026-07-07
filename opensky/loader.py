from datetime import datetime, timezone
import boto3
import json

class BronzeLoader:
    def __init__(self, endpoint, access_key, secret_key, bucket="bronze"):
        self.bucket = bucket
        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def _key(self, flight_type, airport, run_ts):
        date = run_ts.strftime("%Y-%m-%d")
        stamp = run_ts.strftime("%Y%m%dT%H%M%SZ")
        return f"{flight_type}/date={date}/airport={airport}/{airport}_{stamp}.json"

    def land(self, records, flight_type, airport, run_ts=None):
        run_ts = run_ts or datetime.now(timezone.utc)
        key = self._key(flight_type, airport, run_ts)
        body = json.dumps(records).encode("utf-8")
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=body)
        return key
