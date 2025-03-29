# 🗂️ GitHub → Discord Project Board Bot

A simple Python bot that monitors a **GitHub Projects v2 Kanban Board** and sends notifications to a **Discord channel** when cards (project items) are created, moved, or deleted.

---

## ⭐ Features
- Monitors your GitHub Projects v2 board every X seconds
- Detects card movement between columns (status changes)
- Detects new card creation
- Detects card deletion
- Sends formatted notifications to a Discord channel via Webhook
- Uses SQLite to persist card state across restarts

---

## 🚀 Setup Guide

### 1. Create a Discord Webhook
- Go to your Discord server → Channel Settings → Integrations → Webhooks → **New Webhook**
- Copy the **Webhook URL**

---

### 2. Generate a GitHub Personal Access Token
- Go to: https://github.com/settings/tokens → **Generate a Fine-grained Token**
- Required scopes:
  - `read:project`
  - `read:org` *(if the project is under an organization)*
  - `repo` *(only if monitoring private repositories)*

---

### 3. Get your GitHub Project Node ID
GitHub Projects v2 requires a **GraphQL Node ID**, not a numeric ID.

**How to get it:**
1. Go to the [GitHub GraphQL Explorer](https://docs.github.com/en/graphql/overview/explorer)
2. Run this query to list your Projects:
```graphql
query {
  viewer {
    projectsV2(first: 10) {
      nodes {
        id
        title
      }
    }
  }
}
