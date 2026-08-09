from flask import Flask, request, redirect
from utils.zarinpal import send_request, verify_payment
from db.base import SessionLocal
from db.models.user import User
from db.models.group import Group
from datetime import datetime, timedelta
from telebot import telebot
import os
from utils.logger import log_event
import threading
from telebot.types import Update
from db.models.queue import UpdateQueue
app = Flask(__name__)
global_bot = None
# # تعریف بسته‌های اشتراک (برای کاربر و گروه)
# PLANS = {
#     # پلن‌های اکانت شخصی
#     "1": {"amount": 150000, "days": 30, "name": "۱ ماهه شخصی"},
#     "3": {"amount": 390000, "days": 90, "name": "۳ ماهه شخصی"},
#     "6": {"amount": 700000, "days": 180, "name": "۶ ماهه شخصی"},
#     # پلن‌های گروه
#     "group_1": {"amount": 399000, "days": 30, "name": "1 ماهه ویژه گروه"},
#     "group_3": {"amount": 990000, "days": 90, "name": "3 ماهه ویژه گروه"},
#     "group_6": {"amount": 1790000, "days": 180, "name": "6 ماهه ویژه گروه"}
# }
def register_webhook_route(bot):
    """
    این تابع رباتِ کانفیگ‌شده را می‌گیرد و مسیر وب‌هوک را برای آن روی سرور Flask می‌سازد.
    استفاده از توکن در مسیر URL امنیت وب‌هوک را تضمین می‌کند.
    """
    global global_bot
    global_bot = bot
    @app.route(f'/webhook/{bot.token}', methods=['POST'])
    def webhook_receiver():
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            with SessionLocal() as session: 
                new_update = UpdateQueue(update_json=json_string)
                session.add(new_update)
                session.commit()
            return "OK", 200
        
        return "Forbidden", 403

    
# @app.route('/pay/<int:user_id>/<plan_id>')
# def pay(user_id, plan_id):
#     # اگر plan_id با _ شروع شود (یعنی آیدی گروه همراهش باشد مثل group_1_-100123) 
#     # آن را برای چک کردن معتبر بودن پلن، جدا می‌کنیم
#     base_plan_id = plan_id.split('_')[0] + "_" + plan_id.split('_')[1] if plan_id.startswith('group_') else plan_id

#     if base_plan_id not in PLANS:
#         return "❌ پلن انتخابی نامعتبر است."
    
#     plan = PLANS[base_plan_id]
    
#     # ساخت توضیحات اختصاصی برای فاکتور درگاه
#     if plan_id.startswith('group_'):
#         target_group_id = plan_id.split('_')[2]
#         desc = f"خرید اشتراک {plan['name']} ربات صدایار برای گروه {target_group_id}"
#     else:
#         desc = f"خرید اشتراک {plan['name']} ربات صدایار برای آیدی {user_id}"
    
#     status, url_or_err = send_request(plan['amount'], desc, user_id, plan_id)
#     if status:
#         return redirect(url_or_err)
#     return f"❌ خطا در ارتباط با درگاه: {url_or_err}"

# @app.route('/verify')
# def verify():
#     status = request.args.get('Status')
#     authority = request.args.get('Authority')
#     user_id = request.args.get('user_id')
#     plan_id = request.args.get('plan_id')
    
#     base_plan_id = plan_id.split('_')[0] + "_" + plan_id.split('_')[1] if plan_id.startswith('group_') else plan_id

#     if status != 'OK' or base_plan_id not in PLANS:
#         return "❌ پرداخت لغو شد یا اطلاعات نامعتبر است."

#     plan = PLANS[base_plan_id]
#     is_success, ref_id = verify_payment(authority, plan['amount'])
    
#     if is_success:
#         with SessionLocal() as session:
#             now = datetime.now()
            
#             # ===============================================
#             # سناریو ۱: فعال‌سازی اشتراک برای گروه
#             # ===============================================
#             if plan_id.startswith('group_'):
#                 try:
#                     target_group_id = int(plan_id.split('_')[2])
#                     group = session.query(Group).filter(Group.chat_id == target_group_id).first()
                    
#                     if group:
#                         group.is_premium = True
#                         if group.premium_until and group.premium_until > now:
#                             group.premium_until = group.premium_until + timedelta(days=plan['days'])
#                         else:
#                             group.premium_until = now + timedelta(days=plan['days'])
#                         session.commit()
                        
#                         success_msg = (
#                             f"🎉 **پرداخت شما با موفقیت انجام شد!**\n\n"
#                             f"🏢 **گروه فعال شده:** `{target_group_id}`\n"
#                             f"📦 **بسته:** {plan['name']}\n"
#                             f"💳 **کد پیگیری بانکی:** `{ref_id}`\n\n"
#                             f"ربات از هم‌اکنون ویس‌های گروه را به صورت خودکار تبدیل می‌کند."
#                         )
#                         global_bot.send_message(user_id, success_msg, parse_mode="Markdown")
#                         return f"✅ پرداخت موفق! کد پیگیری: {ref_id}. اشتراک گروه فعال شد."
#                     else:
#                         return "❌ پرداخت موفق بود اما گروه در دیتابیس یافت نشد. لطفاً به پشتیبانی پیام دهید."
#                 except Exception as e:
#                     error_details = f"فعالسازی اشتراک برای  گروه {target_group_id} ناموفق بود"
#                     log_event(global_bot, 'error', error_details, send_to_telegram=True)
#                     return f"❌ خطای سیستمی در فعال‌سازی گروه: {e}"
                
           
#             else:
#                 user = session.query(User).filter(User.telegram_id == int(user_id)).first()
#                 if user:
#                     user.is_premium = True
#                     if user.premium_until and user.premium_until > now:
#                         user.premium_until = user.premium_until + timedelta(days=plan['days'])
#                     else:
#                         user.premium_until = now + timedelta(days=plan['days'])
#                     session.commit()
            
#                     success_msg = (
#                         f"🎉 **پرداخت شما با موفقیت انجام شد!**\n\n"
#                         f"📦 بسته فعال شده: {plan['name']}\n"
#                         f"💳 کد پیگیری بانکی: `{ref_id}`\n\n"
#                         f"اکانت شما اکنون ویژه است. ممنون از حمایت شما ❤️"
#                     )
#                     global_bot.send_message(user_id, success_msg, parse_mode="Markdown")
#                     return f"✅ پرداخت موفق! کد پیگیری: {ref_id}. می‌توانید این صفحه را ببندید و به تلگرام برگردید."

#     else:
#         return f"❌ تراکنش ناموفق بود: {ref_id}"
@app.route('/')
def home():
    return "@sedayarbot is alive!", 200