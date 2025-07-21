from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2]/".env", override=False)

API_KEY = os.environ["GROQ_API_KEY"]          # raises if missing
