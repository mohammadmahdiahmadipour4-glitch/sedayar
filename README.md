# Sedayar

Telegram bot that converts Persian voice messages to text using the Groq Whisper API.

## Stack

- Python 3.12
- pyTelegramBotAPI (sync)
- PostgreSQL + SQLAlchemy
- Alembic migrations
- Deployed on Render

## Project structure

```
sedayar/
├── main.py                 # Entry point
├── config/                 # Environment-based settings
├── bot/                    # Bot setup and handlers
├── services/               # Business logic
├── db/                     # SQLAlchemy models and sessions
├── alembic/                # Database migrations
└── utils/                  # Shared utilities
```

## Local setup

1. Create and activate a virtual environment (Python 3.12).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

4. Start PostgreSQL and update `DATABASE_URL` in `.env`.
5. Run migrations:

   ```bash
   alembic upgrade head
   ```

6. Start the bot:

   ```bash
   python main.py
   ```

## Render deployment

1. Push this repository to GitHub.
2. Create a new **Blueprint** on Render using `render.yaml`.
3. Set `TELEGRAM_BOT_TOKEN`, `GROQ_API_KEY`, and `WEBHOOK_URL` in the Render dashboard.
4. Deploy. Render runs migrations during build and starts the bot in webhook mode.

## Environment variables

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather |
| `GROQ_API_KEY` | Groq API key |
| `DATABASE_URL` | PostgreSQL connection string |
| `BOT_MODE` | `polling` (local) or `webhook` (Render) |
| `WEBHOOK_URL` | Public Render service URL (webhook mode) |
| `GROQ_MODEL` | Whisper model name (default: `whisper-large-v3`) |
| `WHISPER_LANGUAGE` | Language hint for Whisper (default: `fa`) |
| `LOG_LEVEL` | Logging level (default: `INFO`) |

## Usage

1. Send `/start` to the bot.
2. Send a voice message or audio file.
3. Receive the transcribed Persian text.
