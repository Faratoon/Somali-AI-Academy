"""
handlers/channels.py  –  Channel & Group management  (FIXED)
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from utils import firebase
from utils.menus import channel_menu, group_menu, back_button
from utils.helpers import check_media_size

# ── States ────────────────────────────────────────────────────────────────────
WAITING_CHANNEL_ID    = 10
WAITING_GROUP_ID      = 11
WAITING_POST_TEXT     = 12
WAITING_POST_CHANNEL  = 13
WAITING_DELETE_MSG_ID = 14
WAITING_EDIT_MSG_ID   = 15
WAITING_EDIT_TEXT     = 16
WAITING_SCHEDULE_TIME = 17
WAITING_WELCOME_TEXT  = 18


async def _send(update, text, **kw):
    """Send or edit depending on context type."""
    q = update.callback_query
    if q:
        await q.answer()
        try:
            await q.edit_message_text(text, **kw)
        except Exception:
            await update.effective_message.reply_text(text, **kw)
    else:
        await update.message.reply_text(text, **kw)


# ── Channel Menu ──────────────────────────────────────────────────────────────
async def channels_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send(update,
        "📢 *Channel Management*\n\nXulo hawsha aad rabto:",
        parse_mode=ParseMode.MARKDOWN, reply_markup=channel_menu()
    )


async def groups_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send(update,
        "👥 *Group Management*\n\nXulo hawsha aad rabto:",
        parse_mode=ParseMode.MARKDOWN, reply_markup=group_menu()
    )


# ── Add Channel ───────────────────────────────────────────────────────────────
async def add_channel_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for"] = "channel_id"
    await _send(update,
        "➕ *Add Channel*\n\n"
        "Channel-ka @username ama ID dir.\n\n"
        "📝 Tusaale: `@mychannel` ama `-1001234567890`\n\n"
        "⚠️ Bot-ka admin ka dhig channel-ka marka hore!\n\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN, reply_markup=back_button("menu_channels")
    )
    return WAITING_CHANNEL_ID


async def add_group_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for"] = "group_id"
    await _send(update,
        "➕ *Add Group*\n\n"
        "Group-ka @username ama ID dir.\n\n"
        "📝 Tusaale: `@mygroup` ama `-1001234567890`\n\n"
        "⚠️ Bot-ka admin ka dhig group-ka marka hore!\n\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN, reply_markup=back_button("menu_groups")
    )
    return WAITING_GROUP_ID


async def receive_channel_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid      = update.effective_user.id
    raw      = update.message.text.strip()
    is_group = context.user_data.get("waiting_for") == "group_id"
    ctype    = "group" if is_group else "channel"

    # Loading message
    loading = await update.message.reply_text("⏳ Checking...")

    try:
        chat = await context.bot.get_chat(raw)
        name = chat.title or raw

        firebase.add_channel(uid, str(chat.id), name, ctype)

        await loading.edit_text(
            f"✅ *{'Group' if is_group else 'Channel'} Added!*\n\n"
            f"📛 Name: `{name}`\n"
            f"🆔 ID: `{chat.id}`\n\n"
            f"Hadda post-ka dir!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=group_menu() if is_group else channel_menu()
        )
    except Exception as e:
        await loading.edit_text(
            f"❌ *Khalad!*\n\n`{str(e)[:200]}`\n\n"
            f"Xaqiiji:\n"
            f"1️⃣ ID/username sax\n"
            f"2️⃣ Bot admin ka dhig\n"
            f"3️⃣ Channel/Group public ah",
            parse_mode=ParseMode.MARKDOWN
        )
    return ConversationHandler.END


# ── List Channels ─────────────────────────────────────────────────────────────
async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid   = query.from_user.id
    ctype = "group" if query.data == "grp_list" else "channel"
    label = "Groups" if ctype == "group" else "Channels"

    try:
        channels = firebase.get_channels(uid, ctype)
    except Exception:
        channels = []

    if not channels:
        await query.edit_message_text(
            f"📋 *My {label}*\n\n"
            f"Wali ma jiraan. ➕ Ku dar mid!\n",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button("menu_channels" if ctype == "channel" else "menu_groups")
        )
        return

    text = f"📋 *My {label}* ({len(channels)} total)\n\n"
    btns = []
    for i, ch in enumerate(channels, 1):
        text += f"{i}. 📢 `{ch['name']}` — ID: `{ch['id']}`\n"
        btns.append([
            InlineKeyboardButton(
                f"🗑️ Remove {ch['name'][:15]}",
                callback_data=f"rm_{ctype}_{ch['id']}"
            )
        ])

    back_cb = "menu_channels" if ctype == "channel" else "menu_groups"
    btns.append([InlineKeyboardButton("🔙 Back", callback_data=back_cb)])

    await query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(btns)
    )


async def remove_channel_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query  = update.callback_query
    await query.answer()
    uid    = query.from_user.id
    # format: rm_channel_ID  or  rm_group_ID
    parts  = query.data.split("_", 2)
    ctype  = parts[1]
    cid    = parts[2]

    try:
        firebase.remove_channel(uid, cid, ctype)
        msg = f"✅ *Removed!*\n\nID: `{cid}`"
    except Exception as e:
        msg = f"❌ Error: {str(e)[:100]}"

    back_cb = "menu_channels" if ctype == "channel" else "menu_groups"
    await query.edit_message_text(
        msg, parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button(back_cb)
    )


# ── Post to All ───────────────────────────────────────────────────────────────
async def post_all_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q     = update.callback_query
    if q:
        await q.answer()
        ctype = "group" if q.data.startswith("grp") or q.data == "bc_groups" else "channel"
        if q.data == "bc_all":
            ctype = "all"
    else:
        ctype = "channel"

    context.user_data["post_target"] = ctype
    label = "Groups" if ctype == "group" else ("All" if ctype == "all" else "Channels")

    await _send(update,
        f"📤 *Post to {label}*\n\n"
        f"Post-kaaga qor:\n"
        f"• Text\n• Photo\n• Video\n• Document\n\n"
        f"💡 Markdown: *bold* _italic_ `code`\n"
        f"/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_channels")
    )
    return WAITING_POST_TEXT


async def receive_post_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid   = update.effective_user.id
    ctype = context.user_data.get("post_target", "channel")

    if not await check_media_size(update):
        return ConversationHandler.END

    # Gather target channels
    if ctype == "all":
        channels = firebase.get_channels(uid, "channel") + firebase.get_channels(uid, "group")
    else:
        channels = firebase.get_channels(uid, ctype)

    if not channels:
        await update.message.reply_text(
            f"❌ Channels/Groups ma jiraan. Ku dar mid marka hore!\n"
            f"➕ /channels ama /groups",
        )
        return ConversationHandler.END

    loading = await update.message.reply_text(f"📤 Sending to {len(channels)} targets...")
    msg     = update.message
    sent, failed = 0, 0

    for ch in channels:
        try:
            cid = ch["id"] if isinstance(ch, dict) else ch
            if msg.text:
                await context.bot.send_message(cid, msg.text, parse_mode=ParseMode.MARKDOWN)
            elif msg.photo:
                await context.bot.send_photo(cid, msg.photo[-1].file_id, caption=msg.caption or "")
            elif msg.video:
                await context.bot.send_video(cid, msg.video.file_id, caption=msg.caption or "")
            elif msg.document:
                await context.bot.send_document(cid, msg.document.file_id, caption=msg.caption or "")
            elif msg.audio:
                await context.bot.send_audio(cid, msg.audio.file_id, caption=msg.caption or "")
            sent += 1
        except Exception:
            failed += 1

    await loading.edit_text(
        f"✅ *Broadcast Complete!*\n\n"
        f"📤 Sent: `{sent}`\n"
        f"❌ Failed: `{failed}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_channels")
    )
    return ConversationHandler.END


# ── Delete Post ───────────────────────────────────────────────────────────────
async def delete_post_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send(update,
        "🗑️ *Delete Post*\n\n"
        "Sidan dir:\n"
        "`CHANNEL_ID MESSAGE_ID`\n\n"
        "📝 Tusaale:\n"
        "`-1001234567890 456`\n\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_channels")
    )
    return WAITING_DELETE_MSG_ID


async def receive_delete_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = update.message.text.strip().split()
    try:
        cid = parts[0]
        mid = int(parts[1])
        await context.bot.delete_message(cid, mid)
        await update.message.reply_text(
            "✅ *Post deleted!*", parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button("menu_channels")
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Delete failed:\n`{str(e)[:150]}`\n\n"
            f"Format: `CHANNEL_ID MESSAGE_ID`",
            parse_mode=ParseMode.MARKDOWN
        )
    return ConversationHandler.END


# ── Edit Post ─────────────────────────────────────────────────────────────────
async def edit_post_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send(update,
        "✏️ *Edit Post – Step 1/2*\n\n"
        "Channel ID iyo Message ID dir:\n"
        "`CHANNEL_ID MESSAGE_ID`\n\n"
        "📝 Tusaale: `-1001234567890 456`\n\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_channels")
    )
    return WAITING_EDIT_MSG_ID


async def receive_edit_msg_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = update.message.text.strip().split()
    try:
        context.user_data["edit_chat_id"] = parts[0]
        context.user_data["edit_msg_id"]  = int(parts[1])
        await update.message.reply_text(
            "✏️ *Edit Post – Step 2/2*\n\nText cusub qor:",
            parse_mode=ParseMode.MARKDOWN
        )
        return WAITING_EDIT_TEXT
    except Exception:
        await update.message.reply_text(
            "❌ Format khalad. Isticmaal: `CHANNEL_ID MESSAGE_ID`",
            parse_mode=ParseMode.MARKDOWN
        )
        return WAITING_EDIT_MSG_ID


async def receive_edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid      = context.user_data.get("edit_chat_id")
    mid      = context.user_data.get("edit_msg_id")
    new_text = update.message.text
    try:
        await context.bot.edit_message_text(
            new_text, chat_id=cid, message_id=mid,
            parse_mode=ParseMode.MARKDOWN
        )
        await update.message.reply_text(
            "✅ *Post edited!*", parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button("menu_channels")
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Edit failed:\n`{str(e)[:150]}`",
            parse_mode=ParseMode.MARKDOWN
        )
    return ConversationHandler.END


# ── Welcome Message ───────────────────────────────────────────────────────────
async def set_welcome_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send(update,
        "🎉 *Welcome Message Setup*\n\n"
        "Variables aad isticmaali kartid:\n"
        "`{name}` → Member-ka magaciisa\n"
        "`{group}` → Group-ka magaciisa\n\n"
        "📝 Welcome message-kaaga qor:\n\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_groups")
    )
    return WAITING_WELCOME_TEXT


async def receive_welcome_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    text = update.message.text
    try:
        firebase.create_or_update_user(uid, {"welcome_message": text})
        await update.message.reply_text(
            f"✅ *Welcome message saved!*\n\n"
            f"*Preview:*\n{text[:300]}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button("menu_groups")
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
    return ConversationHandler.END


# ── New Member Welcome ────────────────────────────────────────────────────────
async def new_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        return
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        try:
            # Try to get welcome msg from the group admin who added the bot
            welcome = "👋 Ku soo dhawow *{name}*! 🎉\n\nWaxaad ku jirtaa *{group}*. Farxad ku soo gal!"
            text    = welcome.format(
                name  = member.first_name or "Friend",
                group = update.message.chat.title or "Group"
            )
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            pass
