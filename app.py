from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

GRAPH_URL = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge

    return "Verification failed", 403


def send_message(to, text):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": text
        }
    }

    requests.post(GRAPH_URL, headers=headers, json=data)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]

        phone = message["from"]
        text = message["text"]["body"].lower()

        if "سلام" in text or "hello" in text or "hi" in text:

            reply = """
🌿 سلام، به درخشان گروپ خوش آمدید.

لطفاً یکی از گزینه‌ها را انتخاب کنید:

1️⃣ محصولات کود زراعتی
2️⃣ قیمت محصولات
3️⃣ دریافت کاتالوگ
4️⃣ نمایندگی فروش
5️⃣ تماس با کارشناسان
"""

        elif text == "1":
            reply = """
🌱 محصولات درخشان گروپ:

• DAP 18-46-0
• UREA 46%
• NPK
• Humic Acid

برای قیمت با ما تماس بگیرید.
"""

        elif text == "2":
            reply = """
💰 برای دریافت قیمت، لطفاً نام محصول و مقدار مورد نیاز خود را ارسال کنید.
"""

        elif text == "3":
            reply = """
📄 کاتالوگ محصولات درخشان گروپ برای شما آماده می‌شود.
"""

        elif text == "4":
            reply = """
🤝 برای درخواست نمایندگی لطفاً:
نام شرکت، شهر و شماره تماس خود را ارسال کنید.
"""

        elif text == "5":
            reply = """
☎️ کارشناسان فروش در خدمت شما هستند.
لطفاً پیام خود را ارسال کنید.
"""

        else:
            reply = "لطفاً یکی از گزینه‌های 1 تا 5 را انتخاب کنید."

        send_message(phone, reply)

    except Exception as e:
        print(e)

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
