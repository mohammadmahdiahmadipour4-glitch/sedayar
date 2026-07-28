# services/tts_service.py
import asyncio
import edge_tts

VOICE = "fa-IR-DilaraNeural"

def text_to_speech(text: str, output_file_path: str = "output.mp3") -> str:
    try:
        async def _generate():
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(output_file_path)

        asyncio.run(_generate())
        return output_file_path
    except Exception as e:
        print(f"Edge TTS Error: {e}")
        return None