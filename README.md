<div align="center">

# 🎙️ Sedayar (صدایار)

**A Telegram bot that turns voice, audio and video into text — and text back into voice.**
Built with a quota system, referral program, admin panel, and a group mode that works automatically or on demand.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQLAlchemy-336791?logo=postgresql&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Whisper-F55036)
![License](https://img.shields.io/badge/License-MIT-green)

[🤖 Try it on Telegram](https://t.me/sedayarBot) · [فارسی](README.fa.md) · [Features](#-features) · [Quick Start](#-quick-start) · [Architecture](#-architecture)

</div>

---

## 📱 Screenshots

<div align="center">
<table>
  <tr>
    <td align="center" valign="top"><img src="https://raw.githubusercontent.com/mohammadmahdiahmadipour4-glitch/sedayar/main/docs/images/main-menu.png" alt="Main menu and language selection" width="200"><br><sub>Main menu and language selection</sub></td>
    <td align="center" valign="top"><img src="https://raw.githubusercontent.com/mohammadmahdiahmadipour4-glitch/sedayar/main/docs/images/video-to-text.png" alt="Video → audio → text" width="200"><br><sub>Video → audio → text</sub></td>
    <td align="center" valign="top"><img src="https://raw.githubusercontent.com/mohammadmahdiahmadipour4-glitch/sedayar/main/docs/images/group-mode.png" alt="Group mode" width="200"><br><sub>Group mode</sub></td>
    <td align="center" valign="top"><img src="https://raw.githubusercontent.com/mohammadmahdiahmadipour4-glitch/sedayar/main/docs/images/admin-panel.png" alt="Admin panel" width="200"><br><sub>Admin panel</sub></td>
  </tr>
</table>
</div>

The main menu gives one-tap access to every feature. Before each transcription the user picks the audio language (Persian, English or auto-detect).

---

## ✨ Features

### 🎧 Media processing

| Feature | What it does |
|---|---|
| **Voice → Text** | Transcribes voice messages and audio files using Groq's Whisper API, tuned for Persian. |
| **Language selection** | The user chooses Persian, English or auto-detect before transcribing. Auto-detect is available, but the bot warns that accuracy may be lower. |
| **Text → Voice** | Converts any text message into a voice message. |
| **Video → Audio** | Extracts the audio track from a video and sends it back as an MP3 file. |
| **Video → Text** | One tap on the "Convert to text" button under the extracted audio returns a full transcription. |
| **Smart Editor** | A "✨ Smart Editor" button under every transcript for cleaning up the raw text. |

### 👥 Group mode

Add Sedayar to any Telegram group and it works for every member.

- **Welcome gift:** when the bot is added, it sends a welcome message and runs in automatic mode for **3 days**, converting every voice message for free. After that it switches to manual mode.
- **Automatic mode:** the bot converts every voice, audio or video message sent in the group on its own.
- **Manual mode:** members reply to a voice message with `/text` and the bot converts it.
- **Free group quota:** group conversions have their own free allowance, so members can try the bot without spending personal credits.

### 👤 User accounts and quotas

- A personal **profile** showing role and remaining quota.
- **Tiered quotas** with daily and monthly limits, plus premium tiers.
- **Referral program:** every user gets a unique invite link and earns free quota when a friend joins through it.
- Every request is logged, so usage is tracked and quota is deducted accurately.

### 🛠️ Admin panel

Admins get a management panel through `/admin`:

| Command | What it does |
|---|---|
| `/users` | List all users |
| `/premium <id>` | Upgrade a user to premium |
| `/premiumgroup <group id>` | Upgrade a group to premium |
| `/stats` | Live bot statistics |
| `/backup` | Download the database file |
| `/broadcast <message>` | Send a message to all users |
| `/ban <id>` / `/unban <id>` | Block or unblock a user |

---

## 🧱 Architecture

```mermaid
flowchart LR
    U[User / Group] --> T[Telegram]
    T -->|Webhook or Polling| H[bot/ handlers]
    H --> S[services/ business logic]
    S --> Q{Quota check}
    Q -->|allowed| G[Groq Whisper API]
    Q -->|denied| H
    S <--> D[(PostgreSQL)]
    G --> S
    S --> H
    H --> T
```

The code is split into layers so each part has one job:

- **`bot/`** talks to Telegram: handlers, keyboards, menus.
- **`services/`** holds the business logic: AI calls, quota math, referrals.
- **`db/`** defines the SQLAlchemy models and session handling.
- **`exceptions/`** defines custom errors, so failures such as "quota exceeded" are handled cleanly.

### Data model

- `Users`: profile, role (Admin / User), quota balance.
- `Transactions / Usage`: one record per processed request.
- `Referrals`: who invited whom, used to assign rewards automatically.

---

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.12 |
| Bot framework | pyTelegramBotAPI (sync) |
| Database | PostgreSQL + SQLAlchemy ORM |
| Migrations | Alembic |
| Speech-to-text | Groq API (Whisper `whisper-large-v3`) |
| Deployment | Render (webhook mode) |

---

## 📁 Project Structure

```
sedayar/
├── main.py          # Entry point (polling / webhook)
├── bot/             # Telegram setup, keyboards, handlers
├── services/        # Business logic, AI integration, quota math
├── db/              # SQLAlchemy models and sessions
├── alembic/         # Database migrations
├── config/          # Settings loaded from environment
├── exceptions/      # Custom exceptions
├── utils/           # Shared helpers
└── tests/           # Automated tests
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12
- A running PostgreSQL server
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A Groq API key from [console.groq.com](https://console.groq.com)

### 1. Clone and install

```bash
git clone https://github.com/mohammadmahdiahmadipour4-glitch/sedayar.git
cd sedayar
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
GROQ_API_KEY=your_groq_key
DATABASE_URL=postgresql://user:password@localhost:5432/sedayar
BOT_MODE=polling
```

| Variable | Description | Default |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Token from BotFather | required |
| `GROQ_API_KEY` | Groq API key | required |
| `DATABASE_URL` | PostgreSQL connection string | required |
| `BOT_MODE` | `polling` (local) or `webhook` (production) | `polling` |
| `WEBHOOK_URL` | Public service URL, needed in webhook mode | – |
| `GROQ_MODEL` | Whisper model name | `whisper-large-v3` |
| `WHISPER_LANGUAGE` | Language hint for transcription | `fa` |
| `LOG_LEVEL` | Logging level | `INFO` |

### 3. Create the database tables

```bash
alembic upgrade head
```

### 4. Run

```bash
python main.py
```

---

## ☁️ Deploying to Render

1. Push the repository to GitHub.
2. Create a new service on [Render](https://render.com) from the repo.
3. Set `TELEGRAM_BOT_TOKEN`, `GROQ_API_KEY`, `DATABASE_URL`, `WEBHOOK_URL` and `BOT_MODE=webhook` in the dashboard.
4. Run `alembic upgrade head` during the build step, then start the app.

---

## 💡 Usage

1. Open [@sedayarBot](https://t.me/sedayarBot) and send `/start`, or add it to a group.
2. Open the menu to see your profile and remaining quota.
3. Send a voice message, audio file, video or text and get the result back.
4. Copy your referral link from the profile section and invite friends to earn extra quota.

**In groups:** the bot starts in automatic mode for the first 3 days, then switches to manual mode. Reply to a voice message with `/text` to convert it.

---

## 🧪 Tests

```bash
pytest
```

---

## 📄 License

Released under the [MIT License](LICENSE).
