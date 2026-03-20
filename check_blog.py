import requests
import time
import hashlib
import os

BLOG_URL = "https://radioactivewaste.seesaa.net/"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"  # ここにWebhookを設定

HASH_FILE = "last_hash.txt"

# HTML取得（429対応）
def fetch_html(url, retries=5, delay=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    for i in range(retries):
        res = requests.get(url, headers=headers)
        if res.status_code == 429:
            print(f"[{i+1}/{retries}] 429 Too Many Requests, retrying in {delay} sec...")
            time.sleep(delay)
            continue
        res.raise_for_status()
        return res.text
    raise Exception("Failed after retries due to 429")

# 差分チェック用ハッシュ
def get_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

# Discord通知
def send_discord_notification(message):
    payload = {"content": message}
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        res.raise_for_status()
        print("Discord通知送信成功")
    except Exception as e:
        print(f"Discord通知失敗: {e}")

# 差分判定
def has_updated(new_hash):
    if not os.path.exists(HASH_FILE):
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
        return False
    with open(HASH_FILE, "r") as f:
        last_hash = f.read().strip()
    if new_hash != last_hash:
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
        return True
    return False

def main():
    try:
        html = fetch_html(BLOG_URL)
    except Exception as e:
        print(f"ブログ取得失敗: {e}")
        return
    current_hash = get_hash(html)
    if has_updated(current_hash):
        print("ブログ更新検知！通知送信中…")
        send_discord_notification(f"ブログが更新されました: {BLOG_URL}")
    else:
        print("更新なしまたは初回実行")

if __name__ == "__main__":
    main()
