from telebot import TeleBot
from telebot.types import ChatMemberUpdated
from db.repositories.group import register_group, deactivate_group
from utils.logger import log_event

def register_group_events_handlers(bot: TeleBot):
    
    # این هندلر فقط تغییرات وضعیت خودِ ربات در گروه‌ها و کانال‌ها را می‌گیرد
    @bot.my_chat_member_handler()
    def handle_my_chat_member(update: ChatMemberUpdated):
        
        chat = update.chat
        new_status = update.new_chat_member.status
        user_who_did_action = update.from_user.id
        user_name = update.from_user.first_name # نام کسی که ربات را ادد یا اخراج کرده
        
        # ما فقط با گروه‌ها و سوپرگروه‌ها کار داریم (کانال‌ها و پی‌وی رو نادیده می‌گیریم)
        if chat.type not in ['group', 'supergroup']:
            return

        # ========================================================
        # ۱. ربات به گروه اضافه شده یا ادمین شده است
        # ========================================================
        if new_status in ['member', 'administrator']:
            
            # ثبت در دیتابیس (تابع ما True برمی‌گرداند اگر گروه کاملاً جدید باشد)
            is_new_group = register_group(
                chat_id=chat.id, 
                title=chat.title, 
                added_by=user_who_did_action
            )
            
            # --- استخراج مالک (Creator) و لیست ادمین‌ها ---
            owner_info = "نامشخص"
            admins_list = []
            
            try:
                admins = bot.get_chat_administrators(chat.id)
                for admin in admins:
                    if not admin.user.is_bot:
                        user_info = f"{admin.user.first_name} (<code>{admin.user.id}</code>)"
                        if admin.user.username:
                            user_info += f" | @{admin.user.username}"
                            
                        if admin.status == 'creator':
                            owner_info = user_info
                        elif admin.status == 'administrator':
                            admins_list.append(f"🔹 {user_info}")
                            
                admins_str = "\n".join(admins_list) if admins_list else "بدون ادمین جانبی"
            except Exception:
                owner_info = "مخفی یا عدم دسترسی"
                admins_str = "نامشخص"
            # ---------------------------------------------
            
            if is_new_group:
                # پیام خوش‌آمدگویی برای گروه جدید
                welcome_text = (
                    "سلام! 👋\n"
                    "ممنون که **صدایار** رو به گروهتون اضافه کردید.\n\n"
                    "🎁 **هدیه خوش‌آمدگویی:**\n"
                    "ربات به مدت **۳ روز** روی حالت «خودکار» قرار گرفت. تو این ۳ روز هر ویسی بفرستید، من درجا و کاملاً رایگان متنش رو براتون می‌فرستم!\n\n"
                    "⚙️ بعد از ۳ روز، ربات روی حالت دستی میره (یعنی فقط با ریپلای کردن دستور `/text` روی ویس‌ها کار می‌کنه).\n\n"
                    "🎙 *همین الان یه ویس بفرستید تا سرعتم رو ببینید!*"
                )
                
                log_msg = (
                    f"🆕 **گروه جدید!**\n\n"
                    f"نام گروه: {chat.title}\n"
                    f"آیدی: <code>{chat.id}</code>\n"
                    f"ادد شده توسط: {user_name} (<code>{user_who_did_action}</code>)\n\n"
                    f"👑 **مالک اصلی:**\n{owner_info}\n\n"
                    f"👥 **سایر ادمین‌ها:**\n{admins_str}"
                )
                log_event(bot, 'group', log_msg, send_to_telegram=True)
                
            else:
                # پیام برای گروهی که قبلاً بوده، اخراج شده و دوباره ادد شده
                welcome_text = (
                    "سلام دوباره! 👋\n"
                    "خوشحالم که دوباره به گروهتون برگشتم.\n\n"
                    "⚠️ مهلت تست خودکار این گروه قبلاً به پایان رسیده. برای تبدیل ویس‌ها به متن، روی ویس مورد نظر ریپلای کنید و دستور `/text` رو بفرستید."
                )
                
                log_msg = (
                    f"🔄 **بازگشت به گروه قدیمی**\n\n"
                    f"نام گروه: {chat.title}\n"
                    f"آیدی: <code>{chat.id}</code>\n"
                    f"ادد شده توسط: {user_name} (<code>{user_who_did_action}</code>)\n\n"
                    f"👑 **مالک اصلی:**\n{owner_info}\n\n"
                    f"👥 **سایر ادمین‌ها:**\n{admins_str}"
                )
                log_event(bot, 'info', log_msg, send_to_telegram=True)
            
            try:
                bot.send_message(chat.id, welcome_text, parse_mode="Markdown")
            except Exception as e:
                print(f"Cannot send message to group {chat.id}. Error: {e}")

        # ========================================================
        # ۲. ربات از گروه اخراج شده یا خودش لفت داده است
        # ========================================================
        elif new_status in ['kicked', 'left']:
            # غیرفعال کردن گروه در دیتابیس برای جلوگیری از هدر رفتن منابع سرور
            deactivate_group(chat.id)
            
            log_msg = (
                f"❌ **اخراج از گروه!**\n\n"
                f"نام گروه: {chat.title}\n"
                f"آیدی: <code>{chat.id}</code>\n"
                f"اخراج توسط: {user_name} (<code>{user_who_did_action}</code>)"
            )
            # با سطح warning می‌فرستیم تا در کانال با آیکون زرد ⚠️ متمایز شود
            log_event(bot, 'warning', log_msg, send_to_telegram=True)