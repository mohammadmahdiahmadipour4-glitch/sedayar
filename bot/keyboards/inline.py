# bot/keyboards/inline.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
def get_smart_edit_keyboard() -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard with a 'Smart Edit' button.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        # callback_data شناسه‌ای است که به ما می‌فهماند کاربر کدام دکمه را زده است
        InlineKeyboardButton(text="✨ ویراستار هوشمند", callback_data="smart_edit")
    )
    return keyboard


def get_video_choice_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🎧 دریافت فایل صوتی", callback_data="vid_audio"),
        InlineKeyboardButton("📝 تبدیل به متن", callback_data="vid_text")
    )
    return markup


def get_transcribe_voice_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📝 تبدیل به متن", callback_data="transcribe_sent_voice")
    )
    return markup

def premium_upgrade_keyboard():
    markup = InlineKeyboardMarkup()
    
    btn = InlineKeyboardButton("💎 خرید اشتراک ویژه", callback_data="buy_premium" , style="Primary")
    markup.add(btn)
    return markup

def lang(prefix) : 
    markup = InlineKeyboardMarkup(row_width=2) 
    fa = InlineKeyboardButton(text="فارسی" , callback_data=f"{prefix}_fa" , style="success")
    en = InlineKeyboardButton(text= "English" , callback_data=f"{prefix}_en" , style="danger")
    auto = InlineKeyboardButton(text="تشخیص خودکار"  , callback_data=f"{prefix}_Auto_detector" , style="primary")
    markup.add(fa , en , auto) 
    return markup