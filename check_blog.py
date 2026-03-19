# check_blog.py
import requests
import hashlib
import os

# 取得するブログのURL
BLOG_URL = "http://radioactivewaste.seesaa.net/"  # ← 実際のURLに置き換えてください

# Discord Webhook URL
DISCORD_WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA")

# ハッシュ保存ファイル
HASH_FILE = "last_hash.txt"

def get_blog_html(url):
    """ブログページのHTMLを取得"""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def compute_hash(content):
    """文字列のSHA256ハッシュを返す"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def read_last_hash(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()
    return None

def save_hash(file_path, hash_value):
    with open(file_path, "w") as f:
        f.write(hash_value)

def send_discord_notification(webhook_url, message):
    """Discordに通知"""
    if not webhook_url:
        print("Discord Webhook URL が設定されていません")
        return
    payload = {"content": message}
    try:
        r = requests.post(webhook_url, json=payload)
        r.raise_for_status()
        print("通知送信成功")
    except Exception as e:
        print(f"通知送信失敗: {e}")

def main():
    try:
        html = get_blog_html(BLOG_URL)
    except Exception as e:
        print(f"ブログ取得失敗: {e}")
        return

    current_hash = compute_hash(html)
    last_hash = read_last_hash(HASH_FILE)

    if last_hash != current_hash:
        print("ブログが更新されました")
        send_discord_notification(DISCORD_WEBHOOK_URL, f"ブログが更新されました: {BLOG_URL}")
        save_hash(HASH_FILE, current_hash)
    else:
        print("更新なし")

if __name__ == "__main__":
    main()
