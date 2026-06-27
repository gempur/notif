import smtplib
import requests

from email.mime.text import MIMEText

SMTP_SERVER = "192.168.10.2"
SMTP_PORT = 25
SMTP_USER = "no-reply@rspkt.id"
SMTP_FROM = "no-reply@rspkt.id"


TELEGRAM_TOKEN = '8325761135:AAEz3SyJLTfJF7n7fwvICblaz7g_2xREhSs'
TELEGRAMCHAT_ID = '-1001253736566'
TELEGRAM_THREAD_ID = 311
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