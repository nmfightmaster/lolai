import os
from unittest.mock import MagicMock, patch
import pytest
from src.llm import LLMClient
from src.models import GameStatsDto, TimelineEventDto

@pytest.fixture
def mock_stats():
    return GameStatsDto(
        match_id="NA1_123456",
        puuid="p1",
        champion_name="Ahri",
        win=False,
        game_creation=1000,
        game_duration=1800, # 30 mins
        kills=5,
        deaths=10, # Feeding
        assists=2,
        kda=0.7,
        total_minions_killed=150,
        neutral_minions_killed=0,
        cs_per_minute=5.0,
        gold_earned=8000,
        gold_per_minute=266,
        total_damage_dealt_to_champions=15000,
        damage_per_minute=500,
        vision_score=15,
        wards_placed=5,
        wards_killed=1,
        team_position="MIDDLE"
    )

@patch("src.llm.genai")
@patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
def test_generate_match_summary(mock_genai, mock_stats):
    # Setup Mock
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "You fed on Ahri. Stop doing that."
    
    # Mock client.models.generate_content
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client
    
    client = LLMClient()
    summary = client.generate_match_summary(stats=mock_stats, events=[])
    
    assert "Ahri" in summary or "Stop" in summary
    assert summary == "You fed on Ahri. Stop doing that."
    
    # Verify prompt content
    args, kwargs = mock_client.models.generate_content.call_args
    # args: (), kwargs: {model: '...', contents: '...'}
    prompt = kwargs['contents']
    assert "Champion: Ahri" in prompt
    assert "Result: Loss" in prompt
    assert "KDA: 5/10/2" in prompt
