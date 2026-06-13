"""
FAQ Agent — Ka jawaaba su'aalaha ardayda ku saabsan AI-ga
"""
import json
import os

class FAQAgent:
    """Agent-ka FAQ — waxa uu u jawaabaa su'aalaha:
    - AI waa maxay?
    - Sidee loo bilaabaa chatbot?
    - Waa maxay Prompt?
    - iyo kuwa kale oo badan"""

    def __init__(self):
        self.faqs = {
            "ai": {
                "keywords": ["waa maxay ai", "ai waa", "artificial intelligence", "sirdoonka macmal", "ai maxay"],
                "answer": "AI (Artificial Intelligence) waa tignoolajiyad ku dayan karta garashada bini'aadamka — waxay baran kartaa, go'aan qaadan kartaa, oo hadalka dadka ka garan kartaa. Tusaale: ChatGPT, Google Gemini, DeepSeek."
            },
            "chatbot": {
                "keywords": ["chatbot waa maxay", "chatbot maxay", "sidee chatbot", "sida loo sameeyo bot", "bot samee"],
                "answer": "Chatbot waa barnaamij AI ah oo dadka la hadli kara. Waxaad ku sameysan kartaa ManyChat, Botpress, ama Python + Telegram API. Koorsada 1-aad casharada 1-6 ayaa ku baraya sida loo bilaabo."
            },
            "prompt": {
                "keywords": ["prompt waa maxay", "prompt engineering", "sida loo qoro prompt", "prompt macnaha"],
                "answer": "Prompt waa tilmaamaha aad siiso AI-ga. Prompt Engineering waa farshaxanka qorista tilmaamaha si AI-ga uu u jawaabo si sax ah. Fiiri Koorsada 1 casharada 8, 9, 17."
            },
            "manychat": {
                "keywords": ["manychat", "many chat", "manychat waa"],
                "answer": "ManyChat waa qalab lagu dhiso chatbot-yada Facebook Messenger, WhatsApp, iyo Telegram iyadoo aan loo baahnayn code. Koorsada 1 casharada 4, 6, 21 ayaa faahfaahinaya."
            },
            "openaikey": {
                "keywords": ["openai key", "api key", "token", "apikey", "api-ga"],
                "answer": "API key-ga waxaad ka helaysaa https://platform.openai.com/api-keys iyadoo aad u baahan tahay account. Ku qor .env file-kaaga si ammaan ah."
            },
            "telegrambot": {
                "keywords": ["telegram bot", "botfather", "telegram token", "bot telegram"],
                "answer": "Si aad u sameysato Telegram Bot: 1) Tag https://t.me/BotFather 2) /newbot 3) Magac u bixi 4) Token-ka ku qor .env-ga. Koorsada 1 casharada 12, 13, 15, 31 ayaa faahfaahinaya."
            },
            "dropshipping": {
                "keywords": ["dropshipping", "dropshipping waa", "zendrop", "dropship"],
                "answer": "Dropshipping waa ganacsi online ah oo aad iibiso alaab adoon haysan keyd — Zendrop ayaa kaa caawinaysa helista alaabta iyo AI-ga suuqgeynta. Fiiri Koorsada 3."
            },
            "videoediting": {
                "keywords": ["video editing", "invideo", "pictory", "lumen5", "video tifatir"],
                "answer": "AI Video Editing waa qalab lagu sameeyo iyo lagu tafatiro videos-ka iyadoo la adeegsanayo AI. InVideo, Pictory.ai, iyo Lumen5 ayaa ka mid ah. Fiiri Koorsada 2."
            },
            "start": {
                "keywords": ["bilow", "sidee u bilaabaa", "aniga oo cusub", "ma cusbihii", "baro aniga"],
                "answer": "Ku billow Koorsada 1 (40 Cashar AI) — casharada 1 ilaa 5 ayaa ah kuwa ugu fudud. Kadib waxaad u gudbi kartaa Koorsada 2 iyo 3. Dhammaan casharada waa bilaash!"
            }
        }

    def get_answer(self, question):
        """Raadi jawaabta su'aasha"""
        question = question.lower()
        for faq in self.faqs.values():
            for keyword in faq["keywords"]:
                if keyword in question:
                    return faq["answer"]
        return None

    def get_all_faqs(self):
        """Soo bandhig dhamaan FAQ-yada"""
        lines = ["❓ **FAQ-yada Somali AI Academy**\n"]
        topics = {
            "ai": "AI waa maxay?",
            "chatbot": "Chatbot waa maxay?",
            "prompt": "Prompt waa maxay?",
            "manychat": "ManyChat waa maxay?",
            "telegrambot": "Sidee loo sameeyaa Telegram Bot?",
            "dropshipping": "Dropshipping waa maxay?",
            "videoediting": "AI Video Editing waa maxay?",
            "start": "Anigu cusub baan ahay — xagee ka bilaabaa?"
        }
        for key, name in topics.items():
            lines.append(f"  • **{name}** — {self.faqs[key]['answer'][:80]}...")
        return "\n".join(lines)
