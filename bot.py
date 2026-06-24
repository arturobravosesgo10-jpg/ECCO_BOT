                                                     from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "7647411316:AAGGQiygGvkpbKrcD28d01N9AAvAL7p0n7s"
API_URL = f"https://api.telegram.org/bot{TOKEN}"


# =========================
# FUNCIONES TELEGRAM
# =========================
def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })


def send_photo(chat_id):
    with open("imagen.jpg", "rb") as f:
        requests.post(f"{API_URL}/sendPhoto",
            data={"chat_id": chat_id, "caption": "⛽ Surtidor ECCO"},
            files={"photo": f}
        )


def send_audio(chat_id):
    with open("bienvenida_ecoo.mp3", "rb") as f:
        requests.post(f"{API_URL}/sendAudio",
            data={"chat_id": chat_id, "caption": "🎧 Mensaje ECCO"},
            files={"audio": f}
        )


def send_document(chat_id):
    with open("informacion_ecco.pdf", "rb") as f:
        requests.post(f"{API_URL}/sendDocument",
            data={"chat_id": chat_id, "caption": "📄 Información ECCO"},
            files={"document": f}
        )


# =========================
# WEBHOOK (TELEGRAM ENTRA AQUÍ)
# =========================
@app.route("/", methods=["POST"])
def webhook():

    data = request.get_json()

    if "message" not in data:
        return "ok"

    msg = data["message"]
    text = msg.get("text", "")
    chat_id = msg["chat"]["id"]

    # /start
    if text == "/start":
        send_message(chat_id,
            "⛽ Bienvenido a ECCO\n\n"
            "Comandos:\n"
            "/texto - precios\n"
            "/imagen - surtidor\n"
            "/audio - mensaje\n"
            "/documento - info"
        )

    # /texto
    elif text == "/texto":
        send_message(chat_id,
            "⛽ SURTIDOR ECCO\n\n"
            "Gasolina Especial: Bs. 3.74\n"
            "Gasolina Premium: Bs. 4.79\n"
            "Diésel: Bs. 3.72\n"
            "GNV: Bs. 1.66"
        )

    # /imagen
    elif text == "/imagen":
        send_photo(chat_id)

    # /audio
    elif text == "/audio":
        send_audio(chat_id)

    # /documento
    elif text == "/documento":
        send_document(chat_id)

    return "ok"


# =========================
# TEST EN NAVEGADOR
# =========================
@app.route("/", methods=["GET"])
def home():
    return "BOT ECCO ACTIVO"


# =========================
# RUN LOCAL
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
