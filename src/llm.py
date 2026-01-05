import os
from google import genai
from typing import List, Optional
from src.models import GameStatsDto, TimelineEventDto

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=self.api_key)

    def generate_match_summary(self, stats: GameStatsDto, events: List[TimelineEventDto]) -> str:
        """
        Generates a text summary of the match using the LLM.
        """
        prompt = self._construct_prompt(stats, events)
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def _construct_prompt(self, stats: GameStatsDto, events: List[TimelineEventDto]) -> str:
        stats_text = (
            f"Match ID: {stats.match_id}\n"
            f"Champion: {stats.champion_name}\n"
            f"Result: {'Win' if stats.win else 'Loss'}\n"
            f"Duration: {stats.game_duration // 60}m {stats.game_duration % 60}s\n"
            f"KDA: {stats.kills}/{stats.deaths}/{stats.assists} ({stats.kda:.2f})\n"
            f"CS: {stats.total_minions_killed + stats.neutral_minions_killed} ({stats.cs_per_minute:.1f}/min)\n"
            f"Gold: {stats.gold_earned} ({stats.gold_per_minute:.0f}/min)\n"
            f"Damage: {stats.total_damage_dealt_to_champions} ({stats.damage_per_minute:.0f}/min)\n"
            f"Vision Score: {stats.vision_score}\n"
            f"Position: {stats.team_position}\n"
        )

        # Filter events for brevity but give enough context
        # We'll take first 10 mins events + all kills involving user + obj kills
        events_text = "Key Timeline Events:\n"
        for event in events:
            # Simple formatter
            timestamp = f"{event.timestamp // 60000}m{int((event.timestamp % 60000) / 1000)}s"
            if event.type == "CHAMPION_KILL":
                actor = "User" if event.killer_id == self._get_pid_from_puuid(events, stats.puuid) else "Enemy" 
                # Note: getting pid is tricky without extra info, but let's assume events passed are already filtered/processed or
                # we just describe "Killer ID {x} killed Victim ID {y}"
                # Actually, TimelineEventDto has killer_id/victim_id but not mapped to names.
                # Steps 3/4 logic should handles this? 
                # Let's just dump raw event for now, LLM can figure out patterns if we are consistent.
                # Better: describe relative to user.
                
                # Wait, TimelineEventDto doesn't have easy lookup for "My PID" unless we passed it.
                # But stats has `puuid`.
                pass
            
            events_text += f"- {timestamp}: {event.type} (Killer: {event.killer_id}, Victim: {event.victim_id})\n"
        
        # Simpler prompting for MVP - just dump the stats and ask for analysis
        prompt = (
            "You are a helpful League of Legends coach. Analyze this match performance based on the specific statistics provided below.\n"
            "Identify why the game was won or lost based on the metrics compared to standard benchmarks.\n"
            "Be concise, encouraging, but direct about mistakes if stats show them (e.g. low CS, high deaths).\n\n"
            "GAME STATS:\n"
            f"{stats_text}\n\n"
            "Provide a 3-sentence summary of the performance."
        )
        return prompt

    def _get_pid_from_puuid(self, events: List[TimelineEventDto], puuid: str) -> Optional[int]:
        # Helper not fully possible with just Event DTO unless we stuck pid in there?
        # Re-checking models.py... TimelineEventDto has puuid.
        # But killer_id is an Int (participantId).
        # We need the map.
        # For this MVP, let's rely just on the Stats summary which is rich enough for a basic coaching comment.
        pass
