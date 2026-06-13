# 🤖 Mfaratoon AI Bot — خدمة إدارة القنوات والمجموعات

<div align="center">

![Bot Status](https://img.shields.io/badge/Bot-Online%20✅-brightgreen?style=for-the-badge&logo=telegram)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange?style=for-the-badge&logo=firebase)
![AI](https://img.shields.io/badge/AI-OpenRouter%20%2B%20Groq-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)

### 🌟 Bot horumarsan oo loogu talagalay maareynta Channels iyo Groups Telegram
### *Dhisay: Mfaratoon — Macallin AI Automation*

[📲 Bot-ka Fur](https://t.me/your_bot) • [📺 YouTube](https://youtube.com) • [📢 Channel](https://t.me/yourchannel)

</div>

---

## 📖 Waa Maxay Bot-kan?

Bot-kan waa **bot horumarsan** oo toos loogu dhisay **maareynta channels iyo groups** Telegram. Wuxuu kuu sahlayaa inaad:

- 📢 **Hal mar** u dirtid post dhammaan channels-kaaga
- 🤖 **AI Assistant** — Somali, Carabi, iyo Ingiriisi ku hadla
- ⏰ **Schedule** — Posts ugu qors waqti gaar ah
- 🎓 **40+ Koorso FREE** — AI Automation, Chatbots, Web Design

---

## ✨ Features — Waxa Bot-ku Samayn Karo

### 📢 Channel & Group Management
| Feature | Sharaxaad |
|---------|-----------|
| ➕ Add Channel/Group | Channel ama Group ku dar bot-ka |
| 📤 Broadcast | Hal mar u dir dhammaan channels |
| ✏️ Edit Post | Post hore wax ka beddel |
| 🗑️ Delete Post | Post tirtir channel kasta |
| ⏰ Schedule Post | Qors post waqti gaar ah |
| 🎉 Welcome Message | Xubin cusub soo dhawee |

### 🤖 AI Assistant
| Feature | Sharaxaad |
|---------|-----------|
| 💬 Nano Banana | Model xawli oo xoog leh |
| 🎨 Midjourney Style | Sawir prompt generation |
| 🖼️ Sora Images | OpenAI Sora style |
| 🤖 GPT Images | GPT-4o image creation |
| 🎨 Flux Images | Flux model |
| 🎥 Veo3 Video | Video creation prompts |
| 🧠 Memory | Wada hadal xasuus Firebase |

### 👑 Premium System
| Plan | Features | Qiimaha |
|------|----------|---------|
| 🆓 Trial (30 Maalin) | Dhammaan features | FREE |
| 👑 Premium | Unlimited + Priority | Contact |

---

## 📁 Qaab-dhismeedka Project-ka

```
📦 telebot1/
│
├── 🚀 main.py                  # Bot-ka bilowga
├── ⚙️  config.py               # Settings & API keys loader
├── 📋 requirements.txt         # Python packages
├── 🔑 .env                     # API Keys (NEVER upload!)
├── 📄 Procfile                 # Railway deployment
├── 🐍 runtime.txt              # Python version
│
├── 📂 handlers/                # Feature handlers
│   ├── start.py                # /start + welcome
│   ├── ai_chat.py              # AI assistant
│   ├── channels.py             # Channel/Group management
│   ├── scheduler.py            # Scheduled posts
│   ├── profile.py              # User profile
│   ├── admin.py                # Admin panel
│   ├── courses.py              # Courses & support
│   └── callbacks.py            # Menu routing
│
└── 📂 utils/                   # Helper modules
    ├── firebase.py             # Database helpers
    ├── menus.py                # All keyboards & menus
    └── helpers.py              # Shared functions
```

---

## 🔧 Setup — Talaabo Talaabo

### 📋 Waxa Loo Baahan Yahay
- ✅ Python 3.11+
- ✅ Telegram Bot Token ([@BotFather](https://t.me/botfather))
- ✅ OpenRouter API Key ([openrouter.ai](https://openrouter.ai/keys))
- ✅ Groq API Key ([console.groq.com](https://console.groq.com/keys))
- ✅ Firebase Project ([console.firebase.google.com](https://console.firebase.google.com))

---

### ⚙️ Local Setup (PC-kaaga)

**1️⃣ Clone gareey:**
```bash
git clone https://github.com/Faratoon/telebot1.git
cd telebot1
```

**2️⃣ Install packages:**
```bash
pip install -r requirements.txt
```

**3️⃣ .env file samee:**
```bash
# .env.example ku copy gareey .env
copy .env.example .env
# Kadibna Notepad ku fur oo keys-kaaga ku buuxi
```

**4️⃣ Firebase credentials:**
```
data/firebase_credentials.json  ← halkan dhig
```

**5️⃣ Run:**
```bash
python main.py
```

---

### ☁️ Railway Deploy (24/7 Online)

**1️⃣ Railway.app account samee:**
> [railway.app](https://railway.app) → Login with GitHub

**2️⃣ New Project:**
> New Project → Deploy from GitHub → Xulo `telebot1`

**3️⃣ Environment Variables ku dar:**
> Railway → Variables tab

```env
BOT_TOKEN                 = your_token
ADMIN_IDS                 = your_telegram_id
OPENROUTER_API_KEY        = your_key
GROQ_API_KEY              = your_key
FIREBASE_DATABASE_URL     = https://your-project.firebaseio.com
FIREBASE_CREDENTIALS_JSON = { paste full JSON content here }
```

**4️⃣ Deploy!** ✅ Bot waa online 24/7!

---

## 🎮 Commands — Amarrada Bot-ka

```
/start       → 🏠 Menu ugu weyn fur
/help        → ❓ Dhammaan commands arag
/menu        → 🎛️ Inline menu
/profile     → 👤 Profile-kaaga arag
/channels    → 📢 Channels maamul
/groups      → 👥 Groups maamul
/broadcast   → 📤 Dhammaan channels u dir
/schedule    → ⏰ Post qors
/clear       → 🗑️ AI memory nadiifi
/admin       → 🔧 Admin panel (admins only)

── AI Models ──────────────────
/nano        → 💬 Nano Banana AI
/midjourney  → 🎨 Midjourney Images
/sora        → 🖼️ Sora Images
/gpt_image   → 🤖 GPT Images
/flux        → 🎨 Flux Images
/veo         → 🎥 Veo3 Video
```

---

## 🔑 Environment Variables

| Variable | Sharaxaad | Meesha laga helo |
|----------|-----------|-----------------|
| `BOT_TOKEN` | Telegram bot token | @BotFather |
| `ADMIN_IDS` | Admin IDs (comma sep) | @userinfobot |
| `OPENROUTER_API_KEY` | OpenRouter API | openrouter.ai/keys |
| `GROQ_API_KEY` | Groq API | console.groq.com |
| `FIREBASE_DATABASE_URL` | Firebase URL | Firebase Console |
| `FIREBASE_CREDENTIALS_JSON` | Firebase JSON (Railway) | Firebase → Service Accounts |
| `FIREBASE_CREDENTIALS_PATH` | JSON file path (Local) | Local file |
| `DAILY_MSG_LIMIT` | Daily message limit | Default: 40 |
| `MAX_MEDIA_SIZE_MB` | Max media size MB | Default: 5 |
| `TRIAL_DAYS` | Trial period days | Default: 30 |
| `COURSE_CHANNEL` | Course channel link | Your channel |
| `SUPPORT_USERNAME` | Support username | @Mfaratoon |

---

## 🛡️ Xeerarka Amaanka

- 🔐 `.env` file weligaa GitHub ku **MA** upload
- 🔐 `firebase_credentials.json` weligaa share **MA** samee
- 🔐 `.gitignore` wuxuu **toos** u ilaaliyaa fayl-yadan
- 🔄 Key-yada beddel kasta oo aad shakiso

---

## 🚀 Roadmap — Mustaqbalka

- [ ] 📊 Analytics dashboard
- [ ] 🔔 Auto-notification system  
- [ ] 💳 Payment integration
- [ ] 📱 Multi-language UI
- [ ] 🤖 Advanced AI models
- [ ] 📈 Channel growth tools

---

## 👨‍💻 Dhisay

<div align="center">

**Mfaratoon** — AI Automation Teacher

[![YouTube](https://img.shields.io/badge/YouTube-70k+-red?style=flat&logo=youtube)](https://youtube.com)
[![Telegram](https://img.shields.io/badge/Telegram-140k+-blue?style=flat&logo=telegram)](https://t.me/yourchannel)

*40+ Koorso FREE ah — AI Automation, Chatbots, Web Design*

</div>

---

<div align="center">
⭐ Haddaad project-kan jecelahay, star-ka riix! ⭐
</div>
