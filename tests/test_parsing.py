import pytest
from src.parsing import parse_match_to_stats, parse_timeline_to_events

def test_parse_match_to_stats():
    puuid = "user_123"
    mock_data = {
        "metadata": {"matchId": "NA1_123"},
        "info": {
            "gameCreation": 1000,
            "gameDuration": 600, # 10 mins
            "participants": [
                {
                    "puuid": "other_guy",
                    "championName": "Annie", 
                    "win": False,
                    "kills": 0, "deaths": 0, "assists": 0, "kda": 0,
                    "totalMinionsKilled": 0, "neutralMinionsKilled": 0,
                    "totalDamageDealtToChampions": 0,
                    "goldEarned": 0,
                    "visionScore": 0, "wardsPlaced": 0, "wardsKilled": 0,
                    "teamPosition": "MIDDLE"
                },
                {
                    "puuid": "user_123",
                    "championName": "Ahri",
                    "win": True,
                    "kills": 5, "deaths": 1, "assists": 2,
                    "totalMinionsKilled": 50, "neutralMinionsKilled": 10, # 60 total
                    "totalDamageDealtToChampions": 10000,
                    "goldEarned": 5000,
                    "visionScore": 15, "wardsPlaced": 5, "wardsKilled": 1,
                    "teamPosition": "MIDDLE"
                }

            ]
        }
    }
    
    stats = parse_match_to_stats(mock_data, puuid)
    
    assert stats.match_id == "NA1_123"
    assert stats.puuid == puuid
    assert stats.champion_name == "Ahri"
    assert stats.win is True
    assert stats.kills == 5
    assert stats.deaths == 1
    assert stats.assists == 2
    assert stats.kda == 7.0
    
    # 60 CS in 10 mins = 6.0 CS/min
    assert stats.cs_per_minute == 6.0
    assert stats.total_minions_killed == 50
    assert stats.neutral_minions_killed == 10
    
    assert stats.gold_earned == 5000
    assert stats.gold_per_minute == 500.0
    
    assert stats.total_damage_dealt_to_champions == 10000
    assert stats.damage_per_minute == 1000.0


def test_parse_timeline_events():
    puuid = "user_123"
    mock_data = {
        "metadata": {"matchId": "NA1_123"},
        "info": {
            "participants": [
                {"participantId": 1, "puuid": "user_123"},
                {"participantId": 2, "puuid": "victim_456"}
            ],
            "frames": [
                {
                    "events": [
                        {
                            "type": "CHAMPION_KILL",
                            "timestamp": 1000,
                            "killerId": 1,
                            "victimId": 2,
                            "position": {"x": 100, "y": 200}
                        },
                        {
                            "type": "CHAMPION_KILL",
                            "timestamp": 2000,
                            "killerId": 2, # Not us
                            "victimId": 3, # Not us
                            "position": {"x": 300, "y": 300}
                        },
                        {
                             "type": "ELITE_MONSTER_KILL",
                             "timestamp": 3000,
                             "killerId": 1,
                             "monsterType": "DRAGON" 
                        }
                    ]
                }
            ]
        }
    }
    
    events = parse_timeline_to_events(mock_data, puuid)
    
    assert len(events) == 2
    
    # Event 1: Kill
    e1 = events[0]
    assert e1.type == "CHAMPION_KILL"
    assert e1.killer_id == 1
    assert e1.victim_id == 2
    assert e1.position_x == 100
    
    # Event 2: Dragon
    e2 = events[1]
    assert e2.type == "ELITE_MONSTER_KILL"
    assert e2.killer_id == 1
    assert e2.monster_type == "DRAGON"
