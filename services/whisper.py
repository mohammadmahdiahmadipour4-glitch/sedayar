# services/whisper.py

from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL, WHISPER_LANGUAGE

def transcribe_audio(file_path: str) -> str:
    """
    Sends the audio file to Groq API and returns the transcribed text.
    Optimized for Persian language accuracy using low temperature and initial prompt.
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    persian_initial_prompt = (
        "سلام، این یک متن فارسی استاندارد است. "
        "لطفاً علائم نگارشی مانند نقطه، کاما و علامت سؤال را رعایت کنید. "
        "کلمات به درستی و با املای دقیق نوشته شده‌اند."
    )
    
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model=GROQ_MODEL,
            language=WHISPER_LANGUAGE,
            prompt=persian_initial_prompt,
            temperature=0.2, # تغییر به 0.2 برای جلوگیری از گیر کردن مدل (Looping)
        )
        
    return transcription.text