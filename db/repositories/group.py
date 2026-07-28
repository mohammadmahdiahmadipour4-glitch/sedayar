from datetime import datetime, timedelta
from db.base import SessionLocal
from db.models.group import Group

def register_group(chat_id: int, title: str, added_by: int = None):
    """ثبت گروه جدید در دیتابیس و فعال‌سازی ۳ روز تست رایگان"""
    with SessionLocal() as session:
        group = session.query(Group).filter(Group.chat_id == chat_id).first()
        now = datetime.now()
        
        if not group:
            # محاسبه زمان پایان تست (۳ روز بعد از همین الان)
            trial_end = now + timedelta(days=3)
            
            group = Group(
                chat_id=chat_id,
                title=title,
                added_by=added_by,
                is_active=True,
                trial_active=True,
                trial_end_date=trial_end
            )
            session.add(group)
            session.commit()
            return True # گروه جدید بود و ثبت شد
            
        else:
            # اگر گروه قبلاً بوده ولی ربات رو اخراج کردن و دوباره ادد کردن:
            # اسمش رو آپدیت می‌کنیم و ربات رو دوباره فعال می‌کنیم
            group.title = title
            group.is_active = True
            session.commit()
            # نکته امنیتی: تست رایگان رو دوباره از صفر شروع نمی‌کنیم تا تقلب نشه!
            return False # گروه از قبل وجود داشت

def is_group_auto_active(chat_id: int) -> bool:
    """
    بررسی می‌کند که آیا ربات در این گروه باید روی حالت 'خودکار' باشد یا خیر.
    (یعنی یا اشتراک ویژه دارد، یا در مهلت ۳ روزه تست است)
    """
    with SessionLocal() as session:
        group = session.query(Group).filter(Group.chat_id == chat_id).first()
        
        # اگر گروه ثبت نشده یا ربات اخراج شده، قطعاً حالت خودکار خاموش است
        if not group or not group.is_active:
            return False
            
        now = datetime.now()
        
        # ۱. اولویت اول: بررسی اشتراک ویژه (Premium)
        if group.is_premium and group.premium_until:
            if group.premium_until > now:
                return True
            else:
                group.is_premium = False # اشتراک ویژه تمام شده
                group.premium_until = None
                
        # ۲. بررسی مهلت تست ۳ روزه رایگان (Trial)
        if group.trial_active and group.trial_end_date:
            if group.trial_end_date > now:
                return True
            else:
                # مهلت تست دقیقاً همین الان تمام شد، پس غیرفعالش می‌کنیم
                group.trial_active = False
                session.commit()
                return False
                
        session.commit()
        return False

def deactivate_group(chat_id: int):
    """وقتی ربات از گروه اخراج (Kick) می‌شود، آن را در دیتابیس غیرفعال می‌کند"""
    with SessionLocal() as session:
        group = session.query(Group).filter(Group.chat_id == chat_id).first()
        if group:
            group.is_active = False
            session.commit()