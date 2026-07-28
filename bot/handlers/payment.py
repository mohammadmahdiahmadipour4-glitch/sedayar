from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# آدرس سرور شما (برای تست روی کامپیوتر شخصی، از Ngrok استفاده کنید)
SERVER_URL = "https://vyoel-5-202-36-16.run.pinggy-free.link"

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
        