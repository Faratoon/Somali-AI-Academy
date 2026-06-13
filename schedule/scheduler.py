"""
Scheduler — Jadwalka tooska ah ee casharada & wargelinta
Waxa uu uga baxaa background-ka (PM2, nohup, ama cron)

Isticmaal: python3 schedule/scheduler.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import logging
import asyncio
from datetime import datetime, time, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from config import BOT_TOKEN, DAILY_LESSON_TIME, TIMEZONE, NOTIFY_BEFORE_MINUTES
from agents.schedule_agent import ScheduleAgent
from agents.notify_agent import NotifyAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sched_agent = ScheduleAgent()
notify_agent = NotifyAgent()

# Load courses
COURSES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "courses.json")
with open(COURSES_FILE, "r", encoding="utf-8") as f:
    courses_data = json.load(f)

async def send_daily_lesson():
    """Dirayso casharka maalin walba"""
    lesson, course = sched_agent.get_daily_lesson(courses_data)
    text = notify_agent.format_lesson_notification(lesson, course)
    logger.info(f"Casharka maanta: {lesson['title']}")
    # Halkan waxaad ku dari kartaa inuu bot-ka u diro channel-ka
    # (waxay u baahan tahay bot instance)
    print(f"\n{'='*50}")
    print(f"📚 Casharka Maanta")
    print(f"{course['name']}")
    print(f"Cashar {lesson['number']}: {lesson['title']}")
    print(f"🔗 {lesson['link']}")
    print(f"{'='*50}\n")
    return text

async def send_weekly_schedule():
    """Dirayso jadwalka toddobaadka Axad kasta"""
    text = sched_agent.get_week_schedule(courses_data)
    logger.info("Jadwalka toddobaadka waa la diray")
    print(f"\n{'='*50}")
    print("📅 Jadwalka Toddobaadka")
    print(text)
    print(f"{'='*50}\n")
    return text

def main():
    tz = timezone(TIMEZONE)
    scheduler = AsyncIOScheduler(timezone=tz)

    # Cashar maalin walba — DAILY_LESSON_TIME
    hour, minute = DAILY_LESSON_TIME.split(":")
    scheduler.add_job(
        send_daily_lesson,
        CronTrigger(hour=int(hour), minute=int(minute), timezone=tz),
        id="daily_lesson",
        replace_existing=True
    )
    logger.info(f"Jadwalka maalinlaha ah: {DAILY_LESSON_TIME} kasta")

    # Jadwalka toddobaadka — Axad kasta 10:00 subaxnimo
    scheduler.add_job(
        send_weekly_schedule,
        CronTrigger(day_of_week="sun", hour=10, minute=0, timezone=tz),
        id="weekly_schedule",
        replace_existing=True
    )
    logger.info("Jadwalka toddobaadka: Axad kasta 10:00")

    # Start
    scheduler.start()
    logger.info(f"✅ Scheduler wuu shaqeynayaa ({TIMEZONE})")
    
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()

if __name__ == "__main__":
    main()
