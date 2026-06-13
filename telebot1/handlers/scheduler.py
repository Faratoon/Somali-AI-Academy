"""
handlers/scheduler.py  –  Scheduled post management
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
import config
from utils import firebase
from utils.menus import back_button
from utils.helpers import check_limits

# State
SCHED_TEXT    = 30
SCHED_TIME    = 31
SCHED_CONFIRM = 32

scheduler = AsyncIOScheduler(timezone=pytz.utc)


async def schedule_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        target = update.effective_message
    else:
        target = update.message

    uid   = update.effective_user.id
    prem  = firebase.is_premium(uid)
    days  = firebase.get_trial_days_left(uid)

    if not prem:
        text = (
            "⏰ *Schedule Post*\n\n"
            f"⭐ Feature-kan Premium ama Trial (baqiyaa `{days}` days)\n\n"
            "Trial-kaagu weli socdaa! Post schedule gareey."
        )
    else:
        text = "⏰ *Schedule Post*\n\nPost-kaaga qor:"

    btns = [
        [InlineKeyboardButton("⏰ Schedule New Post",    callback_data="sched_new")],
        [InlineKeyboardButton("📋 View Scheduled Posts", callback_data="sched_list")],
        [InlineKeyboardButton("🔙 Back",                 callback_data="menu_main")],
    ]
    if hasattr(target, 'edit_text'):
        await target.edit_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(btns))
    else:
        await target.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(btns))


async def schedule_new_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid   = update.effective_user.id

    if not firebase.is_premium(uid):
        days = firebase.get_trial_days_left(uid)
        if days <= 0:
            await query.edit_message_text(
                "❌ *Trial-kaaga waa dhammaaday!*\n\n"
                "⭐ Premium-ga u bixi si aad schedule feature isticmaasho.\n"
                f"📞 Xiriir: {config.SUPPORT_USERNAME}",
                parse_mode=ParseMode.MARKDOWN
            )
            return ConversationHandler.END

    await query.edit_message_text(
        "⏰ *Schedule Post – Step 1/2*\n\n"
        "Post-kaaga qor (text, photo ama video):",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_schedule")
    )
    return SCHED_TEXT


async def receive_sched_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg.text:
        context.user_data["sched_content"] = {"type": "text", "text": msg.text}
    elif msg.photo:
        context.user_data["sched_content"] = {"type": "photo", "file_id": msg.photo[-1].file_id, "caption": msg.caption or ""}
    elif msg.video:
        context.user_data["sched_content"] = {"type": "video", "file_id": msg.video.file_id, "caption": msg.caption or ""}
    else:
        await msg.reply_text("❌ Nooca faylka ma taageeranto. Qor text, photo ama video.")
        return SCHED_TEXT

    await msg.reply_text(
        "⏰ *Schedule Post – Step 2/2*\n\n"
        "Wakhti geli (UTC format):\n"
        "📝 Format: `2025-12-25 14:30`\n\n"
        "💡 Wakhtigan xisaabta UTC ah waa isticmaal",
        parse_mode=ParseMode.MARKDOWN
    )
    return SCHED_TIME


async def receive_sched_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid        = update.effective_user.id
    time_str   = update.message.text.strip()

    try:
        sched_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        sched_dt = pytz.utc.localize(sched_dt)
    except ValueError:
        await update.message.reply_text(
            "❌ Format khalad ah. Isticmaal: `YYYY-MM-DD HH:MM`\n"
            "Tusaale: `2025-12-25 14:30`",
            parse_mode=ParseMode.MARKDOWN
        )
        return SCHED_TIME

    content    = context.user_data.get("sched_content", {})
    channels   = firebase.get_channels(uid, "channel") + firebase.get_channels(uid, "group")

    if not channels:
        await update.message.reply_text("❌ Channel ama group ma jiraan. Ku dar mid marka hore!")
        return ConversationHandler.END

    post_id = firebase.save_scheduled_post(uid, {
        "content":    content,
        "scheduled_at": sched_dt.isoformat(),
        "channels":   [ch["id"] for ch in channels],
    })

    # Add to scheduler
    app = context.application
    scheduler.add_job(
        send_scheduled_post,
        "date",
        run_date  = sched_dt,
        args      = [app, post_id, uid, channels, content],
        id        = post_id
    )

    await update.message.reply_text(
        f"✅ *Post Scheduled!*\n\n"
        f"🕐 Wakhti: `{time_str} UTC`\n"
        f"📢 Channels: `{len(channels)}`\n"
        f"🆔 Post ID: `{post_id[:8]}...`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_schedule")
    )
    return ConversationHandler.END


async def send_scheduled_post(app, post_id: str, uid: int, channels: list, content: dict):
    """Execute scheduled post send."""
    bot  = app.bot
    sent = 0
    for ch in channels:
        try:
            cid = ch["id"] if isinstance(ch, dict) else ch
            if content["type"] == "text":
                await bot.send_message(cid, content["text"], parse_mode=ParseMode.MARKDOWN)
            elif content["type"] == "photo":
                await bot.send_photo(cid, content["file_id"], caption=content.get("caption", ""))
            elif content["type"] == "video":
                await bot.send_video(cid, content["file_id"], caption=content.get("caption", ""))
            sent += 1
        except:
            pass

    firebase.mark_post_sent(post_id)
    try:
        await bot.send_message(
            uid,
            f"✅ *Scheduled post sent!*\n📤 Channels: `{sent}`",
            parse_mode=ParseMode.MARKDOWN
        )
    except:
        pass


async def view_scheduled_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    posts = firebase.get_pending_posts()

    if not posts:
        await query.edit_message_text(
            "📋 *Scheduled Posts*\n\nPosts ma jiraan.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button("menu_schedule")
        )
        return

    text = "📋 *Scheduled Posts:*\n\n"
    for p in posts[:10]:
        text += f"• `{p['id'][:8]}` → {p.get('scheduled_at', 'N/A')[:16]}\n"

    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_button("menu_schedule"))
