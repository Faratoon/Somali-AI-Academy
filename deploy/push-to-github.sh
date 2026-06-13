#!/bin/bash
# ==============================================
# GitHub Push — Somali AI Academy
# ==============================================
# Waxa uu repo-ga ku shubayaa GitHub-kaaga
# ==============================================

set -e

echo "=============================================="
echo "  Somali AI Academy — GitHub Push"
echo "=============================================="

# 1. Check GitHub credentials
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
    echo "✅ GitHub wuu ku xidhan yahay"
    GH_USER=$(gh api user --jq '.login')
    echo "   Username: $GH_USER"
elif [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ Token-ka GitHub wuu jiraa"
else
    echo "⚠️ GitHub kuma xidhna!"
    echo "   Ku xidh: gh auth login"
    echo "   Ama: export GITHUB_TOKEN=ghp_..."
    echo ""
    read -p "Si kastaba ha ahaatee, sii wad? (y/N): " cont
    if [ "$cont" != "y" ]; then
        exit 1
    fi
fi

# 2. Git init (haddii aysan jirin)
if [ ! -d .git ]; then
    echo "📁 Sameynayaa git repo..."
    git init
    git branch -M main
fi

# 3. Add & commit
echo "📦 Committing files..."
git add -A
echo ""
echo "Waxa uu ku jiraa commit-kan:"
git status --short

echo ""
read -p "Magaca commit-ka: " commit_msg
commit_msg=${commit_msg:-"first: Somali AI Academy — initial setup"}

git commit -m "$commit_msg"

# 4. GitHub repo name
echo ""
read -p "Magaca repo-ga GitHub: " repo_name
repo_name=${repo_name:-"Somali-AI-Academy"}

# 5. Try gh or git push
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
    echo "🚀 gh repo create + push..."
    gh repo create "$repo_name" --public --source . --push
else
    echo "🔗 Ku xidh remote..."
    read -p "Remote URL (https://github.com/username/repo.git): " remote_url
    
    if git remote get-url origin &>/dev/null; then
        git remote set-url origin "$remote_url"
    else
        git remote add origin "$remote_url"
    fi
    
    echo "🚀 Push..."
    git push -u origin main
fi

echo ""
echo "=============================================="
echo "  ✅ Repo waa la gu shubay!"
echo "  https://github.com/${GH_USER:-'username'}/$repo_name"
echo "=============================================="
