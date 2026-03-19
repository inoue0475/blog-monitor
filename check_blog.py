import requests
import hashlib
import os
from bs4 import BeautifulSoup

# ==== 設定 ====
BLOG_URL = "http://radioactivewaste.seesaa.net/"
WEBHOOK_URL = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"
STATE_FILE = "hash.txt"

# ==== 本文取得 & 前処理 ====
def get_blog_content():
    response = requests.get(BLOG_URL)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # ここはブログ本文のCSSセレクタに合わせて調整
    main_content = soup.select_one("#main-article")  # 例: #main-article
    if main_content is None:
        raise ValueError("ブログ本文が取得できませんでした。CSSセレクタを確認してください。")
    return main_content.get_text(strip=True)

# ==== ハッシュ管理 ====
def load_old_hash():
    if os.path.exists(STATE_FILE):
        return open(STATE_FILE, "r", encoding="utf-8").read().strip()
    return None

def save_hash(h):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(h)

# ==== 通知 ====
def send_discord_notification(message):
    payload = {"content": message}
    res = requests.post(WEBHOOK_URL, json=payload)
    res.raise_for_status()

# ==== メイン ====
def main():
    try:
        content = get_blog_content()
        new_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
        old_hash = load_old_hash()

        if old_hash != new_hash:
            # ハッシュが違う場合（初回も含む）、通知
            send_discord_notification(f"🆕 ブログ更新を検知しました: {BLOG_URL}")
            save_hash(new_hash)
        else:
            print("更新なし")
    except Exception as e:
        # エラー時も通知（任意）
        send_discord_notification(f"⚠️ ブログ通知スクリプトでエラー発生: {e}")
        raise

if __name__ == "__main__":
    main()
