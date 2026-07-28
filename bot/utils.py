def send_long_message(bot, chat_id, text: str, reply_markup=None, reply_to_message_id=None):
    # اگر متن کوتاه است، یک‌باره همراه با ریپلای ارسال می‌شود
    if len(text) <= 4000:
        return bot.send_message(
            chat_id, 
            text, 
            parse_mode="Markdown", 
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id
        )
    
    # تکه‌تکه کردن متن‌های طولانی
    parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
    last_message = None
    
    for i, part in enumerate(parts):
        # ریپلای فقط روی تکه اول اعمال می‌شود
        current_reply_id = reply_to_message_id if i == 0 else None
        
        if i == len(parts) - 1:
            # بخش آخر: کیبورد شیشه‌ای را می‌گیرد
            last_message = bot.send_message(
                chat_id, 
                part, 
                parse_mode="Markdown", 
                reply_markup=reply_markup,
                reply_to_message_id=current_reply_id
            )
        else:
            # بخش‌های میانی: بدون کیبورد شیشه‌ای
            bot.send_message(
                chat_id, 
                part, 
                parse_mode="Markdown",
                reply_to_message_id=current_reply_id
            )
            
    return last_message