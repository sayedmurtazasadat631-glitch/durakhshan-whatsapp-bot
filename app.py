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


        send_text(phone,

"""
🌿 کود فوق العاده هیومیک اسید


هیومیک اسید یک کود مؤثر برای بهبود ساختمان خاک، تقویت ریشه و افزایش جذب مواد غذایی گیاه می‌باشد.


✅ فواید:

• تقویت رشد ریشه
• افزایش جذب کودها
• بهبود حاصل‌خیزی خاک
• افزایش کیفیت محصولات


📦 بسته‌بندی:

۵ لیتر
۱۰ لیتر
۲۰ لیتر


💰 قیمت:

۵ لیتر: ۵۰۰ افغانی

۱۰ لیتر: ۹۰۰ افغانی

۲۰ لیتر: ۱۸۰۰ افغانی


برای معلومات بیشتر با کارشناسان ما تماس بگیرید.
"""
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


خدمات تخصصی شامل:


✅ آزمایش خاک

✅ آزمایش کودهای زراعتی

✅ آزمایش تخم‌ها

✅ بررسی کیفیت محصولات


ارائه نتایج دقیق و علمی برای رشد بهتر زراعت.
"""
)



    # فروشات


    elif button_id=="sales":


        send_text(phone,

"""
🏪 محل فروشات درخشان گروپ


برای دریافت نزدیک‌ترین مرکز فروش، ولایت خود را ارسال کنید.


📍 بلخ

📍 فاریاب

📍 کندز

📍 بغلان

📍 هلمند

📍 ننگرهار
"""
)



    # کارشناسان


    elif button_id=="experts":


        send_text(phone,

"""
🌱 کارشناسان زراعتی درخشان گروپ


👨‍🌾 انجینر محمد یاسین عزیزی

(لابراتوار و خاک‌شناسی)


👨‍🌾 انجینر فیض محمد خان

(مشاوره کشت و زراعت)


👨‍🌾 انجینر سید اسرار سادات

(حل مشکلات مزارع)


برای مشاوره با ما تماس بگیرید.
"""
)



    # تماس


    elif button_id=="contact":


        send_text(phone,

"""
☎️ تماس با درخشان گروپ


کارشناسان ما آماده پاسخگویی هستند.


واتساپ:

+93786470833


برای قیمت، نمایندگی و همکاری تجارتی پیام دهید.
"""
)


@app.route("/")
def home():
    return "Durakhshan WhatsApp Bot is Running!"


if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
