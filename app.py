from flask import Flask, request
import requests
import os

app = Flask(__name__)


VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")


GRAPH_URL = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"



# ارسال پیام به واتساپ

def send_message(data):

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        GRAPH_URL,
        headers=headers,
        json=data
    )

    print(response.text)


# ارسال پیام متنی

def send_text(phone, text):

    data = {

        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",

        "text": {
            "body": text
        }

    }

    send_message(data)




# تایید Webhook

@app.route("/webhook", methods=["GET"])

def verify_webhook():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")


    if mode == "subscribe" and token == VERIFY_TOKEN:

        return challenge


    return "Verification failed",403





# منوی اصلی

def main_menu(phone):


    data = {


        "messaging_product":"whatsapp",

        "to":phone,

        "type":"interactive",


        "interactive":{


            "type":"list",


            "body":{

                "text":
"""
🌿 به درخشان گروپ خوش آمدید

لطفاً بخش مورد نظر خود را انتخاب نمایید:
"""

            },


            "action":{


                "button":"مشاهده منو",


                "sections":[


                    {

                    "title":"خدمات درخشان گروپ",

                    "rows":[


                        {
                        "id":"products",
                        "title":"📦 محصولات",
                        "description":"کود، پنبه و محصولات زراعتی"
                        },


                        {
                        "id":"sales",
                        "title":"🏪 محل فروشات",
                        "description":"نمایندگی‌ها و مراکز فروش"
                        },


                        {
                        "id":"experts",
                        "title":"🌱 کارشناسان زراعتی",
                        "description":"مشاوره تخصصی"
                        },


                        {
                        "id":"contact",
                        "title":"☎️ تماس با ما",
                        "description":"ارتباط با درخشان گروپ"
                        },


                    ]

                    }


                ]

            }

        }

    }


    send_message(data)





# دریافت پیام‌ها


@app.route("/webhook", methods=["POST"])

def webhook():

    data=request.get_json()


    try:


        message=data["entry"][0]["changes"][0]["value"]["messages"][0]


        phone=message["from"]



        # پیام متنی

        if "text" in message:


            text=message["text"]["body"].lower()



            if (
                "سلام" in text
                or "hello" in text
                or "hi" in text
            ):

                main_menu(phone)



        # انتخاب از منو


        elif "interactive" in message:


            interactive=message["interactive"]



            if "list_reply" in interactive:


                button_id=interactive["list_reply"]["id"]


                handle_button(
                    phone,
                    button_id
                )

    except Exception as e:

        print(e)


    return "OK", 200

def handle_button(phone, button_id):


    # محصولات

    if button_id == "products":


        data = {

            "messaging_product":"whatsapp",
            "to":phone,
            "type":"interactive",

            "interactive":{

                "type":"list",

                "body":{

                    "text":
"""
📦 محصولات درخشان گروپ

محصول مورد نظر را انتخاب کنید:
"""

                },


                "action":{

                    "button":"محصولات",

                    "sections":[

                        {

                        "title":"محصولات زراعتی",

                        "rows":[


                            {
                            "id":"humic",
                            "title":"🌿 هیومیک اسید",
                            "description":"کود ارگانیک تقویت خاک و ریشه"
                            },


                            {
                            "id":"npk",
                            "title":"🌱 کود NPK",
                            "description":"تغذیه کامل گیاه"
                            },


                            {
                            "id":"cotton",
                            "title":"🧵 پنبه پروسس شده",
                            "description":"پنبه با کیفیت صادراتی"
                            },


                            {
                            "id":"lab",
                            "title":"🔬 خدمات لابراتوار",
                            "description":"آزمایش خاک و محصولات"
                            },


                        ]

                        }

                    ]

                }

            }

        }


        send_message(data)



    # هیومیک اسید

    elif button_id=="humic":

        data = {

            "messaging_product":"whatsapp",
            "to":phone,
            "type":"interactive",

            "interactive":{

                "type":"list",

                "body":{
                    "text":
"""
🌿 هیومیک اسید فوق العاده

لطفاً سایز محصول را انتخاب کنید:
"""
                },

                "action":{

                    "button":"انتخاب سایز",

                    "sections":[

                        {

                        "title":"بسته‌ بندی‌ها",

                        "rows":[

                            {
                            "id":"humic5",
                            "title":"🌿 5 لیتری",
                            "description":"کود فوق العاده"
                            },

                            {
                            "id":"humic10",
                            "title":"🌿 10 لیتری",
                            "description":"کود فوق العاده"
                            },

                            {
                            "id":"humic20",
                            "title":"🌿 20 لیتری",
                            "description":"کود فوق العاده"
                            }

                        ]

                        }

                    ]

                }

            }

        }

        send_message(data)


    elif button_id=="humic5":

        send_product(
            phone,
            "humic5.png",
            "🌿 هیومیک اسید ۵ لیتری",
            "500 افغانی"
        )


    elif button_id=="humic10":

        send_product(
            phone,
            "humic10.png",
            "🌿 هیومیک اسید ۱۰ لیتری",
            "900 افغانی"
        )


    elif button_id=="humic20":

        send_product(
            phone,
            "humic20.png",
            "🌿 هیومیک اسید ۲۰ لیتری",
            "1800 افغانی"
        )
    
    # NPK


    elif button_id=="npk":


        send_text(phone,

"""
🌱 کود فوق العاده NPK


کود کامل برای تأمین عناصر ضروری گیاه.


✅ فواید:

• رشد بهتر گیاه
• تقویت ریشه
• افزایش حاصل‌دهی
• بهبود کیفیت محصول


📦 بسته‌بندی:

۱ لیتر


💰 قیمت:

۲۰۰ افغانی
"""
)



    # پنبه


    elif button_id=="cotton":


        send_text(phone,

"""
🧵 پنبه پروسس شده درخشان گروپ


پنبه درخشان گروپ با ماشین‌آلات مدرن و تکنالوژی پیشرفته پروسس شده و برای صنایع نساجی آماده می‌گردد.


✅ کیفیت عالی

✅ الیاف یک‌دست

✅ مناسب برای صنایع نساجی و صادرات
"""
)



    # لابراتوار

    elif button_id=="lab":

        send_text(phone,

"""
🔬 خدمات لابراتوار درخشان گروپ


خدمات تخصصی لابراتوار:


✅ آزمایش خاک

✅ آزمایش کودهای زراعتی

✅ آزمایش تخم‌ها

✅ بررسی کیفیت محصولات زراعتی

✅ ارائه نتایج دقیق و علمی


🌱 هدف ما کمک به دهقانان برای انتخاب درست کود، تخم و روش مناسب کشت می‌باشد.
"""
        )



    # فروشات

    elif button_id=="sales":

        send_text(phone,

"""
🏭 محل فروشات درخشان گروپ


1️⃣ داکتر امرالله صافی

📍 آدرس:
ولایت جلال‌آباد، افغانستان

📞 تماس:
+93 70 222 7922

💬 واتساپ:
https://wa.me/937022227922


━━━━━━━━━━━━━━


2️⃣ حاجی محب الله و امین الله راز

📍 آدرس:
ولایت فاریاب، افغانستان

📞 تماس:
+93 78 627 5466

💬 واتساپ:
https://wa.me/93786275466


━━━━━━━━━━━━━━


3️⃣ قاری شکرالله خان

📍 آدرس:
ولایت کندز، افغانستان

📞 تماس:
+93 79 982 9245

💬 واتساپ:
https://wa.me/93799829245


━━━━━━━━━━━━━━


4️⃣ نقیب الله وزیری

📍 آدرس:
ولسوالی چهاربولک، افغانستان

📞 تماس:
+93 77 801 6161

💬 واتساپ:
https://wa.me/93778016161


━━━━━━━━━━━━━━


5️⃣ آرین شراف

📍 آدرس:
شهر مزارشریف، ولایت بلخ، افغانستان

📞 تماس:
+93 78 655 1516

💬 واتساپ:
https://wa.me/93786551516


━━━━━━━━━━━━━━


6️⃣ عبدالله هلمندی

📍 آدرس:
ولایت هلمند، افغانستان

📞 تماس:
+93 70 551 3709

💬 واتساپ:
https://wa.me/93705513709


━━━━━━━━━━━━━━


7️⃣ ضیالحق بغلان

📍 آدرس:
ولایت بغلان، افغانستان

📞 تماس:
+93 70 022 8685

💬 واتساپ:
https://wa.me/93700228685


━━━━━━━━━━━━━━


8️⃣ پیر محمد

📍 آدرس:
ولسوالی دولت‌آباد، ولایت فاریاب، افغانستان

📞 تماس:
+93 78 803 8543

💬 واتساپ:
https://wa.me/93788038543


🌿 درخشان گروپ؛ نزدیک‌ترین مرکز خدمت‌رسانی به شما
"""
        )



    # کارشناسان

    elif button_id=="experts":

        send_text(phone,

"""
🌱 کارشناسان زراعتی درخشان گروپ

1️⃣ انجنیر محمد یاسین عزیزی

📍 ولایت بلخ
🧑‍🔬 تخصص:
لابراتوار و خاک‌شناسی

📞 تماس:
+93 781449095
💬 واتساپ:
https://wa.me/93781449095


━━━━━━━━━━━━━━

2️⃣ انجنیر فیض محمد خان
📍 ولایت بلخ
🧑‍🔬 تخصص:
مشاوره کشت و زراعت

📞 تماس:
+93 78 873 0949
💬 واتساپ:
https://wa.me/93788730949

━━━━━━━━━━━━━━

3️⃣ انجنیر عبدالغفور بیتنی
📍 ولایت بلخ
🧑‍🔬 تخصص:
راهنمایی استفاده از محصولات زراعتی

📞 تماس:
+93 78 783 3271
💬 واتساپ:
https://wa.me/93787833271

━━━━━━━━━━━━━━


4️⃣ انجنیر سید اسرار سادات

📍 ولایت بلخ

🧑‍🔬 تخصص:
راهنمایی استفاده از محصولات و حل مشکلات مزارع

📞 تماس:
+93 70 401 2659

💬 واتساپ:
https://wa.me/93704012659


━━━━━━━━━━━━━━


5️⃣ انجنیر رحمت الله هیواد مل

📍 ولایت هلمند

🧑‍🔬 تخصص:
مشاوره کشت و زراعت و انتخاب کود مناسب

📞 تماس:
+93 70 025 1198

💬 واتساپ:
https://wa.me/93700251198


━━━━━━━━━━━━━━


6️⃣ انجنیر عبدالجمیل حیدری

📍 ولایت هلمند

🧑‍🔬 تخصص:
مشاوره کشت و زراعت و انتخاب کود مناسب

📞 تماس:
+93 70 727 1310

💬 واتساپ:
https://wa.me/93707271310


🌿 درخشان گروپ؛ همراه مطمئن دهقانان افغانستان
"""
        )


    # تماس


    elif button_id=="contact":


        send_text(phone,

"""
☎️ تماس با درخشان گروپ


کارشناسان ما آماده پاسخگویی هستند.


واتساپ:
https://wa.me/93788333888
+93788333888


برای قیمت، نمایندگی و همکاری تجارتی پیام دهید.
"""
)


def send_product(phone, image, name, price):

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "interactive",
        "interactive": {
            "type": "cta_url",
            "header": {
                "type": "image",
                "image": {
                    "link": f"https://raw.githubusercontent.com/sayedmurtazasadat631-glitch/durakhshan-whatsapp-bot/main/{image}"
                }
            },
            "body": {
                "text": f"""🌿 {name}

💰 قیمت: {price}

کود فوق العاده درخشان گروپ

جهت ثبت سفارش روی دکمه زیر کلیک نمایید."""
            },
            "action": {
                "name": "cta_url",
                "parameters": {
                    "display_text": "🛒 سفارش محصول",
                    "url": f"https://wa.me/93701660911?text=سلام، میخواهم {name} را سفارش دهم."
                }
            }
        }
    }

    print("SENDING PRODUCT:", data)
    send_message(data)

@app.route("/")
def home():
    return "Durakhshan WhatsApp Bot is Running!"


if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
