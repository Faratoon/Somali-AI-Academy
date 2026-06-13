# Deploy Gareynta Somali AI Academy

## 1. Local (Tijaabo)

```bash
cd Somali-AI-Academy
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 delivery/telegram/bot.py
```

## 2. PM2 (Production — Ugu Fiican)

```bash
bash deploy/deploy.sh
# Dooro 1 (PM2)
```

## 3. Docker

```bash
docker compose up -d --build
```

## 4. Render (Free Cloud)

1. Tag https://render.com
2. New + Web Service
3. Ku xidh GitHub repo-gaaga
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python3 delivery/telegram/bot.py`
6. Environment Variables-ka ku qor `.env`-ga

## 5. Railway (Free Cloud)

1. Tag https://railway.app
2. New Project + Deploy from GitHub repo
3. Variables-ka ku qor

## 6. Google Cloud VM

```bash
# SSH gasho VM-ka
sudo apt update && sudo apt install -y python3-pip git
git clone https://github.com/YOUR_USERNAME/Somali-AI-Academy.git
cd Somali-AI-Academy
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Config
nano .env  # Ku qor token-ka

# PM2
npm install -g pm2
pm2 start delivery/telegram/bot.py --interpreter python3 --name somai-bot
pm2 save
pm2 startup
```
