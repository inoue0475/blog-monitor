import requests
import hashlib
import os

URL = "http://radioactivewaste.seesaa.net/"
WEBHOOK = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"

STATE_FILE = "hash.txt"

def get_hash():
    html = requests.get(URL).text
    return hashlib.md5(html.encode()).hexdigest()

def load_old():
    if os.path.exists(STATE_FILE):
        return open(STATE_FILE).read().strip()
    return None

def save(h):
    open(STATE_FILE, "w").write(h)

def notify():
    requests.post(
        WEBHOOK,
        json={"content": "🆕 ブログ更新検知"}
    )

if __name__ == "__main__":
    new = get_hash()
    old = load_old()

    if old and new != old:
        notify()

    save(new)
