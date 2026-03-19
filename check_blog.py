import requests
import hashlib
import os
import traceback

# 設定
URL = "http://radioactivewaste.seesaa.net/"
WEBHOOK = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"
STATE_FILE = "hash.txt"

def get_hash():
    """ブログHTMLのMD5ハッシュを取得"""
    res = requests.get(URL, timeout=10)
    return hashlib.md5(res.text.encode()).hexdigest()

def load_old_hash():
    """前回のハッシュを読み込む"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def save_hash(h):
    """ハッシュを保存"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(h)

def notify():
    """Discordに通知"""
    try:
        res = requests.post(WEBHOOK, json={"content": f"🆕 ブログ更新検知！ {URL}"})
        print("Discordレスポンス:", res.status_code)
    except Exception as e:
        print("Discord通知失敗！")
        traceback.print_exc()

def main():
    try:
        new_hash = get_hash()
        old_hash = load_old_hash()

        # 差分があれば通知
        if old_hash and new_hash != old_hash:
            notify()
        else:
            print("更新なしまたは初回実行")

        # ハッシュは必ず保存
        save_hash(new_hash)

    except Exception as e:
        print("ブログチェック中にエラー発生！")
        traceback.print_exc()

if __name__ == "__main__":
    main()
