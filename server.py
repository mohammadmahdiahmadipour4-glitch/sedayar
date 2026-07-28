from flask import Flask, request, redirect
from utils.zarinpal import send_request, verify_payment
from db.base import SessionLocal
from db.models.user import User
from datetime import datetime, timedelta
from telebot import telebot , TeleBot
import os

app = Flask(__name__)
bot =telebot.TeleBot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
# تعریف بسته‌های اشتراک
PLANS = {
    "1": {"amount": 150000, "days": 30, "name": "۱ ماهه"},
    "3": {"amount": 390000, "days": 90, "name": "۳ ماهه"},
    "6": {"amount": 700000, "days": 180, "name": "۶ ماهه"}
}

@app.route('/pay/<int:user_id>/<plan_id>')
def pay(user_id, plan_id):
    if plan_id not in PLANS:
        return "❌ پلن انتخابی نامعتبر است."
    
    plan = PLANS[plan_id]
    desc = f"خرید اشتراک {plan['name']} ربات صدایار"
    
    status, url_or_err = send_request(plan['amount'], desc, user_id, plan_id)
    if status:
        return redirect(url_or_err) # انتقال کاربر به درگاه پرداخت
    return f"❌ خطا در ارتباط با درگاه: {url_or_err}"

@app.route('/verify')
def verify():
    status = request.args.get('Status')
    authority = request.args.get('Authority')
    user_id = request.args.get('user_id')
    plan_id = request.args.get('plan_id')
    
    if status != 'OK' or plan_id not in PLANS:
        return "❌ پرداخت لغو شد یا اطلاعات نامعتبر است."

    plan = PLANS[plan_id]
    is_success, ref_id = verify_payment(authority, plan['amount'])
    
    if is_success:
        # اتصال به دیتابیس و اعمال اشتراک
        with SessionLocal() as session:
            user = session.query(User).filter(User.telegram_id == int(user_id)).first()
            if user:
                user.is_premium = True
                now = datetime.now()
                # اگر کاربر هنوز اشتراک فعال دارد، روزهای جدید به انقضای قبلی اضافه می‌شود
                if user.premium_until and user.premium_until > now:
                    user.premium_until = user.premium_until + timedelta(days=plan['days'])
                else:
                    user.premium_until = now + timedelta(days=plan['days'])
                session.commit()
        
        # ارسال پیام تایید به کاربر داخل تلگرام
        success_msg = (
            f"🎉 **پرداخت شما با موفقیت انجام شد!**\n\n"
            f"📦 بسته فعال شده: {plan['name']}\n"
            f"💳 کد پیگیری بانکی: `{ref_id}`\n\n"
            f"اکانت شما اکنون ویژه است. ممنون از حمایت شما ❤️"
        )
        bot.send_message(user_id, success_msg, parse_mode="Markdown")
        
        return f"✅ پرداخت موفق! کد پیگیری: {ref_id}. می‌توانید این صفحه را ببندید و به تلگرام برگردید."
    else:
        return f"❌ تراکنش ناموفق بود: {ref_id}"

def run_server():
    app.run(host="0.0.0.0", port=5000)