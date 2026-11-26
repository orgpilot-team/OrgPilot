# OrgPilot / DIDRAH

این مخزن محل طراحی و پیاده‌سازی **DIDRAH**، دستیار ایجنتیک مدیران سازمانی، است. سامانه قرار است داده‌های روزانه سازمان را به گزارش‌های مدیریتی فارسی و قابل‌ردیابی تبدیل کند، پرسش‌های محدود به سطح دسترسی مدیر را پاسخ دهد و تصمیم‌ها و اثر آن‌ها را با کنترل انسانی پیگیری کند.

> وضعیت فعلی: معماری، تصمیم‌های فنی، قرارداد پیاده‌سازی و دیتاست ارزیابی مستند شده‌اند؛ پوشه‌های `src/` و `deploy/` هنوز عمدتاً اسکلت هستند. در حال حاضر فایل solution، پروژه قابل build، Dockerfile یا Compose اجرایی در مخزن وجود ندارد.

## از کجا شروع کنیم؟

برای شناخت یا توسعه پروژه، این ترتیب پیشنهاد می‌شود:

1. [هدف و محدوده](docs/Analytics/docs/01-purpose-and-scope.md) را بخوانید.
2. [قرارداد پیاده‌سازی](docs/Analytics/docs/15-implementation-contract.md) را به‌عنوان قواعد الزام‌آور ارزیابی مرور کنید.
3. [نمای کلی معماری](docs/Analytics/docs/02-architecture-overview.md) و مدل [Structurizr](docs/Analytics/workspace.dsl) را ببینید.
4. برای شناخت داده‌ها، [راهنمای فارسی دیتاست آرکا](docs/arka_dataset/README_FA.md) و قراردادهای `docs/arka_dataset/output_contract/` را بخوانید.
5. پیش از تغییر معماری، فرایند اعتبارسنجی در [راهنمای workspace معماری](docs/Analytics/README.md) را اجرا کنید.

برنامهٔ ترتیبی چهار مرحلهٔ نخست پیاده‌سازی بک‌اند در [Backend development stages](docs/DEVELOPMENT_STAGES.md) ثبت شده است. وضعیت و شواهد تکمیل هر مرحله در همان سند به‌روز می‌شود.

## نقشه مخزن

| مسیر | محتوا و کاربرد |
|---|---|
| [`docs/Analytics/`](docs/Analytics/) | منابع فعال معماری: مدل C4، مستندات فنی و ADRها |
| [`docs/arka_dataset/`](docs/arka_dataset/) | دیتاست ساختگی آرکا، تنظیمات KPI و Workflow، ورودی‌های مدیران و schema خروجی ارزیابی |
| [`src/`](src/) | اسکلت اجزای اجرایی محصول؛ هنوز پیاده‌سازی نشده است |
| [`deploy/`](deploy/) | جایگاه تنظیمات PostgreSQL و OpenTelemetry Collector؛ فعلاً placeholder |
| [`.agents/skills/`](.agents/skills/) | دستورها و راهنماهای کمکی برای عامل‌های توسعه؛ بخشی از runtime محصول نیست |
| [`tmp/`](tmp/) | بریف‌ها، برنامه‌ها، exportها و فایل‌های کاری/تاریخی؛ **منبع معتبر تحلیل، توسعه یا استقرار نیست** |

## Frontend Development Setup

The Web Application is in `src/web-app`. The verified environment uses Node.js `24.15.0` and npm `11.12.1`. The frontend supports the Node.js versions declared in `package.json`: Node.js `20.19.0` or later in the 20.x line, or Node.js `22.12.0` or later. Use npm `11.12.1` to match the recorded package-manager version.

The approved frontend stack is:

| Technology | Responsibility |
|---|---|
| React 19 | Component composition and application rendering |
| React DOM 19 | React rendering in the browser |
| TypeScript | Static type checking |
| Vite | Local development, production builds, and build preview |
| Ant Design and Ant Design Icons | UI component foundation and icons under the DIDRAH Design System |
| Motion | Purposeful transitions and micro-interactions |
| Apache ECharts | Rendering authorized chart specifications |
| React Flow | Interactive presentation of Backend-supplied workflow state |

After you clone or pull the repository, run:

```bash
cd src/web-app
npm ci
npm run dev
```

- `npm ci` installs the exact dependency versions in `package-lock.json`. Run it after you clone the repository and when `package-lock.json` changes.
- `npm run dev` starts the local development server.
- `npm run build` creates the optimized production build.
- `npm run preview` serves the production build locally for verification. Run `npm run build` first.

All frontend dependencies are local to `src/web-app`. The `node_modules` and `dist` directories are generated locally and must not be committed. The `package.json` and `package-lock.json` files must remain tracked. Three.js and Modern Mode dependencies are intentionally deferred.

## مستندات و تحلیل معماری

منابع فعال معماری در `docs/Analytics/` قرار دارند:

- [`workspace.dsl`](docs/Analytics/workspace.dsl): منبع اصلی مدل C4، روابط، viewها و deployment model.
- [`docs/`](docs/Analytics/docs/): توضیح معماری و قراردادهای اجرایی.
- [`adrs/`](docs/Analytics/adrs/): تصمیم‌های معماری و دلیل انتخاب آن‌ها.
- [`README.md`](docs/Analytics/README.md): روش parse، validate، اجرای Structurizr Local و تولید artifactها.
- `workspace.json`: snapshot تولیدشده برای Structurizr Local است؛ منبع ویرایش دستی نیست و باید از منابع بالا بازتولید شود.

### راهنمای موضوعی مستندات

| موضوع | سند |
|---|---|
| هدف، محدوده و مرز عامل هوشمند | [01 — Purpose and scope](docs/Analytics/docs/01-purpose-and-scope.md) |
| فناوری‌ها، containerها و قرارداد بین فرایندها | [02 — Architecture overview](docs/Analytics/docs/02-architecture-overview.md) |
| ورود داده، نرمال‌سازی، KPI و پردازش روزانه | [03 — Data and processing](docs/Analytics/docs/03-data-and-processing.md) |
| امنیت، سطح دسترسی و مرزهای اعتماد | [04 — Security and trust](docs/Analytics/docs/04-security-and-trust.md) |
| جریان گزارش شبانه، پرسش، تصمیم و بازیابی | [05 — Runtime flows](docs/Analytics/docs/05-runtime-flows.md) |
| محیط توسعه و پروفایل استقرار ارزیابی | [06 — Deployment and operations](docs/Analytics/docs/06-deployment-and-operations.md) |
| کیفیت، صحت، تکرارپذیری و کارایی | [07 — Quality attributes](docs/Analytics/docs/07-quality-attributes.md) |
| ریسک‌ها و تصمیم‌های باز | [08 — Risks and open issues](docs/Analytics/docs/08-risks-and-open-issues.md) |
| Web Application | [09 — Web application components](docs/Analytics/docs/09-web-application-components.md) |
| Backend API | [10 — Backend API components](docs/Analytics/docs/10-backend-api-components.md) |
| Background Worker | [11 — Background worker components](docs/Analytics/docs/11-background-worker-components.md) |
| Scheduler و Replay | [12 — Scheduler/replay components](docs/Analytics/docs/12-scheduler-replay-components.md) |
| Agent Runtime | [13 — Agent runtime components](docs/Analytics/docs/13-agent-runtime-components.md) |
| Storeها و قراردادهای مشترک | [14 — Stores and contracts](docs/Analytics/docs/14-stores-and-contracts.md) |
| الزامات قطعی ارزیابی و ابهام‌های حل‌شده | [15 — Implementation contract](docs/Analytics/docs/15-implementation-contract.md) |
| مدل دامنه و محدوده استفاده از DDD | [16 — Domain model](docs/Analytics/docs/16-domain-model.md) |
| قرارداد نمودار میان backend و UI | [17 — Chart presentation contract](docs/Analytics/docs/17-chart-presentation-contract.md) |

ADRها از [`0001`](docs/Analytics/adrs/0001-unified-data-intake-and-preparation.md) تا [`0029`](docs/Analytics/adrs/0029-adopt-feature-based-web-application-and-progressive-presentation.md) تصمیم‌هایی مثل PostgreSQL، پردازش deterministic، صف پایدار Agent Job، modular monolith، observability، پروفایل ارزیابی و ECharts را ثبت می‌کنند. وضعیت درج‌شده داخل هر ADR تعیین می‌کند که آن تصمیم پذیرفته شده است یا نه.

## دیتاست و قرارداد خروجی

`docs/arka_dataset/` دیتاست ساختگی شرکت آرکا و ورودی ارزیابی پروژه است:

- `org/`: ساختار سازمان، مدیران، کارکنان و ماتریس دسترسی.
- `config/`: فرهنگ KPI، SQLهای مرجع، آستانه‌ها، اهداف و تعریف Workflowها.
- `calendar/`: تقویم روزها و رویدادهای شبیه‌سازی‌شده.
- `drops/day_XXX/`: ورودی‌های شبانه و manifest هر روز.
- `history/`: تاریخچه تصمیم‌ها و گزارش‌های قدیمی.
- `manager_inputs/` و `uploads/`: پرسش‌ها، تصمیم‌ها، تغییرات و فایل‌های ورودی مدیران.
- `output_contract/`: schema ماشین‌خوان گزارش و پاسخ پرسش‌ها؛ مرجع سطح فیلد برای خروجی submission.

داده‌ها واقعی نیستند. دیتاست از `day_000` تا `day_090` پردازش می‌شود و خروجی ارزیابی باید گزارش‌های صبح `day_062` تا `day_091` را بسازد. جزئیات chronology، داده‌های دیررس، رکورد تکراری، KPIها و قالب خروجی در [README دیتاست](docs/arka_dataset/README_FA.md) آمده است.

## اجزای پیش‌بینی‌شده محصول

ساختار `src/` بر اساس معماری فعلی این مرزها را نشان می‌دهد:

| جزء | مسئولیت | فناوری پیش‌بینی‌شده |
|---|---|---|
| `web-app` | داشبورد، دستیار و کنترل Workflow | React و TypeScript |
| `backend-api` | API، هویت و دسترسی، اعتبارسنجی، انتشار و هماهنگی تحلیل | ASP.NET Core روی .NET 10 |
| `background-worker` | intake، KPI، snapshot، signal، evidence و ارزیابی اثر تصمیم | .NET 10 Worker |
| `scheduler-replay` | زمان‌بندی، replay، ورودی اسکریپت‌شده و acceptance/parity | .NET 10 |
| `agent-runtime` | اجرای graph محدود، conversation و model gateway | Python 3.12، LangGraph و Pydantic |
| `shared-dotnet` | قراردادها و primitiveهای مشترک بدون مالکیت مشترک داده | کتابخانه‌های .NET |

PostgreSQL تنها پایگاه‌داده محصول است. SQLite فقط oracle مرجع داخل acceptance harness است. هسته deterministic مالک محاسبه KPI، قواعد signal، authorization، validation و publication می‌ماند؛ مدل زبانی اجازه ندارد عدد، سطح دسترسی یا تصمیم عملیاتی را تعیین کند.

## منابع معتبر و تقدم آن‌ها

در صورت تعارض، از این ترتیب استفاده کنید:

1. schemaهای ماشین‌خوان در [`docs/arka_dataset/output_contract/`](docs/arka_dataset/output_contract/) برای شکل خروجی؛
2. [قرارداد پیاده‌سازی](docs/Analytics/docs/15-implementation-contract.md) برای الزامات ارزیابی و پاسخ‌های قطعی TA؛
3. مدل فعال [`workspace.dsl`](docs/Analytics/workspace.dsl)، مستندات `docs/Analytics/docs/` و ADRهای پذیرفته‌شده؛
4. تعریف‌های داده و KPI در `docs/arka_dataset/config/`؛
5. بریف اولیه پروژه برای زمینه محصول، فقط تا جایی که با منابع بالاتر تعارض ندارد.

فایل‌های `tmp/` شامل بریف اولیه، planهای معماری، نیازمندی‌های پیشین frontend، خروجی‌های Mermaid و archive دیتاست‌اند. این فایل‌ها سابقه و زمینه مفیدی می‌دهند، اما نباید مبنای مستقیم تحلیل، پیاده‌سازی یا deployment باشند. نسخه استخراج‌شده `docs/arka_dataset/` به‌جای zip دیتاست و مستندات فعال `docs/Analytics/` به‌جای planها و exportهای `tmp/` استفاده می‌شوند.

## قواعد کلیدی پیاده‌سازی

- زمان کسب‌وکار `Asia/Tehran` است و پردازش باید بر اساس business day باشد، نه ساعت میزبان.
- اجرای ارزیابی یک image و یک entrypoint دارد؛ `/data` فقط‌خواندنی و `/submission` نوشتنی است.
- خروجی‌های عددی و signalها در دو اجرای یکسان باید deterministic باشند.
- تنها egress مجاز در ارزیابی API مدل زبانی است؛ شکست مدل نباید تولید گزارش عددی صحیح را متوقف کند.
- گزارش‌ها و UI فارسی و RTL هستند و هر عدد گزارش باید evidence قابل‌ردیابی داشته باشد.
- اقدام سازمانی خودکار خارج از محدوده است؛ تصمیم و ارسال پیام به تأیید صریح انسان نیاز دارد.
- secret نباید وارد مخزن شود؛ پیکربندی مدل از environment variable می‌آید.

## گام بعدی توسعه

پیش از اضافه‌کردن feature، باید foundation قابل اجرا ساخته شود: solution و پروژه‌ها، Compose توسعه، migrationهای PostgreSQL، قراردادهای مشترک، acceptance harness و entrypoint ارزیابی. سپس مسیر deterministic ورود داده و KPI تا تولید JSON قرارداد پیاده‌سازی شود؛ Agent Runtime و UI بعد از تثبیت این مسیر به آن متصل می‌شوند.

هر تغییر معماری باید هم‌زمان در `workspace.dsl`، سند مرتبط و در صورت نیاز ADR ثبت و طبق [راهنمای اعتبارسنجی](docs/Analytics/README.md) بررسی شود. تغییر schema خروجی یا تعریف KPI نیز باید از منبع معتبر خودش شروع شود، نه از کد مصرف‌کننده.
