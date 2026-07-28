import os
from dotenv import load_dotenv
from utils.logger import log_event  # اضافه کردن لاگر

load_dotenv()

class DeepgramAPIKeyManager:
    def __init__(self):
        # خواندن کلیدها از فایل env و جدا کردنشون با ویرگول
        keys_env = os.getenv("DEEPGRAM_API_KEY", "")
        self.keys = [k.strip() for k in keys_env.split(",") if k.strip()]
        
        if not self.keys:
            raise ValueError("هیچ کلید API در فایل .env یافت نشد!")
        
        self.active_keys = self.keys.copy()
        self.current_index = 0

    def get_key(self):
        """کلید فعال فعلی را برمی‌گرداند"""
        if not self.active_keys:
            raise Exception("🚨 تمام کلیدهای API مسدود یا منقضی شده‌اند!")
        return self.active_keys[self.current_index]

    def switch_key(self, bot=None):
        """کلید فعلی را می‌سوزاند، لاگ می‌کند و به کلید بعدی سوئیچ می‌کند"""
        if not self.active_keys:
            raise Exception("🚨 تمام کلیدها تمام شده‌اند!")
        
        # کلیدی که ارور داده رو از لیست فعال‌ها حذف می‌کنیم
        failed_key = self.active_keys.pop(self.current_index)
        
        # --- سیستم لاگ و اطلاع‌رسانی به ادمین ---
        alert_msg = f"🚨 کلید دیپ‌گرام سوخت!\n🔑 کلید: <code>{failed_key[:8]}...</code>\n🔋 کلیدهای باقی‌مانده: {len(self.active_keys)}"
        print(alert_msg)
        
        if bot:
            log_event(bot, 'error', alert_msg, send_to_telegram=True)
        # ----------------------------------------
        
        if not self.active_keys:
            fatal_msg = "🚨 فاجعه: تمام کلیدهای جایگزین دیپ‌گرام تمام شدند! ربات متوقف شد."
            if bot:
                log_event(bot, 'error', fatal_msg, send_to_telegram=True)
            raise Exception(fatal_msg)
        
        # چون قبلی حذف شد، ایندکس صفر به طور خودکار میشه کلیدِ جدید
        self.current_index = 0 
        print(f"🔄 سوئیچ شد روی کلید جدید: {self.active_keys[self.current_index][:8]}...")
        
        return self.active_keys[self.current_index]

# ساخت یک نمونه از کلاس برای استفاده در کل پروژه
api_manager = DeepgramAPIKeyManager()