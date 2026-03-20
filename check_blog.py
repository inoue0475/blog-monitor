# check_blog.py
import requests
import hashlib
import os

# --- ここをあなたのブログURLに変更 ---
BLOG_URL = "https://radioactivewaste.seesaa.net/"

# --- Discord Webhook URL（直接書き）---
WEBHOOK = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"

# 保存するハッシュファイル名
CACHE_FILE = "cache_hash.txt"

def fetch_html(url):
    """ブログのHTMLを取得"""
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.text

def compute_hash(text):
    """SHA-256でハッシュ計算"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def read_last_hash(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()
    return None

def save_hash(file_path, hash_val):
    with open(file_path, "w") as f:
        f.write(hash_val)

def send_discord(msg):
    """WebhookでDiscordに通知"""
    data = {"content": msg}
    requests.post(WEBHOOK, json=data)

def main():
    html = fetch_html(BLOG_URL)
    current_hash = compute_hash(html)

    old_hash = read_last_hash(CACHE_FILE)
    if old_hash is None:
        # 初回実行 → 保存のみ
        print("初回実行: ハッシュ保存")
        save_hash(CACHE_FILE, current_hash)
        return

    if current_hash != old_hash:
        print("更新を検知！")
        # Discord送信
        send_discord(f"🆕 ブログ更新を検知しました！\n{BLOG_URL}")
        # ハッシュ更新
        save_hash(CACHE_FILE, current_hash)
    else:
        print("更新なし")

if __name__ == "__main__":
    main()
