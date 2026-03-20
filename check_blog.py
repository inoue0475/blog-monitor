import requests
import os

# HTML ファイルのパス
LOCAL_FILE = "last_html.html"
# チェック対象のページ（テスト用HTML）
URL = "https://github.com/inoue0475/blog-monitor/blob/main/test_page.html"
# Discord Webhook URL
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def fetch_html(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def load_last_html():
    if os.path.exists(LOCAL_FILE):
        with open(LOCAL_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_html(html):
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write(html)

def send_discord(message):
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": message})

def main():
    html = fetch_html(URL)
    last_html = load_last_html()
    if html != last_html:
        send_discord("差分を検知しました！")
        save_html(html)
    else:
        print("更新なし")

if __name__ == "__main__":
    main()
