"""
Course Agent — Koorsooyinka soo bandhiga & maamula
"""
import json
import os

class CourseAgent:
    """Agent-ka koorsooyinka — waxa uu ku caawinayaa ardayda inay:
    - Arkaan koorsooyinka dhigma
    - Doortaan casharo
    - Helaan faahfaahin koorsadeed"""

    def __init__(self, courses_file=None):
        if courses_file is None:
            courses_file = os.path.join(os.path.dirname(__file__), "..", "data", "courses.json")
        with open(courses_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.courses = self.data["courses"]

    def list_all_courses(self):
        """Soo bandhig dhamaan koorsooyinka"""
        lines = ["📚 **Dhamaan Koorsooyinka Somali AI Academy**\n"]
        for course in self.courses:
            lines.append(f"{course['emoji']} **{course['name']}**")
            lines.append(f"   {len(course['lessons'])} cashar — {course['type']}")
            lines.append(f"   _{course['description']}_\n")
        return "\n".join(lines)

    def get_course(self, course_id):
        """Hel koorsa gaar ah iyadoo la adeegsanayo id"""
        for course in self.courses:
            if course["id"] == course_id:
                return course
        return None

    def show_course(self, course_id):
        """Soo bandhig koorsa gaar ah iyo casharadeeda"""
        course = self.get_course(course_id)
        if not course:
            return f"❌ Koorsada ID {course_id} lama helin."

        lines = [f"{course['emoji']} **{course['name']}**\n"]
        for lesson in course["lessons"]:
            line = f"  **{lesson['number']}.** {lesson['title']}"
            if lesson.get("link"):
                line += f"\n      🔗 {lesson['link']}"
            lines.append(line)
            lines.append(f"     _{lesson['description']}_\n")
        return "\n".join(lines)

    def get_lesson(self, course_id, lesson_number):
        """Hel cashar gaar ah oo koorsada ka mid ah"""
        course = self.get_course(course_id)
        if not course:
            return None, f"❌ Koorsada ID {course_id} lama helin."
        for lesson in course["lessons"]:
            if lesson["number"] == lesson_number:
                return lesson, course["emoji"]
        return None, f"❌ Casharka {lesson_number} kuma jiro koorsadan."

    def search_lessons(self, keyword):
        """Raadi casharada kuwaas oo ku jira keyword-ka"""
        results = []
        for course in self.courses:
            for lesson in course["lessons"]:
                if keyword.lower() in lesson["title"].lower() or keyword.lower() in lesson["description"].lower():
                    results.append({
                        "course_name": course["name"],
                        "course_id": course["id"],
                        "lesson": lesson
                    })
        return results

    def get_today_lesson(self, day_index=None):
        """Hel casharka maanta (optional: adeegso index)"""
        import datetime
        # Course 1 (40 cashar) — cashar maalintii
        course1 = self.courses[0]
        total = len(course1["lessons"])
        today = day_index if day_index is not None else (datetime.date.today().timetuple().tm_yday % total)
        idx = today % total
        return course1["lessons"][idx], course1
