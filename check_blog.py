# check_blog.py
import requests
import hashlib
import os

# ---- 設定部分 ----
BLOG_URL = "https://radioactivewaste.seesaa.net/"  # 監視したいブログのURL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"  # Webhookに置き換え

# 前回保存するハッシュファイル
HASH_FILE = "last_hash.txt"


def fetch_html(url):
    """ブログページのHTMLを取得"""
    # Discord側で弾かれにくいようブラウザ風User-Agentを付与
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(url, headers=headers, timeout=15)
    res.raise_for_status()
    return res.text


def compute_hash(text):
    """文字列全体からSHA256ハッシュを生成"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_last_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def save_new_hash(hash_value):
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(hash_value)


def send_discord_notification(message):
    """DiscordにWebhookで通知"""
    payload = {"content": message}
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        res.raise_for_status()
        print("Discord通知成功:", res.status_code)
    except Exception as e:
        print("Discord通知失敗:", e)


def main():
    try:
        html = fetch_html(BLOG_URL)
    except Exception as e:
        print("ブログHTML取得失敗:", e)
        return

    new_hash = compute_hash(html)
    old_hash = load_last_hash()

    if old_hash is None:
        # 初回実行 → ハッシュ保存のみ
        print("初回実行: ハッシュを保存します")
        save_new_hash(new_hash)
        return

    if new_hash != old_hash:
        print("差分検出！Discordへ通知します")
        send_discord_notification(f"🆕 ブログ更新検知！ {BLOG_URL}")
        save_new_hash(new_hash)
    else:
        print("更新なし")

if __name__ == "__main__":
    main()
