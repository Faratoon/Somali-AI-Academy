"""
Quiz Generator — Sameeya quiz-yo AI ah oo ku saabsan casharada

Waxa uu isticmaalaa OpenAI API (haddii uu jiro) si uu u sameeyo
su'aalo ku salaysan cashar kasta.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import random
from config import OPENAI_API_KEY

COURSES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "courses.json")

class QuizGenerator:
    """Samee quiz-yo ku salaysan casharada"""
    
    def __init__(self):
        with open(COURSES_FILE, "r", encoding="utf-8") as f:
            self.courses = json.load(f)["courses"]
    
    def generate_manual_quiz(self, course_id, count=5):
        """Samee quiz gacanta lagu sameeyay (OpenAI la'aan)"""
        course = None
        for c in self.courses:
            if c["id"] == course_id:
                course = c
                break
        
        if not course:
            return f"Koorsada {course_id} lama helin."
        
        lessons = course["lessons"]
        selected = random.sample(lessons, min(count, len(lessons)))
        
        lines = [f"📝 **Quiz: {course['name']}**\n"]
        for i, lesson in enumerate(selected, 1):
            lines.append(f"**Su'aal {i}:** Maxaad ka baran kartaa '{lesson['title']}'?\n")
        
        lines.append(f"\nJawaabaha:\n🔗 {lesson['link']}")
        return "\n".join(lines)
    
    def generate_ai_quiz(self, course_id, count=5):
        """Samee quiz iyadoo la adeegsanayo OpenAI"""
        if not OPENAI_API_KEY:
            return self.generate_manual_quiz(course_id, count)
        
        course = None
        for c in self.courses:
            if c["id"] == course_id:
                course = c
                break
        
        if not course:
            return f"Koorsada {course_id} lama helin."
        
        # Halkan ku dar OpenAI API si loo sameeyo su'aalo
        return "🤖 AI Quiz wuxuu u baahan yahay OPENAI_API_KEY"
    
    def quiz_all(self):
        """Samee quiz koorsooyinka oo dhan"""
        results = []
        for course in self.courses:
            quiz = self.generate_manual_quiz(course["id"], 2)
            results.append(quiz)
        return "\n\n".join(results)
