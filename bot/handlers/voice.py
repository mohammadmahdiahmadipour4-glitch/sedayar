import os
from telebot import TeleBot
from bot.messages import VOICE_TO_TEXT
from services.telegram_files import download_telegram_file, delete_local_file
from services.deepgram_service import transcribe_audio
from services.text_processor import improve_text
from bot.keyboards.inline import get_smart_edit_keyboard , lang
from bot.utils import send_long_message
from bot.decorators import require_quota
from bot.messages import TEXT_WATERMARK , CAPTION_WATERMARK

# دیکشنری برای مدیریت دیتای موقتِ هر کاربر به صورت کاملاً مجزا
user_selected_langs = {} 

def register_voice_handlers(bot: TeleBot):
    
    @bot.message_handler(func=lambda message: message.text == VOICE_TO_TEXT and message.chat.type == 'private' )
    def ask_for_lang(message):
        # اصلاح: استفاده از message.chat.id به جای کل آبجکت message
        bot.send_message(
            message.chat.id, 
            "لطفا زبان فایل صوتی خود را انتخاب کنید ! \n در تشخیص خودکار ممکن است دقت پایین تر باشد!", 
            reply_markup=lang('voc') 
        )

    # اصلاح: تغییر به callback_query_handler برای پشتیبانی از کیبورد شیشه‌ای
    @bot.callback_query_handler(func=lambda call: call.data.startswith('voc_'))
    def lang_selector(call): 
        chat_id = call.message.chat.id
        
        # ذخیره زبان اختصاصی برای همین کاربر
        actual_lang = call.data.replace('voc_', '')
        user_selected_langs[chat_id] = actual_lang
        bot.answer_callback_query(call.id)
        
        # ویرایش پیام قبلی و حذف کیبورد
        bot.edit_message_text(
            "🎤 لطفاً فایل صوتی (Voice) خود را ارسال کنید:",
            chat_id=chat_id,
            message_id=call.message.message_id
        )
        
        # ثبت مرحله بعدی با پاس دادن آبجکت پیام به جای متن استرینگ
        bot.register_next_step_handler(call.message, handle_voice_message)

    @bot.message_handler(content_types=['voice', 'audio'] , func=lambda m: m.chat.type == 'private')
    @require_quota(bot)
    def handle_voice_message(message):
        chat_id = message.chat.id
        
        # استخراج زبان انتخاب‌شده توسط کاربر (اگر نبود: تشخیص خودکار)
        user_lang = user_selected_langs.get(chat_id, "Auto_detector")
        
        processing_msg = bot.reply_to(message, "⏳ در حال دانلود فایل از سرور تلگرام...")
        file_path = None
        
        try:
            if message.content_type == 'voice':
                file_id = message.voice.file_id
            else:
                file_id = message.audio.file_id
                
            file_path = download_telegram_file(bot, file_id)
            if not file_path:
                bot.delete_message(chat_id, processing_msg.message_id)
                bot.send_message(chat_id, "❌ خطا در دانلود فایل.")
                return
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_msg.message_id,
                text="✅ فایل دانلود شد.\n🤖 در حال پردازش صوت توسط هوش مصنوعی ..."
            )
            
            transcription = transcribe_audio(file_path , user_lang)
            
            bot.delete_message(chat_id, processing_msg.message_id)
            
            full_text = f"📝 **متن خام ویس شما:**\n\n{transcription}" + TEXT_WATERMARK
            send_long_message(bot, chat_id, full_text, reply_markup=get_smart_edit_keyboard())
            
        except Exception as e:
            bot.delete_message(chat_id, processing_msg.message_id)
            bot.send_message(chat_id, "❌ متأسفانه در پردازش فایل صوتی مشکلی پیش آمد.")
            print(f"Error processing voice with Deepgram: {e}")
            
        finally:
            if file_path and os.path.exists(file_path):
                delete_local_file(file_path)
            
            # پاک کردن زبان از حافظه پس از اتمام پردازش
            if chat_id in user_selected_langs:
                del user_selected_langs[chat_id]

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