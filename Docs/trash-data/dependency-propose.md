پیشنهاد من برای نسخه MVP این است:

> یک Modular Monolith با Next.js در Frontend، FastAPI در Backend، PostgreSQL به‌عنوان پایگاه داده محصول، Worker پایتون، LangGraph با یک Agent محدود و Docker Compose برای اجرا.

این انتخاب با تیم کوچک، اجرای ۳۰ روز Replay، محدودیت ۴ هسته و ۱۶ گیگابایت RAM، و سقف هزینه LLM سازگار است.

## استک پیشنهادی

| بخش | فناوری پیشنهادی | دلیل انتخاب |
|---|---|---|
| معماری | Modular Monolith | API و Worker از یک Codebase استفاده می‌کنند. پیچیدگی Microservice ایجاد نمی‌شود. مرز ماژول‌ها نیز حفظ می‌شود. |
| زبان Backend | Python | بخش اصلی پروژه شامل پردازش داده، SQL، ارزیابی و Agent است. اکوسیستم Python برای این کارها مناسب است. |
| Backend API | FastAPI | APIهای Typed، مستندات OpenAPI و Validation مناسب دارد. با Pydantic و LangGraph نیز هماهنگ است. |
| قرارداد داده | Pydantic | برای Report، Signal، DecisionCard، QuerySpec و پاسخ Agent قرارداد صریح ایجاد می‌کند. خروجی نامعتبر قبل از انتشار رد می‌شود. |
| ORM و Migration | SQLAlchemy + Alembic | SQLAlchemy برای عملیات عادی مناسب است. Alembic تغییرات Schema را نسخه‌دار می‌کند. برای KPIها می‌توان SQL صریح اجرا کرد. |
| Driver پایگاه داده | Psycopg | Driver اصلی PostgreSQL برای Python است. هم API و هم Worker می‌توانند از آن استفاده کنند. |
| پایگاه داده محصول | PostgreSQL | تصمیم فعال معماری است. Transaction، RLS، JSON، Audit و Query تحلیلی را در یک موتور فراهم می‌کند. |
| مرجع صحت KPI | SQLite فقط در Test Harness | SQL مرجع Dataset روی SQLite اجرا می‌شود. نتیجه PostgreSQL باید با آن برابر باشد. SQLite نباید در Runtime محصول استفاده شود. |
| پردازش پس‌زمینه | Worker پایتون از همان Codebase | Ingestion، KPI، Signal، Workflow و گزارش را از مسیر API جدا می‌کند. اشتراک مدل دامنه نیز حفظ می‌شود. |
| صف کار | PostgreSQL Queue با `FOR UPDATE SKIP LOCKED` | برای MVP به Redis، RabbitMQ یا Celery نیاز نیست. تعداد سرویس‌ها و مصرف منابع کم می‌شود. |
| زمان‌بندی و Replay | Python CLI Command | اجرای روز، Replay و ارزیابی باید Clock تزریقی داشته باشند. یک Command مستقل، اجرای Docker و آزمون را ساده می‌کند. |
| Agent | LangGraph با یک Agent | سند استفاده از یک Agent محدود را مشخص کرده است. LangGraph فقط جریان تحلیل، Draft، Validation و Repair را هماهنگ می‌کند. |
| اتصال به مدل | Model Gateway داخلی | Budget، Timeout، Retry، Token، مدل و هزینه را در یک محل کنترل می‌کند. تغییر Provider نیز ساده می‌شود. |
| بررسی SQL تولیدشده | SQLGlot + Query Gateway | SQL را قبل از اجرا Parse می‌کند. فقط `SELECT`، جداول مجاز و ستون‌های مجاز پذیرفته می‌شوند. |
| Frontend | Next.js + TypeScript | برای سه رابط Assistant، Dashboard و Workflow Control Room مناسب است. TypeScript خطای قرارداد API را کم می‌کند. |
| UI | Tailwind CSS + shadcn/ui | ساخت سریع رابط فارسی و RTL را ممکن می‌کند. اجزا قابل کنترل هستند و وابستگی به یک UI framework سنگین ایجاد نمی‌شود. |
| دریافت داده در UI | TanStack Query | Cache، Loading، Retry و Synchronization درخواست‌های API را کنترل می‌کند. |
| جدول و نمودار | TanStack Table + Apache ECharts | جدول‌های تحلیلی، Drill-down و نمودارهای KPI و Workflow را پوشش می‌دهند. ECharts از RTL و نمودارهای مدیریتی پشتیبانی مناسبی دارد. |
| احراز هویت MVP | Session امن در PostgreSQL | Backend باید `AuthContext` را از هویت معتبر بسازد. `manager_id` ورودی کاربر نباید مبنای دسترسی باشد. |
| کنترل دسترسی | PostgreSQL RLS + Query Gateway | RLS کنترل ردیف را در پایگاه داده اعمال می‌کند. Query Gateway ستون، Purpose و نوع Query را نیز کنترل می‌کند. |
| فایل‌های خام | Protected Local Volume با SHA-256 | برای محیط تک‌ماشین و Docker کافی است. فایل اصلی تغییر نمی‌کند. Hash و Manifest در PostgreSQL ثبت می‌شوند. |
| Log و Audit | Structured JSON Logging + Audit Tables | Query، Snapshot، هزینه، Failure و انتشار قابل ردیابی می‌شوند. داده فردی نباید وارد Log عمومی شود. |
| تست Backend | pytest | برای تست واحد، Integration، Replay و آزمون‌های داده مناسب است. |
| تست صحت اعداد | PostgreSQL/SQLite Parity Suite | برای هر ۵۵ KPI، نتیجه PostgreSQL با SQLite مرجع مقایسه می‌شود. این تست یکی از مهم‌ترین تست‌های پروژه است. |
| تست Frontend | Vitest + Testing Library | Componentها، وضعیت‌ها و قراردادهای UI را سریع بررسی می‌کند. |
| تست End-to-End | Playwright | جریان سؤال، گزارش، Dashboard، Workflow و کنترل دسترسی را در مرورگر واقعی آزمایش می‌کند. |
| بسته‌بندی و اجرا | Docker Compose | Web، API، Worker و PostgreSQL را با یک دستور اجرا می‌کند. این مورد با قرارداد تحویل هماهنگ است. |

## ساختار اجرایی پیشنهادی

```text
Web: Next.js
       |
       v
API: FastAPI
       |
       +---- PostgreSQL
       |       - Product data
       |       - RLS
       |       - Queue
       |       - Audit
       |       - Checkpoint
       |
       +---- Protected File Archive
       |
       +---- Model Gateway ---- LLM Provider

Worker:
  Ingestion
  Snapshot
  KPI
  Signal
  Workflow
  LangGraph
  Validator
  Publisher
```

API، Worker و Replay Runner باید از پکیج‌های دامنه مشترک استفاده کنند. با این ساختار، محاسبه KPI در دو محل تکرار نمی‌شود.

## فناوری‌هایی که برای MVP پیشنهاد نمی‌کنم

- Kubernetes: برای یک ماشین و تیم کوچک پیچیدگی اضافی دارد.
- Microservices: مرز شبکه، Deployment و Debug را زیاد می‌کند.
- Redis و Celery: PostgreSQL Queue برای حجم فعلی کافی است.
- Vector Database: نیازمندی RAG یا جست‌وجوی برداری قطعی وجود ندارد.
- Multi-Agent: سند فقط یک Agent محدود را مجاز می‌داند.
- MinIO یا S3 محلی: Protected Volume برای تحویل فعلی کافی است.
- Elasticsearch: Queryهای اصلی ساختاریافته و مبتنی بر PostgreSQL هستند.
- اجرای مستقیم SQL توسط LLM: خطر نشت داده و عدد نادرست ایجاد می‌کند.

## سه تصمیمی که باید قبل از شروع بسته شوند

1. مدل LLM، نسخه مدل و سهم هزینه هر مرحله.
2. مرز دقیق LangGraph شامل Node، State، Retry، Timeout و Checkpoint.
3. رفتار Fallback در زمان قطع یا شکست LLM.

پیشنهاد من برای Fallback این است که KPI، Signal و JSON قطعی تولید شوند. گزارش متنی می‌تواند با Template قطعی ساخته شود. وضعیت Run نیز باید `incomplete` ثبت شود. شکست یک مدیر نباید گزارش معتبر مدیران دیگر را حذف کند.

یک تعارض مهم نیز در اسناد وجود دارد. سند قدیمی‌تر SQLite را پایگاه داده محصول معرفی می‌کند. رجیستر فعال نسخه ۳ و معماری پیشنهادی جدید، PostgreSQL را تنها پایگاه داده محصول می‌دانند. بنابراین مبنای پیاده‌سازی باید PostgreSQL باشد. SQLite فقط Oracle آزمون است.

مبنای حاکمیت اسناد: :codex-file-citation{path="D:\Projects\Arka\Docs\final review\Readme.md" purpose="source"}

معماری پیشنهادی و مرز Containerها: :codex-file-citation{path="D:\Projects\Arka\Docs\final review\proposed-architecture.md" purpose="source"}

تصمیم‌های فعال، PostgreSQL، LangGraph و موارد P0: :codex-file-citation{path="D:\Projects\Arka\Docs\final review\architecture-control-register-v3.md" purpose="source"}

نیازمندی‌های اولیه، محدودیت اجرا، امنیت، RTL و تحویل Docker: :codex-file-citation{path="D:\Projects\Arka\Docs\final review\دیدراه-بریف-۹۱-نیازمندی-هایلایت-و-کامنت.pdf" purpose="source"}