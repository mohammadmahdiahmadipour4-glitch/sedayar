from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from datetime import datetime
from db.base import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(BigInteger, unique=True, index=True) # آیدی تلگرامی گروه (معمولاً منفی است)
    title = Column(String, nullable=True) # اسم گروه
    
    # ذخیره آیدی شخصی که ربات را ادد کرده (برای ارسال فاکتور یا پیام‌های ادمین)
    added_by = Column(BigInteger, nullable=True)
    
    # تاریخ عضویت و وضعیت حضور ربات در گروه
    join_date = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True) # اگر ربات اخراج شد، این False می‌شود
    
    # --- سیستم تست ۳ روزه رایگان (حالت خودکار) ---
    trial_active = Column(Boolean, default=True)
    trial_end_date = Column(DateTime, nullable=True)
    
    # --- سیستم اشتراک ویژه (حالت خودکار دائمی) ---
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime, nullable=True)