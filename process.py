import argparse
import os
import json
import glob
from dotenv import load_dotenv
from src.database import init_db, save_game_stats, save_timeline_events
from src.parsing import parse_match_to_stats, parse_timeline_to_events
from src.riot import RiotClient

load_dotenv()

DATA_DIR = os.path.join(os.getcwd(), "data")

def process_data(target_puuid: str = None):
    print("Initializing Database...")
    init_db()
    
    # Try to find PUUID from args or env
    puuid = target_puuid or os.getenv("RIOT_PUUID")

    if not puuid:
        print("Error: No PUUID provided. Use --user, --puuid, or set RIOT_PUUID env var.")
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
            # Optimization: check if stats already exist? For now, overwrite/ignore is handled by DB logic (replace)
            
            # Additional check: Is this user in the match?
            # parse_match_to_stats raises error if not.
            
            print(f"Parsing Match: {match_id}...", end="")
            
            try:
                stats = parse_match_to_stats(match_data, puuid)
                save_game_stats(stats)
                print(" Done.")
            except ValueError:
                print(" Skipped (User not in match).")
            
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
    parser = argparse.ArgumentParser(description="Process raw JSON files into Database")
    parser.add_argument("--user", help="Riot ID (GameName#TagLine) to resolve PUUID")
    parser.add_argument("--puuid", help="Direct PUUID")
    args = parser.parse_args()

    resolved_puuid = args.puuid
    
    if args.user and not resolved_puuid:
        if "#" not in args.user:
            print("Error: User must be in format GameName#TagLine")
        else:
            name, tag = args.user.split("#")
            print(f"Resolving PUUID for {args.user}...")
            try:
                client = RiotClient()
                account = client.get_account_by_riot_id(name, tag)
                resolved_puuid = account["puuid"]
            except Exception as e:
                print(f"Error resolving user: {e}")
    
    process_data(resolved_puuid)
