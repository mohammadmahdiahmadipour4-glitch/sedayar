from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError, ProgrammingError
Base = declarative_base()

# ایجاد دیتابیس SQLite
engine = create_engine("postgresql://neondb_owner:npg_huLUW04VXlrv@ep-nameless-boat-axnh8wha-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# ساخت Session برای استفاده در ریپازیتوری‌ها
SessionLocal = sessionmaker(bind=engine)

def init_db():
    try : 
        Base.metadata.create_all(engine)
        print("✅ دیتابیس با موفقیت ساخته شد یا از قبل موجود بود.")
    except (OperationalError, ProgrammingError) as e:
        # اگر پردازش دیگری (مثل worker) همزمان در حال ساخت جداول باشد،
        # این ارور نادیده گرفته می‌شود تا ربات کرش نکند.
        print("⚠️ دیتابیس در حال استفاده توسط پردازشی دیگر است. در حال عبور...")
        time.sleep(1)