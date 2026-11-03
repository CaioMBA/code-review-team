import os

SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
REMETENTE = os.environ.get("REMETENTE", "contato@escritorio.com.br")
