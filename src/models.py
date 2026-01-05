from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class GameStatsDto(BaseModel):
    match_id: str
    puuid: str
    champion_name: str
    win: bool
    game_creation: int
    game_duration: int
    
    # KDA
    kills: int
    deaths: int
    assists: int
    kda: float
    
    # Farming
    total_minions_killed: int
    neutral_minions_killed: int # Jungle monsters
    cs_per_minute: float
    
    # Gold / Damage
    gold_earned: int
    gold_per_minute: float
    total_damage_dealt_to_champions: int
    damage_per_minute: float
    
    # Vision
    vision_score: int
    wards_placed: int
    wards_killed: int
    
    # Positions
    team_position: str # TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY

class TimelineEventDto(BaseModel):
    match_id: str
    puuid: str
    timestamp: int # Milliseconds
    type: str # CHAMPION_KILL, ELITE_MONSTER_KILL, TURRET_PLATE_DESTROYED, etc.
    
    # Details (Optional as events vary widely)
    killer_id: Optional[int] = None
    victim_id: Optional[int] = None
    position_x: Optional[int] = None
    position_y: Optional[int] = None
    
    # Specific fields for context
    item_id: Optional[int] = None
    monster_type: Optional[str] = None
    lane_type: Optional[str] = None
