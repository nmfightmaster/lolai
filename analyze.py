import argparse
import sys
from src.riot import RiotClient
from src.analysis import AnalysisEngine

def main():
    parser = argparse.ArgumentParser(description="Analyze League of Legends performance")
    parser.add_argument("--user", help="Riot ID (GameName#TagLine)")
    parser.add_argument("--puuid", help="Direct PUUID to analyze")
    parser.add_argument("--limit", type=int, default=20, help="Number of games to analyze")
    args = parser.parse_args()

    if not args.user and not args.puuid:
        print("Error: Must provide either --user or --puuid")
        sys.exit(1)

    puuid = args.puuid
    
    if args.user:
        if "#" not in args.user:
            print("Error: User must be in format GameName#TagLine")
            sys.exit(1)

        name, tag = args.user.split("#")
        
        print(f"Resolving PUUID for {args.user}...")
        client = RiotClient()
        try:
            account = client.get_account_by_riot_id(name, tag)
            puuid = account["puuid"]
        except Exception as e:
            print(f"Error fetching PUUID: {e}")
            sys.exit(1)

    print(f"Analyzing last {args.limit} games for PUUID: {puuid}...")
    
    engine = AnalysisEngine()
    report = engine.get_user_stats(puuid, args.limit)
    
    if not report:
        print("No games found in database. Run fetch_history.py first.")
        sys.exit(0)
        
    print("\n" + "="*40)
    print(f"ANALYSIS REPORT: {args.user}")
    print("="*40)
    print(f"Games Analyzed: {report.games_analyzed}")
    print(f"Win Rate:       {report.win_rate:.1f}%")
    print("-" * 20)
    print(f"KDA:            {report.avg_kda} ({report.kda_diff})")
    print(f"CSPM:           {report.avg_cspm} ({report.cspm_diff})")
    print(f"Vision Score:   {report.avg_vision_score} ({report.vision_diff})")
    print(f"Gold/Min:       {report.avg_gold_per_min}")
    print("="*40)

if __name__ == "__main__":
    main()
