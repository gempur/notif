import json
import threading
import datetime

import pika

from fungsi import KirimEmail, KirimTelegram

LOG_FILE = "events.log"
QUEUES = ["sambutan", "pesanan", "laporan", "broadcast"]

EMAIL_TO = "gempur@gmail.com"

def log_event(entry: dict) -> None:
    entry["waktu"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── handlers ──────────────────────────────────────────────────────────────────

def handle_sambutan(ch, method, _props, body):
    data = json.loads(body)
    log_event({
        "tipe": "sambutan",
        "label": "Sambutan Pengguna",
        "warna": "violet",
        "detail": f"Halo, {data['nama']}! Email selamat datang terkirim ke {data['email']}",
        "delivery": ["📧 Email", "📱 Telegram"],
        "id": data["id"],
    })

    global EMAIL_TO
    EMAIL_TO = data["email"]

    print(f"[sambutan] 📧  Mengirim email selamat datang ke {EMAIL_TO} ...")
    KirimEmail(EMAIL_TO, "Selamat Datang!", f"Halo, {data['nama']}! Selamat datang di layanan kami.")
    print(f"[sambutan] ✅  Email terkirim ke {EMAIL_TO}")

    print(f"[sambutan] 📱  Mengirim pesan selamat datang ke Telegram ...")
    KirimTelegram(f"Halo, {data['nama']}! Selamat datang di layanan kami.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def handle_pesanan(ch, method, _props, body):
    data = json.loads(body)
    email = EMAIL_TO if EMAIL_TO else data["email"]

    print(f"[pesanan] ✅  Konfirmasi terkirim")
    log_event({
        "tipe": "pesanan",
        "label": "Konfirmasi Pesanan",
        "warna": "amber",
        "detail": f"Pesanan {data['item']} × {data['qty']} telah dikonfirmasi.",
        "delivery": ["📱 Telegram"],
        "id": data["id"],
    })

    print(f"[pesanan] 📧  Mengirim konfirmasi pesanan {data['item']} x{data['qty']} via Email ...")
    KirimEmail(email, f"Konfirmasi Pesanan {data['item']}", f"Pesanan {data['item']} × {data['qty']} telah dikonfirmasi.")
    print(f"[pesanan] ✅  Email terkirim ke {email} dengan subjek 'Konfirmasi Pesanan {data['item']}'")

    print(f"[pesanan] 📱  Mengirim konfirmasi pesanan {data['item']} x{data['qty']} via Telegram ...")
    KirimTelegram(f"Pesanan {data['item']} × {data['qty']} telah dikonfirmasi.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def handle_laporan(ch, method, _props, body):
    data = json.loads(body)
    email = EMAIL_TO 

    log_event({
        "tipe": "laporan",
        "label": "Laporan Statistik",
        "warna": "sky",
        "detail": f"Laporan periode {data['periode']} (format {data['format']}) selesai dibuat dan dikirim.",
        "delivery": ["📧 Email"],
        "id": data["id"],
    })
    print(f"[laporan] 📊  Membuat laporan periode {data['periode']} format {data['format']} ...")
    KirimEmail(email, f"Laporan Periode {data['periode']}", f"Laporan Anda dalam format {data['format']} telah selesai dibuat.")
    print(f"[laporan] ✅  Laporan selesai dan dikirim ke {email} dengan subjek 'Laporan Periode {data['periode']}'")

    print(f"[laporan] 📱  Mengirim notifikasi laporan selesai ke Telegram ...")
    KirimTelegram(f"Laporan periode {data['periode']} (format {data['format']}) telah selesai dibuat.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def handle_broadcast(ch, method, _props, body):
    data = json.loads(body)
    email = EMAIL_TO 

    log_event({
        "tipe": "broadcast",
        "label": "Broadcast Pengumuman",
        "warna": "rose",
        "detail": data["pesan"],
        "delivery": ["📧 Email", "📱 Telegram"],
        "id": data["id"],
    })
    print(f"[broadcast] 📢  Menyebarkan pengumuman ke semua saluran ...")
    KirimEmail(email, "Pengumuman Penting", data["pesan"])
    print(f"[broadcast] ✅  Terkirim ke {email}  via Email + Telegram")

    print(f"[broadcast] 📱  Mengirim pengumuman ke Telegram ...")
    KirimTelegram(data["pesan"])
    ch.basic_ack(delivery_tag=method.delivery_tag)


HANDLERS = {
    "sambutan": handle_sambutan,
    "pesanan": handle_pesanan,
    "laporan": handle_laporan,
    "broadcast": handle_broadcast,
}

# ── consumer threads ───────────────────────────────────────────────────────────

def consume(queue: str) -> None:
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = conn.channel()
    ch.queue_declare(queue=queue, durable=True)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=queue, on_message_callback=HANDLERS[queue])
    print(f"[worker] Mendengarkan antrian: {queue}")
    ch.start_consuming()


if __name__ == "__main__":
    print("[worker] Memulai semua consumer …")
    threads = [threading.Thread(target=consume, args=(q,), daemon=True) for q in QUEUES]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
