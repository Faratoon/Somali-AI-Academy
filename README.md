# Somali AI Academy (SOMAI)

**Waxbarasho AI ah oo af-Soomaali ah** — 4 koorso, 60+ cashar, bots Telegram & WhatsApp ah.

## Dulmarka

Somali AI Academy waa mashruuc furan oo loogu talagalay in dadka Soomaaliyeed ay ku bartaan AI-ga, chatbot-yada, video editing-ka, iyo ganacsiga AI-ga. Waxaa ka mid ah:

- 📚 **4 koorso** oo dhammaystiran (40 cashar AI + Video Editing + Dropshipping + Bulsho)
- 🤖 **Agents** sida Course Agent, FAQ Agent, Schedule Agent
- 📱 **Telegram & WhatsApp bots** oo toos u gudbiya casharada
- 📅 **Jadwal & notifications** oo otomaatig ah
- 🧪 **Quiz-yo & layliyo** oo AI ku dhisan

## Qaabka Repo-ga

```
Somali-AI-Academy/
├── courses/                    # Casharada oo qaabeysan
│   ├── koorsada-1-40-cashar-ai/     # YouTube: Chatbot, Prompt, AI Tools...
│   ├── koorsada-2-ai-video-editing/  # Loom: InVideo, Pictory, Lumen5
│   ├── koorsada-3-dropshipping-zendrop/ # Loom: Dropshipping AI
│   └── koorsada-4-bulshada/          # WhatsApp, Telegram, YouTube links
├── agents/                     # AI Agents-ka
│   ├── course_agent.py         # Course-ka sameeya & soo bandhiga
│   ├── faq_agent.py            # FAQ-ka kaa jawaaba
│   ├── schedule_agent.py       # Jadwalka qorsheeya
│   └── notify_agent.py         # Ardaada u soo dira wargelin
├── delivery/                   # Bots-ka gudbiya casharada
│   ├── telegram/               # Telegram bot-ka
│   └── whatsapp/               # WhatsApp bot-ka
├── schedule/                   # Jadwalka & cron jobs
├── exercises/                  # Quiz-yo & layliyo
├── data/                       # Xogta koorsooyinka (JSON)
├── deploy/                     # Deploy scripts
├── docs/                       # Documentation dheeraad ah
├── config.py                   # Configuration guud
└── requirements.txt            # Python dependencies
```

## Sida Loo Bilaabo

### 1. Clone
```bash
git clone https://github.com/YOUR_USERNAME/Somali-AI-Academy.git
cd Somali-AI-Academy
```

### 2. Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Config
```bash
cp .env.example .env
# Ku buuxi API keys-kaaga (.env file-ka)
```

### 4. Run Bot-ka
```bash
# Telegram bot-ka
python3 delivery/telegram/bot.py

# Jadwalka
python3 schedule/scheduler.py
```

### 5. Deploy (Production)
```bash
# PM2
pm2 start delivery/telegram/bot.py --interpreter python3 --name somai-bot

# Docker
docker compose up -d
```

## API Keys-ka Looga Baahan Yahay

| Key | Halka laga helo | Sharaxaad |
|-----|----------------|-----------|
| `TELEGRAM_BOT_TOKEN` | https://t.me/BotFather | Token-ka bot-kaaga |
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys | OpenAI GPT API |
| `WHATSAPP_API_KEY` | (WhatsApp Business API) | WhatsApp bot |

## Koorsooyinka

| # | Koorsada | Casharo | Nooca |
|---|----------|---------|-------|
| 1 | 40 Cashar AI — Chatbot, Prompt, AI Tools | 40 | YouTube |
| 2 | 14 Maalmood AI Video Editing | 10 | Loom |
| 3 | Dropshipping iyo Zendrop AI | 10 | Loom |
| 4 | Iloodheeraad & Bulshada | 10 | WhatsApp/Telegram/YouTube/FB |

## Agents-ka

### Course Agent
Bot-ka ayaa iska soo bandhiga casharada dhigmaya, oo ardaygu wuu dooran karaa.

### FAQ Agent
Ka jawaaba su'aalaha ardayda ku saabsan AI-ga, chatbot-yada, iyo koorsooyinka.

### Schedule Agent
Jadwalka casharada oo otomaatig ah — ardayda waxaa loo dira wargelin ka hor.

### Notify Agent
Ardayda waxaa loo dira wargelin marka cashar cusub la soo dhigay ama uu jiro live session.

## Kaalin Qaadid (Contributing)

Mashruucan waa furan yahay! Haddii aad rabto inaad ka qayb qaadato:
1. Fork repo-ga
2. Samee branch cusub
3. Push oo fur Pull Request

## License
MIT
