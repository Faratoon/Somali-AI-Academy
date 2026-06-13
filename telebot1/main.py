"""
main.py  –  FINAL CLEAN VERSION  (all bugs fixed)
Mfaratoon AI Channel & Group Manager Bot
"""
import logging
import warnings
warnings.filterwarnings("ignore")

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, filters,
)
import config

# ── Handlers ──────────────────────────────────────────────────────────────────
from handlers.start import start_command, help_command, menu_command

from handlers.ai_chat import (
    ai_chat_handler, ai_menu, select_ai_model, clear_memory_command,
    nano_command, midjourney_command, sora_command,
    gpt_image_command, flux_command, veo_command,
)
from handlers.channels import (
    channels_menu_handler, groups_menu_handler,
    add_channel_start, add_group_start, receive_channel_id,
    list_channels, remove_channel_cb,
    post_all_start, receive_post_and_send,
    delete_post_start, receive_delete_msg,
    edit_post_start, receive_edit_msg_id, receive_edit_text,
    set_welcome_start, receive_welcome_text, new_member_handler,
    WAITING_CHANNEL_ID, WAITING_GROUP_ID, WAITING_POST_TEXT,
    WAITING_DELETE_MSG_ID, WAITING_EDIT_MSG_ID, WAITING_EDIT_TEXT,
    WAITING_WELCOME_TEXT,
)
from handlers.scheduler import (
    schedule_menu, schedule_new_start,
    receive_sched_content, receive_sched_time,
    view_scheduled_posts, scheduler,
    SCHED_TEXT, SCHED_TIME,
)
from handlers.profile  import profile_command, premium_info
from handlers.admin    import (
    admin_command, admin_stats,
    admin_broadcast_start, receive_admin_broadcast,
    grant_premium_start, receive_premium_id,
    ban_user_start, receive_ban_id,
    ADMIN_BROADCAST_TEXT, ADMIN_PREMIUM_ID, ADMIN_BAN_ID,
)
from handlers.courses  import learn_ai_handler, support_handler, info_handler
from handlers.callbacks import (
    main_menu_cb, action_cancel, coming_soon_cb,
    broadcast_menu_cb, settings_menu_cb,
    set_language_cb, save_language_cb,
    notifications_cb, save_notif_cb, clear_memory_cb,
)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format   = "%(asctime)s [%(levelname)s] %(message)s",
    level    = logging.INFO,
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ]
)
logger = logging.getLogger(__name__)

MEDIA = filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.AUDIO


def build_conversations():
    """Build all ConversationHandlers and return as list."""

    add_ch = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(add_channel_start, pattern="^ch_add$"),
            CallbackQueryHandler(add_group_start,   pattern="^grp_add$"),
        ],
        states={
            WAITING_CHANNEL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_channel_id)],
            WAITING_GROUP_ID:   [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_channel_id)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    broadcast = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(post_all_start,
                pattern="^(ch_post_all|grp_post_all|bc_channels|bc_groups|bc_all)$"),
        ],
        states={
            WAITING_POST_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_post_and_send),
                MessageHandler(MEDIA, receive_post_and_send),
            ],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    delete_post = ConversationHandler(
        entry_points=[CallbackQueryHandler(delete_post_start, pattern="^ch_delete$")],
        states={
            WAITING_DELETE_MSG_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_delete_msg)
            ],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    edit_post = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_post_start, pattern="^ch_edit$")],
        states={
            WAITING_EDIT_MSG_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_edit_msg_id)
            ],
            WAITING_EDIT_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_edit_text)
            ],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    sched = ConversationHandler(
        entry_points=[CallbackQueryHandler(schedule_new_start, pattern="^sched_new$")],
        states={
            SCHED_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_sched_content),
                MessageHandler(filters.PHOTO | filters.VIDEO,   receive_sched_content),
            ],
            SCHED_TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_sched_time)
            ],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    welcome = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(set_welcome_start, pattern="^(grp_welcome|set_welcome)$")
        ],
        states={
            WAITING_WELCOME_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_welcome_text)
            ],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    adm_bc = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_broadcast_start, pattern="^adm_broadcast$")],
        states={
            ADMIN_BROADCAST_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_admin_broadcast)
            ],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    adm_prem = ConversationHandler(
        entry_points=[CallbackQueryHandler(grant_premium_start, pattern="^adm_premium$")],
        states={
            ADMIN_PREMIUM_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_premium_id)
            ],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    adm_ban = ConversationHandler(
        entry_points=[CallbackQueryHandler(ban_user_start, pattern="^adm_ban$")],
        states={
            ADMIN_BAN_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_ban_id)
            ],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False, allow_reentry=True,
    )

    return [add_ch, broadcast, delete_post, edit_post, sched, welcome,
            adm_bc, adm_prem, adm_ban]


def main():
    app = Application.builder().token(config.BOT_TOKEN).build()

    # ── Conversations ────────────────────────────────────────────────────────
    for conv in build_conversations():
        app.add_handler(conv)

    # ── Commands ─────────────────────────────────────────────────────────────
    cmds = [
        ("start",      start_command),
        ("help",       help_command),
        ("menu",       menu_command),
        ("profile",    profile_command),
        ("channels",   channels_menu_handler),
        ("groups",     groups_menu_handler),
        ("broadcast",  broadcast_menu_cb),
        ("schedule",   schedule_menu),
        ("settings",   settings_menu_cb),
        ("admin",      admin_command),
        ("clear",      clear_memory_command),
        ("nano",       nano_command),
        ("midjourney", midjourney_command),
        ("sora",       sora_command),
        ("gpt_image",  gpt_image_command),
        ("flux",       flux_command),
        ("veo",        veo_command),
    ]
    for cmd, fn in cmds:
        app.add_handler(CommandHandler(cmd, fn))

    # ── Callbacks ─────────────────────────────────────────────────────────────
    cbs = [
        # Navigation
        ("^menu_main$",        main_menu_cb),
        ("^menu_channels$",    channels_menu_handler),
        ("^menu_groups$",      groups_menu_handler),
        ("^menu_broadcast$",   broadcast_menu_cb),
        ("^menu_settings$",    settings_menu_cb),
        ("^menu_ai$",          ai_menu),
        ("^menu_learn$",       learn_ai_handler),
        ("^menu_schedule$",    schedule_menu),
        ("^menu_profile$",     profile_command),
        ("^menu_support$",     support_handler),
        ("^menu_info$",        info_handler),

        # AI model selection
        ("^ai_(nano|midjourney|sora|gpt_image|flux|veo|chat)$", select_ai_model),

        # Learn / Courses
        ("^learn_",            learn_ai_handler),

        # Channels / Groups
        ("^(ch_list|grp_list)$",  list_channels),
        ("^rm_(channel|group)_.+", remove_channel_cb),

        # Schedule
        ("^sched_list$",       view_scheduled_posts),

        # Profile / Premium
        ("^(prof_upgrade|prof_premium_info)$", premium_info),
        ("^(prof_stats|prof_mychannels|prof_scheduled)$", profile_command),

        # Settings
        ("^set_lang$",         set_language_cb),
        ("^lang_(so|ar|en)$",  save_language_cb),
        ("^set_notif$",        notifications_cb),
        ("^notif_(on|off)$",   save_notif_cb),
        ("^set_clear_mem$",    clear_memory_cb),

        # Admin
        ("^adm_stats$",        admin_stats),

        # Coming soon
        ("^(ch_stats|grp_pin|grp_mute|grp_kick|grp_announce|adm_users|adm_unban)$", coming_soon_cb),

        # Cancel
        ("^action_cancel$",    action_cancel),
    ]
    for pattern, fn in cbs:
        app.add_handler(CallbackQueryHandler(fn, pattern=pattern))

    # ── Messages ─────────────────────────────────────────────────────────────
    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler
    ))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
        ai_chat_handler
    ))
    app.add_handler(MessageHandler(
        MEDIA & filters.ChatType.PRIVATE,
        ai_chat_handler
    ))

    # ── Start ────────────────────────────────────────────────────────────────
    scheduler.start()
    logger.info("Scheduler started.")

    print("\n" + "═"*50)
    print("  🤖  Mfaratoon AI Bot — ONLINE ✅")
    print("  📲  Telegram: /start")
    print("  🛑  Stop: Ctrl+C")
    print("═"*50 + "\n")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
