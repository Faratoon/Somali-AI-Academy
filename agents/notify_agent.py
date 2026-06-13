"""
Notify Agent — Ardayda u soo dira wargelin (notifications)
"""
import datetime
import json
import os

class NotifyAgent:
    """Agent-ka wargelinta — waxa uu u soo dirayaa ardayda:
    - Casharka cusub marka la soo dhigay
    - Wargelin ka hor casharka (X min ka hor)
    - Xusuusin Toddobaadle ah
    - Live sessions-ka"""

    def __init__(self, bot=None):
        self.bot = bot  # Telegram bot instance

    def format_lesson_notification(self, lesson, course):
        """Samee qaabka wargelinta casharka"""
        return (
            f"📚 Casharka Maanta\n\n"
            f"{course['name']}\n"
            f"Cashar {lesson['number']}: {lesson['title']}\n\n"
            f"{lesson['description']}\n\n"
            f"🔗 {lesson['link']}\n\n"
            f"#SomaliAI #Cashar{lesson['number']}"
        )

    def format_reminder(self, lesson, course, minutes_before=60):
        """Samee qaabka xusuusinta"""
        return (
            f"⏰ Xusuusin: {minutes_before} daqiiqo oo kAL"
            f"Cashar kale ayaa soo socda!\n\n"
            f"Cashar {lesson['number']}: {lesson['title']}\n"
            f"🔗 {lesson['link']}"
        )

    def format_live_notification(self, title, link, time):
        """Samee qaabka wargelinta tooska ah (Live)"""
        return (
            f"🔴 Bandhig Tos ah!\n\n"
            f"{title}\n"
            f"Waqtiga: {time}\n\n"
            f"🔗 {link}\n\n"
            f"Halkan nagala soo qaybgal!"
        )

    def format_week_summary(self, courses_data):
        """Samee qaabka soo koobida toddobaadka"""
        from agents.schedule_agent import ScheduleAgent
        sched = ScheduleAgent()
        return sched.get_week_schedule(courses_data)

    def format_welcome(self, first_name):
        """Samee qaabka soo dhawaynta ardayga cusub"""
        return (
            f"Salaam {first_name}! 👋\n\n"
            f"Kusoo dhawow Somali AI Academy — machadka AI-ga ee af-Soomaali ah!\n\n"
            f"Halkan waxaad ka helaysaa:\n"
            f"🤖 40 Cashar oo AI ah (Chatbot, Prompt, Tools)\n"
            f"🎬 AI Video Editing\n"
            f"📦 Dropshipping + AI\n\n"
            f"Amarada:\n"
            f"/courses — Dhammaan koorsooyinka\n"
            f"/course1 — Koorsada 1 (40 Cashar AI)\n"
            f"/course2 — Koorsada 2 (Video Editing)\n"
            f"/course3 — Koorsada 3 (Dropshipping)\n"
            f"/today — Casharka maanta\n"
            f"/schedule — Jadwalka toddobaadka\n"
            f"/faq — FAQ-yada\n"
            f"/platforms — Baraha bulshada\n"
            f"/help — Caawimaad\n\n"
            f"Wax kasta oo aad weydiiso, FAQ Agent-ka ayaa kaaga jawaabaya!"
        )
