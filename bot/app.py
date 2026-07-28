import telebot

from config.settings import BOT_TOKEN


def create_bot() -> telebot.TeleBot:
    """Create and configure Telegram bot instance."""
    return telebot.TeleBot(BOT_TOKEN)