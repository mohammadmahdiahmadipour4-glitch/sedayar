# bot/services/file_service.py

import os
from telebot import TeleBot

def download_telegram_file(bot: TeleBot, file_id: str, save_dir: str = "temp") -> str:
    """
    Downloads a file from Telegram servers and saves it locally.
    Returns the relative path to the saved file.
    """
    # Create temp directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Get file path from Telegram
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Extract extension and create a unique file name
    file_extension = file_info.file_path.split('.')[-1]
    file_path = os.path.join(save_dir, f"{file_id}.{file_extension}")
    
    # Save the file locally
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    return file_path

def delete_local_file(file_path: str):
    """
    Deletes the downloaded file to free up server space.
    """
    if file_path and os.path.exists(file_path):
        os.remove(file_path)