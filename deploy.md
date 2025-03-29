# 🚀 Deployment Guide - GitHub → Discord Kanban Bot (Railway)

This guide will help you deploy your bot to **Railway.app** for free.

---

## 🌐 Prerequisites
- Free account on [Railway](https://railway.app/)
- GitHub account
- Your project folder in a GitHub repo (with `.gitignore` excluding `config.json` & `card_state.db`)

---

## 🗂️ Files Required in Repo
Make sure your repo includes:
```
📂 GitCordHookBot
├── bot.py
├── requirements.txt
├── .gitignore
├── README.md
└── deploy.md  # (this file)
```

Do **NOT** include:
- `config.json`
- `card_state.db`

---

## ⚙️ Railway Deployment Steps

### 1. **Create Railway Project**
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **New Project → Deploy from GitHub Repo**
3. Select your repo (where your bot is stored)

---

### 2. **Add Environment Variables**
Once the project is created:
1. Go to the **Variables** tab in Railway
2. Add these four variables:

| Key             | Value                                  |
|----------------|----------------------------------------|
| `GITHUB_TOKEN` | Your GitHub Personal Access Token      |
| `DISCORD_WEBHOOK` | Your Discord Webhook URL           |
| `PROJECT_ID`   | Your GitHub Project Node ID (starts with `PVT_`) |
| `POLL_INTERVAL`| `300` (or any interval in seconds)     |

---

### 3. **Set Start Command**
In Railway → Project → **Settings → Service → Start Command**:
```
python bot.py
```

---

### 4. **Deploy**
1. Railway will auto-install `requirements.txt`
2. Click **Deploy**
3. View logs to ensure the bot starts:
```
Bot started. Monitoring project board...
```

---

## 🟢 **That's it! Your bot is now live 24/7.**

---

## 🔥 Optional (Advanced)
- You can set logs retention to 30 days in Railway settings.
- You can limit usage under **Usage → Free Tier → Stop Service after X hours**

---

## 🧩 Next Steps
- Edit `.gitignore` to exclude any local `.env` or `config.json` secrets.
- Test by moving a card or creating/deleting an item in your GitHub Project.
- Watch your Discord channel — bot should notify movements.
