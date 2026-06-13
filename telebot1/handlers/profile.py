"""
handlers/profile.py  –  User profile + premium  (FIXED – handles msg & callback)
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import config
from utils import firebase
from utils.menus import profile_menu, back_button


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Works as /profile command AND as inline callback."""
    user  = update.effective_user
    uid   = user.id

    try:
        udata = firebase.get_user(uid)
        prem  = firebase.is_premium(uid)
        days  = firebase.get_trial_days_left(uid)
        chs   = firebase.get_channels(uid, "channel")
        grps  = firebase.get_channels(uid, "group")
    except Exception:
        udata, prem, days, chs, grps = {}, False, 30, [], []

    if udata.get("is_premium"):
        prem_text = "👑 Premium Active ✅"
    elif days > 0:
        prem_text = f"⏳ Trial — `{days}` days left"
    else:
        prem_text = "❌ Trial Expired — Upgrade needed"

    daily_cnt = udata.get("daily_count", 0)

    text = (
        f"👤 *Your Profile*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🆔 ID: `{uid}`\n"
        f"👤 Name: {user.first_name or 'N/A'} {user.last_name or ''}\n"
        f"🔖 Username: @{user.username or 'N/A'}\n\n"
        f"📦 *Plan:* {prem_text}\n"
        f"📢 Channels: `{len(chs)}`\n"
        f"👥 Groups: `{len(grps)}`\n"
        f"💬 Today's msgs: `{daily_cnt}/{config.DAILY_MSG_LIMIT}`\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    kb = profile_menu(prem)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
        )


async def premium_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid  = query.from_user.id

    try:
        days = firebase.get_trial_days_left(uid)
    except Exception:
        days = 0

    text = (
        f"⭐ *Premium Plan*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎁 *Free Trial:* `{days}` days left\n\n"
        f"✅ *Premium Features:*\n"
        f"• ⏰ Unlimited Scheduled Posts\n"
        f"• 📢 Broadcast to All at Once\n"
        f"• 🤖 Priority AI Access\n"
        f"• 📌 Unlimited Channels & Groups\n"
        f"• 🛡️ Priority Support\n\n"
        f"📞 *Contact:* {config.SUPPORT_USERNAME}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    await query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_profile")
    )
