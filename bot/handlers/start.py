from telebot import TeleBot

from bot.messages import WELCOME_MESSAGE
from bot.keyboards.main_menu import get_main_menu
# توابع جدید دیتابیس را ایمپورت می‌کنیم
from db.repositories.user import register_user, add_referral_bonus
from db.base import SessionLocal
from db.models.user import User

def register_start_handler(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def start(message):
        user = message.from_user
        
        # ۱. ثبت یا آپدیت کاربر در دیتابیس
        register_user(telegram_id=user.id, username=user.username)
        
        # ۲. بررسی سیستم دعوت (ریفرال) به روش ضدگلوله
        command_parts = message.text.split()
        if len(command_parts) > 1:
            payload = command_parts[1]
            
            if payload.startswith("ref_"):
                try:
                    inviter_id = int(payload.split("_")[1])
                    
                    # جلوگیری از کلیک کاربر روی لینک خودش
                    if inviter_id != user.id:
                        with SessionLocal() as session:
                            current_user = session.query(User).filter(User.telegram_id == user.id).first()
                            
                            # شرط طلایی: اگر referred_by خالی باشد یعنی با لینک دعوت جدید آمده
                            if current_user and current_user.referred_by is None:
                                
                                # قفل کردن این کاربر تا دیگر نتواند روی لینک کس دیگری کلیک کند
                                current_user.referred_by = inviter_id
                                session.commit()
                                
                                # واریز ۳ شارژ اضطراری به حساب دعوت‌کننده
                                add_referral_bonus(inviter_id, bonus_amount=3)
                                
                                # ارسال پیام تبریک به دعوت‌کننده
                                try:
                                    bot.send_message(
                                        inviter_id, 
                                        "🎉 <b>تبریک!</b>\n\n"
                                        "یک کاربر جدید با لینک شما وارد صدایار شد.\n"
                                        "🎁 <b>۳ پردازش رایگان (شارژ اضطراری)</b> به کیف پول شما اضافه شد!",
                                        parse_mode="HTML"
                                    )
                                except Exception as e:
                                    # اگر شخصِ دعوت‌کننده ربات را بلاک کرده باشد، برنامه کرش نمی‌کند
                                    pass
                except Exception as e:
                    print(f"Error in referral processing: {e}")

        # ۳. ارسال پیام خوش‌آمدگویی و کیبورد اصلی (دقیقاً طبق ساختار خودت)
        bot.reply_to(message, WELCOME_MESSAGE, reply_markup=get_main_menu())