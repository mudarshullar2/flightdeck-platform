from datetime import datetime, timedelta
import requests, os, logging

TOKEN_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_REFRESH_MARGIN = 300

class TokenManager:
    def __init__(self):
        self.token = None
        self.expires_at = None

    def get_token(self):
        if self.token and self.expires_at and datetime.now() < self.expires_at:
            return self.token
        return self._refresh()

    def _refresh(self):
        logging.info("CLIENT_ID=%r SECRET set=%s", CLIENT_ID, bool(CLIENT_SECRET))
        r = requests.post(TOKEN_URL,
                          data={
                              "grant_type": "client_credentials",
                              "client_id": CLIENT_ID,
                              "client_secret": CLIENT_SECRET,
                          })
        r.raise_for_status()
        data = r.json()
        self.token = data["access_token"]
        expires_in = data.get("expires_in", 1800)
        self.expires_at = datetime.now() + timedelta(seconds=expires_in - TOKEN_REFRESH_MARGIN)
        return self.token

    def headers(self):
        return {"Authorization": f"Bearer {self.get_token()}" }
