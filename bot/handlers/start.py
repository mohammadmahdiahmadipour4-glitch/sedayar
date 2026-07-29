from telebot import TeleBot

from bot.messages import WELCOME_MESSAGE
from bot.keyboards.main_menu import get_main_menu
# توابع جدید دیتابیس را ایمپورت می‌کنیم
from db.repositories.user import register_user, add_referral_bonus
from db.base import SessionLocal
from db.models.user import User
from db.models.group import Group
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup
SERVER_URL = "https://sedayarai.ir"
def register_start_handler(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def start(message):
        user = message.from_user
        chat_id = message.chat.id
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

            elif payload.startswith("groupsub_"):
                try:
                    # جدا کردن آیدی گروه از متن (مثلاً -100123456)
                    user_id = message.from_user.id
                    target_group_id = int(payload.split("groupsub_")[1])
                    group_name = "نامشخص"
                    with SessionLocal() as session:
                        target_group = session.query(Group).filter(Group.chat_id == target_group_id).first()
                        if target_group and target_group.title:
                            group_name = target_group.title
                    # ساخت کیبورد پرداخت برای گروه
                    markup = InlineKeyboardMarkup()
                    
                    # در اینجا لینک درگاه پرداخت مستقیم یا ارجاع به کارت‌به‌کارت قرار می‌گیرد
                    # فعلاً یک دکمه شیشه‌ای (Callback) می‌سازیم تا بعداً هندلش کنیم
                    markup.add(InlineKeyboardButton("اشتراک 1 ماهه گروهی💎 : 399,000  تومان💳", url=f"{SERVER_URL}/pay/{user_id}/_group_1_{target_group_id}"))
                    markup.add(InlineKeyboardButton("اشتراک 3 ماهه گروهی💎 : 990,000  تومان💳", url=f"{SERVER_URL}/pay/{user_id}/_group_3_{target_group_id}"))
                    markup.add(InlineKeyboardButton("اشتراک 6 ماهه گروهی💎 : 1,790,000  تومان💳", url=f"{SERVER_URL}/pay/{user_id}/_group_6_{target_group_id}"))
                    invoice_text = (
                        "🏢 **تمدید اشتراک گروه**\n\n"
                        f"شما در حال خرید اشتراک ویژه (تبدیل خودکار و نامحدود ویس‌ها) برای گروه **«{group_name}»** هستید.\n\n"
                        "⏱ **مدت زمان:** یک ماه\n"
                        "💰 **مبلغ:** 399,000 تومان\n\n"
                        "⏱ **مدت زمان:** سه ماه\n"
                        "💰 **مبلغ:** 990,000 تومان\n\n"
                        "⏱ **مدت زمان:** شیش ماه\n"
                        "💰 **مبلغ:** 1,790,000 تومان\n\n"
                        "👇 برای پرداخت روی دکمه زیر کلیک کنید:"
                    )
                    
                    bot.send_message(chat_id, invoice_text, parse_mode="Markdown", reply_markup=markup)
                    return 
                    
                except ValueError:
                    bot.send_message(chat_id, "❌ لینک نامعتبر است.")
                    return

        bot.reply_to(message, WELCOME_MESSAGE, reply_markup=get_main_menu())