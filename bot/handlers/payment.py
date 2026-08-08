from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.zarinpal import send_request
import os
from db.base import SessionLocal
from db.models.user import User
from db.models.group import Group
from datetime import datetime, timedelta
# آدرس سرور شما (برای تست روی کامپیوتر شخصی، از Ngrok استفاده کنید)
SERVER_URL = "https://sedayarai.ir"
ADMIN_ID = os.getenv("ADMIN_ID") 
def register_payment_handlers(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data == 'buy_premium')
    def show_pricing_plans(call: CallbackQuery):
        bot.answer_callback_query(call.id)
        user_id = call.from_user.id
        
        text = (
            "🚀 **ارتقا به حساب ویژه (Premium)**\n\n"
            "✨ **مزایای حساب ویژه:**\n"
            "▫️ سقف مصرف ۳۰ پردازش در روز\n"
            "▫️ اولویت بالا در صف پردازش فایل‌ها\n"
            "▫️ بدون قطعی و تبلیغات\n\n"
            "👇 **لطفاً یکی از بسته‌های زیر را انتخاب کنید:**"
        )
        
        markup = InlineKeyboardMarkup(row_width=1)
        
        # شناسه پلن‌ها را در انتهای لینک می‌فرستیم (1 یا 3 یا 6)
        btn_1 = InlineKeyboardButton("🥉 اشتراک ۱ ماهه - ۱۵۰,۰۰۰ تومان", callback_data="pre_1")
        btn_3 = InlineKeyboardButton("🥈 اشتراک ۳ ماهه - ۳۹۰,۰۰۰ تومان", callback_data="pre_3")
        btn_6 = InlineKeyboardButton("🥇 اشتراک ۶ ماهه - ۷۰۰,۰۰۰ تومان", callback_data="pre_6")
        btn_back = InlineKeyboardButton("🔙 بازگشت به پروفایل", callback_data="back_to_profile")
        
        markup.add(btn_1, btn_3, btn_6, btn_back)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="Markdown",
            reply_markup=markup
        )


    @bot.callback_query_handler(func=lambda call: call.data.startswith('pre_'))
    def process_payment(call: CallbackQuery):
        bot.answer_callback_query(call.id )
        plan_info = call.data.replace('pre_', '')
        msg = bot.send_message(
        call.message.chat.id,
        "💳 **شماره کارت جهت واریز:**\n`6219 8614 2061 7689`\nبه نام: محمد مهدی احمدی پور\n\n"
        "📸 لطفاً مبلغ را واریز کرده و تصویر رسید را همینجا ارسال کنید:",
        parse_mode="Markdown"
    )
        bot.register_next_step_handler(msg , process_receipt, plan_info , call.from_user.id)

    def process_receipt(message, plan_info, user_id):
        if not message.photo and not message.document: 
            bot.send_message(message.chat.id, "❌ لطفاً فقط تصویر رسید را ارسال کنید. عملیات لغو شد")
            return
        bot.send_message(message.chat.id ,"✅ رسید شما دریافت شد و پس از تایید ادمین، اشتراک فعال می‌شود." )

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ تایید", callback_data=f"appr_{user_id}_{plan_info}") ,
            InlineKeyboardButton("❌ رد", callback_data=f"reject_{user_id}")
        )

        caption_text = f"👤 شناسه کاربر: `{user_id}`\n📦 پلن درخواستی: `{plan_info}`\n\nلطفاً رسید پرداختی را بررسی کنید:"

        if message.photo: 
            file_id = message.photo[-1].file_id
            bot.send_photo(chat_id = ADMIN_ID , photo = file_id , caption = caption_text , parse_mode="Markdown" , reply_markup=markup)
        elif message.document:
            file_id = message.document.file_id
            bot.send_document(chat_id = ADMIN_ID , data = file_id , caption = caption_text , parse_mode="Markdown" , reply_markup=markup)



    @bot.callback_query_handler(func=lambda call: call.data.startswith('appr_'))
    def admin_approval(call: CallbackQuery):
        bot.answer_callback_query(call.id, "در حال بررسی و فعال‌سازی...")
        
        # تجزیه دیتای برگشتی
        # حالت شخصی: appr_123456_3  -> parts = ['appr', '123456', '3']
        # حالت گروه: appr_123456_group_-10012_1 -> parts = ['appr', '123456', 'group', '-10012', '1']
        parts = call.data.split('_')
        target_user_id = int(parts[1])
        
        with SessionLocal() as session:
            now = datetime.now()
            
            # --- سناریوی گروه ---
            if 'group' in call.data:
                target_group_id = int(parts[3])
                months = int(parts[4])
                plan_days = months * 30 # محاسبه تعداد روزها بدون نیاز به متغیر PLANS
                
                group = session.query(Group).filter(Group.chat_id == target_group_id).first()
                if group:
                    group.is_premium = True
                    if group.premium_until and group.premium_until > now:
                        group.premium_until += timedelta(days=plan_days)
                    else:
                        group.premium_until = now + timedelta(days=plan_days)
                    session.commit()
                    
                    bot.send_message(
                        target_user_id, 
                        f"🎉 **پرداخت شما تایید شد!**\n\nاشتراک ویژه برای گروه `{target_group_id}` به مدت {months} ماه فعال گردید.", 
                        parse_mode="Markdown"
                    )
                else:
                    bot.send_message(call.from_user.id, f"❌ خطا: گروه {target_group_id} در دیتابیس یافت نشد.")
                    return
                    
            # --- سناریوی شخصی ---
            else:
                months = int(parts[2])
                plan_days = months * 30 # محاسبه تعداد روزها
                
                user = session.query(User).filter(User.telegram_id == target_user_id).first()
                if user:
                    user.is_premium = True
                    if user.premium_until and user.premium_until > now:
                        user.premium_until += timedelta(days=plan_days)
                    else:
                        user.premium_until = now + timedelta(days=plan_days)
                    session.commit()
                    
                    bot.send_message(
                        target_user_id, 
                        f"🎉 **رسید شما تایید شد!**\n\nاشتراک ویژه حساب کاربری شما به مدت {months} ماه فعال گردید. ممنون از حمایت شما ❤️", 
                        parse_mode="Markdown"
                    )
                else:
                    bot.send_message(call.from_user.id, "❌ خطا: کاربر در دیتابیس یافت نشد.")
                    return
                    
        # تغییر کپشن پیام ادمین و حذف دکمه‌های شیشه‌ای برای جلوگیری از کلیک مجدد
        bot.edit_message_caption(
            caption=f"✅ **تایید شد.**\n\nاشتراک کاربر `{target_user_id}` فعال گردید.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=None # این دستور کیبورد شیشه‌ای را حذف می‌کند
        )


    # ==========================================
    # هندلر رد رسید توسط ادمین
    # ==========================================
    @bot.callback_query_handler(func=lambda call: call.data.startswith('reject_'))
    def admin_rejection(call: CallbackQuery):
        bot.answer_callback_query(call.id, "رسید رد شد.")
        
        # تجزیه دیتا (ساختار: reject_123456)
        parts = call.data.split('_')
        target_user_id = int(parts[1])
        
        # ارسال پیام به کاربر مبنی بر رد شدن رسید
        bot.send_message(
            target_user_id, 
            "❌ **رسید ارسالی شما تایید نشد.**\n\n"
            "اطلاعات پرداختی شما نامعتبر بوده یا مبلغ به درستی واریز نشده است. "
            "چنانچه مبلغی از حساب شما کسر شده اما اشتراکی دریافت نکرده‌اید، با پشتیبانی در ارتباط باشید.",
            parse_mode="Markdown"
        )
        
        # تغییر کپشن پیام ادمین و حذف دکمه‌های شیشه‌ای
        bot.edit_message_caption(
            caption=f"❌ **رد شد.**\n\nدرخواست کاربر `{target_user_id}` لغو گردید.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=None
        )

    


    # @bot.callback_query_handler(func=lambda call: call.data.startswith('pay_group_'))
    # def process_group_payment(call):
    #     # ۱. ابتدا به تلگرام می‌گوییم که درخواست دریافت شد تا آیکون ساعت شنی روی دکمه ناپدید شود
    #     bot.answer_callback_query(call.id, "⏳ در حال اتصال به درگاه بانکی...")
        
    #     try:
    #         # ۲. استخراج آیدی گروه از کال‌بک دیتا
    #         target_group_id = int(call.data.split('pay_group_')[1])
    #         user_id = call.from_user.id
            
    #         # ۳. تنظیمات فاکتور (مبلغ به تومان پاس داده می‌شود چون در تابع زرین‌پال ضربدر ۱۰ می‌شود)
    #         amount_toman = 50000 
    #         description = f"خرید اشتراک یک‌ماهه صدایار برای گروه {target_group_id}"
            
    #         # نکته معماری: آیدی گروه را به جای plan_id پاس می‌دهیم 
    #         # تا وقتی کاربر از بانک برگشت، سرور بفهمد کدام گروه باید فعال شود!
    #         plan_identifier = f"group_{target_group_id}"
            
    #         # ۴. ارسال درخواست به زرین‌پال
    #         status, result = send_request(
    #             amount=amount_toman, 
    #             description=description, 
    #             user_id=user_id, 
    #             plan_id=plan_identifier
    #         )
            
    #         if status:
    #             # اگر موفق بود، result همان لینک درگاه بانکی است
    #             markup = InlineKeyboardMarkup()
    #             markup.add(InlineKeyboardButton("🌐 ورود به درگاه پرداخت", url=result))
                
    #             # پیام قبلی (فاکتور) را ویرایش می‌کنیم و لینک پرداخت را زیرش می‌گذاریم
    #             bot.edit_message_text(
    #                 chat_id=call.message.chat.id,
    #                 message_id=call.message.message_id,
    #                 text=(
    #                     "✅ **فاکتور پرداخت ایجاد شد.**\n\n"
    #                     f"💳 **مبلغ:** ۵۰,۰۰۰ تومان\n\n"
    #                     "⚠️ این لینک فقط برای شما و به مدت محدود معتبر است.\n"
    #                     "👇 برای انتقال به صفحه امن بانک روی دکمه زیر کلیک کنید:"
    #                 ),
    #                 parse_mode="Markdown",
    #                 reply_markup=markup
    #             )
    #         else:
    #             # اگر زرین‌پال ارور داد (مثلاً پینگ‌جی قطع بود یا آی‌پی ایران نبود)
    #             bot.send_message(call.message.chat.id, f"❌ خطا در اتصال به درگاه زرین‌پال:\n`{result}`", parse_mode="Markdown")
                
    #     except Exception as e:
    #         bot.send_message(call.message.chat.id, "❌ متأسفانه خطای سیستمی رخ داد. لطفاً به پشتیبانی اطلاع دهید.")
    #         print(f"Payment Generation Error: {e}")