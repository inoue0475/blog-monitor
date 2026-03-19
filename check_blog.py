import requests
import hashlib
import os

# 監視対象ブログURL
URL = "http://radioactivewaste.seesaa.net/"

# Discordテスト用Webhook
WEBHOOK = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"

# ハッシュ保存ファイル
STATE_FILE = "hash.txt"

# HTML全体のMD5ハッシュ取得
def get_hash():
    html = requests.get(URL, timeout=10).text
    return hashlib.md5(html.encode()).hexdigest()

# 前回ハッシュ読み込み
def load_old():
    if os.path.exists(STATE_FILE):
        return open(STATE_FILE).read().strip()
    return None

# ハッシュ保存
def save(h):
    open(STATE_FILE, "w").write(h)

# Discord通知
def notify():
    requests.post(
        WEBHOOK,
        json={"content": "🆕 ブログ更新検知！ http://radioactivewaste.seesaa.net/"}
    )

if __name__ == "__main__":
    new = get_hash()
    old = load_old()

    if old and new != old:
        notify()

    save(new)
