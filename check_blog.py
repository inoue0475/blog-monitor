import requests

WEBHOOK = "ここにテスト用Webhook"

requests.post(
    WEBHOOK,
    json={"content": "🔥 ブログテスト通知"}
)
