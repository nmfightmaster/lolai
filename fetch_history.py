import os
import argparse
import time
from typing import List
from src.riot import RiotClient
from src.storage import save_match_data, save_timeline_data

def get_puuid_from_env() -> str:
    # In a real app we might fetch this from Summoner Name if not in env
    # But user said it's in .env
    puuid = os.getenv("RIOT_PUUID")
    if not puuid:
        raise ValueError("RIOT_PUUID not found in environment variables.")
    return puuid

def file_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(os.getcwd(), "data", filename))

def fetch_history(count: int = 20):
    client = RiotClient()
    puuid = get_puuid_from_env()
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

                # Fetch Timeline
                timeline_data = client.get_match_timeline(match_id)
                save_timeline_data(match_id, timeline_data)
                
                print(f"   -> Saved.")
            except Exception as e:
                print(f"   -> Error fetching {match_id}: {e}")
                
            # Respect rate limits between calls if needed, though requests are sequential and client handles 429s.
            # A small sleep might be nice to be polite if we are aggressive, but client handles headers.
            
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
    args = parser.parse_args()

    try:
        fetch_history(count=args.count)
    except Exception as e:
        print(f"Error: {e}")
