import requests

WEBHOOK = "https://discord.com/api/webhooks/1484205183914348695/DWELElPDGIe8k2hkUmwUZ6TDo7OVSRe2iF85HRqhZ0MeN86gPqz8NEbZRUT8NQFfN5Ny"

requests.post(
    WEBHOOK,
    json={"content": "🔥 ブログテスト通知"}
)
