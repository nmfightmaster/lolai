from unittest.mock import MagicMock, patch
import pytest
from src.riot import RiotClient

@pytest.fixture
def mock_httpx_client():
    with patch("src.riot.httpx.Client") as mock_client:
        yield mock_client

def test_get_match_ids_by_puuid(mock_httpx_client):
    # Setup
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = ["NA1_12345", "NA1_67890"]
    
    mock_instance = mock_httpx_client.return_value.__enter__.return_value
    mock_instance.get.return_value = mock_response
    
    # Execute
    client = RiotClient()
    ids = client.get_match_ids_by_puuid("test_puuid", start=0, count=5)
    
    # Verify
    assert ids == ["NA1_12345", "NA1_67890"]
    mock_instance.get.assert_called_once()
    call_args = mock_instance.get.call_args
    # call_args[0] is args, call_args[1] is kwargs
    url = call_args[0][0]
    kwargs = call_args[1]
    
    assert "by-puuid/test_puuid/ids" in url
    assert kwargs['params'] == {'start': 0, 'count': 5}

def test_get_match_ids_by_puuid_with_filters(mock_httpx_client):
    # Setup
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    
    mock_instance = mock_httpx_client.return_value.__enter__.return_value
    mock_instance.get.return_value = mock_response
    
    # Execute
    client = RiotClient()
    client.get_match_ids_by_puuid("test_puuid", queue=420, type="ranked")
    
    # Verify
    call_args = mock_instance.get.call_args
    kwargs = call_args[1]
    
    assert kwargs['params']['queue'] == 420
    assert kwargs['params']['type'] == "ranked"
