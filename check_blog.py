import requests
import os

# ここにブログURLとWebhook URLを直接書く
BLOG_URL = "https://radioactivewaste.seesaa.net/"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"

# 前回HTMLを保存するファイル
LAST_HTML_FILE = "last_blog.html"

def fetch_html(url):
    res = requests.get(url)
    res.raise_for_status()  # 問題があればここで例外
    return res.text

def send_discord_notification(message):
    payload = {"content": message}
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        res.raise_for_status()
        print("通知送信成功")
    except Exception as e:
        print("通知送信失敗:", e)

def main():
    # 最新HTML取得
    html = fetch_html(BLOG_URL)

    # 前回HTMLが存在するかチェック
    if os.path.exists(LAST_HTML_FILE):
        with open(LAST_HTML_FILE, "r", encoding="utf-8") as f:
            last_html = f.read()
    else:
        last_html = ""

    # 差分判定
    if html != last_html:
        print("差分あり → 通知送信")
        send_discord_notification(f"ブログが更新されました: {BLOG_URL}")
        # 前回HTMLを更新
        with open(LAST_HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html)
    else:
        print("更新なし")

if __name__ == "__main__":
    main()
