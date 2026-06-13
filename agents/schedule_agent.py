"""
Schedule Agent — Jadwalka casharada & wargelinta
"""
import datetime
import json
import os

class ScheduleAgent:
    """Agent-ka jadwalka — waxa uu qorsheeyaa:
    - Casharka maalin kasta (mid koorsada 1 ka mid ah)
    - Wargelinta ardayda (notifications)
    - Jadwalka tooska ah"""

    def __init__(self):
        self.weekdays_so = ["Isniin", "Talaado", "Arbaco", "Khamiis", "Jimce", "Sabti", "Axad"]

    def get_daily_lesson(self, courses_data):
        """Hel casharka maanta — Course 1 oo ah 40 cashar"""
        courses = courses_data["courses"]
        course1 = courses[0]  # 40 Cashar AI
        total = len(course1["lessons"])
        # Isticmaal maalinta sanadka si loo helo casharka maanta
        today = datetime.date.today()
        day_of_year = today.timetuple().tm_yday
        lesson_idx = (day_of_year - 1) % total
        lesson = course1["lessons"][lesson_idx]
        return lesson, course1

    def get_week_schedule(self, courses_data, start_date=None):
        """Soo bandhig jadwalka toddobaadka"""
        if start_date is None:
            start_date = datetime.date.today()
        
        courses = courses_data["courses"]
        course1 = courses[0]
        total = len(course1["lessons"])
        
        day_of_year = start_date.timetuple().tm_yday
        lines = [f"📅 **Jadwalka Toddobaadka** (laga bilaabo {start_date})\n"]
        
        for i in range(7):
            date = start_date + datetime.timedelta(days=i)
            weekday = self.weekdays_so[date.weekday()]
            lesson_idx = (day_of_year + i - 1) % total
            lesson = course1["lessons"][lesson_idx]
            lines.append(f"  **{weekday}, {date}**")
            lines.append(f"  Cashar {lesson['number']}: {lesson['title']}")
            lines.append(f"  🔗 {lesson['link']}\n")
        
        return "\n".join(lines)

    def get_course_schedule(self, course, start_day=1):
        """Soo bandhig jadwalka koorsada oo dhan"""
        lines = [f"📋 **Jadwalka Koorsada:** {course['name']}\n"]
        for lesson in course["lessons"]:
            lines.append(f"  Maalin {lesson['number']}: {lesson['title']}")
        return "\n".join(lines)
