from typing import List, Dict, Any, Optional
from src.models import GameStatsDto, TimelineEventDto

def parse_match_to_stats(match_data: Dict[str, Any], puuid: str) -> GameStatsDto:
    info = match_data["info"]
    game_creation = info["gameCreation"]
    game_duration = info["gameDuration"]
    match_id = match_data["metadata"]["matchId"]
    
    # Find participant
    participant = next((p for p in info["participants"] if p["puuid"] == puuid), None)
    if not participant:
        raise ValueError(f"Participant with PUUID {puuid} not found in match {match_id}")

    # Calculate stats
    kills = participant["kills"]
    deaths = participant["deaths"]
    assists = participant["assists"]
    kda = (kills + assists) / max(1, deaths)
    
    cs = participant["totalMinionsKilled"] + participant["neutralMinionsKilled"]
    cs_per_min = cs / (game_duration / 60) if game_duration > 0 else 0
    
    damage = participant["totalDamageDealtToChampions"]
    damage_per_min = damage / (game_duration / 60) if game_duration > 0 else 0
    
    gold = participant["goldEarned"]
    gold_per_min = gold / (game_duration / 60) if game_duration > 0 else 0
    
    return GameStatsDto(
        match_id=match_id,
        puuid=puuid,
        champion_name=participant["championName"],
        win=participant["win"],
        game_creation=game_creation,
        game_duration=game_duration,
        kills=kills,
        deaths=deaths,
        assists=assists,
        kda=kda,
        total_minions_killed=participant["totalMinionsKilled"],
        neutral_minions_killed=participant["neutralMinionsKilled"],
        cs_per_minute=cs_per_min,
        gold_earned=gold,
        gold_per_minute=gold_per_min,
        total_damage_dealt_to_champions=damage,
        damage_per_minute=damage_per_min,
        vision_score=participant["visionScore"],
        wards_placed=participant["wardsPlaced"],
        wards_killed=participant["wardsKilled"],
        team_position=participant["teamPosition"]
    )

def parse_timeline_to_events(timeline_data: Dict[str, Any], puuid: str) -> List[TimelineEventDto]:
    match_id = timeline_data["metadata"]["matchId"]
    info = timeline_data["info"]
    frames = info["frames"]
    
    # Map participantId to PUUID to filter relevant events
    participants = info["participants"]
    participant_id_map = {p["participantId"]: p["puuid"] for p in participants}
    
    # Find our participant ID
    my_pid = next((pid for pid, p_puuid in participant_id_map.items() if p_puuid == puuid), None)
    
    events = []
    
    for frame in frames:
        for event in frame["events"]:
            # logic to filter interesting events involving the user
            # We want events where the user is the killer, victim, or assister? 
            # For MVP, let's capture strict Kills/Deaths/Objective Kills
            
            event_type = event["type"]
            timestamp = event["timestamp"]
            
            dto = TimelineEventDto(
                match_id=match_id,
                puuid=puuid,
                timestamp=timestamp,
                type=event_type,
                position_x=event.get("position", {}).get("x"),
                position_y=event.get("position", {}).get("y")
            )
            
            should_add = False
            
            if event_type == "CHAMPION_KILL":
                dto.killer_id = event.get("killerId")
                dto.victim_id = event.get("victimId")
                # Add if user involved
                if dto.killer_id == my_pid or dto.victim_id == my_pid:
                    should_add = True
                    
            elif event_type == "ELITE_MONSTER_KILL":
                dto.killer_id = event.get("killerId")
                dto.monster_type = event.get("monsterType")
                # Add if user's team involved (approximate by killerId being user)
                # Or just track all objectives for context? Let's track all objectives for now.
                should_add = True
                
            elif event_type == "TURRET_PLATE_DESTROYED" or event_type == "BUILDING_KILL":
                 # Track structures depending on noise. Let's skip for MVP unless user involved
                 if event.get("killerId") == my_pid:
                     should_add = True

            if should_add:
                events.append(dto)
                
    return events
