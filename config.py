"""
Somali AI Academy — Config Guud
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Telegram (supports both BOT_TOKEN and TELEGRAM_BOT_TOKEN)
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN", "")

# AI Providers
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY", "") or os.getenv("OPENAI_API_KEY", "")

# Platform
COURSE_PLATFORM_URL = os.getenv("COURSE_PLATFORM_URL", "https://mfaratoon-nebvh2nc.manus.space/course")
WEBSITE_URL = os.getenv("WEBSITE_URL", "https://hibomusic.com")

# Social Links
PLATFORMS = {
    "youtube": os.getenv("YOUTUBE_URL", "https://m.youtube.com/user/MrFaraton"),
    "telegram": os.getenv("TELEGRAM_CHANNEL", "https://t.me/Farsamada"),
    "whatsapp": os.getenv("WHATSAPP_COMMUNITY_URL", "https://chat.whatsapp.com/example_link"),
    "substack": os.getenv("SUBSTACK_URL", "https://mfaratoon.substack.com/"),
    "facebook": os.getenv("FACEBOOK_URL", "https://www.facebook.com/soomaalipodcast"),
    "course": COURSE_PLATFORM_URL,
    "website": WEBSITE_URL,
}

# Schedule
NOTIFY_BEFORE_MINUTES = int(os.getenv("NOTIFY_BEFORE_MINUTES", 60))
DAILY_LESSON_TIME = os.getenv("DAILY_LESSON_TIME", "19:00")
TIMEZONE = os.getenv("TIMEZONE", "Africa/Mogadishu")
DAILY_MSG_LIMIT = int(os.getenv("DAILY_MSG_LIMIT", 40))
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", 60))

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/somai.db")

# Firebase (optional)
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "data/firebase_credentials.json")
FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", "")

# Courses file
COURSES_FILE = os.path.join(os.path.dirname(__file__), "data", "courses.json")

# Admin
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "@Mfaratoon")
