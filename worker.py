import json
import time
from telebot.types import Update
from db.base import SessionLocal
from db.models.queue import UpdateQueue
from main import bot

print("⚙️ Worker is ON: Processing and cleaning up the queue...")

while True:
    try:
        with SessionLocal() as session:
            # ۱. گرفتن پیام‌های صف
            pending_updates = session.query(UpdateQueue).order_by(UpdateQueue.created_at.asc()).limit(50).all()

            if pending_updates:
                print(f"📦 Found {len(pending_updates)} pending message(s). Processing...")
                updates_to_process = []
                items_to_delete = []
                
                for item in pending_updates:
                    try:
                        update_dict = json.loads(item.update_json)
                        update_obj = Update.de_json(update_dict)
                        updates_to_process.append(update_obj)
                        
                        # این آیتم باید پس از پردازش پاک شود
                        items_to_delete.append(item)
                    except Exception as e:
                        print(f"❌ Error parsing message: {e}")
                        # اگر پیام مشکل داشت هم برای اینکه گیر نکنیم آن را پاک می‌کنیم
                        items_to_delete.append(item)

                # ۲. ارسال به هندلرها برای پاسخ‌دهی زنده
                if updates_to_process:
                    bot.process_new_updates(updates_to_process)
                    print(f"🚀 Successfully processed {len(updates_to_process)} message(s)!")

                # ۳. حذف کامل پیام‌های پردازش‌شده از دیتابیس برای جلوگیری از افزایش حجم
                for item in items_to_delete:
                    session.delete(item)
                
                session.commit()
                print("🧹 Cleaned up processed messages from database.")
        
        time.sleep(2)

    except Exception as e:
        print(f"❌ Error in worker loop: {e}")
        time.sleep(5)