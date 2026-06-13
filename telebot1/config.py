"""
config.py  –  Central configuration loader
Works both LOCAL (.env file) and CLOUD (Railway environment variables)
"""
import os
import json
import tempfile
from dotenv import load_dotenv

# Load .env file if it exists (local development)
load_dotenv()

# ── Telegram ──────────────────────────────────────────────────────────────────
BOT_TOKEN  = os.getenv("BOT_TOKEN", "")
ADMIN_IDS  = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# ── AI ────────────────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GROQ_API_KEY       = os.getenv("GROQ_API_KEY", "")

# ── Firebase ──────────────────────────────────────────────────────────────────
# On Railway: set FIREBASE_CREDENTIALS_JSON env var with the full JSON content
# On Local:   use FIREBASE_CREDENTIALS_PATH pointing to the JSON file

FIREBASE_DATABASE_URL = os.getenv(
    "FIREBASE_DATABASE_URL",
    "https://telebot1-b8a01-default-rtdb.firebaseio.com"
)

def get_firebase_credentials_path() -> str:
    """
    Returns path to Firebase credentials JSON.
    - If FIREBASE_CREDENTIALS_JSON env var exists (Railway/cloud): write to temp file
    - Else use FIREBASE_CREDENTIALS_PATH (local file)
    """
    json_content = os.getenv("FIREBASE_CREDENTIALS_JSON", "")
    if json_content:
        # Running on Railway – credentials stored as env variable
        try:
            cred_data = json.loads(json_content)
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            )
            json.dump(cred_data, tmp)
            tmp.close()
            return tmp.name
        except Exception as e:
            print(f"[Config] Firebase JSON parse error: {e}")

    # Running locally – use file path
    return os.getenv("FIREBASE_CREDENTIALS_PATH", "data/firebase_credentials.json")

FIREBASE_CREDENTIALS_PATH = get_firebase_credentials_path()

# ── Limits ────────────────────────────────────────────────────────────────────
DAILY_MSG_LIMIT   = int(os.getenv("DAILY_MSG_LIMIT",   40))
MAX_MEDIA_SIZE_MB = int(os.getenv("MAX_MEDIA_SIZE_MB",  5))
MAX_MEDIA_SIZE_B  = MAX_MEDIA_SIZE_MB * 1024 * 1024

# ── Premium ───────────────────────────────────────────────────────────────────
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", 30))

# ── Links ─────────────────────────────────────────────────────────────────────
COURSE_CHANNEL   = os.getenv("COURSE_CHANNEL",   "https://t.me/yourchannel")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "@Mfaratoon")
WEBSITE_URL      = os.getenv("WEBSITE_URL",      "https://yourwebsite.com")

# ── AI System Prompt ──────────────────────────────────────────────────────────
AI_SYSTEM_PROMPT = """You are an intelligent AI assistant specialized in helping students 
learn AI automation, chatbot development, web design, and online courses taught by Mfaratoon.

Your knowledge includes:
- AI tools: ChatGPT, Midjourney, Sora, Flux, Veo, Nano Banana
- Automation: n8n, Make.com, Zapier
- Chatbot builders: Botpress, Chatfuel, ManyChat, ChatSail, Chatbase, JotForm
- Telegram bot development with Python
- Web design and editing
- OpenRouter, Groq AI APIs

When answering:
1. Be helpful, encouraging, and friendly
2. Share relevant course resources when applicable
3. Always respond in the language the user writes in (Somali, Arabic, or English)
4. Keep answers concise but complete
5. Add relevant emojis to make responses engaging
6. If asked about courses, mention Mfaratoon's 40+ FREE courses
"""
