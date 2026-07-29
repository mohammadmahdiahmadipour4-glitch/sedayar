from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.repositories.group import is_group_auto_active
from db.repositories.user import check_and_use_quota
from services.deepgram_service import transcribe_audio 
import os
from utils.logger import log_event
from bot.utils import send_long_message
from bot.messages import TEXT_WATERMARK
from bot.decorators import require_quota
from bot.keyboards.inline import get_smart_edit_keyboard
from db.repositories.group import check_and_mark_expiration_notification
def register_group_voice_handlers(bot: TeleBot):
    # ==========================================
    # ۱. حالت خودکار (خواندن خودکار تمام ویس‌ها)
    # ==========================================
    @bot.message_handler(content_types=['voice', 'audio', 'video_note'], func=lambda m: m.chat.type in ['group', 'supergroup'])
    def auto_group_voice_handler(message: Message):
        chat_id = message.chat.id
        if not is_group_auto_active(chat_id):
            if check_and_mark_expiration_notification(chat_id):
                
                bot_username = bot.get_me().username
                buy_url = f"https://t.me/{bot_username}?start=groupsub_{chat_id}"
                
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("خرید اشتراک ویژه برای این گروه 💎", url=buy_url))
                
                expiration_msg = (
                    "⚠️ **پایان مهلت تست رایگان گروه**\n\n"
                    "کاربران عزیز، مهلت ۳ روزه تست رایگان و تبدیل *خودکار* ویس‌ها در این گروه به پایان رسید.\n\n"
                    "💡 **آیا می‌دانستید؟**\n"
                    "شما همچنان می‌توانید با استفاده از سهمیه شخصی خودتان، ویس‌ها را به صورت دستی تبدیل کنید! (کافیست روی ویس مورد نظر ریپلای کرده و دستور `/text` را بفرستید).\n\n"
                    "👑 مدیران یا اعضای گروه می‌توانند با تهیه اشتراک ویژه، قابلیت تبدیل خودکار و بی‌نهایت را برای **تمام اعضای گروه** مجدداً فعال کنند:"
                )
                
                try:
                    bot.send_message(
                        chat_id=chat_id, 
                        text=expiration_msg, 
                        parse_mode="Markdown", 
                        reply_markup=markup
                    )
                except Exception as e:
                    print(f"Error sending expiration notice to {chat_id}: {e}")
                    
            return
        # ارسال پیام موقت برای اینکه اعضا بدانند ربات در حال کار است
        temp_msg = bot.reply_to(message, "⏳ در حال دانلود و تبدیل به متن...")
        
        file_path = None
        
        try:
            # ۱. پیدا کردن نوع فایل و استخراج شناسه
            if message.content_type == 'voice':
                file_id = message.voice.file_id
                file_ext = ".ogg"
            elif message.content_type == 'audio':
                file_id = message.audio.file_id
                file_ext = ".mp3"
            elif message.content_type == 'video_note':
                file_id = message.video_note.file_id
                file_ext = ".mp4"
            else:
                return

            # ۲. دانلود فایل از سرور تلگرام
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # ۳. ذخیره موقت فایل روی سرور
            file_path = f"temp_auto_{file_id}{file_ext}"
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            # ۴. ارسال مسیر فایل به تابع دیپ‌گرام
            text_result = transcribe_audio(file_path)
            
            # ۵. پاک کردن پیام موقت
            bot.delete_message(chat_id=chat_id, message_id=temp_msg.message_id)
            
            # ۶. نمایش نتیجه با پشتیبانی از ریپلای و متون طولانی
            send_long_message(
                bot=bot,
                chat_id=chat_id,
                text=f"🎙 **متن فایل صوتی:**\n\n{text_result}" + TEXT_WATERMARK,
                reply_to_message_id=message.message_id ,
                reply_markup=get_smart_edit_keyboard()
                )
            
        except Exception as e:
            # مدیریت خطا
            bot.edit_message_text(chat_id=chat_id, message_id=temp_msg.message_id, text="❌ خطایی در پردازش رخ داد.")
            
            owner_info = "نامشخص"
            try:
                admins = bot.get_chat_administrators(chat_id)
                for admin in admins:
                    if admin.status == 'creator':
                        owner_info = f"{admin.user.first_name} (<code>{admin.user.id}</code>)"
                        if admin.user.username:
                            owner_info += f" | @{admin.user.username}"
                        break
            except Exception:
                owner_info = "عدم دسترسی به لیست مدیران"
                
            error_details = (
                f"🚨 **خطای پردازش خودکار**\n\n"
                f"🏢 **گروه:** {message.chat.title}\n"
                f"🆔 **آیدی:** <code>{chat_id}</code>\n"
                f"👑 **مالک:** {owner_info}\n\n"
                f"⚠️ **متن خطا:**\n<code>{e}</code>"
            )
            log_event(bot, 'error', error_details, send_to_telegram=True)
            
        finally:
            # ۷. مدیریت حافظه (پاک کردن فایل موقت)
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
# ==========================================
    # ۲. حالت دستی (فقط با ارسال دستور /text)
    # ==========================================
    @bot.message_handler(commands=['text'], func=lambda m: m.chat.type in ['group', 'supergroup'])
    @require_quota(bot) 
    def manual_group_voice_handler(message: Message):
        user = message.from_user
        
        allowed_types = ['voice', 'audio', 'video_note']
        
        # بررسی اینکه آیا حتماً روی یک ویس ریپلای شده است یا خیر
        if not message.reply_to_message or message.reply_to_message.content_type not in allowed_types:
            bot.reply_to(message, "⚠️ برای تبدیل به متن، باید دستور `/text` را روی یک ویس (Voice) ریپلای کنید.")
            return

        # چون سهمیه در دکوریتور چک شده و کاربر به اینجا رسیده، مستقیماً پردازش را شروع می‌کنیم
        temp_msg = bot.reply_to(message.reply_to_message, f"⏳ درخواست توسط {user.first_name} ثبت شد... در حال دانلود")
        
        try:
            target_msg = message.reply_to_message
            
            # ۱. استخراج شناسه و تعیین پسوند فایل
            if target_msg.content_type == 'voice':
                file_id = target_msg.voice.file_id
                file_ext = ".ogg"
            elif target_msg.content_type == 'audio':
                file_id = target_msg.audio.file_id
                file_ext = ".mp3" 
            elif target_msg.content_type == 'video_note':
                file_id = target_msg.video_note.file_id
                file_ext = ".mp4" 

            # ۲. دانلود فایل
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # ۳. ذخیره موقت
            file_path = f"temp_{file_id}{file_ext}"
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
                
            bot.edit_message_text(chat_id=message.chat.id, message_id=temp_msg.message_id, text="⏳ در حال پردازش هوش مصنوعی...")
            
            # ۴. پردازش متن
            text_result = transcribe_audio(file_path)
            
            # ۵. ارسال نتیجه نهایی با تابع ایمن
            final_text = (
                f"🎙 **متن فایل صوتی:**\n\n{text_result}\n\n"
                "➖➖➖➖➖➖➖\n"
                f"👤 *درخواست شده توسط:* {user.first_name}\n\n" + TEXT_WATERMARK
            )
            
            # ارسال متن نهایی (با پشتیبانی از متون طولانی)
            send_long_message(
                bot=bot,
                chat_id=message.chat.id,
                text=final_text,
                reply_to_message_id=target_msg.message_id , 
                reply_markup=get_smart_edit_keyboard()
            )
            
            # ۶. پاک کردن پیام موقت
            bot.delete_message(chat_id=message.chat.id, message_id=temp_msg.message_id)
            
        except Exception as e:
            bot.edit_message_text(chat_id=message.chat.id, message_id=temp_msg.message_id, text="❌ خطایی در پردازش رخ داد.")
            log_event(bot, 'error', f"خطای پردازش دستی در گروه:\n{e}", send_to_telegram=True)
            
        finally:
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)