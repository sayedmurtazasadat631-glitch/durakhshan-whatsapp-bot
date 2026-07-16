from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

GRAPH_URL = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"


# ارسال پیام واتساپ
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


# تایید Webhook
@app.route("/webhook", methods=["GET"])
def verify_webhook():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge

    return "Verification failed", 403



# دریافت پیام واتساپ
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    try:

        message = data["entry"][0]["changes"][0]["value"]["messages"][0]

        phone = message["from"]
        text = message["text"]["body"].strip().upper()


        text_lower = text.lower()


        # تشخیص زبان و خوش آمدگویی

        if (
            "سلام" in text
            or "hello" in text_lower
            or "hi" in text_lower
        ):

            reply = """
🌿 Welcome to Durakhshan Group
🌿 به درخشان گروپ خوش آمدید

Please select an option:
لطفاً یکی را انتخاب کنید:

#PRODUCTS
📦 Products / محصولات

#BRANCH
🤝 Sales Representatives / نمایندگی فروشات

#SALES
🏪 Sales Locations / محل فروشات

#EXPERTS
🌱 Agricultural Experts / کارشناسان زراعتی

#ABOUT
🏭 About Durakhshan Group / در مورد درخشان گروپ

#CONTACT
☎️ Contact Us / راه‌های تماس
"""


        else:

            reply = handle_message(text)


        send_message(phone, reply)


    except Exception as e:

        print(e)


    return "OK", 200



def handle_message(text):


    # محصولات

    if text == "#PRODUCTS":

        return """
📦 محصولات درخشان گروپ

لطفاً محصول مورد نظر را انتخاب نمایید:

#HUMIC
🌿 کود فوق العاده هیومیک اسید

#NPK
🌿 کود فوق العاده NPK

#COTTON
🧵 پنبه پروسس شده

#LAB
🔬 خدمات لابراتوار

#SEEDS
🌱 تخم و خدمات زراعتی

#OTHER
🌿 سایر محصولات
"""


    # هیومیک اسید

    elif text == "#HUMIC":

        return """
🌿 کود فوق العاده هیومیک اسید

توضیحات:
هیومیک اسید فوق العاده یک کود مؤثر برای بهبود ساختمان خاک، تقویت ریشه و افزایش جذب مواد غذایی گیاه می‌باشد.

✅ فواید:
• تقویت ریشه و رشد بهتر گیاه
• افزایش جذب مواد غذایی
• بهبود کیفیت و حاصل‌خیزی خاک
• افزایش کیفیت و محصول‌دهی

🌱 موارد استفاده:
قابل استفاده برای تمام محصولات زراعتی، باغ‌ها، سبزیجات و کشت‌های مختلف.

📦 بسته‌بندی:
• 5 لیتره
• 10 لیتره
• 20 لیتره

💰 قیمت‌ها:

1️⃣ 5 لیتره: 500 افغانی
2️⃣ 10 لیتره: 900 افغانی
3️⃣ 20 لیتره: 1800 افغانی

#PRODUCTS
بازگشت به محصولات
"""


    # NPK

    elif text == "#NPK":

        return """
🌿 کود فوق العاده NPK

توضیحات:
NPK فوق العاده یک کود کامل برای تأمین عناصر غذایی گیاه، تقویت رشد و افزایش کیفیت محصولات زراعتی می‌باشد.

✅ فواید:
• تأمین مواد غذایی مورد نیاز گیاه
• تقویت ریشه
• افزایش رشد گیاه
• افزایش کیفیت و حاصل‌دهی

🌱 موارد استفاده:
تمام محصولات زراعتی، باغ‌ها و سبزیجات.

📦 بسته‌بندی:
• 1 لیتره

💰 قیمت:

1️⃣ کود فوق العاده NPK یک لیتره: 200 افغانی

#PRODUCTS
بازگشت به محصولات
"""


    # پنبه

    elif text == "#COTTON":

        return """
🧵 پنبه پروسس شده درخشان گروپ

پنبه درخشان گروپ با ماشین‌آلات مدرن و تکنالوژی پیشرفته پروسس شده و برای صنایع نساجی آماده می‌گردد.

✅ کیفیت عالی و الیاف یک‌دست
✅ پروسس با معیارهای جهانی
✅ مناسب برای بازارهای داخلی و صادراتی

#PRODUCTS
"""


    # خدمات لابراتوار

    elif text == "#LAB":

        return """
🔬 خدمات لابراتوار درخشان گروپ

لابراتوار مجهز درخشان گروپ با استفاده از تجهیزات مدرن، آزمایش و بررسی کیفیت محصولات زراعتی را انجام می‌دهد.

خدمات شامل:

✅ آزمایش خاک
✅ بررسی کودهای زراعتی
✅ آزمایش بذور
✅ کنترل کیفیت محصولات
✅ ارائه نتایج دقیق و قابل اعتماد

#PRODUCTS
"""


    # تخم و خدمات زراعتی

    elif text == "#SEEDS":

        return """
🌱 محصولات تخم و خدمات زراعتی

درخشان گروپ با ارائه تخم‌های باکیفیت و خدمات تخصصی زراعتی، زمینه رشد بهتر و حاصل‌دهی بیشتر را فراهم می‌سازد.

شامل:

🌱 پنبه دانه با کیفیت
🌱 تخم‌های اصلاح‌شده زراعتی
🌱 مشاوره کشت و مدیریت مزارع
🌱 بررسی کیفیت تخم‌ها

#PRODUCTS
"""


    # سایر محصولات

    elif text == "#OTHER":

        return """
🌿 سایر محصولات درخشان گروپ

شامل:

🌿 کودهای زراعتی
🌱 محصولات زراعتی
🧵 پنبه و الیاف
🥜 محصولات روغنی
🐄 محصولات خوراک حیوانی

#PRODUCTS
"""


    # نمایندگی فروشات

    elif text == "#BRANCH":

        return """
🤝 نمایندگی‌های فروشات درخشان گروپ

لطفاً ولایت مورد نظر خود را ارسال کنید.

#BALKH
#HELMAND
#FARYAB
#KUNDUZ

"""



    # محل فروشات

    elif text == "#SALES":

        return """
🏪 محل فروشات درخشان گروپ

لطفاً محل فروش مورد نظر را انتخاب کنید:

#BALKH
ولایت بلخ

#JALALABAD
ولایت ننگرهار

#FARYAB
ولایت فاریاب

#KUNDUZ
ولایت کندز

#BAGHLAN
ولایت بغلان

#HELMAND
ولایت هلمند
"""



    # بلخ

    elif text == "#BALKH":

        return """
📍 ولایت بلخ

🏭 درخشان نمبر اول

آدرس:
چهارسرک ولسوالی بلخ، ولایت بلخ، افغانستان

☎️ تماس:
0788730949


🏭 درخشان نمبر دوم

آدرس:
شاهراه مزار-شبرغان، چهارگنبد بلخ

☎️ تماس:
+93786470833
💬 واتساپ:
https://wa.me/93786470833

🏭 درخشان نمبر سوم

آدرس:
شاهراه مزار-ولسوالی بلخ، باغ اوراق بلخ

☎️ تماس:
+93780811613
"""



    # هلمند

    elif text == "#HELMAND":

        return """
📍 ولایت هلمند

🏭 درخشان نمبر چهارم

آدرس:
شاهراه هلمند-نادعلی، جمپ پوسته، ولایت هلمند افغانستان

☎️ تماس:
+93700009263
"""



    # فاریاب

    elif text == "#FARYAB":

        return """
📍 ولایت فاریاب

نام:
حاجی محب الله و امین الله راز

آدرس:
ولایت فاریاب

☎️ تماس:
+93786275466


نام:
پیر محمد

آدرس:
ولسوالی دولت آباد فاریاب

☎️ تماس:
+93788038543
"""



    # کندز

    elif text == "#KUNDUZ":

        return """
📍 ولایت کندز

نام:
قاری شکرالله خان

☎️ تماس:
+93799829245
"""



    # بغلان

    elif text == "#BAGHLAN":

        return """
📍 ولایت بغلان

نام:
ضیالحق بغلان

☎️ تماس:
+93700228685
"""



    # جلال آباد

    elif text == "#JALALABAD":

        return """
📍 ولایت ننگرهار

نام:
داکتر امرالله صافی

☎️ تماس:
+93702227922
"""



    # کارشناسان زراعتی

    elif text == "#EXPERTS":

        return """
🌱 کارشناسان زراعتی درخشان گروپ

#EXPERT1
انجنیر محمد یاسین عزیزی
(لابراتوار و خاک شناسی)

#EXPERT2
انجنیر فیض محمد خان
(مشاوره کشت و زراعت)

#EXPERT3
انجنیر عبدالغفور بیتنی
(راهنمایی استفاده از محصولات)

#EXPERT4
انجنیر سید اسرار سادات
(حل مشکلات مزارع)

#EXPERT5
انجنیر رحمت الله هیواد مل
(مشاوره کشت و انتخاب کود)

#EXPERT6
انجنیر عبدالجمیل حیدری
(مشاوره کشت و انتخاب کود)
"""



    # معلومات شرکت

    elif text == "#ABOUT":

        return """
🌿 درخشان گروپ؛ نماد کیفیت، نوآوری و توسعه پایدار ✨

درخشان گروپ یک مجموعه پیشرو در بخش زراعت، صنعت و تولید می‌باشد.

فعالیت‌های ما شامل:

🌿 تولید کودهای زراعتی
🧵 پروسس پنبه
🔬 خدمات لابراتوار
🌱 محصولات زراعتی
🏭 توسعه صنایع داخلی

هدف ما ایجاد ارزش، حمایت از دهقانان و ساختن آینده روشن برای افغانستان و جهان است.

درخشان گروپ؛ کیفیت، اعتماد و نوآوری.
"""



    # تماس

    elif text == "#CONTACT":

        return """
☎️ راه‌های تماس درخشان گروپ

برای دریافت معلومات بیشتر، قیمت محصولات و همکاری تجارتی با ما تماس بگیرید.

کارشناسان ما آماده خدمت‌رسانی هستند.
"""


    else:

        return """
❌ کد انتخابی درست نیست.

لطفاً یکی از گزینه‌های منو را ارسال کنید:

#PRODUCTS
#SALES
#EXPERTS
#ABOUT
#CONTACT
"""
    

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
