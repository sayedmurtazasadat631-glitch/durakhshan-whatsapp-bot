from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

GRAPH_URL = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"


def send_message(to, data):

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    requests.post(
        GRAPH_URL,
        headers=headers,
        json=data
    )


# تایید واتساپ
@app.route("/webhook", methods=["GET"])
def verify_webhook():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge

    return "Verification failed", 403



# پیام دکمه‌ای اصلی
def main_menu(to):

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "🌿 به درخشان گروپ خوش آمدید\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "products",
                            "title": "📦 محصولات"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "sales",
                            "title": "🏪 فروشات"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "contact",
                            "title": "☎️ تماس"
                        }
                    }
                ]
            }
        }
    }

    send_message(to, data)



@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    try:

        message = data["entry"][0]["changes"][0]["value"]["messages"][0]

        phone = message["from"]


        # اگر پیام متنی باشد
        if "text" in message:

            text = message["text"]["body"].lower()

            if "سلام" in text or "hi" in text or "hello" in text:
                main_menu(phone)


        # اگر دکمه انتخاب شود
        elif "interactive" in message:

            interactive = message["interactive"]

            if "button_reply" in interactive:

                button_id = interactive["button_reply"]["id"]

                handle_button(phone, button_id)


    except Exception as e:
        print(e)


    return "OK", 200



def handle_button(phone, button_id):


    # منوی محصولات
    if button_id == "products":

        data = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "📦 محصولات درخشان گروپ\n\nلطفاً محصول مورد نظر را انتخاب کنید:"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "humic",
                                "title": "🌿 هیومیک اسید"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "npk",
                                "title": "🌱 NPK"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "cotton",
                                "title": "🧵 پنبه"
                            }
                        }
                    ]
                }
            }
        }

        send_message(phone, data)



    # هیومیک اسید

    elif button_id == "humic":

        text = """
🌿 کود فوق العاده هیومیک اسید

هیومیک اسید یک کود ارگانیک مؤثر برای بهبود ساختمان خاک، تقویت ریشه و افزایش جذب مواد غذایی می‌باشد.

✅ فواید:
• تقویت ریشه
• افزایش جذب مواد غذایی
• بهبود حاصل‌خیزی خاک
• افزایش کیفیت محصولات

📦 بسته‌بندی:
5 لیتر
10 لیتر
20 لیتر

💰 قیمت:
5 لیتر: 500 افغانی
10 لیتر: 900 افغانی
20 لیتر: 1800 افغانی
"""

        send_text(phone, text)



    # NPK

    elif button_id == "npk":

        text = """
🌱 کود فوق العاده NPK

کود کامل برای تأمین عناصر غذایی مورد نیاز گیاه.

✅ فواید:
• رشد بهتر گیاه
• تقویت ریشه
• افزایش کیفیت محصول

📦 بسته‌بندی:
1 لیتر

💰 قیمت:
200 افغانی
"""

        send_text(phone, text)



    # پنبه

    elif button_id == "cotton":

        text = """
🧵 پنبه پروسس شده درخشان گروپ

پنبه با استفاده از ماشین‌آلات مدرن پروسس شده و برای صنایع نساجی آماده می‌گردد.

✅ کیفیت عالی
✅ الیاف یک‌دست
✅ مناسب صادرات
"""

        send_text(phone, text)



    # فروشات

    elif button_id == "sales":

        text = """
🏪 محل فروشات درخشان گروپ

لطفاً ولایت خود را انتخاب کنید:

📍 بلخ
📍 فاریاب
📍 بغلان
📍 کندز
📍 هلمند
📍 ننگرهار
"""

        send_text(phone, text)



    # تماس

    elif button_id == "contact":

        text = """
☎️ تماس با درخشان گروپ

کارشناسان ما آماده پاسخگویی هستند.

واتساپ:
+93786470833

درخواست قیمت و نمایندگی را ارسال کنید.
"""

        send_text(phone, text)



def send_text(to, text):

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": text
        }
    }

    send_message(to, data)



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
