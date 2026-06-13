"""
Somali AI Academy — Telegram Bot v2
Qaab cusub: Menu qurux badan, Back button, Daily lessons, Talk Human/Bot
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
import logging
from datetime import date
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler, ContextTypes
)
import httpx

from config import BOT_TOKEN, PLATFORMS
from agents.course_agent import CourseAgent
from agents.faq_agent import FAQAgent
from agents.schedule_agent import ScheduleAgent
from agents.notify_agent import NotifyAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

course_agent = CourseAgent()
faq_agent = FAQAgent()
sched_agent = ScheduleAgent()
notify_agent = NotifyAgent()

# ─── User daily trackers ─────────────────────────
user_daily_lessons = defaultdict(lambda: {"date": "", "count": 0})
user_daily_ai = defaultdict(lambda: {"date": "", "count": 0})
DAILY_LESSON_LIMIT = 2
DAILY_AI_LIMIT = 15

def check_limit(tracker, user_id, limit):
    today = str(date.today())
    data = tracker[user_id]
    if data["date"] != today:
        data["date"] = today
        data["count"] = 0
    return data["count"] < limit

def increment(tracker, user_id):
    today = str(date.today())
    data = tracker[user_id]
    if data["date"] != today:
        data["date"] = today
        data["count"] = 0
    data["count"] += 1

# ─── Main Menu ────────────────────────────────────────
MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("🤖 Talk to Bot (AI)", callback_data="talk_bot")],
    [InlineKeyboardButton("👨‍💻 Talk to Human", callback_data="talk_human")],
    [InlineKeyboardButton("📚 Koorsooyinka", callback_data="courses"),
     InlineKeyboardButton("📅 Casharka Maanta", callback_data="today")],
    [InlineKeyboardButton("🛂 Contacts", callback_data="contacts"),
     InlineKeyboardButton("❓ More Info", callback_data="more_info")],
])

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Ku noqo Menu-ka", callback_data="main_menu")]
])

def make_menu(buttons_rows, back=True):
    """Samee menu leh row kasta 2-3 buttons iyo back button"""
    kb = []
    for row in buttons_rows:
        kb.append([InlineKeyboardButton(b["text"], callback_data=b.get("data", "")) for b in row])
    if back:
        kb.append([InlineKeyboardButton("🔙 Ku noqo Menu-ka", callback_data="main_menu")])
    return InlineKeyboardMarkup(kb)

# ─── Start ────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first = user.first_name or ""
    
    text = (
        f"Salaam {first}! 👋\n\n"
        f"Kusoo dhawow **Somali AI Academy**!\n\n"
        f"Halkan waxaad ka helaysaa:\n"
        f"• 🤖 AI-ga la hadal (su'aal kasta)\n"
        f"• 📚 Koorsooyin AI ah (40+ cashar)\n"
        f"• 📅 Cashar Maalin kasta + Layli\n"
        f"• 👨‍💻 La xiriir Macallinka\n\n"
        f"**Fadlan dooro hoose:**"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=MAIN_MENU)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=MAIN_MENU)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# ─── Talk to Human ────────────────────────────────────
async def talk_human(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👨‍💻 **Talk to a Human**\n\n"
        "Hello! This bot is designed to assist in the development of a "
        "proficient Somali LLM. Please direct your scientific inquiries "
        "to the bot. Other functionalities are limited due to gas and "
        "environmental token constraints.\n\n"
        "**Telegram:** @Mfaratoon\n"
        "**Balan qabso:** https://calendly.com/somaliboks\n\n"
        "Fadlan badhanka hoose ku raac."
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=BACK_BUTTON)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=BACK_BUTTON)

# ─── Talk to Bot (AI) ─────────────────────────────────
async def talk_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 **Talk to the Bot**\n\n"
        "Wax kasta oo aad weydiiso, AI-ga ayaa kaa jawaabaya! "
        "Isticmaal OpenRouter AI si aad u hesho jawaab su'aalahaada.\n\n"
        "**Fudud:** Kaliya qor su'aashaada ciwaanka hoose!\n\n"
        "Tusaale: *Waa maxay ChatGPT?*\n"
        "*Sidee loo sameeyaa Telegram Bot?*"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=BACK_BUTTON)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=BACK_BUTTON)

# ─── Contacts ─────────────────────────────────────────
async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛂 **Contacts**\n\n"
        "**👨‍💻 Cabasho/Caawin:** @Mfaratoon\n\n"
        "**📝 Substack:**\n"
        "https://somalilibrary.substack.com/\n"
        "https://substack.com/chat/5784198\n\n"
        "**📘 Facebook:**\n"
        "https://www.facebook.com/Mfaratoon1\n\n"
        "**🌐 Website:**\n"
        "https://somalibotmaster.net\n\n"
        "**💼 LinkedIn:**\n"
        "https://www.linkedin.com/company/28160517\n\n"
        "**📱 WhatsApp:**\n"
        "https://chat.whatsapp.com/DKWamfx4eHn6kR6EPfjNMX\n\n"
        "**📺 YouTube:**\n"
        "https://m.youtube.com/user/MrFaraton\n\n"
        "**✈️ Telegram:**\n"
        "https://t.me/Farsamada"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=BACK_BUTTON)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=BACK_BUTTON)

# ─── More Info ────────────────────────────────────────
async def more_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "❓ **More Info**\n\n"
        "We are **Somalibotmaster**. We provide instruction on creating "
        "automation, chatbots, and custom chatbots without requiring coding.\n\n"
        "Connect with us:\n\n"
        "📺 **YouTube:** https://shorturl.at/auGJZ\n"
        "📘 **FB Page:** https://www.facebook.com/soomaalipodcast\n"
        "📺 **FB Channel:** https://www.messenger.com/channel/soomaalipodcast/Aba-uQI70rr-LJXY/\n"
        "✈️ **Telegram:** https://t.me/Farsamada\n"
        "📱 **WhatsApp:** https://chat.whatsapp.com/DKWamfx4eHn6kR6EPfjNMX\n"
        "📖 **F. Carabiga:** https://t.me/somaliarabic\n"
        "📚 **F. English 1:** https://t.me/Somalienglish1\n"
        "📚 **F. English 2:** https://t.me/Somalienglish3\n"
        "📚 **FASALKA:** https://t.me/+eJxxMKtunMcwODhk"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=BACK_BUTTON)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=BACK_BUTTON)

# ─── Courses ─────────────────────────────────────────
async def courses_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [{"text": "🤖 Koorsada 1: 40 Cashar AI", "data": "course_1"},
         {"text": "🎬 Koorsada 2: Video Editing", "data": "course_2"}],
        [{"text": "📦 Koorsada 3: Dropshipping", "data": "course_3"},
         {"text": "🌐 Koorsada 4: Bulshada", "data": "course_4"}],
    ]
    text = "📚 **Koorsooyinka Somali AI Academy**\n\nDooro koorsada aad rabto:"
    reply = make_menu(keyboard)
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply)

async def show_course(update: Update, context: ContextTypes.DEFAULT_TYPE, course_id: int):
    text = course_agent.show_course(course_id)
    keyboard = [
        [InlineKeyboardButton("📅 Casharka Maanta", callback_data="today")],
        [InlineKeyboardButton("🔙 Koorsooyinka", callback_data="courses"),
         InlineKeyboardButton("🔙 Menu-ka", callback_data="main_menu")],
    ]
    
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=False)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=False)
    increment(user_daily_lessons, update.effective_user.id)

# ─── Today's Lesson ──────────────────────────────────
async def today_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not check_limit(user_daily_lessons, user_id, DAILY_LESSON_LIMIT):
        text = (
            "⛔ **Maalintii waxaa laga yaabaa 2 cashar oo kAL**\n\n"
            "Waxaad soo aragtay xadka maanta. Booqo berri \n"
            "casharo cusub oo diyaar ah!\n\n"
            "Wixii su'aalo ah, isticmaal 🤖 Talk to Bot (AI)"
        )
        reply = BACK_BUTTON
    else:
        courses_file = context.application.bot_data.get("courses_file", "data/courses.json")
        with open(courses_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        lesson, course = sched_agent.get_daily_lesson(data)
        text = notify_agent.format_lesson_notification(lesson, course)
        increment(user_daily_lessons, user_id)
        reply = make_menu([
            [{"text": "📚 Koorsooyinka", "data": "courses"},
             {"text": "❓ FAQ", "data": "faq"}],
        ])
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply, disable_web_page_preview=False)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply, disable_web_page_preview=False)

# ─── FAQ ──────────────────────────────────────────────
async def faq_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = faq_agent.get_all_faqs()
    keyboard = make_menu([
        [{"text": "🤖 Talk to Bot (AI)", "data": "talk_bot"}],
    ])
    if update.message:
        await update.message.reply_text(text, reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

# ─── AI Response (Talk to Bot) ────────────────────────
async def ai_response(user_text):
    """Isticmaal OpenRouter AI si aad uga jawaabto su'aasha"""
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return (
            "Ma jiro API key. Fadlan ku qor `.env`-ga:\n"
            "`OPENROUTER_API_KEY=sk-or-v1-...`"
        )
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "Waxaad tahay macallin AI ah oo ku hadla af-Soomaali. Waxaad u jawaabtaa su'aalaha ardayda si fudud oo cad. Haddii su'aashu tahay mid AI-ga ku saabsan, si faahfaahsan u sharax. Haddii kale, si guud u caawi."},
                        {"role": "user", "content": user_text}
                    ],
                    "max_tokens": 500,
                }
            )
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"AI error: {e}")
        return f"Waan ka xumahay, qalad ayaa dhacay. Fadlan markale isku day: {str(e)[:100]}"

# ─── Message Handler ──────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Wixii qoraal ah — AI ayaa ka jawaabaya (Talk to Bot)"""
    text = update.message.text
    if not text:
        return
    
    # First try FAQ keywords (fast)
    answer = faq_agent.get_answer(text)
    if answer:
        await update.message.reply_text(answer, reply_markup=BACK_BUTTON)
        return
    
    # Check daily AI limit
    user_id = update.effective_user.id
    if not check_limit(user_daily_ai, user_id, DAILY_AI_LIMIT):
        await update.message.reply_text(
            "⛔ **Xadka AI-ga maanta wuu dhammaaday!**\n\n"
            "Waxaad soo martay 15 su'aal oo maanta. "
            "Booqo berri ama isticmaal 👨‍💻 Talk to Human.",
            reply_markup=BACK_BUTTON
        )
        return
    
    # Tell user we're thinking
    thinking_msg = await update.message.reply_text(
        "🤔 **Waan ka fikirayaa... fadlan sug...**",
        reply_markup=BACK_BUTTON
    )
    
    # Get AI response
    response = await ai_response(text)
    
    # Update the thinking message with the real answer
    await thinking_msg.edit_text(
        f"🤖 **Jawaabta AI-ga:**\n\n{response}",
        reply_markup=BACK_BUTTON
    )
    
    increment(user_daily_ai, user_id)

# ─── Callback Router ──────────────────────────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    routes = {
        "main_menu": main_menu,
        "talk_human": talk_human,
        "talk_bot": talk_bot,
        "contacts": contacts,
        "more_info": more_info,
        "courses": courses_menu,
        "today": today_lesson,
        "faq": faq_menu,
        "course_1": lambda u, c: show_course(u, c, 1),
        "course_2": lambda u, c: show_course(u, c, 2),
        "course_3": lambda u, c: show_course(u, c, 3),
        "course_4": lambda u, c: show_course(u, c, 4),
    }
    
    handler = routes.get(data)
    if handler:
        await handler(update, context)

# ─── Search ───────────────────────────────────────────
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = " ".join(context.args) if context.args else ""
    if not keyword:
        await update.message.reply_text(
            "Fadlan qor keyword-ka aad raadinayso.\n"
            "Tusaale: /search chatbot"
        )
        return
    
    results = course_agent.search_lessons(keyword)
    if not results:
        await update.message.reply_text(f"❌ Waxba lagama helin '{keyword}'.", reply_markup=BACK_BUTTON)
        return
    
    text = f"🔍 Natiijooyinka '{keyword}':\n\n"
    for r in results[:5]:
        lesson = r["lesson"]
        text += f"• {r['course_name']}: Cashar {lesson['number']} — {lesson['title']}\n  {lesson['link']}\n\n"
    
    if len(results) > 5:
        text += f"...iyo {len(results) - 5} kale"
    
    await update.message.reply_text(text, reply_markup=BACK_BUTTON)

# ─── Help ─────────────────────────────────────────────
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🆘 **Caawimaad**\n\n"
        "/start — Menu-ka Guud\n"
        "/courses — Koorsooyinka\n"
        "/today — Casharka Maanta\n"
        "/faq — FAQ-yada\n"
        "/search KEYWORD — Raadi cashar\n\n"
        "Wax kasta oo aad qorto, AI-ga ayaa ka jawaabaya!"
    )
    await update.message.reply_text(text)

# ─── Main ────────────────────────────────────────────
def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN-ka .env-ga ku qor!")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    courses_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "courses.json")
    app.bot_data["courses_file"] = courses_file

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("courses", courses_menu))
    app.add_handler(CommandHandler("today", today_lesson))
    app.add_handler(CommandHandler("faq", faq_menu))
    app.add_handler(CommandHandler("search", search_command))

    # Callback buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # Message handler (Talk to Bot AI)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Somali AI Academy Bot v2 wuu shaqeynayaa! Ctrl+C jooji.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
