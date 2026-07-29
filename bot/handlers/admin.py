from telebot import TeleBot
from db.base import SessionLocal
from db.models.user import User
from db.models.group import Group
import os
import datetime
import time
from sqlalchemy import func
ADMIN_ID = int(os.getenv("ADMIN_ID"))

def register_admin_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(chat_id=message.chat.id , text="دسترسی غیر مجاز ❌")
            return
            
        bot.reply_to(
            message,
            "👑 **به پنل مدیریت ربات خوش آمدید:**\n\n"
            "دستورات موجود:\n"
            "• /users - 📋 مشاهده لیست کاربران\n"
            "• /premium [آیدی] - ⭐ ارتقا به کاربر ویژه\n"
            "• /premiumgroup [آیدی گروه] - 💎 ارتقا به گروه ویژه\n"
            "• /stats - 📊 آمار لحظه‌ای ربات\n"
            "• /backup - 📁 دریافت فایل دیتابیس\n"
            "• /broadcast [پیام] - 📢 ارسال پیام همگانی\n"
            "• /ban [آیدی] - 🚫 مسدود کردن کاربر\n"
            "• /unban [آیدی] - ✅ رفع مسدودی کاربر",
            
        )
    @bot.message_handler(commands=['user', 'users'])
    def list_users(message):
        if message.from_user.id != ADMIN_ID:
            return
            
        with SessionLocal() as session:
            users = session.query(User).all()
            
            if not users:
                bot.reply_to(message, "📂 هیچ کاربری در دیتابیس ثبت نشده است.")
                return
                
            text = "📋 <b>لیست کاربران ربات:</b>\n\n"
            for u in users:
                uname = f"@{u.username}" if u.username else "بدون یوزرنیم"
                status = "⭐ ویژه" if u.is_premium else "👤 عادی"
                # به جای ` ` از تگ <code> استفاده می‌کنیم
                text += f"🆔 <code>{u.telegram_id}</code> | {uname} | {status} | مصرف: {u.daily_usage}\n"
                
            if len(text) > 4000:
                text = text[:4000] + "\n...(لیست طولانی است)"
                
            bot.reply_to(message, text, parse_mode="HTML")
            
    @bot.message_handler(commands=['premium'])
    def make_user_premium(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(chat_id=message.chat.id , text="دسترسی غیر مجاز ❌")
            return
            
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ لطفاً آیدی عددی کاربر را وارد کنید.\nمثال: `/premium 123456789`", parse_mode="Markdown")
            return
            
        try:
            target_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "❌ آیدی عددی باید فقط شامل عدد باشد.")
            return
            
        with SessionLocal() as session:
            user = session.query(User).filter(User.telegram_id == target_id).first()
            if not user:
                bot.reply_to(message, "❌ کاربری با این آیدی عددی در دیتابیس پیدا نشد.")
                return
                
            user.is_premium = True
            
            # Setting the premium expiration date to 30 days from now
            now = datetime.datetime.now()
            if user.premium_until and user.premium_until > now:
                 user.premium_until = user.premium_until + datetime.timedelta(days=30)
            else:
                 user.premium_until = now + datetime.timedelta(days=30)

            session.commit()
            bot.reply_to(message, f"✅ کاربر با آیدی `{target_id}` با موفقیت به اکانت **ویژه (Premium)** برای یک ماه ارتقا یافت.", parse_mode="Markdown")

    @bot.message_handler(commands=['premiumgroup'])
    def make_group_premium(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(chat_id=message.chat.id , text="دسترسی غیر مجاز ❌")
            return
            
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ لطفاً آیدی عددی گروه را وارد کنید.\nمثال: `/premiumgroup -100123456789`", parse_mode="Markdown")
            return
            
        try:
            target_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "❌ آیدی گروه باید فقط شامل عدد (و علامت منفی در صورت نیاز) باشد.")
            return
            
        with SessionLocal() as session:
            group = session.query(Group).filter(Group.chat_id == target_id).first()
            if not group:
                bot.reply_to(message, "❌ گروهی با این آیدی در دیتابیس پیدا نشد.")
                return
                
            group.is_premium = True
            
            now = datetime.datetime.now()
            if group.premium_until and group.premium_until > now:
                 group.premium_until = group.premium_until + datetime.timedelta(days=30)
            else:
                 group.premium_until = now + datetime.timedelta(days=30)
                 
            session.commit()
            bot.reply_to(message, f"✅ گروه با آیدی `{target_id}` با موفقیت به **گروه ویژه (Premium)** برای یک ماه ارتقا یافت.", parse_mode="Markdown")


    @bot.message_handler(commands=['stats'])
    def show_stats(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(chat_id=message.chat.id , text="دسترسی غیر مجاز ❌")
            return
            
        with SessionLocal() as session:
            # دریافت تعداد کل و ویژه
            total_users = session.query(func.count(User.id)).scalar() or 0
            premium_users = session.query(func.count(User.id)).filter(User.is_premium == True).scalar() or 0
            
            # آمار پردازش‌های امروز
            today = datetime.date.today()
            active_today = session.query(func.count(User.id)).filter(
                User.last_reset_date == today, 
                User.daily_usage > 0
            ).scalar() or 0
            
            total_usage = session.query(func.sum(User.daily_usage)).filter(
                User.last_reset_date == today
            ).scalar() or 0
            
            text = (
                "📊 *آمار وضعیت ربات:*\n\n"
                f"👥 کل کاربران: `{total_users}` نفر\n"
                f"⭐ کاربران ویژه: `{premium_users}` نفر\n\n"
                f"⚡ کاربران فعال امروز: `{active_today}` نفر\n"
                f"⚙️ مجموع پردازش‌های امروز: `{total_usage}` بار"
            )
            bot.reply_to(message, text, parse_mode="Markdown")


    @bot.message_handler(commands=['backup'])
    def send_backup(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(chat_id=message.chat.id , text="دسترسی غیر مجاز ❌")

            return
            
        db_path = "sedayar.db"  # مسیر فایل دیتابیس در پوشه اصلی
        
        if not os.path.exists(db_path):
            bot.reply_to(message, "❌ فایل دیتابیس پیدا نشد!")
            return
            
        bot.reply_to(message, "⏳ در حال آماده‌سازی فایل پشتیبان...")
        
        try:
            with open(db_path, 'rb') as doc:
                bot.send_document(
                    message.chat.id, 
                    doc, 
                    caption=f"📁 فایل پشتیبان دیتابیس\n📅 تاریخ: {datetime.date.today()}"
                )
        except Exception as e:
            bot.reply_to(message, f"❌ خطا در ارسال فایل: {e}")



    @bot.message_handler(commands=['broadcast'])
    def broadcast_message(message):
        if message.from_user.id != ADMIN_ID:
            return
            
        text = message.text.replace('/broadcast', '').strip()
        if not text:
            bot.reply_to(message, "❌ لطفاً پیام خود را وارد کنید.\nمثال: `/broadcast سلام کاربران عزیز، سرور آپدیت شد.`")
            return
            
        bot.reply_to(message, "⏳ در حال ارسال پیام به کاربران...")
        
        with SessionLocal() as session:
            users = session.query(User).all()
            success = 0
            failed = 0
            
            for u in users:
                try:
                    bot.send_message(u.telegram_id, text)
                    success += 1
                    time.sleep(0.05)  # جلوگیری از محدودیت Flood تلگرام
                except Exception:
                    # کاربری که ربات را بلاک کرده باشد
                    failed += 1
                    
            bot.reply_to(
                message, 
                f"✅ ارسال همگانی به پایان رسید!\n\n"
                f"🟢 موفق: `{success}` نفر\n"
                f"🔴 ناموفق (بلاک کرده‌اند): `{failed}` نفر", 
                parse_mode="Markdown"
            )

    @bot.message_handler(commands=['ban', 'unban'])
    def manage_ban(message):
        if message.from_user.id != ADMIN_ID:
            return
            
        command = message.text.split()[0]  # /ban یا /unban
        parts = message.text.split()
        
        if len(parts) < 2:
            bot.reply_to(message, f"❌ لطفاً آیدی عددی را وارد کنید.\nمثال: `{command} 123456789`", parse_mode="Markdown")
            return
            
        try:
            target_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "❌ آیدی عددی باید فقط عدد باشد.")
            return
            
        with SessionLocal() as session:
            user = session.query(User).filter(User.telegram_id == target_id).first()
            if not user:
                bot.reply_to(message, "❌ کاربر یافت نشد.")
                return
                
            is_banning = (command == '/ban')
            user.is_banned = is_banning
            session.commit()
            
            status = "🚫 مسدود" if is_banning else "✅ رفع مسدودیت"
            bot.reply_to(message, f"کاربر `{target_id}` با موفقیت **{status}** شد.", parse_mode="Markdown")