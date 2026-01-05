import json
import os
from typing import Any, Dict
from src.schemas import MatchDto, MatchTimelineDto

DATA_DIR = os.path.join(os.getcwd(), "data")

def save_json(filename: str, data: Dict[str, Any]) -> str:
    """
    Save dictionary data to a JSON file in the data directory.
    Returns the absolute path of the saved file.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return filepath

def save_match_data(match_id: str, match_data: Dict[str, Any]) -> str:
    """
    Validates and saves match data.
    """
    # Validation
    MatchDto.model_validate(match_data)
    
    filename = f"match_{match_id}.json"
    return save_json(filename, match_data)

def save_timeline_data(match_id: str, timeline_data: Dict[str, Any]) -> str:
    """
    Validates and saves timeline data.
    """
    # Validation
    MatchTimelineDto.model_validate(timeline_data)
    
    filename = f"timeline_{match_id}.json"
    return save_json(filename, timeline_data)
