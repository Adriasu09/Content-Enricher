from dotenv import load_dotenv
import os

load_dotenv()

WIKIPEDIA_LANG = os.getenv("WIKIPEDIA_LANG", "en")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")