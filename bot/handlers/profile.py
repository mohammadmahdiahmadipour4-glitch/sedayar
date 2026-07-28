from telebot import TeleBot
from db.base import SessionLocal
from db.models.user import User
from bot.messages import PROFILE  # برای خواندن متن دکمه حساب کاربری
from bot.keyboards.inline import premium_upgrade_keyboard  # برای خواندن کیبورد شیشه‌ای
# ایمپورت سقف‌های روزانه از ریپازیتوری تا همه‌جا یکسان باشه
from db.repositories.user import FREE_DAILY_LIMIT, PREMIUM_DAILY_LIMIT

def register_profile_handlers(bot: TeleBot):
    
    # چک کردن اینکه پیام کاربر با متغیر PROFILE برابر باشد یا دستورات متنی
    @bot.message_handler(func=lambda m: m.text == PROFILE or m.text in ['/me', '/profile'])
    def show_profile(m):
        user_id = m.from_user.id
        
        with SessionLocal() as session:
            user = session.query(User).filter(User.telegram_id == user_id).first()
            
            if not user:
                bot.send_message(m.chat.id, "❌ اطلاعات شما هنوز ثبت نشده است. لطفاً ربات را /start کنید.")
                return
                
            status = "⭐️ ویژه (Premium)" if user.is_premium else "👤 عادی (Free)"
            quota_used = user.daily_usage
            
            text = (
                "👤 **پروفایل کاربری شما**\n\n"
                f"🆔 آیدی عددی: `{user.telegram_id}`\n"
                f"💎 وضعیت اکانت: {status}\n"
                "➖➖➖➖➖➖➖\n"
            )
            
            markup = None
            if not user.is_premium:
                quota_left = max(0, FREE_DAILY_LIMIT - quota_used)
                text += f"🔋 سهمیه مصرف‌شده امروز: {quota_used} از {FREE_DAILY_LIMIT}\n"
                text += f"⚡️ سهمیه باقیمانده: {quota_left}\n"
                text += f"🎁 شارژ اضطراری (کیف پول): {user.bonus_quota} پردازش\n"
                text += "➖➖➖➖➖➖➖\n"
                text += f"👥 تعداد افراد دعوت شده: {user.total_referrals} نفر\n\n"
                text += "💡 برای استفاده نامحدود، می‌توانید اکانت خود را ارتقا دهید."
                
                # دریافت کیبورد شیشه‌ای به صورت ماژولار از پوشه keyboards
                markup = premium_upgrade_keyboard()
            else:
                text += f"📈 پردازش‌های امروز شما: {quota_used}\n"
                text += f"🎁 شارژ اضطراری (ذخیره شده): {user.bonus_quota} پردازش\n"
                text += "➖➖➖➖➖➖➖\n"
                text += f"👥 تعداد افراد دعوت شده: {user.total_referrals} نفر\n"
                
            bot.send_message(m.chat.id, text, parse_mode="Markdown", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'back_to_profile' and call.message.chat.type == 'private' )
    def back_to_profile(call):
        # ۱. متوقف کردن علامت لودینگ (ساعت شنی) روی دکمه شیشه‌ای
        bot.answer_callback_query(call.id)
        
        # ۲. پاک کردن پیام منوی قیمت‌ها تا صفحه چت شلوغ نشه
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        # ۳. ترفند اصلی: فرستنده پیام رو از "ربات" به "کاربری که کلیک کرده" تغییر می‌دیم
        call.message.from_user = call.from_user
        
        # ۴. حالا تابع نمایش پروفایل رو با خیال راحت صدا می‌زنیم
        show_profile(call.message)