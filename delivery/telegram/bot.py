"""
Somali AI Academy — Telegram Bot
Bot-ka waxa uu u adeegaa sidii Course + FAQ + Schedule + Notify Agent
"""
import sys
import os

# Add repo root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler, ContextTypes
)

from config import BOT_TOKEN, COURSE_PLATFORM_URL, PLATFORMS
from agents.course_agent import CourseAgent
from agents.faq_agent import FAQAgent
from agents.schedule_agent import ScheduleAgent
from agents.notify_agent import NotifyAgent

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agents
course_agent = CourseAgent()
faq_agent = FAQAgent()
schedule_agent = ScheduleAgent()
notify_agent = NotifyAgent()

# ─── Commands ───────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Soo dhawoow ardayga cusub"""
    first_name = update.effective_user.first_name or ""
    welcome = notify_agent.format_welcome(first_name)
    
    keyboard = [
        [InlineKeyboardButton("📚 Koorsooyinka", callback_data="courses")],
        [InlineKeyboardButton("📅 Casharka Maanta", callback_data="today")],
        [InlineKeyboardButton("❓ FAQ / Su'aalo", callback_data="faq")],
        [InlineKeyboardButton("🌐 Baraha Bulshada", callback_data="platforms")],
        [InlineKeyboardButton("🔙 Sax", callback_data="cancel")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Caawimaad"""
    text = (
        "🆘 **Caawimaad**\n\n"
        "/start — Soo dhawoow\n"
        "/courses — Dhammaan koorsooyinka\n"
        "/course1 — Koorsada 1 (40 Cashar AI)\n"
        "/course2 — Koorsada 2 (Video Editing)\n"
        "/course3 — Koorsada 3 (Dropshipping)\n"
        "/course4 — Iloodheeraad & Bulshada\n"
        "/today — Casharka maanta\n"
        "/schedule — Jadwalka toddobaadka\n"
        "/faq — FAQ-yada\n"
        "/platforms — Baraha bulshada\n"
        "/search KEYWORD — Raadi cashar\n"
        "/help — Caawimaad\n\n"
        "Wax kasta oo aad qorto, waxaan ka jawaabayaa FAQ Agent!"
    )
    await update.message.reply_text(text)

async def courses_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Soo bandhig koorsooyinka"""
    text = course_agent.list_all_courses()
    
    keyboard = [
        [InlineKeyboardButton("🤖 Koorsada 1 (40 Cashar)", callback_data="course_1")],
        [InlineKeyboardButton("🎬 Koorsada 2 (Video Editing)", callback_data="course_2")],
        [InlineKeyboardButton("📦 Koorsada 3 (Dropshipping)", callback_data="course_3")],
        [InlineKeyboardButton("🌐 Koorsada 4 (Bulshada)", callback_data="course_4")],
        [InlineKeyboardButton("🔙 Sax", callback_data="cancel")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def course_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, course_id: int):
    """Show specific course"""
    text = course_agent.show_course(course_id)
    keyboard = [[InlineKeyboardButton("🔙 Koorsooyinka", callback_data="courses")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, disable_web_page_preview=False)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, disable_web_page_preview=False)

async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Casharka maanta"""
    with open(context.application.bot_data.get("courses_file", "data/courses.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    lesson, course = schedule_agent.get_daily_lesson(data)
    text = notify_agent.format_lesson_notification(lesson, course)
    await update.message.reply_text(text, disable_web_page_preview=False)

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jadwalka toddobaadka"""
    with open(context.application.bot_data.get("courses_file", "data/courses.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    text = schedule_agent.get_week_schedule(data)
    await update.message.reply_text(text, disable_web_page_preview=False)

async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FAQ-yada"""
    text = faq_agent.get_all_faqs()
    
    keyboard = [
        [InlineKeyboardButton("🔙 Sax", callback_data="cancel")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def platforms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Baraha bulshada"""
    text = (
        "🌐 **Baraha Bulshada & Platform-yada**\n\n"
        f"📺 YouTube: {PLATFORMS['youtube']}\n"
        f"✈️ Telegram: {PLATFORMS['telegram']}\n"
        f"💬 WhatsApp: {PLATFORMS['whatsapp']}\n"
        f"📝 Substack: {PLATFORMS['substack']}\n"
        f"📘 Facebook: {PLATFORMS['facebook']}\n"
        f"🎓 Course Page: {PLATFORMS['course']}"
    )
    await update.message.reply_text(text)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Raadi cashar"""
    keyword = " ".join(context.args) if context.args else ""
    if not keyword:
        await update.message.reply_text(
            "Fadlan qor keyword-ka aad raadinayso.\n"
            "Tusaale: /search chatbot"
        )
        return
    
    results = course_agent.search_lessons(keyword)
    if not results:
        await update.message.reply_text(f"❌ Waxba lagama helin '{keyword}'.")
        return
    
    text = f"🔍 Natiijooyinka '{keyword}':\n\n"
    for r in results[:5]:
        lesson = r["lesson"]
        text += f"• {r['course_name']}: Cashar {lesson['number']} — {lesson['title']}\n  {lesson['link']}\n\n"
    
    if len(results) > 5:
        text += f"...iyo {len(results) - 5} kale"
    
    await update.message.reply_text(text)

# ─── Callback Buttons ──────────────────────────────

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button clicks"""
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "cancel":
        await query.edit_message_text("✅ Waa la joojiyay. /help ku qor amarro.")
        return
    
    if data == "courses":
        text = course_agent.list_all_courses()
        keyboard = [
            [InlineKeyboardButton("🤖 Koorsada 1", callback_data="course_1")],
            [InlineKeyboardButton("🎬 Koorsada 2", callback_data="course_2")],
            [InlineKeyboardButton("📦 Koorsada 3", callback_data="course_3")],
            [InlineKeyboardButton("🌐 Koorsada 4", callback_data="course_4")],
            [InlineKeyboardButton("🔙 Sax", callback_data="cancel")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "today":
        courses_file = context.application.bot_data.get("courses_file", "data/courses.json")
        with open(courses_file, "r", encoding="utf-8") as f:
            data_json = json.load(f)
        lesson, course = schedule_agent.get_daily_lesson(data_json)
        text = notify_agent.format_lesson_notification(lesson, course)
        await query.edit_message_text(text, disable_web_page_preview=False)
        return
    
    if data == "faq":
        text = faq_agent.get_all_faqs()
        keyboard = [[InlineKeyboardButton("🔙 Sax", callback_data="cancel")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    if data == "platforms":
        text = (
            "🌐 Baraha Bulshada & Platform-yada\n\n"
            f"📺 YouTube: {PLATFORMS['youtube']}\n"
            f"✈️ Telegram: {PLATFORMS['telegram']}\n"
            f"💬 WhatsApp: {PLATFORMS['whatsapp']}\n"
            f"📝 Substack: {PLATFORMS['substack']}\n"
            f"📘 Facebook: {PLATFORMS['facebook']}\n"
            f"🎓 Course Page: {PLATFORMS['course']}"
        )
        await query.edit_message_text(text)
        return
    
    if data.startswith("course_"):
        course_id = int(data.split("_")[1])
        text = course_agent.show_course(course_id)
        keyboard = [
            [InlineKeyboardButton("🔙 Koorsooyinka", callback_data="courses")],
            [InlineKeyboardButton("🔙 Sax", callback_data="cancel")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=False)
        return

# ─── Message Handler (FAQ Agent) ────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Wixii qoraal ah — FAQ Agent ayaa ka jawaabaya"""
    text = update.message.text
    if not text:
        return
    
    # Try FAQ agent first
    answer = faq_agent.get_answer(text)
    if answer:
        keyboard = [
            [InlineKeyboardButton("❓ FAQ Dhammaan", callback_data="faq")],
            [InlineKeyboardButton("🔙 Sax", callback_data="cancel")],
        ]
        await update.message.reply_text(answer, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    # No FAQ match — offer help
    await update.message.reply_text(
        f"Fadlan isticmaal /faq si aad u aragto FAQ-yada, "
        f"ama /search KEYWORD aad u raadiso cashar.\n\n"
        f"Waxaad kaloo qori kartaa su'aashaada si cad."
    )

# ─── Main ──────────────────────────────────────────────

async def course1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await course_detail(update, context, 1)

async def course2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await course_detail(update, context, 2)

async def course3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await course_detail(update, context, 3)

async def course4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await course_detail(update, context, 4)

def main():
    if not BOT_TOKEN or BOT_TOKEN.startswith("6875"):
        print("BOT_TOKEN-ka .env-ga ku qor!")
        print(f"${BOT_TOKEN}")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    
    # Store courses file path
    courses_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "courses.json")
    app.bot_data["courses_file"] = courses_file

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("courses", courses_command))
    app.add_handler(CommandHandler("course1", course1))
    app.add_handler(CommandHandler("course2", course2))
    app.add_handler(CommandHandler("course3", course3))
    app.add_handler(CommandHandler("course4", course4))
    app.add_handler(CommandHandler("today", today_command))
    app.add_handler(CommandHandler("schedule", schedule_command))
    app.add_handler(CommandHandler("faq", faq_command))
    app.add_handler(CommandHandler("platforms", platforms_command))
    app.add_handler(CommandHandler("search", search_command))

    # Callback buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # Message handler (FAQ)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Somali AI Academy Bot wuu shaqeynayaa! Ctrl+C jooji.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
