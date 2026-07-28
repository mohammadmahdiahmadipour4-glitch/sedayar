from bot.app import create_bot
from bot.handlers.start import register_start_handler
from bot.handlers.voice import register_voice_handlers
from bot.handlers.text_to_voice import register_tts_handlers
from bot.handlers.video import register_video_handlers
from db.base import init_db
from bot.handlers.admin import register_admin_handlers
from bot.handlers.profile import register_profile_handlers
from bot.handlers.payment import register_payment_handlers
from bot.handlers.help_support import register_help_support_handlers
from bot.handlers.refral import register_referral_handlers
from bot.handlers.group_events import register_group_events_handlers
from bot.handlers.group_voice import register_group_voice_handlers
from utils.logger import log_event
from server import run_server
import threading

bot = create_bot()
init_db()
register_start_handler(bot)
register_voice_handlers(bot)
register_tts_handlers(bot)
register_video_handlers(bot)
register_admin_handlers(bot)
register_profile_handlers(bot)
register_payment_handlers(bot)
register_help_support_handlers(bot)
register_referral_handlers(bot)
register_group_events_handlers(bot)
register_group_voice_handlers(bot) 

server_thread = threading.Thread(target=run_server , daemon=True)
log_event(bot, 'info', "🚀 ربات صدایار با موفقیت روشن شد و آماده به کار است.", send_to_telegram=True)
print("🤖 Sedayar Bot is running...")

bot.infinity_polling()