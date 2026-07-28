from functools import wraps
from db.repositories.user import check_and_use_quota, is_user_banned
from bot.keyboards.inline import premium_upgrade_keyboard

def require_quota(bot):
    def decorator(func):
        @wraps(func)
        def wrapper(obj, *args, **kwargs):
            user = obj.from_user
            user_id = user.id
            username = user.username  # بازگرداندن یوزرنیم برای بازسازی دیتابیس
            
            chat_id = obj.message.chat.id if hasattr(obj, 'message') else obj.chat.id

            # ۱. اول چک می‌کنیم کاربر بن نشده باشد
            if is_user_banned(user_id):
                bot.send_message(
                    chat_id, 
                    "🚫 **دسترسی شما به ربات مسدود شده است.**\n\nدر صورت بروز اشتباه با پشتیبانی تماس بگیرید.", 
                    parse_mode="Markdown"
                )
                return

            # ۲. بررسی سهمیه باقیمانده (ارسال یوزرنیم برای جلوگیری از حذف دائمی کاربر)
            if not check_and_use_quota(user_id, username):
                bot.reply_to(
                    obj, 
                    "💎 **سهمیه روزانه شما به پایان رسیده است.**\n\n"
                    "لطفاً فردا مجدداً تلاش کنید یا برای استفاده تا ۳۰ پردازش در روز، اشتراک ویژه تهیه کنید.",
                    parse_mode="Markdown",
                    reply_markup=premium_upgrade_keyboard() 
                )
                return
            
            # ۳. در صورت تایید سهمیه، تابع پردازش اجرا می‌شود
            return func(obj, *args, **kwargs)
        return wrapper
    return decorator