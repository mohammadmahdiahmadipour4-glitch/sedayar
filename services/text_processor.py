# services/text_processor.py

from groq import Groq
from config.settings import GROQ_API_KEY

def improve_text(raw_text: str) -> str:
    """
    Advanced text processor using Few-Shot prompting and strict guidelines 
    to perfect transcribed Persian audio texts.
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    system_prompt = (
        "تو یک ویراستار ارشد و متخصصِ پاکسازی متونِ تبدیل شده از صوت (Speech-to-Text) به زبان فارسی هستی. "
        "کار تو این است که متن‌های خام، بی‌نظم و دارای غلط املایی را به متن‌های کاملاً تمیز، دقیق و سلیس تبدیل کنی.\n\n"
        
        "قوانین سخت‌گیرانهٔ تو:\n"
        "۱. **اصلاح املایی هوشمند:** کلماتی که به دلیل اشتباهِ موتورِ شنوایی، املای نادرست دارند را با توجه به سیاق و معنی جمله اصلاح کن (مثلاً اصلاح اشتباهات کلمات هم‌آوا).\n"
        "۲. **علائم نگارشی:** نقطه، کاما، علامت سؤال و فاصله نیم‌فاصله‌ها را به صورت کاملاً استاندارد و حرفه‌ای رعایت کن.\n"
        "۳. **حفظ لحن:** لحن کاربر (چه محاوره‌ای و عامیانه، چه رسمی و کتابی) را دست‌نخورده نگه دار و به لحن کتابی تبدیلش نکن.\n"
        "۴. **عدم اضافه‌کاری:** به هیچ وجه از خودت جمله، توضیح، مقدمه یا موخره‌ای اضافه نکن.\n\n"
        
        "مثال برای نوع عملکرد:\n"
        "ورودی خام: سلام خوب هستی میخواستم بگم فردا اون فایل پروژه رو بفرست برامون.\n"
        "خروجی ویرایش‌شده: سلام، خوب هستی؟ می‌خواستم بگم فردا اون فایل پروژه رو بفرست برامون.\n\n"
        
        "مستقیماً و بدون هیچ‌گونه مقدمه یا توضیح، فقط متن نهایی ویرایش‌شده را برگردان."
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        model="openai/gpt-oss-120b",
        temperature=0.1, # دمای بسیار پایین برای اینکه مدل کاملاً روی قوانین متمرکز بماند و خلاقیت بی‌جا نکند
    )
    
    return response.choices[0].message.content.strip()