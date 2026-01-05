import pytest
import sqlite3
import os
from src.models import GameStatsDto
from src.database import init_db, save_game_stats, get_db_connection, DB_NAME

@pytest.fixture
def clean_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    init_db()
    yield
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def test_save_and_retrieve_stats(clean_db):
    stats = GameStatsDto(
        match_id="NA1_123",
        puuid="user_123",
        champion_name="Ahri",
        win=True,
        game_creation=1000,
        game_duration=600,
        kills=5, deaths=1, assists=2, kda=7.0,
        total_minions_killed=50, neutral_minions_killed=10, cs_per_minute=6.0,
        gold_earned=5000, gold_per_minute=500.0,
        total_damage_dealt_to_champions=10000, damage_per_minute=1000.0,
        vision_score=15, wards_placed=5, wards_killed=1,
        team_position="MIDDLE"
    )
    
    save_game_stats(stats)
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM game_stats WHERE match_id = ?", ("NA1_123",))
    row = c.fetchone()
    conn.close()
    
    assert row["match_id"] == "NA1_123"
    assert row["champion_name"] == "Ahri"
    assert row["kills"] == 5
