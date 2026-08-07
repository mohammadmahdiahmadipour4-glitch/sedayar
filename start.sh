#!/bin/bash
# استفاده از فلگ -u برای جلوگیری از بافر شدن خروجی
python -u worker.py &

# اجرای وب‌سرور در پیش‌زمینه
gunicorn main:app
