"""
Somali AI Academy — Config Guud
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# OpenAI (optional — for FAQ AI agent)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Platform
COURSE_PLATFORM_URL = os.getenv("COURSE_PLATFORM_URL", "https://mfaratoon-nebvh2nc.manus.space/course")

# Schedule
NOTIFY_BEFORE_MINUTES = int(os.getenv("NOTIFY_BEFORE_MINUTES", 60))
DAILY_LESSON_TIME = os.getenv("DAILY_LESSON_TIME", "19:00")
TIMEZONE = os.getenv("TIMEZONE", "Africa/Mogadishu")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/somai.db")

# Courses file
COURSES_FILE = os.path.join(os.path.dirname(__file__), "data", "courses.json")

# Platform links
PLATFORMS = {
    "youtube": "https://m.youtube.com/user/MrFaraton",
    "telegram": "https://t.me/Farsamada",
    "whatsapp": "https://chat.whatsapp.com/BRk1xgsg4ohKAaWN7oDRIe",
    "substack": "https://mfaratoon.substack.com/",
    "facebook": "https://www.facebook.com/soomaalipodcast",
    "course": COURSE_PLATFORM_URL,
}
