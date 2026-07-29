from sqlalchemy import Column, Integer, Boolean, DateTime, BigInteger , String 
import datetime
from db.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username =Column(String , nullable=True)
    is_premium = Column(Boolean, default=False)
    premium_until =Column(DateTime , nullable = True)
    is_banned = Column(Boolean , default=False)
    daily_usage = Column(Integer, default=0)
    last_reset_date = Column(DateTime, default=datetime.date.today)
    bonus_quota = Column(Integer , default=0)
    total_referrals = Column(Integer, default=0)
    referred_by = Column(BigInteger, nullable=True)
