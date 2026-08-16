import os
from telebot import TeleBot
from bot.messages import VIDEO_TO_TEXT, CAPTION_WATERMARK, TEXT_WATERMARK
from services.telegram_files import download_telegram_file, delete_local_file
from services.video_service import extract_audio_from_video
from services.deepgram_service import transcribe_audio
from bot.keyboards.inline import (
    get_video_choice_keyboard, 
    get_smart_edit_keyboard, 
    get_transcribe_voice_keyboard,
    lang
)
from bot.utils import send_long_message
from bot.decorators import require_quota

# دیکشنری‌ها برای مدیریت دیتای موقتِ هر کاربر به صورت کاملاً مجزا
user_temp_audios = {}
user_selected_langs = {} 

def register_video_handlers(bot: TeleBot):
    
    @bot.message_handler(func=lambda message: message.text == VIDEO_TO_TEXT)
    def ask_for_lang(message):
        bot.send_message(
            message.chat.id, 
            "لطفا زبان ویدیو خود را انتخاب کنید ! \n در تشخیص خودکار ممکن است دقت پایین تر باشد!", 
            reply_markup=lang("vlang")
        )

    # تغییر به callback_query_handler برای دریافت دیتای دکمه‌های شیشه‌ای
    @bot.callback_query_handler(func=lambda call: call.data.startswith('vlang_'))
    def lang_selector(call): 
        chat_id = call.message.chat.id
        actual_lang = call.data.replace('vlang_', '')
        # ذخیره زبان اختصاصی کاربر در دیکشنری موقت
        user_selected_langs[chat_id] = actual_lang 
        
        bot.answer_callback_query(call.id)
        
        # ویرایش پیام قبلی و حذف کیبورد زبان
        bot.edit_message_text(
            "🎬 لطفاً ویدیو یا فایل ویدیویی خود را بفرستید:",
            chat_id=chat_id,
            message_id=call.message.message_id
        )
        bot.register_next_step_handler(call.message, process_video_message)

    @require_quota(bot)
    def process_video_message(message):
        file_path = None
        try:
            if message.content_type == 'document':
                if not message.document.mime_type or 'video' not in message.document.mime_type:
                    bot.reply_to(message, "❌ لطفاً یک فایل ویدیویی معتبر ارسال کنید.")
                    return
                file_id = message.document.file_id
            elif message.content_type == 'video':
                file_id = message.video.file_id
            else:
                bot.reply_to(message, "❌ لطفاً فقط ویدیو ارسال کنید.")
                return
                
            processing_msg = bot.reply_to(message, "⏳ در حال دریافت ویدیو...")
            
            file_path = download_telegram_file(bot, file_id)
            if not file_path:
                bot.edit_message_text("❌ خطا در دانلود فایل.", message.chat.id, processing_msg.message_id)
                return
                
            bot.edit_message_text("⏳ در حال استخراج صوت از ویدیو...", message.chat.id, processing_msg.message_id)
            
            audio_path = f"audio_{message.chat.id}.mp3"
            extracted_file = extract_audio_from_video(file_path, audio_path)
            
            if not extracted_file:
                bot.edit_message_text("❌ خطا در استخراج صوت.", message.chat.id, processing_msg.message_id)
                return
                
            user_temp_audios[message.chat.id] = audio_path
            
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=processing_msg.message_id,
                text="✅ ویدیو دریافت شد. لطفاً انتخاب کنید چه کاری انجام دهم:",
                reply_markup=get_video_choice_keyboard()
            )
            
        except Exception as e:
            print(f"Video Error: {e}")
            bot.reply_to(message, "❌ خطا در پردازش ویدیو.")
        finally:
            if file_path and os.path.exists(file_path):
                delete_local_file(file_path)

    @bot.callback_query_handler(func=lambda call: call.data in ["vid_audio", "vid_text"])
    def handle_video_choice(call):
        chat_id = call.message.chat.id
        audio_path = user_temp_audios.get(chat_id)
        
        # فراخوانی زبان کاربر. اگر پیدا نشد دیفالت روی اتوماتیک باشه
        user_lang = user_selected_langs.get(chat_id, "Auto_detector") 
        
        try:
            bot.answer_callback_query(call.id)
            
            if not audio_path or not os.path.exists(audio_path):
                bot.edit_message_text(
                    text="❌ فایل منقضی شده است. لطفاً دوباره ویدیو را ارسال کنید.",
                    chat_id=chat_id,
                    message_id=call.message.message_id
                )
                return
                
            if call.data == "vid_audio":
                bot.edit_message_text(
                    text="⏳ در حال آماده‌سازی و ارسال فایل صوتی...",
                    chat_id=chat_id,
                    message_id=call.message.message_id
                )
                bot.send_chat_action(chat_id, 'upload_audio')
                
                with open(audio_path, "rb") as audio:
                    bot.send_voice(
                        chat_id, 
                        audio, 
                        caption="🎧 فایل صوتی استخراج شده از ویدیو\n" + CAPTION_WATERMARK, 
                        timeout=120,
                        reply_markup=get_transcribe_voice_keyboard()
                    )
                    
                bot.delete_message(chat_id, call.message.message_id)
                
            elif call.data == "vid_text":
                bot.edit_message_text(
                    text="⏳ در حال تبدیل صوت به متن (ممکن است کمی زمان‌بر باشد)...",
                    chat_id=chat_id,
                    message_id=call.message.message_id
                )
                bot.send_chat_action(chat_id, 'typing')
                
                transcription = transcribe_audio(audio_path, user_lang)
                
                bot.delete_message(chat_id, call.message.message_id)
                full_text = f"📝 **متن استخراج شده از ویدیو:**\n\n{transcription}"
                send_long_message(bot, chat_id, full_text, reply_markup=get_smart_edit_keyboard())
                
        except Exception as e:
            print(f"Callback Video Error: {e}")
            bot.send_message(chat_id, "❌ خطایی در پردازش درخواست شما رخ داد.")
            
        finally:
            if chat_id in user_temp_audios:
                del user_temp_audios[chat_id]
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
                
            # پاک کردن زبان از مموری به محض اتمام پردازش 
            if chat_id in user_selected_langs:
                del user_selected_langs[chat_id]

    @bot.callback_query_handler(func=lambda call: call.data == "transcribe_sent_voice")
    @require_quota(bot)
    def handle_transcribe_sent_voice(call):
        chat_id = call.message.chat.id
        file_path = None
        user_lang = user_selected_langs.get(chat_id, "Auto_detector")
        
        try:
            bot.answer_callback_query(call.id, "در حال آماده‌سازی...")
            
            file_id = None
            if call.message.voice:
                file_id = call.message.voice.file_id
            elif call.message.audio:
                file_id = call.message.audio.file_id
                
            if not file_id:
                bot.send_message(chat_id, "❌ فایل صوتی یافت نشد.")
                return
                
            processing_msg = bot.send_message(
                chat_id,
                "⏳ در حال دانلود و تبدیل صوت به متن..."
            )
            bot.send_chat_action(chat_id, 'typing')
            
            file_path = download_telegram_file(bot, file_id)
            if not file_path:
                bot.delete_message(chat_id, processing_msg.message_id)
                bot.send_message(chat_id, "❌ خطا در دانلود فایل.")
                return
                
            transcription = transcribe_audio(file_path, user_lang)
            
            bot.delete_message(chat_id, processing_msg.message_id)
            full_text = f"📝 **متن استخراج شده:**\n\n{transcription}" + TEXT_WATERMARK
            send_long_message(bot, chat_id, full_text, reply_markup=get_smart_edit_keyboard())
            
        except Exception as e:
            print(f"Transcribe Sent Voice Error: {e}")
            bot.send_message(chat_id, "❌ خطایی در پردازش رخ داد.")
        finally:
            if file_path and os.path.exists(file_path):
                delete_local_file(file_path)