from flask import Flask, request
import requests
import os
from products import products

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

    requests.post(
        GRAPH_URL,
        headers=headers,
        json=data
    )



@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    try:

        message = data["entry"][0]["changes"][0]["value"]["messages"][0]

        phone = message["from"]
        text = message["text"]["body"].lower().strip()


        # خوش آمدگویی دری و انگلیسی

        if (
            "سلام" in text
            or "hello" in text
            or "hi" in text
        ):

            reply = """
🌿 سلام، به درخشان گروپ خوش آمدید.

لطفاً یکی را انتخاب کنید:

1️⃣ محصولات درخشان گروپ
2️⃣ قیمت محصولات
3️⃣ دریافت کاتالوگ
4️⃣ درخواست نمایندگی
5️⃣ تماس با کارشناسان زراعتی
6️⃣ در مورد درخشان گروپ
7️⃣ راه‌های بیشتر تماس
"""


        # منوی محصولات

        elif text == "1":

            reply = """
📦 محصولات درخشان گروپ

لطفاً دسته محصول را انتخاب نمایید:

1️⃣ کود فوق العاده هیومیک اسید
2️⃣ کود فوق العاده NPK

0️⃣ بازگشت
"""


        # هیومیک اسید

        elif text == "1":

            reply = products["humic_acid"]["dari"]



        # NPK

        elif text == "2":

            reply = products["npk"]["dari"]



        elif text == "3":

            reply = """
📄 کاتالوگ محصولات درخشان گروپ برای شما آماده می‌شود.
"""



        elif text == "4":

            reply = """
🤝 درخواست نمایندگی درخشان گروپ

لطفاً معلومات زیر را ارسال کنید:

نام:
ولایت:
آدرس:
شماره تماس:
"""



        elif text == "5":

            reply = """
🌱 کارشناسان زراعتی درخشان گروپ

لطفاً مشکل یا سوال زراعتی خود را ارسال کنید.
"""



        elif text == "6":

            reply = """
🌿 درخشان گروپ؛ نماد کیفیت، نوآوری و توسعه پایدار.

درخشان گروپ در بخش زراعت، صنعت و تولید فعالیت داشته و محصولات با کیفیت را برای بازارهای داخلی و بین‌المللی عرضه می‌نماید.

کیفیت، اعتماد و نوآوری؛ ارزش‌های اصلی ما هستند. 🌍
"""



        elif text == "7":

            reply = """
☎️ راه‌های تماس درخشان گروپ

لطفاً سوال یا درخواست خود را ارسال کنید، کارشناسان ما پاسخ خواهند داد.
"""



        else:

            reply = """
لطفاً یکی از گزینه‌های منو را انتخاب کنید.
"""



        send_message(phone, reply)


    except Exception as e:

        print(e)


    return "OK", 200



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
