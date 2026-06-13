#!/bin/bash
# ==============================================
# Somali AI Academy — Deploy Script
# ==============================================
# Waxa uu kuu caawinayaa inaad si dhakhso ah u
# dejiso bot-ka & scheduler-ka
# ==============================================

set -e

echo "=============================================="
echo "  Somali AI Academy — Deploy"
echo "=============================================="

# 1. Check .env exists
if [ ! -f .env ]; then
    echo "❌ .env file-ka ma jiro!"
    echo "   Ka samee: cp .env.example .env"
    echo "   Kadib ku buuxi token-kaaga."
    exit 1
fi

# 2. Check Python venv
if [ ! -d venv ]; then
    echo "📦 Sameynaya virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# 3. Install requirements
echo "📥 Rakibayaa dependencies-ka..."
pip install -q -r requirements.txt

# 4. Choose deploy mode
echo ""
echo "Dooro habka deploy-ga:"
echo "  1) PM2 (ugu fiican)"
echo "  2) Docker"
echo "  3) nohup (fudud)"
echo "  4) Tijaabo (run now)"
echo ""
read -p "Dooro (1-4): " mode

case $mode in
    1)
        echo "🚀 PM2 ku shubayaa..."
        command -v pm2 || npm install -g pm2
        
        # Telegram bot
        pm2 start delivery/telegram/bot.py \
            --interpreter python3 \
            --name somai-bot \
            -- --env $(pwd)/.env
        
        # Scheduler
        pm2 start schedule/scheduler.py \
            --interpreter python3 \
            --name somai-scheduler \
            -- --env $(pwd)/.env
        
        pm2 save
        pm2 status
        echo "✅ PM2 deploy waa gudbantahay!"
        ;;
    2)
        echo "🐳 Docker ku shubayaa..."
        docker compose up -d --build
        echo "✅ Docker deploy waa gudbantahay!"
        ;;
    3)
        echo "🟢 nohup ku shubayaa..."
        nohup python3 delivery/telegram/bot.py > bot.log 2>&1 &
        nohup python3 schedule/scheduler.py > scheduler.log 2>&1 &
        echo "✅ Bot-ka wuu shaqeynayaa (PID: $!)"
        echo "   Log-ga: tail -f bot.log"
        ;;
    4)
        echo "🧪 Tijaabo..."
        echo "   Bot: python3 delivery/telegram/bot.py"
        echo "   Scheduler: python3 schedule/scheduler.py"
        python3 delivery/telegram/bot.py &
        ;;
esac
