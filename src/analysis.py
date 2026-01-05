from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from src.models import GameStatsDto
from src.database import get_recent_games

class AnalysisReport(BaseModel):
    games_analyzed: int
    win_rate: float
    avg_kda: float
    avg_cspm: float
    avg_gold_per_min: float
    avg_vision_score: float
    
    # Simple comparison strings for MVP (e.g., "ABOVE", "BELOW")
    kda_diff: str
    cspm_diff: str
    vision_diff: str

class AnalysisEngine:
    # Hardcoded baselines for MVP (approx Gold/Plat average)
    BASELINE_KDA = 3.0
    BASELINE_CSPM = 6.5
    BASELINE_VISION = 20.0 # Dependent on role/length, but using static for MVP

    def get_user_stats(self, puuid: str, limit: int = 20) -> Optional[AnalysisReport]:
        games = get_recent_games(puuid, limit)
        if not games:
            return None
            
        count = len(games)
        wins = sum(1 for g in games if g.win)
        avg_kda = sum(g.kda for g in games) / count
        avg_cspm = sum(g.cs_per_minute for g in games) / count
        avg_gpm = sum(g.gold_per_minute for g in games) / count
        avg_vision = sum(g.vision_score for g in games) / count
        
        return AnalysisReport(
            games_analyzed=count,
            win_rate=wins / count * 100,
            avg_kda=round(avg_kda, 2),
            avg_cspm=round(avg_cspm, 2),
            avg_gold_per_min=round(avg_gpm, 2),
            avg_vision_score=round(avg_vision, 2),
            kda_diff=self._compare(avg_kda, self.BASELINE_KDA),
            cspm_diff=self._compare(avg_cspm, self.BASELINE_CSPM),
            vision_diff=self._compare(avg_vision, self.BASELINE_VISION)
        )
        
    def _compare(self, actual: float, baseline: float) -> str:
        if actual >= baseline:
            return "GOOD"
        elif actual >= baseline * 0.8:
            return "OKAY"
        else:
            return "NEEDS_IMPROVEMENT"
