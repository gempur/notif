import json
import uuid

import pika
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

LOG_FILE = "events.log"


def publish(queue: str, payload: dict) -> None:
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = conn.channel()
    ch.queue_declare(queue=queue, durable=True)
    ch.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    conn.close()


@app.route("/")
def home() -> str:
    return render_template("home.html")


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/demo")
def demo() -> str:
    return render_template("demo.html")


@app.route("/demo/sambutan", methods=["POST"])
def demo_sambutan():
    publish("sambutan", {
        "id": str(uuid.uuid4()),
        "nama": request.form["nama"],
        "email": request.form["email"],
    })
    return jsonify(ok=True)


@app.route("/demo/pesanan", methods=["POST"])
def demo_pesanan():
    publish("pesanan", {
        "id": str(uuid.uuid4()),
        "item": request.form["item"],
        "qty": int(request.form["qty"]),
    })
    return jsonify(ok=True)


@app.route("/demo/laporan", methods=["POST"])
def demo_laporan():
    publish("laporan", {
        "id": str(uuid.uuid4()),
        "periode": request.form["periode"],
        "format": request.form.get("format", "PDF"),
    })
    return jsonify(ok=True)


@app.route("/demo/broadcast", methods=["POST"])
def demo_broadcast():
    publish("broadcast", {
        "id": str(uuid.uuid4()),
        "pesan": request.form["pesan"],
    })
    return jsonify(ok=True)


@app.route("/demo/log")
def demo_log():
    try:
        with open(LOG_FILE) as f:
            events = [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        events = []
    return jsonify(list(reversed(events[-50:])))


if __name__ == "__main__":
    app.run(debug=True, port=8013)
