from telebot import TeleBot
from telebot.types import Message

def register_referral_handlers(bot: TeleBot):
    
    @bot.message_handler(func=lambda message: message.text == "🎁 دریافت سهمیه رایگان")
    def send_referral_link(message: Message):
        user_id = message.from_user.id
        
        # دریافت اتوماتیک یوزرنیم ربات (برای ساخت لینک تمیز)
        bot_info = bot.get_me()
        bot_username = bot_info.username
        
        # ساخت لینک اختصاصی کاربر
        ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        
        # متن جذابی که کاربر رو ترغیب کنه لینک رو برای بقیه بفرسته
        promo_text = (
            "🎁 <b>دریافت شارژ اضطراری رایگان!</b>\n\n"
            "سهمیه روزانه‌ات تموم شده؟ هیچ مشکلی نیست!\n"
            "لینک اختصاصی زیر رو برای دوستان، هم‌کلاسی‌ها یا گروه‌های خودت بفرست.\n\n"
            f"🔗 <b>لینک اختصاصی شما:</b>\n<code>{ref_link}</code>\n\n"
            "به ازای <b>هر نفری</b> که با لینک شما وارد صدایار بشه، <b>۳ پردازش رایگان</b> به کیف پول اضطراری شما اضافه می‌شه که هر زمان سهمیه روزانه‌ات صفر شد می‌تونی ازشون استفاده کنی! 🚀"
        )
        
        # ارسال پیام به صورت ریپلای روی پیام کاربر
        bot.reply_to(message, promo_text, parse_mode="HTML")