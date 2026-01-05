import pytest
from unittest.mock import patch, MagicMock
from src.riot import RiotClient

@pytest.fixture
def mock_env_key(monkeypatch):
    monkeypatch.setenv("RIOT_API_KEY", "test-key")

@patch("src.riot.httpx.Client")
def test_get_match(mock_client_cls, mock_env_key):
    # Setup mock
    mock_response = MagicMock()
    mock_response.json.return_value = {"metadata": {"matchId": "NA1_123"}, "info": {}}
    mock_response.raise_for_status.return_value = None
    
    mock_client_instance = MagicMock()
    mock_client_instance.get.return_value = mock_response
    mock_client_instance.__enter__.return_value = mock_client_instance
    mock_client_cls.return_value = mock_client_instance

    # Run
    client = RiotClient()
    result = client.get_match("NA1_123")

    # Verify
    assert result["metadata"]["matchId"] == "NA1_123"
    mock_client_instance.get.assert_called_with("https://americas.api.riotgames.com/lol/match/v5/matches/NA1_123")
