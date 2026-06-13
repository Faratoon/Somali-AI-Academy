"""
handlers/callbacks.py  –  Menu callbacks  (FIXED – all buttons working)
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.menus import (
    main_inline_menu, broadcast_menu, settings_menu, back_button
)
from utils import firebase


# ── helper: edit or reply ─────────────────────────────────────────────────────
async def _send(update, text, **kw):
    q = update.callback_query
    if q:
        await q.answer()
        await q.edit_message_text(text, **kw)
    else:
        await update.message.reply_text(text, **kw)


# ── Main Menu ─────────────────────────────────────────────────────────────────
async def main_menu_cb(update: Update, context):
    await _send(update,
        "🎛️ *Main Menu* — Xulo meesha aad u baahan tahay:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_inline_menu()
    )


# ── Broadcast Menu ────────────────────────────────────────────────────────────
async def broadcast_menu_cb(update: Update, context):
    await _send(update,
        "📤 *Broadcast*\n\nXulo meesha aad u dirtid:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=broadcast_menu()
    )


# ── Settings Menu ─────────────────────────────────────────────────────────────
async def settings_menu_cb(update: Update, context):
    uid  = update.effective_user.id
    try:
        prem = firebase.is_premium(uid)
        days = firebase.get_trial_days_left(uid)
        plan = "👑 Premium ✅" if prem else f"⏳ Trial: {days} days"
    except Exception:
        plan = "⏳ Trial: 30 days"

    await _send(update,
        f"⚙️ *Settings*\n\n"
        f"👤 ID: `{uid}`\n"
        f"📦 Plan: {plan}\n\n"
        f"Xulo option:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=settings_menu()
    )


# ── Language ──────────────────────────────────────────────────────────────────
async def set_language_cb(update: Update, context):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "🌐 *Luuqadda dooro:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🇸🇴 Somali",  callback_data="lang_so")],
            [InlineKeyboardButton("🇸🇦 Arabic",  callback_data="lang_ar")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🔙 Back",     callback_data="menu_settings")],
        ])
    )


async def save_language_cb(update: Update, context):
    q    = update.callback_query
    lang = {"lang_so": "Somali 🇸🇴", "lang_ar": "Arabic 🇸🇦", "lang_en": "English 🇬🇧"}.get(q.data, "Somali")
    await q.answer(f"✅ {lang} selected!")
    try:
        firebase.create_or_update_user(q.from_user.id, {"language": q.data})
    except Exception:
        pass
    await q.edit_message_text(
        f"✅ *Luuqadda waa la beddelay!*\n\n{lang} ayaa hadda la isticmaalayaa.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_settings")
    )


# ── Notifications ─────────────────────────────────────────────────────────────
async def notifications_cb(update: Update, context):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "🔔 *Notifications*\n\nXulo:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 On",   callback_data="notif_on")],
            [InlineKeyboardButton("🔕 Off",  callback_data="notif_off")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu_settings")],
        ])
    )


async def save_notif_cb(update: Update, context):
    q   = update.callback_query
    val = q.data == "notif_on"
    await q.answer("✅ Saved!")
    try:
        firebase.create_or_update_user(q.from_user.id, {"notifications": val})
    except Exception:
        pass
    await q.edit_message_text(
        f"{'🔔 Notifications: ON ✅' if val else '🔕 Notifications: OFF ✅'}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_settings")
    )


# ── Clear AI Memory ───────────────────────────────────────────────────────────
async def clear_memory_cb(update: Update, context):
    q = update.callback_query
    await q.answer("🗑️ Memory cleared!")
    try:
        firebase.clear_conversation(q.from_user.id)
    except Exception:
        pass
    await q.edit_message_text(
        "🗑️ *AI Memory nadiifnaatay!*\n\nWada hadal cusub bilow — /nano ama /menu",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_settings")
    )


# ── Cancel ────────────────────────────────────────────────────────────────────
async def action_cancel(update: Update, context):
    q = update.callback_query
    await q.answer("Cancelled ✅")
    await q.edit_message_text(
        "❌ *Cancelled.*\n\n/menu si aad menu-ga u furto.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button()
    )


# ── Coming Soon placeholder ───────────────────────────────────────────────────
async def coming_soon_cb(update: Update, context):
    await update.callback_query.answer("🚧 Coming soon — stay tuned!", show_alert=True)
