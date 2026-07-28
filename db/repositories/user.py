from datetime import datetime
from db.base import SessionLocal
from db.models.user import User

FREE_DAILY_LIMIT = 7
PREMIUM_DAILY_LIMIT = 30 

def check_and_use_quota(telegram_id: int, username: str = None) -> bool:
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        now = datetime.now()
        today = now.date()

        # ۱. مکانیزم بازسازی خودکار
        if not user:
            user = User(
                telegram_id=telegram_id, 
                username=username,
                daily_usage=0,
                bonus_quota=0,
                last_reset_date=now
            )
            session.add(user)
            session.commit()
        elif username and user.username != username:
            user.username = username

        # ۲. بررسی انقضای اشتراک ویژه
        if user.is_premium and user.premium_until:
            if user.premium_until < now:
                user.is_premium = False       
                user.premium_until = None     
        
        # ۳. ریست شدن شمارنده در روز جدید (شارژ اضطراری ریست نمی‌شود)
        if user.last_reset_date is None or user.last_reset_date.date() < today:
            user.daily_usage = 0
            user.last_reset_date = now
            
        # ۴. بررسی سهمیه‌ها بر اساس نوع اکانت
        if user.is_premium:
            if user.daily_usage < PREMIUM_DAILY_LIMIT:
                user.daily_usage += 1
                session.commit()
                return True
            return False
            
        else:
            # --- منطق کاربر عادی ---
            # الف) اولویت با مصرف سهمیه ۷ تایی روزانه
            if user.daily_usage < FREE_DAILY_LIMIT:
                user.daily_usage += 1
                session.commit()
                return True
                
            # ب) اگر روزانه تمام شده بود، برداشت از کیف پول اضطراری
            elif user.bonus_quota > 0:
                user.bonus_quota -= 1  # کسر یک واحد از شارژ اضطراری
                session.commit()
                return True
                
            # ج) اگر هر دو تمام شده بودند
            else:
                session.commit() 
                return False

def add_referral_bonus(telegram_id: int, bonus_amount: int = 3):
    """شارژ اضطراری و شمارنده دعوت‌های کاربر را افزایش می‌دهد"""
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.bonus_quota += bonus_amount
            user.total_referrals += 1  # اضافه شدن یک نفر به آمار دعوت‌ها
            session.commit()
def register_user(telegram_id: int, username: str = None):
    """ثبت کاربر جدید در دیتابیس هنگام زدن دکمه استارت (بدون کسر سهمیه)"""
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        
        # اگر کاربر نبود، ثبتش کن
        if not user:
            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
        # اگر بود اما یوزرنیمش عوض شده بود، آپدیتش کن
        elif username and user.username != username:
            user.username = username
            
        session.commit()


def is_user_banned(telegram_id: int) -> bool:
    """بررسی می‌کند که آیا کاربر مسدود شده است یا خیر"""
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        return user.is_banned if user else False