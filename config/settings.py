from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "whisper-large-v3")
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "fa")
BOT_MODE = os.getenv("BOT_MODE", "polling")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing.")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
