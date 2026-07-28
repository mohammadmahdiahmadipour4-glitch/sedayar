# services/video_service.py
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def extract_audio_from_video(video_path: str, output_audio_path: str = "extracted_audio.mp3") -> str:
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        
        audio_clip.write_audiofile(output_audio_path, logger=None)
        
        audio_clip.close()
        video_clip.close()
        
        if os.path.exists(output_audio_path):
            return output_audio_path
        return None
    except Exception as e:
        print(f"Video Extraction Error: {e}")
        return None