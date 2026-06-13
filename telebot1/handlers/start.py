"""
handlers/start.py  –  /start, /help, /menu  (FIXED – handles message + callback)
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.menus import main_menu_keyboard, main_inline_menu
from utils import firebase


WELCOME_TEXT = """\
🌟 *Ku soo dhawow {name}!*

━━━━━━━━━━━━━━━━━━━━━
🤖 *AI Channel & Group Manager Bot*
━━━━━━━━━━━━━━━━━━━━━

✅ *Bot-kan wuxuu kuu sahlayaa:*

📢 Channels & Groups maamul
📤 Hal mar dhammaan channels u dir
⏰ Posts qorso (Schedule)
✏️ Edit · 🗑️ Delete posts
🎉 Welcome messages auto
🤖 AI Assistant (Somali / Arabic / English)
☘️ 40+ Koorso FREE

━━━━━━━━━━━━━━━━━━━━━
⏳ *Trial:* `{trial_days}` days remaining
━━━━━━━━━━━━━━━━━━━━━

👇 *Menu-ga hoose xulo:*
"""

HELP_TEXT = """\
📖 *Commands Guide*
━━━━━━━━━━━━━━━━━━━━━

🏠 *General:*
/start      → Menu ugu weyn
/help       → Commands-kan arag
/menu       → Inline menu fur
/profile    → Profile-kaaga

📢 *Channel & Group:*
/channels   → Channels maamul
/groups     → Groups maamul
/broadcast  → Dhammaan u dir
/schedule   → Post qorso

🤖 *AI Models:*
/nano       → 💬 Nano Banana
/midjourney → 🎨 Midjourney
/sora       → 🖼️ Sora Images
/gpt_image  → 🤖 GPT Images
/flux       → 🎨 Flux Images
/veo        → 🎥 Veo3 Video

⚙️ *Settings:*
/settings   → Settings
/clear      → AI memory nadiifi
/admin      → Admin panel (admins)
/cancel     → Wax jooji

━━━━━━━━━━━━━━━━━━━━━
💡 Buttons-ka hoose waa ugu fudud!
"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid  = user.id

    # Save/update user in Firebase
    try:
        firebase.create_or_update_user(uid, {
            "user_id":    uid,
            "first_name": user.first_name or "",
            "last_name":  user.last_name  or "",
            "username":   user.username   or "",
        })
        trial_days = firebase.get_trial_days_left(uid)
    except Exception:
        trial_days = 30

    name = user.first_name or "Friend"
    text = WELCOME_TEXT.format(name=name, trial_days=trial_days)

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )
    await update.message.reply_text(
        "🎛️ *Main Menu:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_inline_menu()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎛️ *Main Menu:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_inline_menu()
    )
