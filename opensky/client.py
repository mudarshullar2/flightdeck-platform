import requests
import logging

BASE_URL = "https://opensky-network.org/api"

class OpenSkyClient:
    def __init__(self, token_manager, timeout=30):
        self.token_manager = token_manager
        self.timeout = timeout

    def _get(self, path, params):
        r = requests.get(
            f"{BASE_URL}{path}",
            headers=self.token_manager.headers(),
            params=params,
            timeout=self.timeout
        )
        if r.status_code == 404: #according to the documentation, it means no data available right now
           logging.info("No data available")
           return []
        r.raise_for_status()
        return r.json()

    def get_arrivals(self, airport, begin, end):
        return self._get(
            "/flights/arrival",
            {"airport": airport, "begin": begin, "end": end}
        )

    def get_departure(self, airport, begin, end):
        return self._get(
            "/flights/departure",
            {"airport": airport, "begin": begin, "end": end}
        )
