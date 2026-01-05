from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

class MatchMetadata(BaseModel):
    dataVersion: str
    matchId: str
    participants: List[str]

    model_config = ConfigDict(extra='ignore')

class MatchInfo(BaseModel):
    gameCreation: int
    gameDuration: int
    gameId: int
    gameMode: str
    participants: List[Dict[str, Any]] # Keeping detailed participant validation flexible for now

    model_config = ConfigDict(extra='ignore')

class MatchDto(BaseModel):
    metadata: MatchMetadata
    info: MatchInfo

    model_config = ConfigDict(extra='ignore')

class MatchTimelineDto(BaseModel):
    metadata: MatchMetadata
    info: Dict[str, Any] # Timeline info is complex, treating as dict for step 1

    model_config = ConfigDict(extra='ignore')
