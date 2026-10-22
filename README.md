# 🎙️ Sedayar Bot

**Sedayar** is an advanced, production-ready Telegram bot designed for seamless media processing. Powered by the Groq Whisper API, it handles Voice-to-Text (STT), Text-to-Speech (TTS), and Video-to-Audio conversions while incorporating a robust user management and monetization architecture.

Built with scale and business logic in mind, Sedayar can operate in private chats or serve as a smart, automated assistant in Telegram groups.

## ✨ Key Features

### 🎧 AI-Powered Media Processing

* **Voice-to-Text (STT):** Highly accurate Persian transcription using Groq's Whisper API.

* **Text-to-Voice (TTS):** Converts user text into natural-sounding voice messages.

* **Video Processing:** Extracts audio tracks from video files and provides full text transcriptions.

### 👥 Smart Group Integration

* **Group Assistant Mode:** Can be added to any Telegram group to serve its members.

* **Automated & Manual Modes:** Configurable to either automatically convert all media sent in the group or wait for manual trigger commands.

* **Free Group Quotas:** Specialized free processing quotas tailored specifically for group interactions.

### 💼 Business Logic & Monetization

* **Tiered Quota System:** Tracks user usage with daily/monthly limits and premium tiers.

* **Referral Program:** A built-in viral loop where users earn free processing quotas by inviting friends via unique referral links.

* **Admin Dashboard:** Comprehensive admin controls to manage users, monitor platform usage, and manually adjust quotas.

## 🗄️ Database Architecture

The project utilizes **PostgreSQL** with **SQLAlchemy ORM** to ensure data integrity. Key entities include:

* `Users`: Stores user profiles, roles (Admin/User), and current quota balances.

* `Transactions/Usage`: Logs every media processing request to track API usage and deduct quotas accurately.

* `Referrals`: Manages the invite system, tracking who invited whom to automatically assign rewards.

## 🛠️ Tech Stack

* **Language:** Python 3.12

* **Framework:** pyTelegramBotAPI (sync)

* **Database:** PostgreSQL + SQLAlchemy ORM

* **Migrations:** Alembic

* **AI Integration:** Groq API (Whisper Model)

* **Deployment:** Render (Webhook mode)

## 📁 Project Structure

```
sedayar/
├── main.py                 # Entry point (Webhook/Polling configuration)
├── config/                 # Environment-based settings and constants
├── bot/                    # Telegram bot setup, keyboards, and message handlers
├── services/               # Core business logic, AI integration, and quota math
├── db/                     # SQLAlchemy models and database session management
├── alembic/                # Database migration scripts
└── utils/                  # Shared utilities and helper functions

```

## 🚀 Local Setup

1. **Clone and setup environment:**

   ```
   git clone https://github.com/mohammadmahdiahmadipour4-glitch/sedayar.git
   cd sedayar
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   ```

2. **Install dependencies:**

   ```
   pip install -r requirements.txt
   
   ```

3. **Configure Environment Variables:**

   ```
   cp .env.example .env
   # Edit .env with your specific tokens and database credentials
   
   ```

4. **Initialize Database:**
   Ensure your local PostgreSQL server is running, then apply migrations:

   ```
   alembic upgrade head
   
   ```

5. **Run the Bot (Polling Mode):**

   ```
   python main.py
   
   ```

## ☁️ Render Deployment

1. Push this repository to your GitHub account.

2. Create a new **Blueprint** on Render using the provided `render.yaml`.

3. Set your secret environment variables (`TELEGRAM_BOT_TOKEN`, `GROQ_API_KEY`, and `WEBHOOK_URL`) in the Render dashboard.

4. Deploy! Render will automatically run database migrations (`alembic upgrade head`) during the build phase and start the bot in webhook mode.

## ⚙️ Environment Variables

| Variable | Description | 
| ----- | ----- | 
| `TELEGRAM_BOT_TOKEN` | Telegram bot token obtained from BotFather | 
| `GROQ_API_KEY` | Groq API key for media processing | 
| `DATABASE_URL` | PostgreSQL connection string | 
| `BOT_MODE` | Set to `polling` (local) or `webhook` (Render) | 
| `WEBHOOK_URL` | Public Render service URL (required for webhook mode) | 
| `GROQ_MODEL` | Whisper model name (default: `whisper-large-v3`) | 
| `WHISPER_LANGUAGE` | Language hint for Whisper (default: `fa` for Persian) | 
| `LOG_LEVEL` | Logging level (default: `INFO`) | 

## 💡 Usage

1. Send `/start` to the bot in a private chat or add it to your group.

2. Navigate the inline keyboard menu to check your profile and quota status.

3. Send a voice message, video, or text to see the AI in action.

4. Generate a referral link from the profile section to invite friends and earn extra processing credits!