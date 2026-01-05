import time
import httpx
from typing import Any, Dict, List, Optional
from src.config import get_riot_api_key

class RiotClient:
    """
    Minimal Riot API Client using httpx.
    """
    def __init__(self, region: str = "americas", platform: str = "na1"):
        self.api_key = get_riot_api_key()
        self.region = region
        self.platform = platform
        self.base_url_region = f"https://{region}.api.riotgames.com"
        self.base_url_platform = f"https://{platform}.api.riotgames.com"
        self.headers = {
            "X-Riot-Token": self.api_key
        }

    def _get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Internal method to make GET requests.
        Handles 429 Rate Limited responses by sleeping.
        """
        while True:
            with httpx.Client(headers=self.headers) as client:
                response = client.get(url, params=params)
                
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 1))
                    print(f"Rate limited. Sleeping for {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response.json()

    def get_account_by_riot_id(self, game_name: str, tag_line: str) -> Dict[str, Any]:
        """
        Get account information by Riot ID.
        Endpoint: /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}
        """
        url = f"{self.base_url_region}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return self._get(url)

    def get_match_ids_by_puuid(
        self, 
        puuid: str, 
        start: int = 0, 
        count: int = 20, 
        queue: Optional[int] = None, 
        type: Optional[str] = None
    ) -> List[str]:
        """
        Get a list of match IDs by PUUID.
        Endpoint: /lol/match/v5/matches/by-puuid/{puuid}/ids
        """
        url = f"{self.base_url_region}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {
            "start": start,
            "count": count
        }
        if queue:
            params["queue"] = queue
        if type:
            params["type"] = type
            
        # The API returns a list of strings, not a dict
        return self._get(url, params=params)

    def get_match(self, match_id: str) -> Dict[str, Any]:
        """
        Get match details by match ID.
        Endpoint: /lol/match/v5/matches/{matchId}
        """
        url = f"{self.base_url_region}/lol/match/v5/matches/{match_id}"
        return self._get(url)

    def get_match_timeline(self, match_id: str) -> Dict[str, Any]:
        """
        Get match timeline by match ID.
        Endpoint: /lol/match/v5/matches/{matchId}/timeline
        """
        url = f"{self.base_url_region}/lol/match/v5/matches/{match_id}/timeline"
        return self._get(url)
