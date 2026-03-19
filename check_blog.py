import requests

WEBHOOK = "https://discord.com/api/webhooks/1484212069439111458/K3bVjxTyTq18Bo1IH3MpzQ9WhuFEqYnSX-Toka2t3BMhxNnZlmFxHli-r0YACj038UtA"

requests.post(
    WEBHOOK,
    json={"content": "🔥 テスト通知（blog側）"}
)
