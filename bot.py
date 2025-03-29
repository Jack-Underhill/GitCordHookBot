import time
import json
import requests
import sqlite3
import os

# ------------ Load Config ------------ 
# Try to load from environment variables first
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
PROJECT_ID = os.getenv('PROJECT_ID')
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', 100))

# If running locally, fallback to config.json
if not GITHUB_TOKEN or not DISCORD_WEBHOOK or not PROJECT_ID:
    with open('config.json') as f:
        config = json.load(f)
    GITHUB_TOKEN = config['github_token']
    DISCORD_WEBHOOK = config['discord_webhook']
    PROJECT_ID = config['project_id']
    POLL_INTERVAL = config.get('poll_interval', 60)

headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

# ------------ Database Setup ------------
conn = sqlite3.connect('card_state.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS card_state (
        card_id TEXT PRIMARY KEY,
        column TEXT,
        title TEXT
    )
''')
conn.commit()

# ------------ Bot Functions ------------
def fetch_project_items():
    url = "https://api.github.com/graphql"

    query = """
    query ($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          items(first: 100) {
            nodes {
              id
              content {
                ... on Issue {
                  title
                }
                ... on PullRequest {
                  title
                }
              }
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                  }
                  ... on ProjectV2ItemFieldTextValue {
                    text
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    variables = {
        "projectId": PROJECT_ID
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json={"query": query, "variables": variables},
            timeout=10
        )

        if response.status_code != 200:
            print(f"GraphQL API error: {response.status_code} - {response.text}")
            return {}

        data = response.json()
        if "errors" in data:
            print("GraphQL errors:", data["errors"])
            return {}

        items = {}

        nodes = data['data']['node']['items']['nodes']
        for node in nodes:
            item_id = node['id']

            # Determine title
            if node['content']:
                title = node['content']['title']
            else:
                # Try to pull from fieldValues (draft item)
                title = "Untitled"
                for field in node['fieldValues']['nodes']:
                    if 'text' in field and field['text']:
                        title = field['text']
                        break

            # Determine column/status
            status = "Unknown"
            for field in node['fieldValues']['nodes']:
                if 'name' in field and field['name']:
                    status = field['name']

            items[item_id] = {
                'note': title,
                'column': status
            }

        return items

    except requests.exceptions.RequestException as e:
        print(f"Error fetching project items: {e}")
        return {}

def send_discord_message(content):
    data = {"content": content}
    try:
        response = requests.post(DISCORD_WEBHOOK, json=data, timeout=10)
        if response.status_code != 204:
            print(f"Failed to send Discord message: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Discord message: {e}")


def get_last_column(card_id):
    cursor.execute('SELECT column FROM card_state WHERE card_id = ?', (card_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def update_card_state(card_id, column, title):
    cursor.execute('REPLACE INTO card_state (card_id, column, title) VALUES (?, ?, ?)', (card_id, column, title))
    conn.commit()

def handle_new_cards(current_state):
    new_cards = []
    for card_id, card in current_state.items():
        last_column = get_last_column(card_id)
        if last_column is None:
            # New card detected
            msg = f"🆕 New card created: '**{card['note']}**' in **{card['column']}**"
            print(msg)
            send_discord_message(msg)
            update_card_state(card_id, card['column'], card['note'])
            new_cards.append(card_id)
    return new_cards

def handle_deleted_cards(current_state):
    cursor.execute('SELECT card_id, title FROM card_state')
    stored = {row[0]: row[1] for row in cursor.fetchall()}
    current_ids = set(current_state.keys())

    deleted_ids = set(stored.keys()) - current_ids
    for card_id in deleted_ids:
        title = stored[card_id]
        msg = f"❌ Card deleted: '**{title}**'"
        print(msg)
        send_discord_message(msg)
        cursor.execute('DELETE FROM card_state WHERE card_id = ?', (card_id,))
    conn.commit()


def main():
    print("Bot started. Monitoring project board...")

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            current_state = fetch_project_items()

            handle_new_cards(current_state)
            handle_deleted_cards(current_state)

            # Detect movement
            for card_id, card in current_state.items():
                last_column = get_last_column(card_id)
                if last_column and card['column'] != last_column:
                    msg = f"📋 Card '**{card['note']}**' moved to **{card['column']}**"
                    print(msg)
                    send_discord_message(msg)
                    update_card_state(card_id, card['column'], card['note'])

    except KeyboardInterrupt:
        print("\nBot stopped by user (Ctrl+C).")

    finally:
        conn.close()
        print("Database connection closed.")



if __name__ == "__main__":
    main()
