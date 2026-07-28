from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bot.messages import (
    VOICE_TO_TEXT , TEXT_TO_SPEECH , VIDEO_TO_TEXT , PROFILE , HELP , SUPPORT , REFRAL_MESSAGE
)

def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    keyboard.add(
        KeyboardButton(VOICE_TO_TEXT),
        KeyboardButton(TEXT_TO_SPEECH)
    )
    
    keyboard.add(
        KeyboardButton(VIDEO_TO_TEXT)
    )
    
    keyboard.add(
        KeyboardButton(PROFILE),
        KeyboardButton(HELP)
    )
    keyboard.add(
        KeyboardButton(SUPPORT) , 
        KeyboardButton(REFRAL_MESSAGE)
    )
   
    
    return keyboard