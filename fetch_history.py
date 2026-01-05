import os
import argparse
import time
from typing import List
from src.riot import RiotClient
from src.storage import save_match_data, save_timeline_data
from src.database import init_db, save_game_stats, save_timeline_events
from src.parsing import parse_match_to_stats, parse_timeline_to_events

def get_puuid_from_env() -> str:
    # In a real app we might fetch this from Summoner Name if not in env
    # But user said it's in .env
    puuid = os.getenv("RIOT_PUUID")
    if not puuid:
        raise ValueError("RIOT_PUUID not found in environment variables.")
    return puuid

def file_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(os.getcwd(), "data", filename))

def fetch_history(puuid: str, count: int = 20):
    init_db()
    client = RiotClient()
    print(f"Fetching last {count} matches for PUUID: {puuid}...")

    matches_fetched = 0
    start_index = 0
    batch_size = 100 # Max allowed by Riot is 100

    while matches_fetched < count:
        current_batch_size = min(batch_size, count - matches_fetched)
        print(f" Requesting batch: start={start_index}, count={current_batch_size}")
        
        match_ids = client.get_match_ids_by_puuid(puuid, start=start_index, count=current_batch_size)
        
        if not match_ids:
            print("No more matches found.")
            break

        print(f" Found {len(match_ids)} match IDs.")

        for match_id in match_ids:
            # Check for existing
            if file_exists(f"match_{match_id}.json") and file_exists(f"timeline_{match_id}.json"):
                print(f"  [Skipping] {match_id} (already exists)")
                matches_fetched += 1
                continue

            print(f"  [Fetching] {match_id}...")
            
            try:
                # Fetch Match
                match_data = client.get_match(match_id)
                save_match_data(match_id, match_data)

                # Parse & Save Match Stats
                try:
                    stats = parse_match_to_stats(match_data, puuid)
                    save_game_stats(stats)
                except ValueError as ve:
                     print(f"   -> Info: {ve} (User likely not in this match)")
                except Exception as pe:
                     print(f"   -> Warning: Failed to parse stats: {pe}")

                # Fetch Timeline
                timeline_data = client.get_match_timeline(match_id)
                save_timeline_data(match_id, timeline_data)
                
                # Parse & Save Events
                try:
                    events = parse_timeline_to_events(timeline_data, puuid)
                    save_timeline_events(events)
                except Exception as pe:
                    print(f"   -> Warning: Failed to parse events: {pe}")
                
                print(f"   -> Saved & Processed.")
            except Exception as e:
                print(f"   -> Error fetching/processing {match_id}: {e}")
                
            matches_fetched += 1
            if matches_fetched >= count:
                break
        
        start_index += len(match_ids)
        
        # Stop if we got fewer than requested (end of history)
        if len(match_ids) < current_batch_size:
             break

    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch League of Legends match history.")
    parser.add_argument("--count", type=int, default=20, help="Number of matches to fetch")
    parser.add_argument("--user", help="Riot ID (GameName#TagLine)")
    parser.add_argument("--puuid", help="Direct PUUID")
    args = parser.parse_args()

    client = RiotClient()
    target_puuid = None

    try:
        if args.puuid:
            target_puuid = args.puuid
        elif args.user:
            if "#" not in args.user:
                raise ValueError("User must be in format GameName#TagLine")
            name, tag = args.user.split("#")
            print(f"Resolving PUUID for {args.user}...")
            account = client.get_account_by_riot_id(name, tag)
            target_puuid = account["puuid"]
        else:
            # Fallback to env
            target_puuid = get_puuid_from_env()

        fetch_history(puuid=target_puuid, count=args.count)
    except Exception as e:
        print(f"Error: {e}")
