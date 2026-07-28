from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# ایجاد دیتابیس SQLite
engine = create_engine('sqlite:///sedayar.db')

# ساخت Session برای استفاده در ریپازیتوری‌ها
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)