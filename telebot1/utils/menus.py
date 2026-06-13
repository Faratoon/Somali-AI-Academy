"""
utils/menus.py  –  All inline & reply keyboards
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


# ── MAIN MENU (Reply Keyboard) ────────────────────────────────────────────────
def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        ["➕ Add Channel", "👥 Add Group"],
        ["📢 Broadcast", "⏰ Schedule Post"],
        ["🤖 AI Assistant", "☘️ Learn AI"],
        ["👤 My Profile", "⚙️ Settings"],
        ["📞 Contact Support", "❓ Help & Info"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


# ── MAIN INLINE MENU ──────────────────────────────────────────────────────────
def main_inline_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("📢 Channels",  callback_data="menu_channels"),
            InlineKeyboardButton("👥 Groups",    callback_data="menu_groups"),
        ],
        [
            InlineKeyboardButton("🤖 AI Chat",   callback_data="menu_ai"),
            InlineKeyboardButton("☘️ Learn AI",  callback_data="menu_learn"),
        ],
        [
            InlineKeyboardButton("📤 Broadcast", callback_data="menu_broadcast"),
            InlineKeyboardButton("⏰ Schedule",  callback_data="menu_schedule"),
        ],
        [
            InlineKeyboardButton("👤 Profile",   callback_data="menu_profile"),
            InlineKeyboardButton("⚙️ Settings",  callback_data="menu_settings"),
        ],
        [
            InlineKeyboardButton("👨‍💻 Talk to Person",  callback_data="menu_support"),
            InlineKeyboardButton("❓ More Info",         callback_data="menu_info"),
        ],
        [
            InlineKeyboardButton("🌐 Website",  url="https://yourwebsite.com"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


# ── AI MODELS MENU ────────────────────────────────────────────────────────────
def ai_models_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("💬 Nano Banana",    callback_data="ai_nano")],
        [InlineKeyboardButton("🎨 Midjourney",     callback_data="ai_midjourney")],
        [InlineKeyboardButton("🖼️ Sora Images",    callback_data="ai_sora")],
        [InlineKeyboardButton("🤖 GPT Images",     callback_data="ai_gpt_image")],
        [InlineKeyboardButton("🎨 Flux Images",    callback_data="ai_flux")],
        [InlineKeyboardButton("🎥 Veo3 Video",     callback_data="ai_veo")],
        [InlineKeyboardButton("💬 General Chat",   callback_data="ai_chat")],
        [InlineKeyboardButton("🔙 Back",           callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── LEARN AI MENU ─────────────────────────────────────────────────────────────
def learn_ai_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🤖 AI Automation",      callback_data="learn_automation")],
        [InlineKeyboardButton("💬 Custom Chatbots",     callback_data="learn_chatbots")],
        [InlineKeyboardButton("🌐 Web Design + AI",    callback_data="learn_web")],
        [InlineKeyboardButton("📲 Telegram Bots",      callback_data="learn_tgbots")],
        [InlineKeyboardButton("🔧 n8n / Make.com",     callback_data="learn_n8n")],
        [InlineKeyboardButton("📚 All Courses",        callback_data="learn_all")],
        [InlineKeyboardButton("🔙 Back",               callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── CHANNEL MANAGEMENT MENU ───────────────────────────────────────────────────
def channel_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("➕ Add Channel",    callback_data="ch_add"),
            InlineKeyboardButton("📋 My Channels",   callback_data="ch_list"),
        ],
        [
            InlineKeyboardButton("📤 Post to All",   callback_data="ch_post_all"),
            InlineKeyboardButton("📝 Post to One",   callback_data="ch_post_one"),
        ],
        [
            InlineKeyboardButton("✏️ Edit Post",     callback_data="ch_edit"),
            InlineKeyboardButton("🗑️ Delete Post",   callback_data="ch_delete"),
        ],
        [
            InlineKeyboardButton("⏰ Schedule Post", callback_data="ch_schedule"),
            InlineKeyboardButton("📊 Stats",         callback_data="ch_stats"),
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── GROUP MANAGEMENT MENU ─────────────────────────────────────────────────────
def group_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("➕ Add Group",     callback_data="grp_add"),
            InlineKeyboardButton("📋 My Groups",     callback_data="grp_list"),
        ],
        [
            InlineKeyboardButton("📤 Post to All",   callback_data="grp_post_all"),
            InlineKeyboardButton("📢 Announce",      callback_data="grp_announce"),
        ],
        [
            InlineKeyboardButton("🚫 Mute Member",   callback_data="grp_mute"),
            InlineKeyboardButton("👢 Kick Member",   callback_data="grp_kick"),
        ],
        [
            InlineKeyboardButton("🎉 Welcome Msg",   callback_data="grp_welcome"),
            InlineKeyboardButton("📌 Pin Message",   callback_data="grp_pin"),
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── BROADCAST MENU ────────────────────────────────────────────────────────────
def broadcast_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("📢 Broadcast to Channels", callback_data="bc_channels")],
        [InlineKeyboardButton("👥 Broadcast to Groups",   callback_data="bc_groups")],
        [InlineKeyboardButton("🌐 Broadcast to All",      callback_data="bc_all")],
        [InlineKeyboardButton("⏰ Schedule Broadcast",    callback_data="bc_schedule")],
        [InlineKeyboardButton("🔙 Back",                  callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── PROFILE MENU ──────────────────────────────────────────────────────────────
def profile_menu(is_prem: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("📊 My Stats",         callback_data="prof_stats")],
        [InlineKeyboardButton("📋 My Channels & Groups", callback_data="prof_mychannels")],
        [InlineKeyboardButton("🗓️ Scheduled Posts",  callback_data="prof_scheduled")],
    ]
    if not is_prem:
        buttons.append([InlineKeyboardButton("⭐ Upgrade to Premium", callback_data="prof_upgrade")])
    else:
        buttons.append([InlineKeyboardButton("👑 Premium Active ✅",  callback_data="prof_premium_info")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


# ── SETTINGS MENU ─────────────────────────────────────────────────────────────
def settings_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🌐 Change Language",     callback_data="set_lang")],
        [InlineKeyboardButton("🔔 Notifications",       callback_data="set_notif")],
        [InlineKeyboardButton("🗑️ Clear AI Memory",    callback_data="set_clear_mem")],
        [InlineKeyboardButton("📝 Welcome Message",     callback_data="set_welcome")],
        [InlineKeyboardButton("🔙 Back",                callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── ADMIN PANEL MENU ──────────────────────────────────────────────────────────
def admin_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("👥 All Users",      callback_data="adm_users"),
            InlineKeyboardButton("📊 Statistics",     callback_data="adm_stats"),
        ],
        [
            InlineKeyboardButton("📢 Admin Broadcast", callback_data="adm_broadcast"),
            InlineKeyboardButton("⭐ Grant Premium",   callback_data="adm_premium"),
        ],
        [
            InlineKeyboardButton("🚫 Ban User",        callback_data="adm_ban"),
            InlineKeyboardButton("✅ Unban User",      callback_data="adm_unban"),
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── CONFIRM / CANCEL ──────────────────────────────────────────────────────────
def confirm_cancel(confirm_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirm", callback_data=confirm_data),
            InlineKeyboardButton("❌ Cancel",  callback_data="action_cancel"),
        ]
    ])


def back_button(data: str = "menu_main") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=data)]])
