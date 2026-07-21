from flask import Flask, request
import requests
import os
from datetime import datetime
from urllib.parse import quote

app = Flask(__name__)

from supabase import create_client


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)



# ==============================
# ذخیره سفارش در Supabase
# ==============================

def save_order(phone, product):

    now = datetime.now()


    data = {

        "phone": phone,

        "product": product,

        "date": now.strftime("%Y-%m-%d %H:%M:%S"),

        "day": now.strftime("%Y-%m-%d"),

        "month": now.strftime("%Y-%m"),

        "year": now.strftime("%Y")

    }


    result = supabase.table("orders").insert(data).execute()


    print("==============================")

    print("✅ SUPABASE ORDER SAVED")

    print("📞 PHONE:", phone)

    print("📦 PRODUCT:", product)

    print("==============================")
    

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
# مدیر سیستم

ADMIN_NUMBERS = [

    "93701660911"

]

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
DG به شرکت درخشان گروپ خوش آمدید

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

    data = request.get_json()

    print("========== NEW MESSAGE ==========")
    print(data)
    print("=================================")

    try:


        message = data["entry"][0]["changes"][0]["value"]["messages"][0]

        print("MESSAGE:")
        print(message)

        phone = message["from"]

        
        # پیام متنی

        if "text" in message:

            text = message["text"]["body"].lower()

            print("TEXT:", text)



            if text == "گزارش فروش":

                if phone in ADMIN_NUMBERS:

                    send_sales_report(phone)

                else:

                    send_text(
                        phone,
                        "❌ شما دسترسی به گزارش فروش ندارید."
                    )

                return "OK", 200



            if text == "گزارش امروز":

                if phone in ADMIN_NUMBERS:

                    send_today_report(phone)

                else:

                    send_text(
                        phone,
                        "❌ دسترسی ندارید."
                    )

                return "OK", 200



            if text == "گزارش ماهانه":

                if phone in ADMIN_NUMBERS:

                    send_month_report(phone)

                else:

                    send_text(
                        phone,
                        "❌ دسترسی ندارید."
                    )

                return "OK", 200
                

            # ثبت سفارش مشتری

            if (
                "سفارش" in text
                or "میخواهم" in text
                or "می خواهم" in text
                or "order" in text
            ):

                product_name = text.replace(
                    "سلام، میخواهم",
                    ""
                ).replace(
                    "سلام میخواهم",
                    ""
                ).replace(
                    "را سفارش دهم",
                    ""
                ).strip()


                save_order(
                    phone,
                    product_name
                )


                send_text(
                    phone,
                    f"""
✅ سفارش شما ثبت شد.

📦 محصول انتخابی:
{product_name}

📞 کارمندان درخشان گروپ به زودی جهت تکمیل سفارش با شما تماس می‌گیرند.

🌱 تشکر از اعتماد شما.
"""
                )


                return "OK", 200



            if (
                "سلام" in text
                or "hello" in text
                or "hi" in text
            ):



                main_menu(phone)



        # انتخاب از منو


        if "interactive" in message:

            print("INTERACTIVE FOUND")

            interactive = message["interactive"]

            print(interactive)


            if "list_reply" in interactive:

                button_id = interactive["list_reply"]["id"]

                print("BUTTON ID:", button_id)

                handle_button(
                    phone,
                    button_id
                )


            elif "button_reply" in interactive:

                button_id = interactive["button_reply"]["id"]

                print("BUTTON ID:", button_id)

                handle_button(
                    phone,
                    button_id
                )


    except Exception as e:

        print(e)


    return "OK", 200

def handle_button(phone, button_id):

    print("BUTTON CLICKED:", button_id)

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


    elif button_id == "humic5":

        send_product(
            phone,
            "humic5.png",
            "🌿 هیومیک اسید ۵ لیتری",
            "500 افغانی",
            "humic5"
        )


    elif button_id == "humic10":

        send_product(
            phone,
            "humic10.png",
            "🌿 هیومیک اسید ۱۰ لیتری",
            "900 افغانی",
            "humic10"
        )


    elif button_id == "humic20":

        send_product(
            phone,
            "humic20.png",
            "🌿 هیومیک اسید ۲۰ لیتری",
            "1800 افغانی",
            "humic20"
        )



    # NPK


    elif button_id == "npk":

        send_product(

            phone,

            "NPK.png",

            "🌱 کود فوق العاده NPK",

            "۲۰۰ افغانی",

            "npk"

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




    elif button_id == "sales":

        data = {

            "messaging_product": "whatsapp",
            "to": phone,
            "type": "interactive",

            "interactive": {

                "type": "list",

                "body": {

                    "text": """
🏪 محل فروشات درخشان گروپ

لطفاً نوع مرکز مورد نظر را انتخاب نمایید:
"""

                },

                "action": {

                    "button": "انتخاب",

                    "sections": [

                        {

                            "title": "نوع مرکز",

                            "rows": [

                                {
                                    "id": "factories",
                                    "title": "🏭 فابریکه‌ها",
                                    "description": "آدرس فابریکه‌های درخشان گروپ"
                                },

                                {
                                    "id": "branches",
                                    "title": "🏪 نمایندگی‌ها",
                                    "description": "مراکز فروش در ولایات"
                                }

                            ]

                        }

                    ]

                }

            }

        }

        send_message(data)


    # فابریکه‌ها

    elif button_id == "factories":

        data = {

            "messaging_product": "whatsapp",
            "to": phone,
            "type": "interactive",

            "interactive": {

                "type": "list",

                "body": {

                    "text": """
🏭 فابریکه‌های درخشان گروپ

لطفاً فابریکه مورد نظر را انتخاب نمایید:
"""

                },

                "action": {

                    "button": "انتخاب فابریکه",

                    "sections": [

                        {

                            "title": "فابریکه‌ها",

                            "rows": [

                                {
                                    "id": "factory_balkh2",
                                    "title": "درخشان نمبر 2 بلخ",
                                    "description": "شاهراه مزار-شبرغان، بلخ افغانستان"
                                },

                                {
                                    "id": "factory_helmand4",
                                    "title": "درخشان نمبر 4 هلمند",
                                    "description": "سرک نادعلی، منطقه جمپ پوسته بولان هلمند"
                                },

                                {
                                    "id": "factory_balkh1",
                                    "title": "درخشان نمبر 1 بلخ",
                                    "description": "شاهراه مزارشبرغان، چهارسرکه ولسوالی بلخ"
                                },

                                {
                                    "id": "factory_balkh3",
                                    "title": "درخشان نمبر 3 بلخ",
                                    "description": "شاهراه مزار، ولسوالی بلخ، باغ اوراق"
                                }

                            ]

                        }

                    ]

                }

            }

        }

        send_message(data)


    # معلومات فابریکه‌ها

    elif button_id == "factory_balkh2":

        send_factory(
            phone,
            "🏭 فابریکه درخشان نمبر 2 بلخ",
            "شاهراه مزار - شبرغان، ولایت بلخ، افغانستان"
        )


    elif button_id == "factory_helmand4":

        send_factory(
            phone,
            "🏭 فابریکه درخشان نمبر 4 هلمند",
            "سرک نادعلی، منطقه جمپ پوسته بولان، ولایت هلمند، افغانستان"
        )


    elif button_id == "factory_balkh1":

        send_factory(
            phone,
            "🏭 فابریکه درخشان نمبر 1 بلخ",
            "شاهراه مزارشبرغان، چهارسرکه ولسوالی بلخ، افغانستان"
        )


    elif button_id == "factory_balkh3":

        send_factory(
            phone,
            "🏭 فابریکه درخشان نمبر 3 بلخ",
            "شاهراه مزار، ولسوالی بلخ، باغ اوراق، افغانستان"
        )
        
        
    # نمایندگی‌ها

    elif button_id == "branches":

        data = {

            "messaging_product": "whatsapp",
            "to": phone,
            "type": "interactive",

            "interactive": {

                "type": "list",

                "body": {

                    "text": """
🏪 نمایندگی‌ها و مراکز فروش درخشان گروپ

لطفاً ولایت مورد نظر را انتخاب نمایید:
"""

                },

                "action": {

                    "button": "انتخاب ولایت",

                    "sections": [

                        {

                            "title": "نمایندگی‌ها",

                            "rows": [

                                {
                                    "id": "jalalabad",
                                    "title": "جلال‌آباد",
                                    "description": "نمایندگی فروش"
                                },

                                {
                                    "id": "faryab",
                                    "title": "فاریاب",
                                    "description": "نمایندگی فروش"
                                },

                                {
                                    "id": "kunduz",
                                    "title": "کندز",
                                    "description": "قاری شکرالله"
                                },

                                {
                                    "id": "mazar",
                                    "title": "مزارشریف",
                                    "description": "آرین شراف"
                                },

                                {
                                    "id": "charbolak",
                                    "title": "چهاربولک",
                                    "description": "نقیب الله وزیری"
                                },

                                {
                                    "id": "dawlatabad",
                                    "title": "دولت‌آباد",
                                    "description": "پیر محمد"
                                },

                                {
                                    "id": "baghlan",
                                    "title": "بغلان",
                                    "description": "ضیالحق بغلان"
                                },

                                {
                                    "id": "helmand",
                                    "title": "هلمند",
                                    "description": "عبدالله هلمندی"
                                }

                            ]

                        }

                    ]

                }

            }

        }

        send_message(data)

    
    elif button_id=="jalalabad":

        send_sales(
            phone,
            "داکتر امرالله صافی",
            "ولایت جلال‌آباد، افغانستان",
            "+93704012659",
            None
        )


    elif button_id=="faryab":

        send_sales(
            phone,
            "حاجی محب الله و امین الله راز",
            "ولایت فاریاب، افغانستان",
            "+93704012659",
            None
        )


    elif button_id=="kunduz":

        send_sales(
            phone,
            "قاری شکرالله خان",
            "ولایت کندز، افغانستان",
            "+93704012659",
            None
        )


    elif button_id=="charbolak":

        send_sales(
            phone,
            "نقیب الله وزیری",
            "ولسوالی چهاربولک، افغانستان",
            "+93704012659",
            None
        )


    elif button_id=="mazar":

        send_sales(
            phone,
            "آرین شراف",
            "شهر مزارشریف، ولایت بلخ، افغانستان",
            "+93704012659",
            None
        )


    elif button_id=="helmand":

        send_sales(
            phone,
            "عبدالله هلمندی",
            "ولایت هلمند، افغانستان",
            "+93704012659",
            None
        )


    elif button_id=="baghlan":

        send_sales(
            phone,
            "ضیالحق بغلان",
            "ولایت بغلان، افغانستان",
            "+93704012659",
            None
        )


    elif button_id=="dawlatabad":

        send_sales(
            phone,
            "پیر محمد",
            "ولسوالی دولت‌آباد، ولایت فاریاب، افغانستان",
            "+93704012659",
            None
        )



    # کارشناسان

    elif button_id=="experts":

        data = {

            "messaging_product":"whatsapp",

            "to":phone,

            "type":"interactive",

            "interactive":{

                "type":"list",

                "body":{

                    "text":"👨‍🌾 لطفاً کارشناس مورد نظر را انتخاب نمایید."

                },

                "action":{

                    "button":"انتخاب کارشناس",

                    "sections":[

                        {

                            "title":"کارشناسان زراعتی",

                            "rows":[

                                {
                                    "id":"yasin",
                                    "title":"انجنیر محمد یاسین عزیزی",
                                    "description":"لابراتوار و خاک‌شناسی"
                                },

                                {
                                    "id":"faiz",
                                    "title":"انجنیر فیض محمد خان",
                                    "description":"مشاوره کشت و زراعت"
                                },

                                {
                                    "id":"ghafor",
                                    "title":"انجنیر عبدالغفور بیتنی",
                                    "description":"راهنمایی محصولات زراعتی"
                                },

                                {
                                    "id":"esrar",
                                    "title":"انجنیر سید اسرار سادات",
                                    "description":"حل مشکلات مزارع"
                                },

                                {
                                    "id":"hewad",
                                    "title":"انجنیر رحمت الله هیوادمل",
                                    "description":"مشاوره انتخاب کود"
                                },

                                {
                                    "id":"jamil",
                                    "title":"انجنیر عبدالجمیل حیدری",
                                    "description":"مشاوره انتخاب کود"
                                }

                            ]

                        }

                    ]

                }

            }

        }

        send_message(data)


    elif button_id=="yasin":

        send_expert(
            phone,
            "yasin.png",
            "انجنیر محمد یاسین عزیزی",
            "ولایت بلخ",
            "لابراتوار و خاک‌شناسی",
            "+93781449095"
        )


    elif button_id=="faiz":

        send_expert(
            phone,
            "faiz.png",
            "انجنیر فیض محمد خان",
            "ولایت بلخ",
            "مشاوره کشت و زراعت",
            "93788730949"
        )


    elif button_id=="ghafor":

        send_expert(
            phone,
            "ghafor.png",
            "انجنیر عبدالغفور بیتنی",
            "ولایت بلخ",
            "راهنمایی استفاده از محصولات زراعتی",
            "93787833271"
        )


    elif button_id=="esrar":

        send_expert(
            phone,
            "esrar.png",
            "انجنیر سید اسرار سادات",
            "ولایت بلخ",
            "حل مشکلات مزارع و مشاوره زراعتی",
            "93704012659"
        )


    elif button_id=="hewad":

        send_expert(
            phone,
            "hewad.png",
            "انجنیر رحمت الله هیوادمل",
            "ولایت هلمند",
            "مشاوره کشت و انتخاب کود",
            "93700251198"
        )


    elif button_id=="jamil":

        send_expert(
            phone,
            "jamil.png",
            "انجنیر عبدالجمیل حیدری",
            "ولایت هلمند",
            "مشاوره کشت و انتخاب کود",
            "93707271310"
        )


    # ==============================
    # ثبت سفارش محصول
    # ==============================

    elif button_id.startswith("order_"):

        product_id = button_id.replace(
            "order_",
            ""
        )


        product_names = {

            "humic5":
                "🌿 هیومیک اسید ۵ لیتری",

            "humic10":
                "🌿 هیومیک اسید ۱۰ لیتری",

            "humic20":
                "🌿 هیومیک اسید ۲۰ لیتری",

            "NPK":
                "🌱 کود فوق العاده NPK",

            "npk":
                "🌱 کود فوق العاده NPK"

        }


        product = product_names.get(
            product_id,
            product_id
        )


        save_order(
            phone,
            product
        )


        print("==============================")
        print("🛒 NEW ORDER")
        print("📞 PHONE:", phone)
        print("📦 PRODUCT:", product)
        print("==============================")


        send_text(
            phone,
            f"""
✅ سفارش شما با موفقیت ثبت شد.


📦 محصول انتخابی:

{product}


📞 کارشناسان درخشان گروپ در کوتاه‌ترین زمان ممکن جهت تکمیل سفارش با شما تماس خواهند گرفت.


🌱 از اعتماد شما سپاسگزاریم.
"""
        )

    # تماس

    elif button_id=="contact":

        send_text(
            phone,
            """
☎️ تماس با درخشان گروپ

کارشناسان ما آماده پاسخگویی هستند.

📲 واتساپ:
https://wa.me/93701660911

📞 +93701660911

برای قیمت، نمایندگی و همکاری تجارتی پیام دهید.
"""
        )


def send_product(phone, image, name, price, product_id=None):


    save_order(
        phone,
        name
    )


    notify_sales(
        phone,
        name
    )


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

                "text": f"""
🌿 {name}


💰 قیمت:
{price}


✅ سفارش شما ثبت شد.


📞 کارشناسان فروش درخشان گروپ به زودی با شما تماس می‌گیرند.
"""

            },


            "action": {

                "name": "cta_url",


                "parameters": {

                    "display_text": "💬 تماس با فروش",

                    "url": f"https://wa.me/93704012659?text={quote('سلام، در مورد سفارش ' + name + ' معلومات میخواهم')}"

                }

            }

        }

    }


    print("SENDING PRODUCT:", data)


    send_message(data)


def notify_sales(phone, product):


    sales_numbers = [

        "93701660911",

        "93704012659"

    ]


    customer_link = f"https://wa.me/{phone}?text={quote('سلام، در مورد سفارش شما از درخشان گروپ تماس گرفتم.')}"

    for sales_number in sales_numbers:

    data = {

        "messaging_product": "whatsapp",

        "to": sales_number,

        "type": "interactive",

        "interactive": {

            "type": "cta_url",

            "body": {

                "text": f"""
🛒 سفارش جدید درخشان گروپ


📦 محصول:

{product}


📞 شماره مشتری:

+{phone}


برای تکمیل سفارش با مشتری تماس بگیرید.
"""

            },


            "action": {

                "name": "cta_url",

                "parameters": {

                    "display_text": "💬 پاسخ مشتری",

                    "url": customer_link

                }

            }

        }

    }


    send_message(data)


def send_expert(phone,image,name,province,specialty,whatsapp):

    data = {
        "messaging_product":"whatsapp",
        "to":phone,
        "type":"interactive",

        "interactive":{

            "type":"cta_url",

            "header":{
                "type":"image",
                "image":{
                    "link":f"https://raw.githubusercontent.com/sayedmurtazasadat631-glitch/durakhshan-whatsapp-bot/main/{image}"
                }
            },

            "body":{
                "text":f"""👨‍🌾 {name}

📍 {province}

🎓 تخصص:
{specialty}

برای دریافت مشاوره تخصصی روی دکمه زیر کلیک نمایید."""
            },

            "action":{
                "name":"cta_url",

                "parameters":{
                    "display_text":"💬 گفتگو با کارشناس",
                    "url":f"https://wa.me/{whatsapp}"
                }
            }

        }

    }

    send_message(data)


def send_sales(phone, name, location, whatsapp, image=None):

    print("SALES BUTTON CLICKED:", name)


    if image:

        header = {

            "type":"image",

            "image":{

                "link":f"https://raw.githubusercontent.com/sayedmurtazasadat631-glitch/durakhshan-whatsapp-bot/main/{image}"

            }

        }


    else:

        header = None



    data = {

        "messaging_product":"whatsapp",

        "to":phone,

        "type":"interactive",

        "interactive":{

            "type":"cta_url",

            "body":{

                "text":f"""🏪 مرکز فروش درخشان گروپ


👤 مسئول فروش:
{name}


📍 آدرس:
{location}


برای معلومات و سفارش کود درخشان گروپ روی دکمه زیر کلیک نمایید."""

            },


            "action":{

                "name":"cta_url",

                "parameters":{

                    "display_text":"💬 تماس واتساپ",

                    "url": f"https://wa.me/93704012659?text=سلام، معلومات و سفارش از {name} در {location} را میخواهم."

                }

            }

        }

    }



    if header:

        data["interactive"]["header"] = header



    print("SENDING SALES:", data)


    send_message(data)


def send_factory(phone, name, location):

    data = {

        "messaging_product": "whatsapp",

        "to": phone,

        "type": "interactive",

        "interactive": {

            "type": "cta_url",

            "body": {

                "text": f"""
{name}


📍 آدرس:
{location}


برای معلومات، سفارش و همکاری تجارتی با درخشان گروپ تماس بگیرید.
"""

            },

            "action": {

                "name": "cta_url",

                "parameters": {

                    "display_text": "💬 تماس واتساپ",

                    "url": f"https://wa.me/93704012659?text=سلام، معلومات {name} را میخواهم."

                }

            }

        }

    }


    send_message(data)
    
# گزارش فروش مدیر

def send_sales_report(phone):

    result = supabase.table("orders") \
        .select("product") \
        .execute()


    orders = result.data


    if not orders:

        send_text(
            phone,
            "📊 هنوز هیچ سفارشی ثبت نشده است."
        )

        return



    products = {}


    for order in orders:

        product = order["product"]

        if product in products:

            products[product] += 1

        else:

            products[product] = 1



    report = """
📊 گزارش فروش درخشان گروپ


"""


    total = 0


    for product, count in products.items():

        report += f"""
📦 محصول:
{product}

🛒 تعداد سفارش:
{count}

----------------
"""

        total += count



    report += f"""

✅ مجموع سفارشات:
{total}

📅 تاریخ گزارش:
{datetime.now().strftime("%Y-%m-%d %H:%M")}

"""


    send_text(
        phone,
        report
    )

# گزارش فروش امروز

def send_today_report(phone):

    today = datetime.now().strftime("%Y-%m-%d")


    result = supabase.table("orders") \
        .select("product") \
        .eq("day", today) \
        .execute()


    orders = result.data


    if not orders:

        send_text(
            phone,
            "📊 امروز هیچ سفارشی ثبت نشده است."
        )

        return



    products = {}


    for order in orders:

        product = order["product"]

        if product in products:

            products[product] += 1

        else:

            products[product] = 1



    report = """
📊 گزارش فروش امروز
درخشان گروپ


"""


    total = 0


    for product, count in products.items():

        report += f"""
📦 محصول:
{product}

🛒 تعداد سفارش:
{count}

----------------
"""

        total += count



    report += f"""

✅ مجموع سفارشات امروز:
{total}

📅 تاریخ:
{today}

"""


    send_text(
        phone,
        report
    )





# گزارش فروش ماهانه

def send_month_report(phone):

    month = datetime.now().strftime("%Y-%m")


    result = supabase.table("orders") \
        .select("product") \
        .eq("month", month) \
        .execute()


    orders = result.data


    if not orders:

        send_text(
            phone,
            "📊 این ماه هنوز سفارشی ثبت نشده است."
        )

        return



    products = {}


    for order in orders:

        product = order["product"]

        if product in products:

            products[product] += 1

        else:

            products[product] = 1



    report = """
📊 گزارش فروش ماهانه
درخشان گروپ


"""


    total = 0


    for product, count in products.items():

        report += f"""
📦 محصول:
{product}

🛒 تعداد سفارش:
{count}

----------------
"""

        total += count



    report += f"""

✅ مجموع سفارشات ماه:
{total}

📅 ماه:
{month}

"""


    send_text(
        phone,
        report
    )


@app.route("/")
def home():
    return "Durakhshan WhatsApp Bot is Running!"


if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
