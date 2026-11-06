import os

SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SENDER = os.environ.get("SENDER", "contact@office.example.com")
