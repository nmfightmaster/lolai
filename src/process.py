import os
import json
import glob
from dotenv import load_dotenv
from src.database import init_db, save_game_stats, save_timeline_events
from src.parsing import parse_match_to_stats, parse_timeline_to_events

load_dotenv()

DATA_DIR = os.path.join(os.getcwd(), "data")

def get_puuid_from_match_file(match_data: dict) -> str:
    # We need to know WHICH participant is the user to extract stats.
    # In a real app we'd pass the PUUID in.
    # For now, let's assume valid PUUID is in env or derived.
    # Actually, we should probably pass PUUID as arg to the script.
    # BUT, to make it easy, let's just grab the PUUID from the .env if available
    return os.getenv("RIOT_PUUID")

def process_data():
    print("Initializing Database...")
    init_db()
    
    puuid = os.getenv("RIOT_PUUID")
    if not puuid:
        print("Error: RIOT_PUUID not found in environment.")
        return

    print(f"Processing data for PUUID: {puuid}")
    
    # 1. Process Matches
    match_files = glob.glob(os.path.join(DATA_DIR, "match_*.json"))
    print(f"Found {len(match_files)} match files.")
    
    for match_file in match_files:
        try:
            with open(match_file, 'r') as f:
                match_data = json.load(f)
            
            match_id = match_data["metadata"]["matchId"]
            print(f"Parsing Match: {match_id}...", end="")
            
            stats = parse_match_to_stats(match_data, puuid)
            save_game_stats(stats)
            print(" Done.")
            
        except Exception as e:
            print(f" Failed: {e}")

    # 2. Process Timelines
    timeline_files = glob.glob(os.path.join(DATA_DIR, "timeline_*.json"))
    print(f"Found {len(timeline_files)} timeline files.")
    
    for timeline_file in timeline_files:
        try:
            with open(timeline_file, 'r') as f:
                timeline_data = json.load(f)
                
            match_id = timeline_data["metadata"]["matchId"]
            print(f"Parsing Timeline: {match_id}...", end="")
            
            events = parse_timeline_to_events(timeline_data, puuid)
            save_timeline_events(events)
            print(f" Done ({len(events)} events).")
            
        except Exception as e:
            print(f" Failed: {e}")

if __name__ == "__main__":
    process_data()
