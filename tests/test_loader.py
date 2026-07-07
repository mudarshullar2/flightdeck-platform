import json
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from opensky import BronzeLoader

def _make_loader():
    with patch("opensky.loader.boto3.client") as mock_client:
        loader = BronzeLoader(
            endpoint="http://fake:9000",
            access_key="key",
            secret_key="secret"
        )
    loader.s3 = MagicMock()
    return loader

def test_key_structure():
    loader = _make_loader()
    ts = datetime(2026, 7, 7, 12, 0, 0, tzinfo=timezone.utc)
    key = loader._key("arrivals", "EDDB", ts)
    assert key == "arrivals/date=2026-07-07/airport=EDDB/EDDB_20260707T120000Z.json"

def test_land_puts_object_with_correct_args():
    loader = _make_loader()
    ts = datetime(2026, 7, 7, 12, 0, 0, tzinfo=timezone.utc)
    records = [{"icao24": "abc"}, {"icao24": "def"}]
    returned_key = loader.land(records, "departures", "EDDB", run_ts=ts)
    expected_key = "departures/date=2026-07-07/airport=EDDB/EDDB_20260707T120000Z.json"
    assert returned_key == expected_key

    loader.s3.put_object.assert_called_once()
    _, kwargs = loader.s3.put_object.call_args
    assert kwargs["Bucket"] == "bronze"
    assert kwargs["Key"] == expected_key

    assert json.loads(kwargs["Body"].decode("utf-8")) == records

def test_land_generates_timestamp_when_none_given():
    loader = _make_loader()

    loader.land([{"icao24": "abc"}], "arrivals", "EDDB")

    loader.s3.put_object.assert_called_once()
    _, kwargs = loader.s3.put_object.call_args
    assert kwargs["Key"].startswith("arrivals/date=")
    assert kwargs["Key"].endswith(".json")
