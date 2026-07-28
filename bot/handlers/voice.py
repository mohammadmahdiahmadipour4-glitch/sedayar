import os
from telebot import TeleBot
from bot.messages import VOICE_TO_TEXT
from services.telegram_files import download_telegram_file, delete_local_file
from services.deepgram_service import transcribe_audio
from services.text_processor import improve_text
from bot.keyboards.inline import get_smart_edit_keyboard
from bot.utils import send_long_message
from bot.decorators import require_quota
from bot.messages import TEXT_WATERMARK , CAPTION_WATERMARK
def register_voice_handlers(bot: TeleBot):
    
    @bot.message_handler(func=lambda message: message.text == VOICE_TO_TEXT and message.chat.type == 'private' )
    def ask_for_voice(message):
        msg = bot.reply_to(message, "🎤 لطفاً فایل صوتی (Voice) خود را ارسال کنید:")
        bot.register_next_step_handler(msg, handle_voice_message)

    @bot.message_handler(content_types=['voice', 'audio'] , func=lambda m: m.chat.type == 'private')
    @require_quota(bot)
    def handle_voice_message(message):
        processing_msg = bot.reply_to(message, "⏳ در حال دانلود فایل از سرور تلگرام...")
        file_path = None
        
        try:
            if message.content_type == 'voice':
                file_id = message.voice.file_id
            else:
                file_id = message.audio.file_id
                
            file_path = download_telegram_file(bot, file_id)
            if not file_path:
                bot.delete_message(message.chat.id, processing_msg.message_id)
                bot.send_message(message.chat.id, "❌ خطا در دانلود فایل.")
                return
            
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=processing_msg.message_id,
                text="✅ فایل دانلود شد.\n🤖 در حال پردازش صوت توسط هوش مصنوعی ..."
            )
            
            transcription = transcribe_audio(file_path)
            
            bot.delete_message(message.chat.id, processing_msg.message_id)
            
            full_text = f"📝 **متن خام ویس شما:**\n\n{transcription}" + TEXT_WATERMARK
            send_long_message(bot, message.chat.id, full_text, reply_markup=get_smart_edit_keyboard())
            
        except Exception as e:
            bot.delete_message(message.chat.id, processing_msg.message_id)
            bot.send_message(message.chat.id, "❌ متأسفانه در پردازش فایل صوتی مشکلی پیش آمد.")
            print(f"Error processing voice with Deepgram: {e}")
            
        finally:
            if file_path and os.path.exists(file_path):
                delete_local_file(file_path)

    @bot.callback_query_handler(func=lambda call: call.data == "smart_edit")
    @require_quota(bot)
    def process_smart_edit(call):
        bot.answer_callback_query(call.id, "در حال ویراستاری متن... ⏳")
        
        original_text = call.message.text
        if not original_text:
            return
            
        raw_content = original_text.replace("📝 متن خام ویس شما:", "").replace("📝 **متن خام ویس شما:**", "").strip()
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        processing_msg = bot.send_message(
            call.message.chat.id,
            "✨ *در حال اعمال تغییرات ویراستار هوشمند...*",
            parse_mode="Markdown"
        )
        bot.send_chat_action(call.message.chat.id, 'typing')
        
        try:
            improved_text = improve_text(raw_content)
            
            bot.delete_message(call.message.chat.id, processing_msg.message_id)
            
            final_text = f"📝 **متن خام:**\n{raw_content}\n\n✨ **متن ویرایش شده:**\n{improved_text}" 
            send_long_message(bot, call.message.chat.id, final_text)
            
        except Exception as e:
            bot.delete_message(call.message.chat.id, processing_msg.message_id)
            error_text = f"{original_text}\n\n❌ *خطا در اتصال به ویراستار.*"
            send_long_message(bot, call.message.chat.id, error_text, reply_markup=get_smart_edit_keyboard())
            print(f"Error in smart edit: {e}")