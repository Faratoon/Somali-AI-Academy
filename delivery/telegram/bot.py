"""
Somali AI Academy — Telegram Bot v4
- Cashar hal mar: Next/Previous buttons
- Conversational course matching
- User session tracking
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

# ─── User session (which lesson they're on) ──────
# { user_id: {"course_id": 1, "lesson_idx": 0} }
user_session = {}

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

# ─── Main Menu ────────────────────────────────────
MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("🤖 Talk to Bot (AI)", callback_data="talk_bot")],
    [InlineKeyboardButton("👨‍💻 Talk to Human", callback_data="talk_human")],
    [InlineKeyboardButton("📚 Buugaagta", callback_data="books"),
     InlineKeyboardButton("📚 Koorsooyinka", callback_data="courses")],
    [InlineKeyboardButton("💰 Courses & Fees", callback_data="fees"),
     InlineKeyboardButton("📅 Casharka Maanta", callback_data="today")],
    [InlineKeyboardButton("🛂 Contacts", callback_data="contacts"),
     InlineKeyboardButton("❓ More Info", callback_data="more_info")],
])

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Ku noqo Menu-ka", callback_data="main_menu")]
])

def make_menu(buttons_rows, back=True):
    kb = []
    for row in buttons_rows:
        kb.append([InlineKeyboardButton(b["text"], callback_data=b.get("data", "")) for b in row])
    if back:
        kb.append([InlineKeyboardButton("🔙 Ku noqo Menu-ka", callback_data="main_menu")])
    return InlineKeyboardMarkup(kb)

# ─── Start ────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first = user.first_name or ""
    
    text = (
        f"Salaam {first}! 👋\n\n"
        f"Kusoo dhawow **Somali AI Academy**!\n\n"
        f"🏆 **Free Books ilaa 2028:**\n"
        f"1. Isbar AI 🧠 — **FREE**\n"
        f"2. ChatGPT Basic Prompts 🤖 — **FREE**\n"
        f"3. Isbar Linux 🐧 — **FREE**\n\n"
        f"🎓 **Free Courses:**\n"
        f"   AI Video Editing 🎥\n"
        f"   WhatsApp/Telegram Bot 📱\n\n"
        f"**Maxaad rabtaa inaad barato?**\n"
        f"Kaliya qor waxa aad rabto, AI-ga ayaa koorsada ku habboon kuu soo jeedinaya!\n\n"
        f"Tusaale: *Waxaan rabaa inaan barto chatbot-ka*"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=MAIN_MENU)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=MAIN_MENU)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# ─── Talk to Human ────────────────────────────────
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

# ─── Talk to Bot (AI) ─────────────────────────────
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

# ─── Contacts ─────────────────────────────────────
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

# ─── More Info ────────────────────────────────────
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

# ─── Courses ─────────────────────────────────────
COURSE_SHORT_DESC = {
    1: "🤖 Chatbots, Prompt Engineering, ManyChat, AI Tools — 40 cashar",
    2: "🎬 InVideo, Pictory.ai, Lumen5 — 10 cashar",
    3: "📦 Zendrop, Dropshipping AI — 10 cashar",
    4: "🌐 WhatsApp, Telegram, YouTube, FB — Bulshada",
}

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

async def show_lesson(update, context, user_id, direction="start"):
    """Show one lesson at a time with Next/Previous"""
    uid = user_id
    if uid not in user_session:
        user_session[uid] = {"course_id": 1, "lesson_idx": 0}
    
    session = user_session[uid]
    course = course_agent.get_course(session["course_id"])
    if not course:
        return
    
    total = len(course["lessons"])
    
    if direction == "next":
        session["lesson_idx"] = min(session["lesson_idx"] + 1, total - 1)
    elif direction == "prev":
        session["lesson_idx"] = max(session["lesson_idx"] - 1, 0)
    elif direction == "start":
        session["lesson_idx"] = 0
    
    idx = session["lesson_idx"]
    lesson = course["lessons"][idx]
    
    text = (
        f"{course['emoji']} **{course['name']}**\n\n"
        f"📖 **Cashar {lesson['number']}: {lesson['title']}**\n"
        f"_{lesson['description']}_\n\n"
        f"🔗 {lesson['link']}\n\n"
        f"📊 **Horukac:** {idx + 1} / {total}"
    )
    
    # Build navigation buttons
    nav = []
    nav_row = []
    if idx > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Hore", callback_data="lesson_prev"))
    if idx < total - 1:
        nav_row.append(InlineKeyboardButton("➡️ Xiga", callback_data="lesson_next"))
    if nav_row:
        nav.append(nav_row)
    
    nav.append([
        InlineKeyboardButton("🔙 Koorsooyinka", callback_data="courses"),
        InlineKeyboardButton("🔙 Menu-ka", callback_data="main_menu"),
    ])
    
    reply = InlineKeyboardMarkup(nav)
    
    # Check daily limit
    if not check_limit(user_daily_lessons, uid, DAILY_LESSON_LIMIT):
        text = (
            "⛔ **Maalintii 2 cashar oo kAL**\n\n"
            "Waxaad soo aragtay xadka maanta. Berri waa la sii wadi karaa!\n\n"
            "Wixii su'aalo ah, isticmaal 🤖 Talk to Bot (AI)"
        )
        reply = BACK_BUTTON
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply, disable_web_page_preview=False)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply, disable_web_page_preview=False)
    
    increment(user_daily_lessons, uid)

# ─── Course entry point ──────────────────────────
async def show_course(update, context, course_id: int):
    """Start showing a course from lesson 1"""
    user_id = update.effective_user.id
    user_session[user_id] = {"course_id": course_id, "lesson_idx": 0}
    await show_lesson(update, context, user_id, "start")

async def lesson_next(update, context):
    """Show next lesson"""
    await show_lesson(update, context, update.effective_user.id, "next")

async def lesson_prev(update, context):
    """Show previous lesson"""
    await show_lesson(update, context, update.effective_user.id, "prev")

# ─── Today's Lesson ──────────────────────────────
async def today_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    courses_file = context.application.bot_data.get("courses_file", "data/courses.json")
    with open(courses_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    lesson, course = sched_agent.get_daily_lesson(data)
    text = notify_agent.format_lesson_notification(lesson, course)
    
    reply = make_menu([
        [{"text": "📚 Koorsooyinka", "data": "courses"},
         {"text": "❓ FAQ", "data": "faq"}],
    ])
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply, disable_web_page_preview=False)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply, disable_web_page_preview=False)

# ─── FAQ ─────────────────────────────────────────
async def faq_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = faq_agent.get_all_faqs()
    keyboard = make_menu([
        [{"text": "🤖 Talk to Bot (AI)", "data": "talk_bot"}],
    ])
    if update.message:
        await update.message.reply_text(text, reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

# ─── Conversational Course Matching ──────────────
COURSE_KEYWORDS = {
    1: ["chatbot", "bot", "chat", "prompt", "manychat", "ai tool", "ai chatbot", "gpt", "chatgpt", "telegram bot"],
    2: ["video", "edit", "invideo", "pictory", "lumen5", "video editing", "tifatir"],
    3: ["dropshipping", "zendrop", "ganacsi", "iib", "shopping", "online store"],
    4: ["bulsho", "community", "whatsapp group", "telegram channel", "facebook", "youtube channel"],
}

def match_course(user_text):
    """Match user text to the right course"""
    text = user_text.lower()
    scores = {}
    for cid, keywords in COURSE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[cid] = score
    if scores:
        return max(scores, key=scores.get)
    return None

# ─── AI Response ─────────────────────────────────
async def ai_response(user_text):
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return (
            "Ma jiro API key. Fadlan ku qor `.env`-ga:\n"
            "OPENROUTER_API_KEY=your-key-here"
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
        return f"Waan ka xumahay, qalad ayaa dhacay: {str(e)[:100]}"

# ─── Message Handler ─────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI + Course matching + FAQ"""
    text = update.message.text
    if not text:
        return
    
    # 1. Try FAQ first (fast)
    answer = faq_agent.get_answer(text)
    if answer:
        await update.message.reply_text(answer, reply_markup=BACK_BUTTON)
        return
    
    # 2. Try course matching
    matched = match_course(text)
    if matched:
        course = course_agent.get_course(matched)
        emoji = course["emoji"] if course else "📚"
        response = (
            f"🎯 **Waxaan u maleynayaa inaad rabto Koorsada {matched}!**\n\n"
            f"{COURSE_SHORT_DESC[matched]}\n\n"
            f"Ma rabtaa inaad eegto?"
        )
        keyboard = [
            [InlineKeyboardButton(f"✅ Haa, tus", callback_data=f"course_{matched}"),
             InlineKeyboardButton("🔙 Menu-ka", callback_data="main_menu")],
        ]
        await update.message.reply_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    # 3. Check AI daily limit
    user_id = update.effective_user.id
    if not check_limit(user_daily_ai, user_id, DAILY_AI_LIMIT):
        await update.message.reply_text(
            "⛔ **Xadka AI-ga maanta wuu dhammaaday!**\n\n"
            "Waxaad soo martay 15 su'aal oo maanta. "
            "Booqo berri ama isticmaal 👨‍💻 Talk to Human.",
            reply_markup=BACK_BUTTON
        )
        return
    
    # 4. Get AI response
    thinking_msg = await update.message.reply_text(
        "🤔 **Waan ka fikirayaa... fadlan sug...**",
        reply_markup=BACK_BUTTON
    )
    
    response = await ai_response(text)
    
    await thinking_msg.edit_text(
        f"🤖 **Jawaabta AI-ga:**\n\n{response}",
        reply_markup=BACK_BUTTON
    )
    
    increment(user_daily_ai, user_id)

# ─── Callback Router ────────────────────────────
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
        "books": "books_menu",
        "fees": "fees_menu",
        "courses": courses_menu,
        "today": today_lesson,
        "faq": faq_menu,
        "lesson_next": lesson_next,
        "lesson_prev": lesson_prev,
        "course_1": lambda u, c: show_course(u, c, 1),
        "course_2": lambda u, c: show_course(u, c, 2),
        "course_3": lambda u, c: show_course(u, c, 3),
        "course_4": lambda u, c: show_course(u, c, 4),
    }
    
    # Handle books / fees here since they need context
    if data == "books":
        await books_menu(update, context)
        return
    if data == "fees":
        await fees_menu(update, context)
        return
    
    # Handle book_1..book_5
    if data.startswith("book_"):
        book_id = int(data.split("_")[1])
        await show_book(update, context, book_id)
        return
    
    handler = routes.get(data)
    if handler:
        await handler(update, context)

# ─── Books ────────────────────────────────────────
BOOKS_DATA = [
    {"id": 1, "title": "ISBAR COMPUTER", "emoji": "💻", "price": "$15", 
     "desc": "Computer Basics, Software & Hardware, Windows 11, Mac OS, Microsoft Office, Adobe Photoshop, OBS Studio", "free": False},
    {"id": 2, "title": "ISBAR PROGRAMMING", "emoji": "👨‍💻", "price": "$15",
     "desc": "Basics of Programming, Web Development, Luqadaha Programming-ka, Database, Code Editor & IDE", "free": False},
    {"id": 3, "title": "ISBAR AI", "emoji": "🧠", "price": "FREE 🎉",
     "desc": "Taariikhda AI, AI & Waxbarashada, AI & Shaqooyinka, AI & Graphic Design, AI & Ganacsiga", "free": True},
    {"id": 4, "title": "ISBAR PROMPTS (ChatGPT)", "emoji": "🤖", "price": "FREE 🎉",
     "desc": "Waa maxay ChatGPT?, Sida loola xiriiro, Shaqooyinka & ChatGPT, ChatGPT & Business-ka", "free": True},
    {"id": 5, "title": "ISBAR LINUX Macallin La'aan", "emoji": "🐧", "price": "FREE 🎉",
     "desc": "Aasaaska Linux, Amarrada Linux, Isticmaalka nidaamka, Noqo khabiir Linux", "free": True},
]

async def books_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 **AFARTAN BUUG – ISBAR MACALLIN LA'AAN!**\n\n"
        "Baro Computer, Programming, AI & ChatGPT adigoo gurigaaga jooga!\n\n"
        "🏆 **2 Buug oo FREE ah ilaa 2028:**\n"
        "   • Isbar AI 🧠\n"
        "   • ChatGPT Basic Prompts 🤖\n"
        "   • Isbar Linux 🐧\n\n"
        "🛍 **DHAMMAAN BUUGAAGTA haddii aad wada iibsatid – $15 kaliya!**\n"
        "💥 **Bonus:** Buug HACKING Af Soomaali ah – bilaash!\n\n"
        "👇 **Dooro buug:**"
    )
    
    buttons = []
    for b in BOOKS_DATA:
        badge = "FREE" if b["free"] else b["price"]
        buttons.append([{"text": f"{b['emoji']} {b['title']} [{badge}]", "data": f"book_{b['id']}"}])
    
    reply = make_menu(buttons)
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply)

async def show_book(update: Update, context: ContextTypes.DEFAULT_TYPE, book_id: int):
    book = None
    for b in BOOKS_DATA:
        if b["id"] == book_id:
            book = b
            break
    
    if not book:
        if update.callback_query:
            await update.callback_query.edit_message_text("❌ Buuggan lama helin.", reply_markup=BACK_BUTTON)
        return
    
    price_line = "**💰 FREE ilaa 2028!** 🎉" if book["free"] else f"**💰 Qiimaha:** {book['price']}"
    text = (
        f"{book['emoji']} **{book['title']}**\n\n"
        f"{book['desc']}\n\n"
        f"{price_line}\n\n"
        f"🖋 Editor: @Mfaratoon\n\n"
        f"📥 **Si aad u hesho:** @Mfaratoon"
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=BACK_BUTTON)

# ─── Courses & Fees ────────────────────────────────
async def fees_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💰 **Courses & Fees**\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🔹 **Paid Courses – $34** (Student: $10)\n"
        "Koorsa kasta 4-5 maalmood\n\n"
        "📱 WhatsApp Automation Business Bot — **Free**\n"
        "📞 Telegram Automation Business Bot — **Free**\n"
        "💬 Messenger Automation Business Bot — **$34 (Student: $10)**\n"
        "📸 Instagram Automation Business Bot — **$34 (Student: $10)**\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🎓 **Free Courses:**\n\n"
        "🎥 AI Video Editing — **Free**\n"
        "   Duration: 4-5 days\n\n"
        "📝 AI ChatGPT - Somali Data Writing — **$24 (Student: $10)**\n"
        "   Duration: 4-5 days\n\n"
        "🌐 Web Design with AI Tools — **$24 (Student: $10)**\n"
        "   Duration: 4-5 days\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🛡️ **Security Course (Af-Soomaali)**\n"
        "   Kali Linux, Python, Basic\n"
        "   Duration: 3-4 months\n"
        "   **Price: $26.9/session (Student: $10)**\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🏆 **Free Books ilaa 2028:**\n"
        "   • Isbar AI 🧠\n"
        "   • ChatGPT Basic Prompts 🤖\n"
        "   • Isbar Linux 🐧\n\n"
        "📦 **All Books Bundle: $15**\n"
        "   Bonus: Buug HACKING Af-Soomaali ah — **FREE!**\n\n"
        "📲 **Kusoo xidhiidh @Mfaratoon si aad u iibsato!**"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=BACK_BUTTON)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=BACK_BUTTON)

# ─── Search ───────────────────────────────────────
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

# ─── Help ─────────────────────────────────────────
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🆘 **Caawimaad**\n\n"
        "/start — Menu-ka Guud\n"
        "/courses — Koorsooyinka\n"
        "/today — Casharka Maanta\n"
        "/books — Buugaagta\n"
        "/fees — Courses & Fees\n"
        "/faq — FAQ-yada\n"
        "/search KEYWORD — Raadi cashar\n\n"
        "Wax kasta oo aad qorto, AI-ga ayaa kuu soo jeedinaya\n"
        "koorsada ku habboon ama ka jawaabaya su'aashaada!"
    )
    await update.message.reply_text(text)

# ─── Main ─────────────────────────────────────────
def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN-ka .env-ga ku qor!")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    courses_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "courses.json")
    app.bot_data["courses_file"] = courses_file

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("courses", courses_menu))
    app.add_handler(CommandHandler("today", today_lesson))
    app.add_handler(CommandHandler("books", books_menu))
    app.add_handler(CommandHandler("fees", fees_menu))
    app.add_handler(CommandHandler("faq", faq_menu))
    app.add_handler(CommandHandler("search", search_command))

    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Somali AI Academy Bot v4 wuu shaqeynayaa! Ctrl+C jooji.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
