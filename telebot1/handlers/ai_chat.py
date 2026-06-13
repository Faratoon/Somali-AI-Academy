"""
handlers/ai_chat.py  –  AI assistant using OpenRouter / Groq
"""
import aiohttp
import json
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode, ChatAction
import config
from utils import firebase
from utils.helpers import check_limits
from utils.menus import ai_models_menu, back_button

# Conversation states
AI_CHATTING = 1


async def ai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "🤖 *AI Assistant*\n\n"
            "Xulo model-ka aad rabto:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_models_menu()
        )
    else:
        await update.message.reply_text(
            "🤖 *AI Assistant*\n\nXulo model-ka aad rabto:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_models_menu()
        )


MODEL_MAP = {
    "ai_nano":      ("meta-llama/llama-3.1-8b-instruct:free", "💬 Nano Banana"),
    "ai_chat":      ("meta-llama/llama-3.1-8b-instruct:free", "💬 General Chat"),
    "ai_midjourney":("openai/gpt-4o", "🎨 Midjourney Style"),
    "ai_sora":      ("openai/gpt-4o", "🖼️ Sora Style"),
    "ai_gpt_image": ("openai/gpt-4o", "🤖 GPT Image"),
    "ai_flux":      ("openai/gpt-4o", "🎨 Flux Style"),
    "ai_veo":       ("openai/gpt-4o", "🎥 Veo3 Video"),
}

async def select_ai_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cb_data = query.data

    model_id, model_name = MODEL_MAP.get(cb_data, ("meta-llama/llama-3.1-8b-instruct:free", "💬 AI"))
    context.user_data["ai_model"]      = model_id
    context.user_data["ai_model_name"] = model_name
    context.user_data["ai_mode"]       = True

    await query.edit_message_text(
        f"✅ *{model_name}* selected!\n\n"
        f"💬 Hadda wax i weydii – Somali, Arabic ama English ku qor.\n"
        f"🔄 /clear si uu tariikhda uga tirtiro\n"
        f"🔙 /menu si aad ugu noqoto menu-ga",
        parse_mode=ParseMode.MARKDOWN,
    )


async def ai_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages when AI mode is active."""
    if not context.user_data.get("ai_mode"):
        return  # Not in AI mode

    user    = update.effective_user
    uid     = user.id
    text    = update.message.text or ""

    # Check limits
    if not await check_limits(update, context):
        return

    # Show typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Get conversation history
    history = firebase.get_conversation(uid)

    # Add user message
    history.append({"role": "user", "content": text})

    # Build messages list
    messages = [{"role": "system", "content": config.AI_SYSTEM_PROMPT}] + history

    model = context.user_data.get("ai_model", "meta-llama/llama-3.1-8b-instruct:free")

    try:
        reply_text = await call_openrouter(messages, model)
    except Exception as e:
        reply_text = f"❌ AI jawaab ma siin karin: {str(e)[:100]}"

    # Save updated history
    history.append({"role": "assistant", "content": reply_text})
    firebase.save_conversation(uid, history)

    await update.message.reply_text(
        reply_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_ai")
    )


async def call_openrouter(messages: list, model: str) -> str:
    """Call OpenRouter API."""
    if not config.OPENROUTER_API_KEY:
        return "⚠️ OpenRouter API key ma jiro. Fadlan .env file-ka hubi."

    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://t.me/yourbot",
        "X-Title":       "Mfaratoon AI Bot",
    }
    payload = {
        "model":       model,
        "messages":    messages,
        "max_tokens":  1024,
        "temperature": 0.7,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            data = await resp.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            elif "error" in data:
                return f"❌ API Error: {data['error'].get('message', 'Unknown error')}"
            return "❌ Jawaab lama helin."


async def call_groq(messages: list) -> str:
    """Fallback: Call Groq API."""
    if not config.GROQ_API_KEY:
        return "⚠️ Groq API key ma jiro."

    headers = {
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model":    "llama3-8b-8192",
        "messages": messages,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        ) as resp:
            data = await resp.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            return "❌ Groq jawaab ma siinin."


async def clear_memory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    firebase.clear_conversation(uid)
    await update.message.reply_text(
        "🗑️ *AI memory cleared!*\n\nWada hadashu waa nadiifnaatay. "
        "Waxaad bilaabi kartaa wada hadal cusub.",
        parse_mode=ParseMode.MARKDOWN
    )


async def nano_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ai_model"]      = "meta-llama/llama-3.1-8b-instruct:free"
    context.user_data["ai_model_name"] = "💬 Nano Banana"
    context.user_data["ai_mode"]       = True
    await update.message.reply_text("💬 *Nano Banana* ready! Wax i weydii 👇", parse_mode=ParseMode.MARKDOWN)

async def midjourney_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ai_model"]      = "openai/gpt-4o"
    context.user_data["ai_model_name"] = "🎨 Midjourney"
    context.user_data["ai_mode"]       = True
    await update.message.reply_text("🎨 *Midjourney* mode active! Sawir prompt-kaaga qor 👇", parse_mode=ParseMode.MARKDOWN)

async def sora_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ai_model"]      = "openai/gpt-4o"
    context.user_data["ai_model_name"] = "🖼️ Sora"
    context.user_data["ai_mode"]       = True
    await update.message.reply_text("🖼️ *Sora Images* mode active! 👇", parse_mode=ParseMode.MARKDOWN)

async def gpt_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ai_model"]      = "openai/gpt-4o"
    context.user_data["ai_model_name"] = "🤖 GPT Image"
    context.user_data["ai_mode"]       = True
    await update.message.reply_text("🤖 *GPT Image* mode active! 👇", parse_mode=ParseMode.MARKDOWN)

async def flux_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ai_model"]      = "openai/gpt-4o"
    context.user_data["ai_model_name"] = "🎨 Flux"
    context.user_data["ai_mode"]       = True
    await update.message.reply_text("🎨 *Flux Images* mode active! 👇", parse_mode=ParseMode.MARKDOWN)

async def veo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ai_model"]      = "openai/gpt-4o"
    context.user_data["ai_model_name"] = "🎥 Veo3"
    context.user_data["ai_mode"]       = True
    await update.message.reply_text("🎥 *Veo3 Video* mode active! Prompt-kaaga qor 👇", parse_mode=ParseMode.MARKDOWN)
