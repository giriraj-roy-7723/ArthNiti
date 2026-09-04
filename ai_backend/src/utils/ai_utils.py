import os
from google import genai

from dotenv import load_dotenv
load_dotenv() 

def get_gemini_client() -> genai.Client:

    """Initializes and returns the Gemini client."""
    key = os.getenv("GEMINI_API_KEY")

    if not key:
        raise ValueError("Missing 'GEMINI_API_KEY'. Set it as an environment variable.")
    return genai.Client(api_key=key)
