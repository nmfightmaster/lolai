import sys
import argparse
from src.riot import RiotClient
from src.storage import save_match_data, save_timeline_data

def main():
    parser = argparse.ArgumentParser(description="Smoke test for Riot API connectivity")
    parser.add_argument("match_id", help="Match ID to fetch (e.g., NA1_500000000)")
    args = parser.parse_args()

    print(f"🔥 Starting Smoke Test for Match ID: {args.match_id}")

    try:
        client = RiotClient()
        
        print(f"1. Fetching Match: {args.match_id}...")
        match_data = client.get_match(args.match_id)
        match_path = save_match_data(args.match_id, match_data)
        print(f"   ✅ Match saved to: {match_path}")

        print(f"2. Fetching Timeline: {args.match_id}...")
        timeline_data = client.get_match_timeline(args.match_id)
        timeline_path = save_timeline_data(args.match_id, timeline_data)
        print(f"   ✅ Timeline saved to: {timeline_path}")

        print("\n✨ Smoke Test PASSED! ✨")

    except Exception as e:
        print(f"\n❌ Smoke Test FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
