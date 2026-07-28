# bot/handlers/text_to_voice.py
import os
from telebot import TeleBot
from bot.messages import TEXT_TO_SPEECH
from services.google_tts import text_to_speech
from bot.messages import TEXT_WATERMARK , CAPTION_WATERMARK
def register_tts_handlers(bot: TeleBot):
    
    # ۱. وقتی کاربر روی دکمه کلیک کرد
    @bot.message_handler(func=lambda message: message.text == TEXT_TO_SPEECH)
    def ask_for_text(message):
        msg = bot.reply_to(message, "✍️ لطفاً متنی که می‌خواهید به صوت تبدیل شود را بفرستید:")
        # منتظر ماندن برای پیام بعدی کاربر
        bot.register_next_step_handler(msg, process_text_to_voice)

    # ۲. پردازش متن دریافتی و تبدیل به ویس
    def process_text_to_voice(message):
        if not message.text:
            bot.reply_to(message, "❌ لطفاً فقط متن ارسال کنید.")
            return
            
        text_content = message.text
        processing_msg = bot.reply_to(message, "⏳ در حال تولید فایل صوتی...")
        
        output_path = "tts_output.mp3"
        try:
            # تولید فایل صوتی با گوگل
            result_file = text_to_speech(text_content, output_path)
            
            if result_file and os.path.exists(result_file):
                with open(result_file, "rb") as audio:
                    bot.send_voice(message.chat.id, audio, caption="🎧 فایل صوتی شما آماده است.\n" +CAPTION_WATERMARK )
                bot.delete_message(message.chat.id, processing_msg.message_id)
            else:
                bot.edit_message_text("❌ خطا در تولید صوت.", message.chat.id, processing_msg.message_id)
                
        except Exception as e:
            print(f"TTS Handler Error: {e}")
            bot.edit_message_text("❌ خطایی در پردازش رخ داد.", message.chat.id, processing_msg.message_id)
            
        finally:
            # پاکسازی فایل موقت از روی سرور
            if os.path.exists(output_path):
                os.remove(output_path)