# GitHub → Discord Project Board Bot

A simple Python bot that monitors a GitHub Project Board and notifies a Discord channel when a card is moved to a different column.

---

## ⭐ Features
- Polls GitHub Project Board every X seconds
- Detects card movement between columns
- Sends message to Discord via Webhook
- Uses SQLite to persist card state across restarts

---

## 🚀 Setup Guide

### 1. Create a Discord Webhook
- Go to your Discord server → Channel Settings → Integrations → Webhooks → **New Webhook**
- Name it and copy the **Webhook URL**

### 2. Generate a GitHub Personal Access Token
- Go to: https://github.com/settings/tokens → **Generate a classic token**
- Recommended scopes:
  - `repo` (if private repo)
  - `read:org`
  - `read:project`

### 3. Get your Project Board ID
- Use GitHub's API or inspect your project board URL
- Example URL: `https://github.com/orgs/YOURORG/projects/123` → Project ID is **123**

### 4. Configure `config.json`
Create a `config.json` file in the same directory as `bot.py`:
```json
{
  "github_token": "YOUR_GITHUB_TOKEN",
  "discord_webhook": "YOUR_DISCORD_WEBHOOK_URL",
  "project_id": "YOUR_PROJECT_ID",
  "poll_interval": 60
}
```

### 5. Install Dependencies
```
pip install requests
```

### 6. Run the Bot
```
python bot.py
```
The bot will now monitor your board and post a Discord message when a card changes columns.

---

## 🗂️ File Structure
```
📂 github_discord_bot_template
├── bot.py           # Main bot script
├── config.json      # Your configuration
├── card_state.db    # SQLite database (auto-created)
└── README.md        # This file
```

---

## ⚙️ Optional Improvements
- Add command-line options for project selection
- Add Issue creation/closure automation
- Track multiple boards simultaneously
- Add advanced filtering rules

---

## 🧩 License
This is an open template you can modify for personal and team use.
