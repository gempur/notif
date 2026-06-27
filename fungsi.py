import os
import smtplib
import requests
from dotenv import load_dotenv

from email.mime.text import MIMEText

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_FROM = os.getenv("SMTP_FROM")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAMCHAT_ID = os.getenv("TELEGRAMCHAT_ID")
TELEGRAM_THREAD_ID = int(os.getenv("TELEGRAM_THREAD_ID"))
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'

def KirimEmail(to, subject, body):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.sendmail(SMTP_FROM, [to], msg.as_string())
    
    return f"Email terkirim ke {to} dengan subjek '{subject}'"

def KirimTelegram(message):

    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": TELEGRAMCHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_notification": False,
        "reply_to_message_id": TELEGRAM_THREAD_ID
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return f"Pesan Telegram terkirim: {message}"
    else:
        return f"Gagal mengirim pesan Telegram: {response.text}"