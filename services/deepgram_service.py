from deepgram import DeepgramClient
# فرض می‌کنیم فایل api_switcher رو در پوشه utils ساختی
from utils.api_switcher import api_manager 

def transcribe_audio(file_path: str  , language: str) -> str:
    """
    Sends the downloaded Telegram voice file to Deepgram API (Nova-3 Model) 
    using the official SDK and Auto-API Key Rotation.
    """
    # فایل صوتی را فقط یک بار می‌خوانیم تا در حلقه مدام هارد دیسک درگیر نشود
    try:
        with open(file_path, "rb") as file:
            audio_data = file.read()
    except Exception as e:
        print(f"File Read Error: {e}")
        return "❌ خطا در خواندن فایل صوتی در سرور."

    # حلقه بی‌نهایت برای تست کلیدها تا زمانی که یکی جواب بدهد
    while True:
        try:
            # ۱. دریافت کلید فعال فعلی از سوئیچر
            current_key = api_manager.get_key()
            
            # ۲. مقداردهی کلاینت دیپ‌گرام با این کلید
            deepgram = DeepgramClient(api_key=current_key)

            if language == "Auto_detctor" : 
                response = deepgram.listen.v1.media.transcribe_file(
                                request=audio_data,
                                model="nova-3",
                                detect_language= True,
                                smart_format=True
                            )

            # ۳. ارسال فایل به مدل Nova-3
            response = deepgram.listen.v1.media.transcribe_file(
                request=audio_data,
                model="nova-3",
                language=language,
                smart_format=True
            )
            
            # ۴. استخراج متن نهایی
            transcript = response.results.channels[0].alternatives[0].transcript
            return transcript

        except Exception as e:
            error_msg = str(e).lower()
            print(f"Deepgram Error with key {current_key[:6]}***: {e}")
            
            # بررسی اینکه آیا ارور به خاطر اتمام اعتبار (401/402/403) یا محدودیت درخواست (429) است؟
            if any(code in error_msg for code in ["401", "402", "403", "429", "unauthorized", "rate limit"]):
                try:
                    print("⚠️ در حال سوئیچ به کلید جدید...")
                    api_manager.switch_key()
                    continue  # برگرد به اول حلقه و با کلید جدید تلاش کن
                except Exception as switch_err:
                    # اگر سوئیچر ارور داد یعنی تمام کلیدها سوخته‌اند
                    print(f"All keys exhausted: {switch_err}")
                    return "❌ سهمیه سرور پردازش موقتاً به اتمام رسیده است. لطفاً بعداً تلاش کنید."
            else:
                # اگر ارور چیز دیگری بود (مثلاً سرور دیپ‌گرام قطع بود)
                return "❌ متأسفانه در ارتباط با سرور دیپ‌گرام خطای ناشناخته‌ای رخ داد."