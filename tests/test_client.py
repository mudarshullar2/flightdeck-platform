from unittest.mock import patch, MagicMock
from opensky import OpenSkyClient

class FakeTokenManager:
    def headers(self):
        return {"Authorization": "Bearer test-token"}

def _fake_response(payload):
    resp = MagicMock()
    resp.json.return_value = payload
    resp.raise_for_status.return_value = None
    return resp

@patch("opensky.client.requests.get")
def test_get_arrivals_builds_correct_request(mock_get):
    mock_get.return_value = _fake_response([{"icao24": "abc"}])
    client = OpenSkyClient(FakeTokenManager())
    result = client.get_arrivals("EDDB", 1000, 2000)
    assert result == [{"icao24": "abc"}]

    args, kwargs = mock_get.call_args
    assert args[0] == "https://opensky-network.org/api/flights/arrival"
    assert kwargs["params"] == {"airport": "EDDB", "begin": 1000, "end": 2000}
    assert kwargs["headers"] == {"Authorization": "Bearer test-token"}

@patch("opensky.client.requests.get")
def test_get_departures_builds_correct_request(mock_get):
    mock_get.return_value = _fake_response([])
    client = OpenSkyClient(FakeTokenManager())
    result = client.get_departure("EDDB", 1000, 2000)
    assert result == []

    args, kwargs = mock_get.call_args
    assert args[0] == "https://opensky-network.org/api/flights/departure"
    assert kwargs["params"] == {"airport": "EDDB", "begin": 1000, "end": 2000}
