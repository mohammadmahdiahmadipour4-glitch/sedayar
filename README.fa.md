<div dir="rtl" align="right">

<div align="center">

# 🎙️ صدایار (Sedayar)

**ربات تلگرامی که ویس، صوت و ویدیو را به متن و متن را به ویس تبدیل می‌کند.**
همراه با سیستم سهمیه‌بندی، دعوت دوستان، پنل ادمین و حالت گروه (خودکار یا دستی).

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQLAlchemy-336791?logo=postgresql&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Whisper-F55036)
![License](https://img.shields.io/badge/License-MIT-green)

[🤖 امتحان ربات در تلگرام](https://t.me/sedayarBot) · [English](README.md)

</div>

---

## 📱 تصاویر ربات

<div align="center">
<table>
  <tr>
    <td align="center" valign="top"><img src="https://raw.githubusercontent.com/mohammadmahdiahmadipour4-glitch/sedayar/main/docs/images/main-menu.png" alt="منوی اصلی و انتخاب زبان" width="200"><br><sub>منوی اصلی و انتخاب زبان</sub></td>
    <td align="center" valign="top"><img src="https://raw.githubusercontent.com/mohammadmahdiahmadipour4-glitch/sedayar/main/docs/images/video-to-text.png" alt="ویدیو به صوت و متن" width="200"><br><sub>ویدیو به صوت و متن</sub></td>
    <td align="center" valign="top"><img src="https://raw.githubusercontent.com/mohammadmahdiahmadipour4-glitch/sedayar/main/docs/images/group-mode.png" alt="حالت گروه" width="200"><br><sub>حالت گروه</sub></td>
    <td align="center" valign="top"><img src="https://raw.githubusercontent.com/mohammadmahdiahmadipour4-glitch/sedayar/main/docs/images/admin-panel.png" alt="پنل ادمین" width="200"><br><sub>پنل ادمین</sub></td>
  </tr>
</table>
</div>

منوی اصلی دسترسی یک‌کلیکی به همهٔ امکانات می‌دهد. قبل از هر تبدیل، کاربر زبان فایل صوتی را انتخاب می‌کند (فارسی، انگلیسی یا تشخیص خودکار).

---

## ✨ امکانات

### 🎧 پردازش رسانه

| قابلیت | توضیح |
|---|---|
| **ویس به متن** | تبدیل ویس و فایل صوتی به متن با Whisper از Groq، با دقت بالا برای فارسی |
| **انتخاب زبان** | کاربر قبل از تبدیل، فارسی، انگلیسی یا تشخیص خودکار را انتخاب می‌کند. تشخیص خودکار هم هست، ولی ربات هشدار می‌دهد که دقتش ممکن است کمتر باشد |
| **متن به ویس** | تبدیل هر متن به پیام صوتی |
| **ویدیو به صوت** | استخراج صدای ویدیو و ارسال آن به‌صورت فایل MP3 |
| **ویدیو به متن** | با یک ضربه روی دکمهٔ «تبدیل به متن» زیر صوت استخراج‌شده، متن کامل ویدیو ارسال می‌شود |
| **ویراستار هوشمند** | دکمهٔ «✨ ویراستار هوشمند» زیر هر متن برای مرتب‌سازی متن خام |

### 👥 حالت گروه

ربات را به هر گروه تلگرام اضافه کنید تا برای همهٔ اعضا کار کند.

- **هدیهٔ خوش‌آمدگویی:** با اضافه شدن ربات، یک پیام خوش‌آمد می‌فرستد و **۳ روز** در حالت خودکار می‌ماند و همهٔ ویس‌ها را رایگان تبدیل می‌کند. بعد از آن به حالت دستی می‌رود.
- **حالت خودکار:** ربات همهٔ ویس‌ها، صوت‌ها و ویدیوهای گروه را خودش تبدیل می‌کند.
- **حالت دستی:** اعضا روی یک ویس ریپلای می‌کنند و دستور `/text` را می‌فرستند تا ربات آن را تبدیل کند.
- **سهمیهٔ رایگان گروه:** تبدیل در گروه سهمیهٔ رایگان جداگانه دارد، پس اعضا بدون مصرف اعتبار شخصی ربات را امتحان می‌کنند.

### 👤 حساب کاربری و سهمیه

- **پروفایل شخصی** شامل نقش و سهمیهٔ باقی‌مانده
- **سهمیه‌بندی پلکانی** با محدودیت روزانه و ماهانه و پلن‌های ویژه
- **سیستم دعوت:** هر کاربر لینک دعوت اختصاصی دارد و با ورود هر دوست، سهمیهٔ رایگان می‌گیرد
- ثبت همهٔ درخواست‌ها برای محاسبهٔ دقیق مصرف و کسر سهمیه

### 🛠️ پنل ادمین

ادمین‌ها با دستور `/admin` به پنل مدیریت دسترسی دارند:

| دستور | کاربرد |
|---|---|
| `/users` | مشاهدهٔ لیست کاربران |
| `/premium <آیدی>` | ارتقا به کاربر ویژه |
| `/premiumgroup <آیدی گروه>` | ارتقا به گروه ویژه |
| `/stats` | آمار لحظه‌ای ربات |
| `/backup` | دریافت فایل دیتابیس |
| `/broadcast <پیام>` | ارسال پیام همگانی |
| `/ban <آیدی>` و `/unban <آیدی>` | مسدود کردن و رفع مسدودی کاربر |

---

## 🧱 معماری

```mermaid
flowchart LR
    U[کاربر / گروه] --> T[تلگرام]
    T -->|Webhook یا Polling| H[هندلرهای bot]
    H --> S[services: منطق برنامه]
    S --> Q{بررسی سهمیه}
    Q -->|مجاز| G[Groq Whisper]
    Q -->|رد شد| H
    S <--> D[(PostgreSQL)]
    G --> S
    S --> H
    H --> T
```

کد به لایه‌هایی تقسیم شده که هرکدام یک وظیفه دارد:

- **`bot/`** ارتباط با تلگرام: هندلرها، کیبوردها و منوها
- **`services/`** منطق اصلی: فراخوانی هوش مصنوعی، محاسبهٔ سهمیه، دعوت‌ها
- **`db/`** مدل‌های SQLAlchemy و مدیریت session
- **`exceptions/`** خطاهای سفارشی، مثل «سهمیه تمام شده»

### مدل داده

- `Users`: پروفایل، نقش (ادمین / کاربر)، موجودی سهمیه
- `Transactions / Usage`: یک رکورد برای هر درخواست پردازش‌شده
- `Referrals`: ثبت اینکه چه کسی چه کسی را دعوت کرده، برای اعطای خودکار پاداش

---

## 🛠️ تکنولوژی‌ها

| بخش | ابزار |
|---|---|
| زبان | Python 3.12 |
| فریم‌ورک ربات | pyTelegramBotAPI (sync) |
| دیتابیس | PostgreSQL + SQLAlchemy ORM |
| مایگریشن | Alembic |
| تبدیل گفتار به متن | Groq API (مدل `whisper-large-v3`) |
| دیپلوی | Render (حالت webhook) |

---

## 📁 ساختار پروژه

```
sedayar/
├── main.py          # نقطهٔ شروع (polling / webhook)
├── bot/             # راه‌اندازی تلگرام، کیبورد، هندلرها
├── services/        # منطق برنامه، هوش مصنوعی، سهمیه
├── db/              # مدل‌ها و session دیتابیس
├── alembic/         # مایگریشن‌ها
├── config/          # تنظیمات از محیط
├── exceptions/      # خطاهای سفارشی
├── utils/           # ابزارهای مشترک
└── tests/           # تست‌ها
```

---

## 🚀 راه‌اندازی

### پیش‌نیازها

- Python 3.12
- سرور PostgreSQL در حال اجرا
- توکن ربات از [@BotFather](https://t.me/BotFather)
- کلید API از [Groq](https://console.groq.com)

### ۱. دریافت و نصب

```bash
git clone https://github.com/mohammadmahdiahmadipour4-glitch/sedayar.git
cd sedayar
python -m venv venv
source venv/bin/activate        # ویندوز: venv\Scripts\activate
pip install -r requirements.txt
```

### ۲. تنظیمات

فایل `.env` را در ریشهٔ پروژه بسازید:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
GROQ_API_KEY=your_groq_key
DATABASE_URL=postgresql://user:password@localhost:5432/sedayar
BOT_MODE=polling
```

| متغیر | توضیح | پیش‌فرض |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | توکن BotFather | الزامی |
| `GROQ_API_KEY` | کلید Groq | الزامی |
| `DATABASE_URL` | آدرس اتصال PostgreSQL | الزامی |
| `BOT_MODE` | `polling` (محلی) یا `webhook` (سرور) | `polling` |
| `WEBHOOK_URL` | آدرس عمومی سرویس، در حالت webhook لازم است | – |
| `GROQ_MODEL` | نام مدل Whisper | `whisper-large-v3` |
| `WHISPER_LANGUAGE` | زبان تشخیص | `fa` |
| `LOG_LEVEL` | سطح لاگ | `INFO` |

### ۳. ساخت جدول‌های دیتابیس

```bash
alembic upgrade head
```

### ۴. اجرا

```bash
python main.py
```

---

## ☁️ دیپلوی روی Render

1. پروژه را روی گیت‌هاب push کنید.
2. در [Render](https://render.com) یک سرویس جدید از روی ریپو بسازید.
3. متغیرهای `TELEGRAM_BOT_TOKEN`، `GROQ_API_KEY`، `DATABASE_URL`، `WEBHOOK_URL` و `BOT_MODE=webhook` را در داشبورد وارد کنید.
4. در مرحلهٔ build دستور `alembic upgrade head` را اجرا کنید و بعد برنامه را start کنید.

---

## 💡 نحوهٔ استفاده

1. ربات [@sedayarBot](https://t.me/sedayarBot) را باز کنید و `/start` بفرستید، یا آن را به گروه اضافه کنید.
2. از منو پروفایل و سهمیهٔ باقی‌مانده را ببینید.
3. ویس، فایل صوتی، ویدیو یا متن بفرستید و نتیجه را بگیرید.
4. لینک دعوت را از بخش پروفایل کپی کنید و با دعوت دوستان سهمیهٔ بیشتر بگیرید.

**در گروه:** ربات ۳ روز اول در حالت خودکار است و بعد به حالت دستی می‌رود. روی ویس ریپلای کنید و `/text` بفرستید تا تبدیل شود.

---

## 🧪 تست

```bash
pytest
```

---

## 📄 مجوز

این پروژه تحت [مجوز MIT](LICENSE) منتشر شده است.

</div>
