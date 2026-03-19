import requests

WEBHOOK = "https://discord.com/api/webhooks/1484210034840830043/o07phlzYEK3LoiRQkg_dp3eJTvRJLZnWJdF05TVeyNImpmYgBFFXdBk_MIQE8U3PBlro"

requests.post(
    WEBHOOK,
    json={"content": "🔥 テスト通知（blog側）"}
)
