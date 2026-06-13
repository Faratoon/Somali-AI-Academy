"""
handlers/courses.py  –  Learn AI / Courses section
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import config
from utils.menus import learn_ai_menu, back_button


COURSES_DATA = {
    "learn_automation": {
        "title": "🤖 AI Automation",
        "desc": (
            "📚 *AI Automation Courses*\n\n"
            "Waxaad baranayso:\n"
            "• n8n workflow automation\n"
            "• Make.com (Integromat)\n"
            "• Zapier automations\n"
            "• API integrations\n"
            "• Trigger-based workflows\n\n"
            "🔗 *Course Link:* [Ku dhageyso halkaan]({channel})\n"
            "📞 Support: {support}"
        )
    },
    "learn_chatbots": {
        "title": "💬 Custom Chatbots",
        "desc": (
            "📚 *Custom Chatbot Courses*\n\n"
            "Waxaad baranayso:\n"
            "• Botpress setup & flows\n"
            "• Chatfuel for Facebook\n"
            "• ManyChat automation\n"
            "• ChatSail & ChatBase\n"
            "• JotForm AI forms\n"
            "• OpenRouter integration\n\n"
            "🔗 *Course Link:* [Ku dhageyso halkaan]({channel})\n"
            "📞 Support: {support}"
        )
    },
    "learn_web": {
        "title": "🌐 Web Design + AI",
        "desc": (
            "📚 *AI Web Design Courses*\n\n"
            "Waxaad baranayso:\n"
            "• Vibe Coding (no-code web)\n"
            "• Landing page design\n"
            "• AI website builders\n"
            "• HTML/CSS basics\n"
            "• WordPress + AI plugins\n\n"
            "🔗 *Course Link:* [Ku dhageyso halkaan]({channel})\n"
            "📞 Support: {support}"
        )
    },
    "learn_tgbots": {
        "title": "📲 Telegram Bots",
        "desc": (
            "📚 *Telegram Bot Development*\n\n"
            "Waxaad baranayso:\n"
            "• BotFather setup\n"
            "• Python telegram bot\n"
            "• No-code bot builders\n"
            "• Firebase integration\n"
            "• Channel management bots\n"
            "• AI-powered bots\n\n"
            "🔗 *Course Link:* [Ku dhageyso halkaan]({channel})\n"
            "📞 Support: {support}"
        )
    },
    "learn_n8n": {
        "title": "🔧 n8n / Make.com",
        "desc": (
            "📚 *n8n & Make.com Automation*\n\n"
            "Waxaad baranayso:\n"
            "• n8n self-hosted setup\n"
            "• Make.com scenarios\n"
            "• Webhook integrations\n"
            "• Social media automation\n"
            "• Email automation\n"
            "• Database automation\n\n"
            "🔗 *Course Link:* [Ku dhageyso halkaan]({channel})\n"
            "📞 Support: {support}"
        )
    },
    "learn_all": {
        "title": "📚 All Courses (40+ Courses)",
        "desc": (
            "🎓 *Mfaratoon AI Academy – 40+ Courses*\n\n"
            "📦 *Full Course List:*\n"
            "1️⃣ AI Automation (n8n, Make)\n"
            "2️⃣ Custom Chatbots\n"
            "3️⃣ Telegram Bot Dev\n"
            "4️⃣ Web Design + AI\n"
            "5️⃣ AI Image Generation\n"
            "6️⃣ AI Video Creation\n"
            "7️⃣ Prompt Engineering\n"
            "8️⃣ OpenRouter / Groq APIs\n"
            "9️⃣ Firebase + AI\n"
            "🔟 Business Automation\n"
            "... iyo 30+ courses dheeraad ah!\n\n"
            "💰 *Dhammaantood FREE ah!*\n\n"
            "🔗 *Channel:* [Arag Courses]({channel})\n"
            "📞 *Support:* {support}\n"
            "🌐 *Website:* {website}"
        )
    }
}


async def learn_ai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        cb = query.data

        if cb == "menu_learn":
            await query.edit_message_text(
                "☘️ *Learn AI – Courses*\n\nXulo koorsaha aad rabto:",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=learn_ai_menu()
            )
            return

        course = COURSES_DATA.get(cb)
        if course:
            text = course["desc"].format(
                channel = config.COURSE_CHANNEL,
                support = config.SUPPORT_USERNAME,
                website = config.WEBSITE_URL
            )
            await query.edit_message_text(
                text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=back_button("menu_learn"),
                disable_web_page_preview=False
            )
    else:
        await update.message.reply_text(
            "☘️ *Learn AI – Courses*\n\nXulo koorsaha aad rabto:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=learn_ai_menu()
        )


async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        target = query
    else:
        target = update.message

    text = (
        f"👨‍💻 *Talk to a Person / Support*\n\n"
        f"📞 Telegram: {config.SUPPORT_USERNAME}\n"
        f"🌐 Website: {config.WEBSITE_URL}\n\n"
        f"⏰ Response time: Usually within a few hours\n"
        f"🌍 Languages: Somali, Arabic, English"
    )
    if hasattr(target, 'edit_message_text'):
        await target.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_button("menu_main"))
    else:
        await target.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()

    text = (
        "❓ *More Info*\n\n"
        "🤖 *Bot Features:*\n"
        "• Multi-channel management\n"
        "• AI assistant (Somali/Arabic/English)\n"
        "• Schedule & auto-post\n"
        "• Welcome messages\n"
        "• Group admin tools\n"
        "• 40+ AI courses (FREE)\n\n"
        f"📢 *Channel:* {config.COURSE_CHANNEL}\n"
        f"📞 *Support:* {config.SUPPORT_USERNAME}\n"
        f"🌐 *Website:* {config.WEBSITE_URL}\n\n"
        "💡 Use /help to see all commands"
    )
    if query:
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_button("menu_main"))
    else:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
