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

    print("FULL MESSAGE:")
    print(data)

    try:


        message=data["entry"][0]["changes"][0]["value"]["messages"][0]


        phone=message["from"]



        # پیام متنی

        if "interactive" not in message and "text" in message:


            text = message["text"]["body"].lower()


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


                button_id = interactive["list_reply"]["id"]
                
                print("BUTTON ID RECEIVED:")
                print(button_id)

                
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

        send_product(
            phone,
            "NPK.png",
            "🌱 کود فوق العاده NPK",
            "۲۰۰ افغانی"
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

    elif button_id == "sales":

        data = {

            "messaging_product": "whatsapp",

            "to": phone,

            "type": "interactive",

            "interactive": {

                "type": "list",

                "body": {

                    "text": "🏭 لطفاً محل فروش نزدیک خود را انتخاب نمایید."

                },

                "action": {

                    "button": "انتخاب محل",

                    "sections": [

                        {

                            "title": "مراکز فروش درخشان گروپ",

                            "rows": [

                                {
                                    "id": "jalalabad",
                                    "title": "داکتر امرالله صافی",
                                    "description": "ولایت جلال‌آباد"
                                },

                                {
                                    "id": "faryab",
                                    "title": "حاجی محب الله و امین الله راز",
                                    "description": "ولایت فاریاب"
                                },

                                {
                                    "id": "kunduz",
                                    "title": "قاری شکرالله خان",
                                    "description": "ولایت کندز"
                                },

                                {
                                    "id": "charbolak",
                                    "title": "نقیب الله وزیری",
                                    "description": "ولسوالی چهاربولک"
                                },

                                {
                                    "id": "mazar",
                                    "title": "آرین شراف",
                                    "description": "شهر مزارشریف، ولایت بلخ"
                                },

                                {
                                    "id": "helmand",
                                    "title": "عبدالله هلمندی",
                                    "description": "ولایت هلمند"
                                },

                                {
                                    "id": "baghlan",
                                    "title": "ضیالحق بغلان",
                                    "description": "ولایت بغلان"
                                },

                                {
                                    "id": "dawlatabad",
                                    "title": "پیر محمد",
                                    "description": "دولت‌آباد، ولایت فاریاب"
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

                    "url":"https://wa.me/93704012659?text=سلام%20معلومات%20و%20سفارش%20کود%20درخشان%20گروپ%20را%20میخواهم"

                }

            }

        }

    }



    if header:

        data["interactive"]["header"] = header



    print("SENDING SALES:", data)


    send_message(data)


@app.route("/")
def home():
    return "Durakhshan WhatsApp Bot is Running!"


if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
