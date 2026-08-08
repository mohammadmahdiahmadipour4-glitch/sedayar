from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# ایجاد دیتابیس SQLite
engine = create_engine("postgresql://neondb_owner:npg_huLUW04VXlrv@ep-nameless-boat-axnh8wha-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# ساخت Session برای استفاده در ریپازیتوری‌ها
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)