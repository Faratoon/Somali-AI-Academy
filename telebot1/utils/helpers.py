"""
utils/helpers.py  –  Shared helper functions (FIXED)
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import config
from utils import firebase


async def check_limits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check daily message limit. Returns True if allowed."""
    user_id = update.effective_user.id
    
    # Skip limit for admins
    if user_id in config.ADMIN_IDS:
        return True
    
    allowed, count = firebase.check_and_increment_msg(user_id)
    if not allowed:
        msg = (
            f"⚠️ *Barakacday!*\n\n"
            f"Maanta `{config.DAILY_MSG_LIMIT}` fariin ayaad dir-tay. "
            f"Berri ku soo noqo! 😊\n\n"
            f"_Daily limit reached. Come back tomorrow!_"
        )
        if update.callback_query:
            await update.callback_query.answer(
                f"⚠️ Daily limit reached! Come back tomorrow.", show_alert=True
            )
        elif update.message:
            await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        return False
    return True


async def check_media_size(update: Update) -> bool:
    """Check if media file is within size limit."""
    msg = update.message
    if not msg:
        return True
        
    file_size = 0
    if msg.photo:       file_size = msg.photo[-1].file_size or 0
    elif msg.video:     file_size = msg.video.file_size or 0
    elif msg.document:  file_size = msg.document.file_size or 0
    elif msg.audio:     file_size = msg.audio.file_size or 0

    if file_size > config.MAX_MEDIA_SIZE_B:
        size_mb = file_size / (1024 * 1024)
        await msg.reply_text(
            f"❌ *Faylku waaa weyn yahay!*\n\n"
            f"📦 Cabbirkaaga: `{size_mb:.1f} MB`\n"
            f"📏 Xadka: `{config.MAX_MEDIA_SIZE_MB} MB`\n\n"
            f"Fadlan faylka ka yareey oo dib u dir.",
            parse_mode=ParseMode.MARKDOWN
        )
        return False
    return True


def is_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS


async def safe_reply(update: Update, text: str, **kwargs):
    """Safely reply whether it's a message or callback."""
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(text, **kwargs)
        elif update.message:
            await update.message.reply_text(text, **kwargs)
    except Exception:
        try:
            if update.message:
                await update.message.reply_text(text, **kwargs)
        except Exception:
            pass
