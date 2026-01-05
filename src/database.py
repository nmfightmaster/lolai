import sqlite3
import os
from typing import List, Optional
from src.models import GameStatsDto, TimelineEventDto

DB_NAME = "lolai.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Game Stats Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS game_stats (
            match_id TEXT,
            puuid TEXT,
            champion_name TEXT,
            win BOOLEAN,
            game_creation INTEGER,
            game_duration INTEGER,
            
            kills INTEGER,
            deaths INTEGER,
            assists INTEGER,
            kda REAL,
            
            total_minions_killed INTEGER,
            neutral_minions_killed INTEGER,
            cs_per_minute REAL,
            
            gold_earned INTEGER,
            gold_per_minute REAL,
            total_damage_dealt_to_champions INTEGER,
            damage_per_minute REAL,
            
            vision_score INTEGER,
            wards_placed INTEGER,
            wards_killed INTEGER,
            
            team_position TEXT,
            
            PRIMARY KEY (match_id, puuid)
        )
    ''')
    
    # Timeline Events Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS timeline_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id TEXT,
            puuid TEXT,
            timestamp INTEGER,
            type TEXT,
            
            killer_id INTEGER,
            victim_id INTEGER,
            position_x INTEGER,
            position_y INTEGER,
            
            item_id INTEGER,
            monster_type TEXT,
            lane_type TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_game_stats(stats: GameStatsDto):
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT OR REPLACE INTO game_stats (
            match_id, puuid, champion_name, win, game_creation, game_duration,
            kills, deaths, assists, kda,
            total_minions_killed, neutral_minions_killed, cs_per_minute,
            gold_earned, gold_per_minute, total_damage_dealt_to_champions, damage_per_minute,
            vision_score, wards_placed, wards_killed, team_position
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        stats.match_id, stats.puuid, stats.champion_name, stats.win, stats.game_creation, stats.game_duration,
        stats.kills, stats.deaths, stats.assists, stats.kda,
        stats.total_minions_killed, stats.neutral_minions_killed, stats.cs_per_minute,
        stats.gold_earned, stats.gold_per_minute, stats.total_damage_dealt_to_champions, stats.damage_per_minute,
        stats.vision_score, stats.wards_placed, stats.wards_killed, stats.team_position
    ))
    
    conn.commit()
    conn.close()

def save_timeline_events(events: List[TimelineEventDto]):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Batch insert for performance
    data_to_insert = [
        (e.match_id, e.puuid, e.timestamp, e.type, e.killer_id, e.victim_id, e.position_x, e.position_y, e.item_id, e.monster_type, e.lane_type)
        for e in events
    ]
    
    c.executemany('''
        INSERT INTO timeline_events (
            match_id, puuid, timestamp, type,
            killer_id, victim_id, position_x, position_y,
            item_id, monster_type, lane_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data_to_insert)
    
    conn.commit()
    conn.close()

def get_recent_games(puuid: str, limit: int = 20) -> List[GameStatsDto]:
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM game_stats 
        WHERE puuid = ? 
        ORDER BY game_creation DESC 
        LIMIT ?
    ''', (puuid, limit))
    
    rows = c.fetchall()
    conn.close()
    
    return [
        GameStatsDto(
            match_id=row['match_id'],
            puuid=row['puuid'],
            champion_name=row['champion_name'],
            win=bool(row['win']),
            game_creation=row['game_creation'],
            game_duration=row['game_duration'],
            kills=row['kills'],
            deaths=row['deaths'],
            assists=row['assists'],
            kda=row['kda'],
            total_minions_killed=row['total_minions_killed'],
            neutral_minions_killed=row['neutral_minions_killed'],
            cs_per_minute=row['cs_per_minute'],
            gold_earned=row['gold_earned'],
            gold_per_minute=row['gold_per_minute'],
            total_damage_dealt_to_champions=row['total_damage_dealt_to_champions'],
            damage_per_minute=row['damage_per_minute'],
            vision_score=row['vision_score'],
            wards_placed=row['wards_placed'],
            wards_killed=row['wards_killed'],
            team_position=row['team_position']
        ) for row in rows
    ]

def get_timeline_events(match_id: str, puuid: str) -> List[TimelineEventDto]:
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM timeline_events 
        WHERE match_id = ? AND puuid = ?
        ORDER BY timestamp ASC
    ''', (match_id, puuid))
    
    rows = c.fetchall()
    conn.close()
    
    return [
        TimelineEventDto(
            match_id=row['match_id'],
            puuid=row['puuid'],
            timestamp=row['timestamp'],
            type=row['type'],
            killer_id=row['killer_id'],
            victim_id=row['victim_id'],
            position_x=row['position_x'],
            position_y=row['position_y'],
            item_id=row['item_id'],
            monster_type=row['monster_type'],
            lane_type=row['lane_type']
        ) for row in rows
    ]
