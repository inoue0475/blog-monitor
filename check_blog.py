import requests
import hashlib
import os
from bs4 import BeautifulSoup

URL = "http://radioactivewaste.seesaa.net/"
WEBHOOK = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"
STATE_FILE = "hash.txt"

def safe_requests_get(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("ブログ取得エラー:", e)
        return None

def get_blog_hash(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        main_content = soup.select_one("#main-article") or soup
        return hashlib.md5(main_content.get_text(strip=True).encode()).hexdigest()
    except Exception as e:
        print("ハッシュ生成エラー:", e)
        return None

def load_old_hash():
    try:
        if os.path.exists(STATE_FILE):
            return open(STATE_FILE).read().strip()
    except Exception as e:
        print("ハッシュ読み込みエラー:", e)
    return None

def save_hash(h):
    try:
        with open(STATE_FILE, "w") as f:
            f.write(h)
    except Exception as e:
        print("ハッシュ保存エラー:", e)

def notify_discord(message):
    try:
        res = requests.post(WEBHOOK, json={"content": message})
        print("Discord送信ステータス:", res.status_code)
    except Exception as e:
        print("Discord送信エラー:", e)

if __name__ == "__main__":
    try:
        html = safe_requests_get(URL)
        if html is None:
            print("HTML取得失敗、終了")
        else:
            new_hash = get_blog_hash(html)
            if new_hash is None:
                print("ハッシュ生成失敗、終了")
            else:
                old_hash = load_old_hash()
                if old_hash is None:
                    print("初回実行、ハッシュ保存のみ")
                elif old_hash != new_hash:
                    print("ブログ更新検知！")
                    notify_discord(f"🆕 ブログ更新検知！ {URL}")
                else:
                    print("更新なし")
                save_hash(new_hash)
    except Exception as e:
        print("未知のエラー:", e)

print("完了")
