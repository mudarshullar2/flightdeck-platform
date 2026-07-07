from unittest.mock import patch, MagicMock
from opensky import TokenManager

def _fake_response(token="aabb225", expires_in=1800):
    resp = MagicMock()
    resp.json.return_value = {"access_token": token, "expires_in": expires_in}
    resp.raise_for_status.return_value = None
    return resp

@patch("opensky.auth.requests.post")
def test_reuses_cached_token(mock_post):
    mock_post.return_value = _fake_response()
    tokenManager = TokenManager()
    tokenManager.get_token()
    tokenManager.get_token()
    assert mock_post.call_count == 1

@patch("opensky.auth.requests.post")
def test_headers_contain_bearer_token(mock_post):
    mock_post.return_value = _fake_response(token="msh1234")
    tokenManager = TokenManager()
    headers = tokenManager.headers()
    assert headers == {"Authorization": "Bearer msh1234"}
