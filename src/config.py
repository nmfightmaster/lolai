import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_riot_api_key() -> str:
    """
    Retrieve the Riot API key from environment variables.
    Raises ValueError if not found.
    """
    key = os.getenv("RIOT_API_KEY")
    if not key:
        raise ValueError("RIOT_API_KEY environment variable is not set")
    return key
