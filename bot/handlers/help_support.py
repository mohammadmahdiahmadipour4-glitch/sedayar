from telebot import TeleBot
from telebot.types import Message
from bot.messages import HELP
def register_help_support_handlers(bot: TeleBot):
    
    # هندلر دکمه راهنما
    @bot.message_handler(func=lambda message: message.text == HELP)
    def send_help(message: Message):
        help_text = (
            "📖 **راهنمای استفاده از صدایار**\n\n"
            "کار با ربات بسیار ساده است:\n"
            "🎙 ویس بفرستید\n"
            "🎵 فایل صوتی فوروارد کنید\n\n"
            "⚡️ ما متن را در سریع‌ترین زمان برایتان ارسال می‌کنیم.\n\n"
            "📊 **سهمیه‌ها:**\n"
            "▫️ عادی: 7 بار در روز\n"
            "▫️ ویژه: 30 بار در روز"
        )
        bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

    # هندلر دکمه پشتیبانی
    @bot.message_handler(func=lambda message: message.text == '👨‍💻 پشتیبانی')
    def send_support(message: Message):
        support_text = (
            "<b>👨‍💻ارتباط با پشتیبانی</b>\n\n"
            "در صورت بروز مشکل در خرید اشتراک یا خطاهای ربات، به آیدی زیر پیام دهید:\n\n"
            "🆔 @Mohammad_Ahp" 
        )
        bot.send_message(message.chat.id, support_text, parse_mode="HTML")