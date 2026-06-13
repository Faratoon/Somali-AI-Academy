"""
WhatsApp Bot — Somali AI Academy
Waa qaab sahlan oo WhatsApp-ka loogu gudbiyo casharada.
Waxay u baahan tahay: twilio API ama whatsapp-web.js

Isticmaal: https://www.twilio.com/whatsapp
Ama: https://github.com/pedroslopez/whatsapp-web.js
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import logging
from config import WHATSAPP_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COURSES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "courses.json")

class WhatsAppBot:
    """WhatsApp bot-ka — wuxuu u dirayaa casharada WhatsApp-ka"""
    
    def __init__(self):
        self.api_key = WHATSAPP_API_KEY
        with open(COURSES_FILE, "r", encoding="utf-8") as f:
            self.courses_data = json.load(f)
    
    def send_message(self, to_number, message):
        """U dir fariin WhatsApp-ka (API baahan)"""
        # Halkan ku dar Twilio API ama baashaal
        # https://www.twilio.com/docs/whatsapp/quickstart/python
        logger.info(f"Fariin loo diray {to_number}")
        print(f"📱 WhatsApp -> {to_number}")
        print(f"   {message[:100]}...")
        return True
    
    def send_daily_lesson(self, to_number):
        """Dirayso casharka maanta"""
        from agents.schedule_agent import ScheduleAgent
        from agents.notify_agent import NotifyAgent
        
        sched = ScheduleAgent()
        notif = NotifyAgent()
        lesson, course = sched.get_daily_lesson(self.courses_data)
        msg = notif.format_lesson_notification(lesson, course)
        return self.send_message(to_number, msg)
    
    def send_course_link(self, to_number, course_name):
        """Dirayso link-ka koorsada"""
        msg = f"Koorsada {course_name} waxaad ka helaysaa: {COURSE_PLATFORM_URL}"
        return self.send_message(to_number, msg)

if __name__ == "__main__":
    print("✅ WhatsApp Bot ready — ku xidh Twilio ama whatsapp-web.js")
