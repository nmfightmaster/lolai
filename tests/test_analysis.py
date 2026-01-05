import pytest
from unittest.mock import patch, MagicMock
from src.analysis import AnalysisEngine
from src.models import GameStatsDto

@pytest.fixture
def mock_games():
    # Helper to create a dummy GSD
    def create_game(win, kda, cspm, vision, gold_pm):
        return GameStatsDto(
            match_id="NA1_123", puuid="test_puuid", champion_name="Ahri",
            win=win, game_creation=1000, game_duration=1800,
            kills=5, deaths=5, assists=5, kda=kda,
            total_minions_killed=200, neutral_minions_killed=0, cs_per_minute=cspm,
            gold_earned=10000, gold_per_minute=gold_pm,
            total_damage_dealt_to_champions=20000, damage_per_minute=600,
            vision_score=vision, wards_placed=10, wards_killed=2,
            team_position="MIDDLE"
        )
    
    return [
        create_game(True, 4.0, 7.0, 25, 400),
        create_game(False, 2.0, 6.0, 15, 300)
    ]

@patch('src.analysis.get_recent_games')
def test_get_user_stats(mock_get_games, mock_games):
    mock_get_games.return_value = mock_games
    
    engine = AnalysisEngine()
    report = engine.get_user_stats("test_puuid", 20)
    
    assert report.games_analyzed == 2
    assert report.win_rate == 50.0
    
    # Averages
    # KDA: (4.0 + 2.0) / 2 = 3.0
    assert report.avg_kda == 3.0
    assert report.kda_diff == "GOOD" # Baseline is 3.0
    
    # CSPM: (7.0 + 6.0) / 2 = 6.5
    assert report.avg_cspm == 6.5
    assert report.cspm_diff == "GOOD" # Baseline is 6.5
    
    # Vision: (25 + 15) / 2 = 20
    assert report.avg_vision_score == 20.0
    assert report.vision_diff == "GOOD" # Baseline is 20.0

@patch('src.analysis.get_recent_games')
def test_get_user_stats_needs_improvement(mock_get_games):
    # Poor performance game
    game = GameStatsDto(
            match_id="NA1_123", puuid="test_puuid", champion_name="Ahri",
            win=False, game_creation=1000, game_duration=1800,
            kills=0, deaths=5, assists=0, kda=0.0,
            total_minions_killed=100, neutral_minions_killed=0, cs_per_minute=3.0,
            gold_earned=5000, gold_per_minute=200,
            total_damage_dealt_to_champions=5000, damage_per_minute=100,
            vision_score=5, wards_placed=0, wards_killed=0,
            team_position="MIDDLE"
    )
    mock_get_games.return_value = [game]
    
    engine = AnalysisEngine()
    report = engine.get_user_stats("test_puuid")
    
    assert report.avg_kda == 0.0
    assert report.kda_diff == "NEEDS_IMPROVEMENT"
    
    assert report.avg_cspm == 3.0
    assert report.cspm_diff == "NEEDS_IMPROVEMENT"

@patch('src.analysis.get_recent_games')
def test_no_games(mock_get_games):
    mock_get_games.return_value = []
    engine = AnalysisEngine()
    report = engine.get_user_stats("test_puuid")
    assert report is None
