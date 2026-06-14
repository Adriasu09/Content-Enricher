from dotenv import load_dotenv
import os

load_dotenv()

WIKIPEDIA_LANG = os.getenv("WIKIPEDIA_LANG", "en")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.groq.com/openai/v1")
AI_MODEL = os.getenv("AI_MODEL", "llama-3.1-8b-instant")