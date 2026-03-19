import requests
import hashlib
import os
from bs4 import BeautifulSoup

# 監視するブログURL
URL = "http://radioactivewaste.seesaa.net/"

# Discord Webhook URL
WEBHOOK = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"

# 差分判定用ハッシュファイル
STATE_FILE = "hash.txt"

def get_blog_hash():
    """ブログ本文を取得してハッシュ化"""
    try:
        res = requests.get(URL, timeout=10)
        res.raise_for_status()
        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        # 本文の抽出（記事部分を指定）
        main_content = soup.select_one("#main-article")
        if main_content is None:
            print("記事本文が取得できませんでした")
            main_content = soup  # fallback: 全HTML

        content_text = main_content.get_text(strip=True)
        return hashlib.md5(content_text.encode()).hexdigest()
    except Exception as e:
        print("ブログ取得エラー:", e)
        return None

def load_old_hash():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return None

def save_hash(h):
    with open(STATE_FILE, "w") as f:
        f.write(h)

def notify_discord(message):
    try:
        res = requests.post(WEBHOOK, json={"content": message})
        print("Discord送信ステータス:", res.status_code)
        if res.status_code != 200:
            print(res.text)
    except Exception as e:
        print("Discord送信エラー:", e)

if __name__ == "__main__":
    new_hash = get_blog_hash()
    if new_hash is None:
        print("ハッシュ取得失敗、終了")
        exit(1)

    old_hash = load_old_hash()

    if old_hash is None:
        print("初回実行、ハッシュ保存のみ")
    elif old_hash != new_hash:
        print("ブログ更新検知！")
        notify_discord("🆕 ブログ更新検知！ {}".format(URL))
    else:
        print("更新なし")

    save_hash(new_hash)
