"""
handlers/admin.py  –  Admin-only panel
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
import config
from utils import firebase
from utils.helpers import is_admin
from utils.menus import admin_menu, back_button

ADMIN_BROADCAST_TEXT = 50
ADMIN_PREMIUM_ID     = 51
ADMIN_BAN_ID         = 52


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await update.message.reply_text("❌ Access denied.")
        return

    await update.message.reply_text(
        "🔧 *Admin Panel*\n\nKu soo dhawow Admin Panel-ka:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=admin_menu()
    )


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not is_admin(query.from_user.id):
        await query.answer("❌ Access denied", show_alert=True)
        return

    db = firebase.get_db()
    if db:
        users_count = len(list(db.collection("users").stream()))
        posts_count = len(list(db.collection("scheduled_posts").stream()))
    else:
        users_count = posts_count = "N/A"

    await query.edit_message_text(
        f"📊 *Bot Statistics*\n\n"
        f"👥 Total Users: `{users_count}`\n"
        f"📅 Scheduled Posts: `{posts_count}`\n",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("adm_menu")
    )


async def admin_broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not is_admin(query.from_user.id):
        return
    await query.edit_message_text(
        "📢 *Admin Broadcast*\n\nFariin qor – dhammaan users-yada ayaa la diri doonaa:",
        parse_mode=ParseMode.MARKDOWN
    )
    return ADMIN_BROADCAST_TEXT


async def receive_admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END

    text = update.message.text
    db   = firebase.get_db()
    if not db:
        await update.message.reply_text("❌ Firebase error.")
        return ConversationHandler.END

    users = list(db.collection("users").stream())
    sent  = 0
    for u in users:
        try:
            await context.bot.send_message(u.id, f"📢 *Admin Message:*\n\n{text}", parse_mode=ParseMode.MARKDOWN)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"✅ Sent to `{sent}` users!", parse_mode=ParseMode.MARKDOWN)
    return ConversationHandler.END


async def grant_premium_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not is_admin(query.from_user.id):
        return
    await query.edit_message_text("⭐ User ID dir si Premium loo siiyo:")
    return ADMIN_PREMIUM_ID


async def receive_premium_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    try:
        target_id = int(update.message.text.strip())
        firebase.create_or_update_user(target_id, {"is_premium": True})
        await update.message.reply_text(f"✅ Premium granted to `{target_id}`!", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ ID khalad ah.")
    return ConversationHandler.END


async def ban_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not is_admin(query.from_user.id):
        return
    await query.edit_message_text("🚫 User ID dir si aad u banno:")
    return ADMIN_BAN_ID


async def receive_ban_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END
    try:
        target_id = int(update.message.text.strip())
        firebase.create_or_update_user(target_id, {"is_banned": True})
        await update.message.reply_text(f"🚫 User `{target_id}` banned!", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ ID khalad ah.")
    return ConversationHandler.END
