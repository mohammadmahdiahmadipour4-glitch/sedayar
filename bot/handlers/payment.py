from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.zarinpal import send_request
# آدرس سرور شما (برای تست روی کامپیوتر شخصی، از Ngrok استفاده کنید)
SERVER_URL = "https://sedayarai.ir"

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
        btn_1 = InlineKeyboardButton("🥉 اشتراک ۱ ماهه - ۱۵۰,۰۰۰ تومان", url=f"{SERVER_URL}/pay/{user_id}/1")
        btn_3 = InlineKeyboardButton("🥈 اشتراک ۳ ماهه - ۳۹۰,۰۰۰ تومان", url=f"{SERVER_URL}/pay/{user_id}/3")
        btn_6 = InlineKeyboardButton("🥇 اشتراک ۶ ماهه - ۷۰۰,۰۰۰ تومان", url=f"{SERVER_URL}/pay/{user_id}/6")
        btn_back = InlineKeyboardButton("🔙 بازگشت به پروفایل", callback_data="back_to_profile")
        
        markup.add(btn_1, btn_3, btn_6, btn_back)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="Markdown",
            reply_markup=markup
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('pay_group_'))
    def process_group_payment(call):
        # ۱. ابتدا به تلگرام می‌گوییم که درخواست دریافت شد تا آیکون ساعت شنی روی دکمه ناپدید شود
        bot.answer_callback_query(call.id, "⏳ در حال اتصال به درگاه بانکی...")
        
        try:
            # ۲. استخراج آیدی گروه از کال‌بک دیتا
            target_group_id = int(call.data.split('pay_group_')[1])
            user_id = call.from_user.id
            
            # ۳. تنظیمات فاکتور (مبلغ به تومان پاس داده می‌شود چون در تابع زرین‌پال ضربدر ۱۰ می‌شود)
            amount_toman = 50000 
            description = f"خرید اشتراک یک‌ماهه صدایار برای گروه {target_group_id}"
            
            # نکته معماری: آیدی گروه را به جای plan_id پاس می‌دهیم 
            # تا وقتی کاربر از بانک برگشت، سرور بفهمد کدام گروه باید فعال شود!
            plan_identifier = f"group_{target_group_id}"
            
            # ۴. ارسال درخواست به زرین‌پال
            status, result = send_request(
                amount=amount_toman, 
                description=description, 
                user_id=user_id, 
                plan_id=plan_identifier
            )
            
            if status:
                # اگر موفق بود، result همان لینک درگاه بانکی است
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("🌐 ورود به درگاه پرداخت", url=result))
                
                # پیام قبلی (فاکتور) را ویرایش می‌کنیم و لینک پرداخت را زیرش می‌گذاریم
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=(
                        "✅ **فاکتور پرداخت ایجاد شد.**\n\n"
                        f"💳 **مبلغ:** ۵۰,۰۰۰ تومان\n\n"
                        "⚠️ این لینک فقط برای شما و به مدت محدود معتبر است.\n"
                        "👇 برای انتقال به صفحه امن بانک روی دکمه زیر کلیک کنید:"
                    ),
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            else:
                # اگر زرین‌پال ارور داد (مثلاً پینگ‌جی قطع بود یا آی‌پی ایران نبود)
                bot.send_message(call.message.chat.id, f"❌ خطا در اتصال به درگاه زرین‌پال:\n`{result}`", parse_mode="Markdown")
                
        except Exception as e:
            bot.send_message(call.message.chat.id, "❌ متأسفانه خطای سیستمی رخ داد. لطفاً به پشتیبانی اطلاع دهید.")
            print(f"Payment Generation Error: {e}")