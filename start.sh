#!/bin/bash
# اجرای ورکر در پس‌زمینه
python worker.py &

# اجرای وب‌سرور در پیش‌زمینه
gunicorn main:app
