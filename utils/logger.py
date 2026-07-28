import logging
from logging.handlers import RotatingFileHandler
from telebot import TeleBot
from datetime import datetime

# ==========================================
# ۱. تنظیمات فایل لاگ سرور (لایه‌ی خاموش)
# ==========================================
# فرمت نمایش: زمان - سطح خطر - پیام
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# سیستم چرخشی: هر فایل نهایتاً ۵ مگابایت، حداکثر ۳ بک‌آپ (جلوگیری از پر شدن هارد سرور)
file_handler = RotatingFileHandler(
    'sedayar_bot.log', maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8'
)
file_handler.setFormatter(log_formatter)

logger = logging.getLogger('SedayarLogger')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# ==========================================
# ۲. تنظیمات کانال تلگرام ادمین (لایه‌ی بیدار)
# ==========================================
# آیدی کانال پرایوت خودت رو اینجا بذار (حتماً با 100- شروع بشه)
ADMIN_CHANNEL_ID = -1004392152334 

def log_event(bot: TeleBot, event_type: str, message: str, send_to_telegram: bool = False):
    """
    تابع جامع لاگ‌گیری.
    اگر send_to_telegram روی True باشد، علاوه بر فایل، به کانال ادمین هم ارسال می‌شود.
    """
    
    # ۱. ثبت در فایل سرور
    if event_type == 'error':
        logger.error(message)
    elif event_type == 'warning':
        logger.warning(message)
    else:
        logger.info(message)
        
    # ۲. ارسال به کانال تلگرام (در صورت نیاز)
    if send_to_telegram:
        # انتخاب ایموجی و هشتگ بر اساس نوع رویداد
        emojis = {
            'info': ('✅', '#اطلاعات'),
            'warning': ('⚠️', '#هشدار'),
            'error': ('🚨', '#خطا'),
            'payment': ('💳', '#فروش'),
            'group': ('🏢', '#گروه_جدید')
        }
        
        icon, hashtag = emojis.get(event_type, ('📝', '#لاگ'))
        
        telegram_message = (
            f"{icon} {hashtag}\n"
            "➖➖➖➖➖➖➖➖\n"
            f"{message}\n\n"
            f"⏱ <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>"
        )
        try:
            bot.send_message(ADMIN_CHANNEL_ID, telegram_message, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Failed to send log to Telegram channel: {e}")