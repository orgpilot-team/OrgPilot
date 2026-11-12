# معماری پیشنهادی دیدراه

وضعیت سند: **پیشنهاد برای بازبینی تیم**  
تاریخ: ۱۴۰۵/۰۸/۲۱ برابر با 2026-11-12  
دامنه: معماری محصول، داده، امنیت، Agent، اجرا و پذیرش  
مرحله بعد: تبدیل این سند به مدل C4 و پیاده‌سازی در Structurizr

## ۱. هدف سند

این سند معماری پیشنهادی سامانه دیدراه را تعریف می‌کند. این معماری باید نیازمندی‌های بریف، قرارداد دیتاست و تصمیم جدید تیم برای استفاده از PostgreSQL را پوشش دهد.

این سند یک Baseline پیشنهادی است. هنوز همه تصمیم‌ها بسته نشده‌اند. موارد حل‌نشده در بخش «تصمیم‌های باز» ثبت شده‌اند. تیم نباید یک تصمیم باز را به‌عنوان واقعیت قطعی پیاده‌سازی کند.

### ۱.۱. ترتیب اعتبار منابع

در صورت تعارض، ترتیب بررسی چنین است:

1. بریف پروژه و پاسخ رسمی برگزارکننده.
2. قراردادهای ماشین‌خوان دیتاست و فایل‌های ارزیابی.
3. تصمیم‌های ثبت‌شده تیم.
4. این معماری پیشنهادی.
5. اسناد معماری و ممیزی پیشین.

تصمیم جدید تیم این است که **PostgreSQL تنها پایگاه داده محصول باشد**. تصمیم قدیمی SQLite به‌عنوان پایگاه داده محصول منسوخ است. SQLite فقط می‌تواند در آزمون مستقل، برای اجرای SQL مرجع دیتاست، استفاده شود. SQLite بخشی از مسیر Runtime محصول نیست.

### ۱.۲. برچسب وضعیت

در این سند از چهار وضعیت استفاده می‌شود:

- `Requirement`: الزام بریف یا قرارداد عرضه‌شده.
- `Accepted`: تصمیم ثبت‌شده تیم.
- `Proposed`: طراحی پیشنهادی که هنوز به تصویب تیم نیاز دارد.
- `Open`: تصمیم یا قرارداد حل‌نشده.

## ۲. خلاصه معماری

معماری پیشنهادی یک **Modular Monolith** است. Backend API و Background Worker از یک Codebase و مدل دامنه مشترک استفاده می‌کنند، ولی در Processهای جدا اجرا می‌شوند. این تفکیک، مسیر تعاملی مدیر را از پردازش شبانه و Replay جدا می‌کند.

اجزای اصلی عبارت‌اند از:

1. رابط وب فارسی و راست‌به‌چپ.
2. Backend API برای احراز هویت، ورودی مدیر و خواندن خروجی.
3. Background Worker برای دریافت داده، محاسبه، Signal، Workflow، تحلیل و گزارش.
4. PostgreSQL برای داده محصول، Snapshot، KPI، مجوز، گزارش، Audit و Checkpoint.
5. Protected File Archive برای فایل‌های خام و Uploadها.
6. یک LLM Provider که فقط از طریق Model Gateway فراخوانی می‌شود.
7. Replay and Evaluation Runner برای اجرای ۳۰ روز ارزیابی و آزمون پذیرش.

منطق عدد، KPI، Signal، Workflow، مجوز و Validation قطعی است. LLM عدد، مجوز یا Signal تولید نمی‌کند. LLM فقط در تحلیل شواهد مجاز، ساخت پیش‌نویس Insight Brief، نگارش فارسی و پاسخ گفت‌وگویی محدود استفاده می‌شود.

## ۳. اهداف و حدود معماری

### ۳.۱. اهداف

معماری باید این نتایج را فراهم کند:

- دریافت شبانه داده‌های CRM، سفارش، انبار، تیکت، وظایف و منابع عرضه‌شده.
- اجرای SQL ثبت‌شده برای KPIها.
- تولید Signal بدون LLM.
- بازسازی سه Workflow و محاسبه SLA و گلوگاه مرحله.
- تولید گزارش فارسی و JSON برای هر مدیر فعال.
- پاسخ گفت‌وگویی با SQL فقط‌خواندنی و کنترل‌شده.
- کنترل ردیف و ستون برای تمام Queryها.
- جلوگیری از Prompt Injection از متن تیکت و فایل.
- ثبت تصمیم مدیر و ساخت پیش‌نویس اقدام، بدون اجرای خودکار اقدام.
- Replay قابل تکرار روی دیتاست توسعه و دیتاست پنهان.
- اجرای یک روز کامل در حداکثر ۱۵ دقیقه روی ماشین مرجع.
- محدودکردن هزینه LLM هر روز کامل به حداکثر ۵ دلار.

### ۳.۲. خارج از محدوده نسخه اول

- اقدام اجرایی خودکار در سامانه‌های سازمانی.
- رتبه‌بندی یا ارزیابی عملکرد کارکنان.
- پایش حضور، موقعیت یا مرخصی فردی.
- اتصال به سامانه واقعی سازمان.
- Multi-Agent.
- Microserviceهای مستقل.
- Kubernetes.
- Vector Database بدون نیاز اندازه‌گیری‌شده.
- Forecast و What-if به‌عنوان الزام اصلی.
- پیام‌رسان، Voice و گزارش هیئت‌مدیره به‌عنوان الزام پذیرش روزانه.

## ۴. اصول معماری

### ۴.۱. یک منبع حقیقت برای عدد

هر عدد منتشرشده باید به این زنجیره متصل باشد:

`عدد گزارش → QueryRun → تعریف KPI یا Query ثبت‌شده → Snapshot → Fact/Projection → رکورد منبع → فایل و Manifest`

LLM، UI و Serializer اجازه محاسبه یا گردکردن دوباره عدد را ندارند.

### ۴.۲. هسته قطعی، Agent محدود

این اجزا خارج از تصمیم‌گیری Agent هستند:

- دریافت و Parse داده.
- کنترل کیفیت داده.
- Snapshot و Projection.
- محاسبه KPI.
- Signal و Escalation.
- Workflow و SLA.
- مجوز ردیف و ستون.
- کنترل عدد و خروجی.
- انتشار گزارش.

Agent فقط ابزارهای محدود و ازپیش‌تعریف‌شده را فراخوانی می‌کند.

### ۴.۳. مجوز قبل و بعد از LLM

Evidence پیش از ورود به LLM محدود می‌شود. خروجی نیز پیش از انتشار دوباره کنترل می‌شود. LLM هیچ Credential پایگاه داده یا دسترسی مستقیم به فایل ندارد.

### ۴.۴. Snapshot ثابت

هر Run از یک Snapshot ثابت داده، سازمان، مجوز و Configuration استفاده می‌کند. ورود فایل یا تغییر تنظیم در میانه Run نتیجه همان Run را تغییر نمی‌دهد.

### ۴.۵. طراحی برای Replay

Clock محصول باید قابل تزریق باشد. هیچ منطق محصول به تاریخ سیستم، شماره روز خاص، شناسه حادثه یا دیتاست توسعه وابسته نیست.

### ۴.۶. انتشار مستقل و قابل ممیزی

گزارش هر مدیر یک واحد انتشار مستقل است. متن و JSON همان مدیر با هم و به‌صورت Atomic منتشر می‌شوند. شکست گزارش یک مدیر، گزارش معتبر مدیر دیگر را متوقف نمی‌کند. پوشش ناقص روز باید ثبت شود.

### ۴.۷. توسعه با Configuration

افزودن Source، KPI، تیم، واحد یا سطح مدیریتی نباید بازطراحی Pipeline را لازم کند. تغییر باید از Adapter، Registry یا Configuration نسخه‌دار انجام شود.

## ۵. نمای Context پیشنهادی

این عناصر در نمای C4 System Context استفاده خواهند شد.

### ۵.۱. اشخاص

| شناسه پیشنهادی | شخص | تعامل |
|---|---|---|
| `SeniorManager` | مدیر ارشد | گزارش سازمان، Workflowها، موارد تشدیدشده و تصمیم‌ها را می‌بیند. |
| `UnitManager` | مدیر واحد | گزارش واحد و تیم‌های زیرمجموعه را می‌بیند. |
| `TeamSupervisor` | سرپرست تیم | گزارش تیم و داده کاری اعضای مستقیم را در Purpose مجاز می‌بیند. |
| `Evaluator` | مدرس یا ارزیاب | Docker، Replay، خروجی JSON و معیارهای پذیرش را اجرا می‌کند. |
| `Operator` | مسئول فنی | Run، Failure، هزینه، Backup و Restore را پایش می‌کند. |

### ۵.۲. سامانه‌های خارجی

| شناسه پیشنهادی | سامانه | نقش |
|---|---|---|
| `NightlySources` | فایل‌های منبع شبانه | Dropهای CRM، سفارش، انبار، تیکت، وظیفه و منابع دیگر را می‌دهد. |
| `ManagerInputFeed` | ورودی مدیر | سؤال، اولویت، Threshold، Upload، تصمیم و تغییر سازمان را می‌دهد. |
| `IdentityProvider` | منبع هویت | هویت کاربر و Session معتبر را ارائه می‌کند؛ انتخاب محصول یا روش داخلی هنوز باز است. |
| `LLMProvider` | ارائه‌دهنده مدل | تحلیل محدود و نگارش ساختاریافته را انجام می‌دهد. |
| `HiddenDataset` | دیتاست ارزیابی | همان قرارداد داده را با رویدادهای متفاوت ارائه می‌کند. |

### ۵.۳. سامانه اصلی

`DIDRAH` یک دستیار ایجنتیک محدود برای هوش مدیریتی و پشتیبانی تصمیم است. سامانه داده شبانه را پردازش می‌کند، KPI و Workflow را محاسبه می‌کند، Signal می‌سازد، Evidence مجاز را تحلیل می‌کند و گزارش و پاسخ تعاملی می‌دهد.

## ۶. نمای Container پیشنهادی

این Containerها در C4 Container View مدل می‌شوند.

| شناسه پیشنهادی | Container | فناوری پیشنهادی | مسئولیت |
|---|---|---|---|
| `WebApp` | Web UI فارسی RTL | React/Next.js یا معادل مورد تأیید تیم | سه رابط منطقی Assistant، Dashboard و Workflow Control Room را ارائه می‌کند. |
| `BackendApi` | Backend API | Python Web Framework | احراز هویت، AuthContext، ورودی مدیر، Query و تحویل گزارش. |
| `BackgroundWorker` | Worker | Python Worker Process | Ingestion، Snapshot، KPI، Signal، Workflow، Agent flow و Publication job. |
| `SchedulerReplay` | Scheduler و Replay Runner | Process یا Command مستقل در همان Codebase | Clock شبیه‌سازی، اجرای روز، Replay و آزمون. |
| `ProductDatabase` | PostgreSQL | PostgreSQL | تنها پایگاه داده محصول و مسیر Query. |
| `FileArchive` | Protected File Archive | Volume یا Object Storage محلی محافظت‌شده | فایل خام، Upload، Hash و Manifest. |

`ModelGateway` یک Component داخلی مشترک در Codebase است، نه یک Container مستقل. این Component تنها مسیر تماس API یا Worker با `LLMProvider` است. LangGraph نیز Runtime داخلی API و Worker است و Container مستقل اجباری نیست.

سه رابط بریف می‌توانند در یک Web Container پیاده‌سازی شوند. آن‌ها باید Route، Navigation و قرارداد دسترسی روشن داشته باشند:

- دستیار گفت‌وگومحور.
- Dashboard سطح‌بندی‌شده.
- Workflow Control Room ویژه مدیر ارشد.

### ۶.۱. مرز استقرار

`BackendApi`، `BackgroundWorker` و `SchedulerReplay` از یک Artifact و Codebase استفاده می‌کنند. آن‌ها Processهای مستقل هستند. این طراحی یک Distributed System کامل ایجاد نمی‌کند.

در نسخه تحویل، Docker Compose حداقل این سرویس‌ها را اجرا می‌کند:

- Web.
- API.
- Worker.
- PostgreSQL.

Scheduler می‌تواند به‌صورت Command در Container Worker اجرا شود. Archive و PostgreSQL از Volumeهای پایدار استفاده می‌کنند.

### ۶.۲. قواعد استقرار پیشنهادی

- Web فقط Backend API را فراخوانی می‌کند و اتصال مستقیم به PostgreSQL ندارد.
- PostgreSQL و Archive در شبکه یا مرز Data قرار می‌گیرند و از بیرون منتشر نمی‌شوند.
- API و Worker از Roleهای جدا برای PostgreSQL استفاده می‌کنند.
- Migration پیش از Readyشدن API و Worker اجرا و نسخه آن ثبت می‌شود.
- Secretها در Image، Repository، Prompt یا Log ذخیره نمی‌شوند.
- Job queue نسخه اول می‌تواند در PostgreSQL باشد. Claim کار با Lease و الگوی `FOR UPDATE SKIP LOCKED` انجام می‌شود.
- Timezone کسب‌وکار `Asia/Tehran` است. Timestamp فنی با Offset یا UTC ذخیره می‌شود. Business date شمسی و Drop day جدا نگهداری می‌شوند.
- Encoding تمام فایل‌ها و خروجی‌ها UTF-8 است.
- محیط توسعه و ارزیابی از همان Imageها و Migrationها استفاده می‌کنند.

## ۷. اجزای داخلی Backend و Worker

این اجزا در مرحله بعد در Component View مدل می‌شوند.

### ۷.۱. اجزای Backend API

| شناسه پیشنهادی | جزء | مسئولیت |
|---|---|---|
| `IdentityBoundary` | Identity Boundary | احراز هویت و ساخت AuthContext از هویت معتبر. |
| `AuthorizationService` | Authorization Service | محاسبه Scope، Purpose و Policy Bundle. |
| `ManagerInputService` | Manager Input Service | دریافت سؤال، اولویت، تنظیم، Upload، تصمیم و تغییر سازمان. |
| `QueryGateway` | Query Gateway | کنترل و اجرای SQL فقط‌خواندنی با RLS. |
| `ReportApi` | Report API | خواندن نسخه مجاز گزارش، Dashboard و Workflow. |
| `DecisionTracker` | Decision Tracker | ثبت تصمیم، ارجاع، بستن و Draft اقدام. |
| `ConfigurationService` | Configuration Service | ساخت و فعال‌سازی نسخه تنظیمات مجاز. |
| `ModelGateway` | Model Gateway | اعمال Budget، Timeout، Token log و تماس کنترل‌شده با LLM Provider. |

### ۷.۲. اجزای Worker

| شناسه پیشنهادی | جزء | مسئولیت |
|---|---|---|
| `IngestionCoordinator` | هماهنگ‌کننده دریافت | کنترل Manifest، Idempotency، Hash و وضعیت Source. |
| `SourceAdapters` | Adapterهای منبع | Parse و نگاشت Schema نسخه‌دار. |
| `DataQualityService` | کیفیت داده | ثبت Missing، Duplicate، Late Arrival، Correction و Schema Change. |
| `SnapshotService` | Snapshot | ثابت‌کردن Cutoff و نسخه‌های داده و تنظیم. |
| `ProjectionService` | Projection | ساخت Factها و Projectionهای قابل بازسازی. |
| `SemanticRegistry` | Semantic Registry | نگهداری تعریف KPI، واحد، هدف، مالک، SQL و Dependency. |
| `ReferenceCalculator` | محاسبه‌گر KPI | اجرای SQL ثبت‌شده PostgreSQL و ثبت QueryRun. |
| `SignalEngine` | موتور Signal | تشخیص قطعی، Episode، Suppression و Escalation. |
| `WorkflowEngine` | موتور Workflow | بازسازی Case، Stage، SLA و Bottleneck. |
| `EvidenceService` | Evidence Service | ساخت EvidenceBundle محدود به Scope. |
| `AgentOrchestrator` | هماهنگ‌کننده Agent | اجرای Graph گزارش و Graph تعاملی. |
| `OutputValidator` | کنترل خروجی | کنترل عدد، Query، Scope، Schema، Evidence، لحن و Recurrence. |
| `Publisher` | Publisher | انتشار Atomic متن و JSON و ثبت Failure. |
| `EvaluationService` | ارزیابی | محاسبه پوشش، صحت، کشف، نشت، زمان و هزینه. |

`ModelGateway` و قراردادهای Agent می‌توانند به‌صورت Package مشترک میان API و Worker استفاده شوند. هر Process باید Budget و Audit مشترک روز را از PostgreSQL بخواند؛ Restart نباید سقف هزینه را Reset کند.

## ۸. معماری داده PostgreSQL

### ۸.۱. نقش PostgreSQL

`Accepted`: PostgreSQL تنها موتور پایگاه داده محصول است. موارد زیر در PostgreSQL اجرا یا ذخیره می‌شوند:

- داده استاندارد و Projectionها.
- Snapshot و نسخه‌های Configuration.
- اجرای همه KPIهای محصول.
- Queryهای تعاملی و Text-to-SQL.
- سازمان، Scope و Policy.
- Signal، Workflow و Decision.
- Insight، Report، Query Receipt و Audit.
- LangGraph Checkpoint.

فایل خام در Archive نگهداری می‌شود. Archive پایگاه داده دوم و مسیر Query مدیر نیست.

### ۸.۲. Schemaهای منطقی پیشنهادی

| Schema | محتوا |
|---|---|
| `ingest` | Batch، Manifest، SourceStatus، SchemaVersion و DataIssue. |
| `core` | موجودیت‌ها، رویدادها و Factهای استاندارد. |
| `org` | OrgNode، OrgEdgeVersion، Manager و AccessGrantVersion. |
| `semantic` | KpiDefinition، KpiVersion، Target، Threshold و Dependency. |
| `analytics` | Snapshot، KpiObservation، QueryRun، SignalEpisode و Evidence. |
| `workflow` | WorkflowDefinition، Case، StageObservation و SLA result. |
| `reporting` | InsightVersion، ReportVersion، ReportItem و PublicationReceipt. |
| `decision` | DecisionEvent، ActionDraft و FollowUpObservation. |
| `agent` | Thread، Checkpoint، ModelCall و BudgetLedger. |
| `audit` | Security event، Config change، Job outcome و Validation receipt. |

نام نهایی Schemaها `Proposed` است. مرز مالکیت آن‌ها مهم‌تر از نام است.

### ۸.۳. موجودیت‌های اصلی

- `SourceFile`: Hash، مسیر Archive، Source، Drop و زمان دریافت.
- `BatchReceipt`: نتیجه دریافت و Idempotency.
- `Snapshot`: Cutoff داده، سازمان، Policy و Configuration.
- `KpiDefinitionVersion`: تعریف، SQL، واحد، Precision، Target و Owner.
- `KpiObservation`: مقدار یا Null، Entity، Dimension، تاریخ و QueryRun.
- `DataIssue`: نوع مسئله، Source، تاریخ و اثر.
- `SignalEpisode`: سری، Rule version، Owner، Severity و تاریخچه گیرنده.
- `WorkflowObservation`: Case، Stage، زمان، SLA و Bottleneck evidence.
- `EvidenceBundle`: Fact، Query، محدودیت، تعارض و DataIssue.
- `InsightVersion`: خلاصه، علت‌ها، Confidence، گزینه‌ها و Evidence.
- `ReportVersion`: مدیر، روز، متن، JSON، Snapshot و Validation.
- `DecisionEvent`: Actor، انتخاب، زمان، معیار موفقیت و Draft.
- `QueryReceipt`: SQL، Params، Principal، Purpose، Snapshot، Row count و Result hash.

### ۸.۴. زمان و نسخه

رکوردهای حساس باید حداقل این دو زمان را جدا کنند:

- `effective_at`: زمان اثر در کسب‌وکار یا Replay.
- `known_at`: زمانی که سامانه از رکورد آگاه شد.

این تفکیک برای اصلاح تاریخی، Late Arrival، تغییر سازمان و جلوگیری از نشت آینده لازم است.

گزارش منتشرشده Immutable است. اصلاح بعدی نسخه جدید می‌سازد و به نسخه قبلی با `supersedes` متصل می‌شود.

## ۹. دریافت داده و Replay

### ۹.۱. جریان دریافت

1. Scheduler یک Drop را بر اساس Clock شبیه‌سازی‌شده فعال می‌کند.
2. IngestionCoordinator فایل‌ها و Manifest را شناسایی می‌کند.
3. فایل اصلی پیش از Parse در Archive ثبت و Hash می‌شود.
4. SourceAdapter بر اساس SchemaVersion فایل را Parse می‌کند.
5. ردیف معتبر و ردیف ردشده جدا ثبت می‌شوند.
6. DataQualityService مسئله داده را ثبت می‌کند.
7. Batch به‌صورت Atomic Commit می‌شود.
8. ProjectionService Projectionهای لازم را می‌سازد یا به‌روزرسانی می‌کند.

### ۹.۲. قواعد دریافت

- فایل خام تغییر نمی‌کند.
- اجرای دوباره همان Batch نتیجه دوم ایجاد نمی‌کند.
- Duplicate فنی با Duplicate کسب‌وکار یکی نیست.
- Missing Source اجرای کل روز را متوقف نمی‌کند.
- Schema ناشناخته به حدس و Parse خاموش منجر نمی‌شود.
- Data Issue به‌تنهایی Business Signal نیست.
- مقدار ناموجود با صفر جایگزین نمی‌شود.

### ۹.۳. Clock ارزیابی

- `day_000` بار اولیه است.
- روزهای ۱ تا ۶۰ تاریخچه هستند.
- گزارش صبح `R` فقط Dropهای `000..R-1` را می‌بیند.
- اجرای ارزیابی، صبح‌های ۶۲ تا ۹۱ را تولید می‌کند.
- ورودی مدیر در روز `D` روی گزارش `D+1` اثر می‌گذارد.
- پرسش روز `D` داده Dropهای تا `D-1` را می‌بیند.

این قواعد از قرارداد دیتاست می‌آیند و `Requirement` هستند.

## ۱۰. Semantic Layer و KPI

### ۱۰.۱. تعریف KPI

۵۵ تعریف عرضه‌شده منبع حقیقت هستند. هر تعریف شامل این موارد است:

- شناسه.
- Entity و Dimension.
- واحد و جهت.
- Target، Warn و Crit.
- Rule.
- Owner.
- SQL مرجع.
- Precision و قاعده گردکردن.
- مهلت تشدید.

عدد حدود ۱۵۰ در بریف، هدف تعداد KPI نیست. ۵۵ تعریف می‌توانند سری‌ها و Observationهای بیشتری تولید کنند.

### ۱۰.۲. انتقال SQL مرجع به PostgreSQL

SQL عرضه‌شده با Dialect SQLite است. محصول باید نسخه PostgreSQL هر Query را ثبت کند.

برای هر KPI این اطلاعات نگهداری می‌شود:

- Hash مربوط به SQL اصلی SQLite.
- SQL تبدیل‌شده PostgreSQL.
- نسخه تبدیل.
- Fixtureهای Parity.
- نتیجه مقایسه Row set، Null، Precision و Value.
- وضعیت پذیرش.

SQLite فقط در Test Harness مستقل نقش Oracle مرجع دارد. Runtime محصول هیچ Query محصول را در SQLite اجرا نمی‌کند.

### ۱۰.۳. قواعد محاسبه

- گردکردن فقط طبق قرارداد KPI انجام می‌شود.
- UI و LLM مقدار را دوباره گرد نمی‌کنند.
- نبود ردیف، Null و صفر سه وضعیت متفاوت هستند.
- Rate از صورت و مخرج محاسبه می‌شود.
- Average از Sum و Count محاسبه می‌شود.
- Median از Observationهای اصلی محاسبه می‌شود.
- مقدارهای گرد‌شده فرزند برای Rollup استفاده نمی‌شوند.
- Breakdown جدید یک Query ثبت‌شده مستقل می‌خواهد.

### ۱۰.۴. Recalculation

نسخه اول می‌تواند هر صبح همه ۵۵ Query را برای Snapshot ثابت اجرا کند. درستی از بهینه‌سازی مهم‌تر است.

Selective Recalculation فقط بعد از Benchmark و آزمون برابری با Full Rebuild فعال می‌شود. اگر Dependency دقیق معلوم نیست، بازسازی گسترده‌تر مجاز است. حذف اثر واقعی مجاز نیست.

## ۱۱. Signal و Workflow

### ۱۱.۱. Signal Engine

Signal Engine قطعی است و قواعد R1 تا R8 را اجرا می‌کند. ورودی آن KPI واجد شرایط، Baseline، Calendar، RuleVersion و تاریخچه گیرنده است.

State داخلی پیشنهادی:

- `candidate`
- `owned`
- `open`
- `suppressed`
- `escalated`
- `resolved`
- `data_blocked`

این Stateها داخلی هستند. آن‌ها نباید بدون قرارداد به Enum خروجی JSON تبدیل شوند.

Signal برای هر گیرنده تاریخچه جدا دارد:

- اولین مشاهده.
- آخرین ارسال.
- مقدار نخست.
- مقدار آخر.
- دلیل تشدید.
- نسخه Rule.

### ۱۱.۲. انتخاب حداکثر پنج مورد

ترتیب پیشنهادی انتخاب:

1. شدت انحراف.
2. اثر مشتری.
3. اثر مالی پشتیبانی‌شده.
4. بین‌واحدی بودن.
5. Confidence شواهد.
6. اولویت ثبت‌شده مدیر.

وزن دقیق این عوامل `Open` است. اولویت مدیر نمی‌تواند دسترسی را گسترش دهد یا Data Issue را پنهان کند.

### ۱۱.۳. Workflow Engine

سه Workflow عرضه‌شده عبارت‌اند از:

- سفارش تا تحویل.
- شکایت تا حل.
- سرنخ تا قرارداد سازمانی.

Workflow Engine از Event Log این موارد را تولید می‌کند:

- Case و مسیر طی‌شده.
- Stage جاری.
- زمان انتظار.
- درصد SLA.
- Backlog.
- Bottleneck.
- ترتیب نامعتبر یا Stage مفقود.

Case باز با مدت صفر یا Case کامل فرض نمی‌شود. SLA مفقود نیز صفر نیست.

## ۱۲. تحلیل، Evidence و Agent

### ۱۲.۱. Evidence Bundle

EvidenceService پیش از فراخوانی LLM یک بسته محدود می‌سازد. بسته می‌تواند شامل این موارد باشد:

- KPI و Query مرجع.
- Drill-down مجاز.
- Workflow evidence.
- Calendar context.
- ظرفیت تجمیعی تیم.
- تصمیم‌های گذشته.
- Data Issue.
- محدودیت و تعارض.

هر Fact به Query، Snapshot و Source pointer متصل است.

### ۱۲.۲. یک Agent و دو Graph

معماری از یک Agent محدود و دو Graph استفاده می‌کند:

1. `ManagerReportGraph`: تحلیل Evidence، ساخت Insight، نگارش، Validation و Repair محدود.
2. `InteractiveAssistantGraph`: سؤال، Clarification، تولید SQL نامزد، اجرای کنترل‌شده و پاسخ.

Ingestion، KPI، Signal، Workflow، Authorization و Publication Node تصمیم‌گیر Agent نیستند. آن‌ها Tool یا Service قطعی هستند.

### ۱۲.۳. State و Checkpoint

State فقط Reference نگه می‌دارد:

- `run_id`
- `thread_id`
- `manager_id`
- `report_day`
- `snapshot_id`
- `policy_bundle_id`
- `evidence_bundle_id`
- `draft_version_id`
- `budget_usage`
- `validation_result`
- `error_code`

Raw row، Credential و SQL privilege در State قرار نمی‌گیرند. Checkpoint در PostgreSQL ذخیره می‌شود.

### ۱۲.۴. ابزارهای Agent

ابزارهای مجاز پیشنهادی:

- `read_kpi`
- `query_scoped_data`
- `read_workflow`
- `read_calendar_context`
- `read_decision_history`
- `propose_action_draft`

ابزار ارسال پیام، تغییر هدف، جابه‌جایی نیرو، ویرایش Source یا اجرای اقدام سازمانی وجود ندارد.

## ۱۳. Text-to-SQL و Query Gateway

### ۱۳.۱. جریان پیشنهادی

1. مدیر سؤال را ارسال می‌کند.
2. Backend از Session معتبر `AuthContext` می‌سازد.
3. Agent در صورت ابهام سؤال Clarification می‌خواهد.
4. Agent یک SQL نامزد و QuerySpec ساختارمند تولید می‌کند.
5. QueryGateway SQL را Parse و AST را کنترل می‌کند.
6. QueryGateway Scope و Purpose را به‌صورت Server-side اعمال می‌کند.
7. Query با Role فقط‌خواندنی و RLS اجباری اجرا می‌شود.
8. نتیجه، SQL واقعی، Params و QueryReceipt ثبت می‌شوند.
9. پاسخ فارسی و JSON از نتیجه واقعی ساخته می‌شوند.
10. Query ID و SQL نهایی اجراشده، در حد مجاز، کنار پاسخ نمایش داده می‌شوند.

### ۱۳.۲. قواعد SQL تعاملی

- فقط یک Statement از نوع `SELECT` مجاز است.
- DDL، DML، COPY، SET، CALL و Transaction control رد می‌شوند.
- Relation و Function باید در Allowlist باشند.
- Schemaهای داخلی، Audit و Raw در دسترس نیستند.
- Query دارای Statement Timeout است.
- تعداد ردیف و حجم نتیجه محدود است.
- Query Plan و Error نباید اطلاعات خارج Scope را افشا کنند.
- SQL اجراشده با SQL پیشنهادی اجرا‌نشده اشتباه نمی‌شود.
- SQL و نتیجه با Principal، Purpose، Snapshot و Policy ثبت می‌شوند.

## ۱۴. امنیت و کنترل دسترسی

### ۱۴.۱. مدل اعتماد

این ورودی‌ها غیرقابل اعتماد هستند:

- فایل‌های Source.
- متن Ticket.
- Upload مدیر.
- Prompt کاربر.
- خروجی LLM.

این ورودی‌ها نمی‌توانند Policy، Credential، مقصد گزارش، عدد یا Tool مجاز را تغییر دهند.

### ۱۴.۲. کنترل دسترسی PostgreSQL

`Requirement`: کنترل ردیف برای تمام Queryهای مدیر و گفت‌وگو باید در لایه داده اعمال شود. `Proposed`: PostgreSQL RLS کنترل اصلی ردیف باشد و Query Gateway کنترل‌های تکمیلی را اعمال کند.

طراحی پیشنهادی:

- جدول‌های حساس دارای RLS Policy هستند.
- جدول‌های Report، Query receipt و Artifact metadata نیز بر اساس گیرنده و Purpose کنترل می‌شوند.
- `FORCE ROW LEVEL SECURITY` فعال است.
- Role مسیر Query، Owner جدول نیست.
- Role مسیر Query `SUPERUSER` یا `BYPASSRLS` نیست.
- Principal و Purpose با `SET LOCAL` و فقط توسط Backend معتبر تنظیم می‌شوند.
- SQL کاربر اجازه اجرای `SET`, `SET ROLE` یا `set_config` ندارد.
- Connection Pool در پایان Transaction Context را پاک می‌کند.
- Viewهای Query ترجیحاً `security_invoker` هستند.
- ستون‌های حساس فقط از Projectionهای تأییدشده ارائه می‌شوند.
- Batch Role از Query Role جدا است.
- LLM Credential مستقیم ندارد.

Roleهای اولیه پیشنهادی:

- `migration_owner`: مالک Migration و Objectها؛ برای Runtime استفاده نمی‌شود.
- `ingestion_writer`: نوشتن Batch و داده استاندارد در محدوده مشخص.
- `analytics_worker`: اجرای محاسبات ثبت‌شده و نوشتن Observationها.
- `application_api`: خواندن و نوشتن عملیات مجاز API.
- `agent_query_reader`: اجرای Query تعاملی فقط‌خواندنی با RLS.
- `audit_reader`: خواندن Audit برای نقش عملیاتی مجاز.

نام Roleها پیشنهادی است. جداسازی مالکیت و Privilege الزام طراحی است.

### ۱۴.۳. سطح دسترسی نقش‌ها

- مدیر ارشد: داده تجمیعی سازمان و واحدها؛ بدون داده فردی کارکنان.
- مدیر واحد: داده تجمیعی واحد و تیم‌ها؛ بدون داده فردی کارکنان.
- سرپرست: داده تیم و داده کاری اعضای مستقیم، فقط برای مدیریت بار کار.
- مرخصی و Availability در تحلیل سطوح بالاتر فقط ظرفیت تجمیعی است.

بالابودن در سلسله‌مراتب به معنی مجوز داده فردی نیست.

### ۱۴.۴. دفاع چندلایه

RLS تنها کنترل نیست. این کنترل‌ها نیز لازم‌اند:

- Relation allowlist.
- Column projection.
- AST validation.
- Purpose check.
- Evidence filtering.
- Output validation.
- Scope-aware cache.
- Audit log.
- آزمون نشت منفی برای هر نقش.

## ۱۵. Insight Brief و گزارش

### ۱۵.۱. مدل داخلی Insight Brief

هر Insight Brief باید این هشت بخش را داشته باشد:

1. خلاصه و اثر.
2. KPI و انحراف.
3. Breakdown.
4. علت‌های محتمل و Confidence.
5. گزینه‌های تصمیم.
6. سابقه و تصمیم‌های قبلی.
7. مالک پیشنهادی.
8. Queryهای مرجع.

هر علت منتشرشده حداقل دو گروه Evidence مستقل، محدودیت و علت جایگزین می‌خواهد. همبستگی به‌عنوان علیت نوشته نمی‌شود.

### ۱۵.۲. مدل گزارش مدیر

هر Package حداقل شامل این موارد است:

- سلامت Scope.
- حداکثر پنج مورد مهم.
- Signal، عدد، Target، علت، Confidence و Owner.
- ChartSpec.
- DecisionCard برای مورد مهم یا Escalated.
- تصمیم‌های منتظر.
- اقدام‌های باز و Deadline.
- اثر مشاهده‌شده تصمیم قبلی.
- Data Issues.
- لینک Dashboard.

### ۱۵.۳. Projection نقش‌ها

- مدیر ارشد: پنج KPI کلیدی، سه Workflow، Bottleneck، Escalation و اثر تصمیم.
- مدیر واحد: وضعیت دو تیم، Signal واحد، وابستگی بین‌واحدی و تصمیم‌ها.
- سرپرست: کارهای تیم، Backlog، Blocker، بار کار مجاز و اقدام‌های درخواستی.

همه Projectionها از Insight و Evidence مشترک ساخته می‌شوند، ولی Scope گیرنده جدا اعمال می‌شود. Insight مشترک مجوز مشترک ایجاد نمی‌کند.

### ۱۵.۴. خروجی ماشین‌خوان

فایل خروجی مطابق مسیر و Schema عرضه‌شده تولید می‌شود:

`submission/briefs/day_XXX/<manager_id>.json`

متن فارسی و JSON از یک مدل محتوای Validation‌شده ساخته می‌شوند. هر عدد متن باید در JSON به `query_id` و KPI مربوط متصل باشد.

تعارض `suppressed` در بریف و `ongoing` در Schema رسمی هنوز `Open` است. تا حل رسمی:

- State داخلی Suppression حفظ می‌شود.
- Enum نامعتبر به JSON اضافه نمی‌شود.
- مورد بدون تغییر در `open_items` یا محل مورد تأیید Schema نگهداری می‌شود.
- نگاشت نهایی باید در EvaluationProfile نسخه‌دار شود.

## ۱۶. تصمیم و پیگیری

سامانه گزینه پیشنهاد می‌دهد. مدیر تصمیم می‌گیرد.

پس از تصمیم معتبر مدیر:

1. DecisionEvent ثبت می‌شود.
2. ActionDraft ساخته می‌شود.
3. مدیر Draft را تأیید و خودش ارسال می‌کند.
4. سامانه Observationهای بعدی را با معیار موفقیت مقایسه می‌کند.
5. نتیجه به‌عنوان بهبود، بدترشدن، بدون تغییر یا زودبودن ارزیابی ثبت می‌شود.

ثبت Decision اجرای واقعی اقدام را اثبات نمی‌کند. داده Replay ثابت است و به تصمیم تیم واکنش پویا نشان نمی‌دهد.

## ۱۷. جریان شبانه

جریان مرجع اجرای روز:

1. Scheduler، Clock و EvaluationProfile را ثابت می‌کند.
2. Scheduler یک Run Lease در PostgreSQL می‌گیرد تا دو اجرای همان روز هم‌زمان فعال نشوند.
3. Dropهای مجاز دریافت و Archive می‌شوند.
4. Batchهای معتبر Commit می‌شوند.
5. Snapshot داده، سازمان، Policy و Config ساخته می‌شود.
6. Projectionها ساخته یا تکمیل می‌شوند.
7. همه KPIهای Canonical اجرا می‌شوند.
8. Workflowها بازسازی می‌شوند.
9. Signalها و Episodeها محاسبه می‌شوند.
10. برای هر مدیر فعال، Signalهای مجاز انتخاب می‌شوند.
11. EvidenceBundle مجاز ساخته می‌شود.
12. Agent Insight و Draft را می‌سازد.
13. OutputValidator عدد، Scope، Evidence، Schema و Recurrence را کنترل می‌کند.
14. Package معتبر همان مدیر Atomic منتشر می‌شود.
15. Failure مدیر دیگر ثبت می‌شود و مانع انتشار Package معتبر نمی‌شود.
16. DayRunOutcome پوشش، زمان، هزینه و Failureها را ثبت می‌کند.

## ۱۸. جریان تعاملی مدیر

### ۱۸.۱. سؤال

`Manager → Web → API → Agent → QueryGateway → PostgreSQL → Agent → Validator → Manager`

### ۱۸.۲. تغییر تنظیم

`Manager → API → ConfigurationService → Validation → Candidate Version → Approval → Effective Version`

تغییر فرمول Canonical موجود با Overwrite خام انجام نمی‌شود. نسخه قبلی حفظ می‌شود.

### ۱۸.۳. تصمیم

`Manager → API → DecisionTracker → DecisionEvent → ActionDraft → Manager Confirmation`

هیچ مرحله‌ای پیام یا وظیفه را بدون تأیید مدیر ارسال نمی‌کند.

## ۱۹. خطا و بازیابی

| خطا | رفتار پیشنهادی |
|---|---|
| Source مفقود | DataIssue ثبت شود؛ Scope سالم ادامه دهد؛ مقدار ناموجود Null باشد. |
| Schema ناشناخته | فایل Quarantine شود؛ SourceStatus نامعتبر باشد؛ حدس زده نشود. |
| KPI Query ناموفق | مقدار ساخته نشود؛ Query failure و اثر آن ثبت شود. |
| LLM ناموفق | Retry محدود؛ سپس Fallback معتبر یا Failure صریح. |
| Budget تمام‌شده | فراخوانی جدید متوقف و Failure ثبت شود. |
| Validation ناموفق | خروجی منتشر نشود؛ Repair محدود با همان Snapshot انجام شود. |
| گزارش یک مدیر ناموفق | گزارش معتبر مدیران دیگر منتشر شود؛ روز ناقص بماند. |
| Worker متوقف‌شده | Run از Checkpoint و Idempotency key ادامه یابد. |

Retry همان Idempotency key را حفظ می‌کند. Retry نباید Report، Signal یا Decision تکراری بسازد.

### ۱۹.۱. Backup و Restore

Backup باید PostgreSQL و Archive Manifest را در یک Checkpoint سازگار نگه دارد. Restore زمانی معتبر است که:

- Hash فایل‌ها برابر باشد.
- Snapshot قابل بازسازی باشد.
- Query مرجع نمونه نتیجه برابر بدهد.
- گزارش نمونه با Snapshot و نسخه یکسان بازتولید شود.

Retention و دوره Backup هنوز `Open` هستند.

## ۲۰. مشاهده‌پذیری و Audit

برای هر Run این اطلاعات ثبت می‌شوند:

- زمان هر Stage.
- تعداد فایل و ردیف پذیرفته یا ردشده.
- Queryهای موفق و ناموفق.
- تعداد KPI Observation.
- Signal جدید، Escalated و Suppressed.
- گزارش موفق و ناموفق.
- Token و هزینه هر Model call.
- تعداد Retry و Repair.
- Scope refusal و Access denial.
- Result hash و Artifact version.

Log نباید داده خارج Scope، SQL دارای پارامتر حساس یا متن فردی نامجاز را برای نقش عادی آشکار کند.

نسخه اول می‌تواند Log و Metric را از API، Worker و PostgreSQL جمع کند. انتخاب Stack مشاهده‌پذیری باز است. Health و Readiness حداقل باید این موارد را جدا گزارش کنند:

- API.
- Worker و Run Lease.
- PostgreSQL و Migration version.
- Archive write/read.
- LLM Provider و Model Gateway.

Job ناموفق پس از Retry محدود باید به Dead-letter state برود و برای Operator قابل مشاهده باشد.

## ۲۱. اهداف غیرعملکردی و معیار پذیرش

| معیار | هدف |
|---|---|
| پوشش | هر صبح برای هر مدیر فعال یک گزارش. |
| زمان | یک روز کامل حداکثر ۱۵ دقیقه روی ماشین مرجع. |
| هزینه LLM | حداکثر ۵ دلار برای همه گزارش‌ها، تحلیل‌ها، QA و Retry همان روز. |
| درستی عدد | صفر عدد نادرست پس از گردکردن مرجع. |
| امنیت | صفر نشت داده در سه سطح مدیریت. |
| کشف | حداقل ۹۰٪ رویدادهای کاشته‌شده در ۲۴ ساعت و برای مالک درست. |
| گفت‌وگو | حداقل ۸۵٪ دقت روی پرسش‌ها، شامل Refusal درست. |
| Workflow | هر سه Workflow با SLA و Bottleneck مرحله. |
| خروجی | متن فارسی RTL و JSON معتبر برای هر Package. |
| تعمیم | اجرای دیتاست پنهان بدون تغییر کد. |
| تحویل | اجرای سامانه با یک دستور Docker. |

حدود عددی باید در EvaluationProfile ثبت شوند، زیرا بریف اجازه نهایی‌شدن آن‌ها توسط برگزارکننده را می‌دهد.

## ۲۲. تصمیم‌های باز

### ۲۲.۱. P0؛ پیش از تثبیت Baseline معماری

1. قرارداد تبدیل و Parity هر ۵۵ SQL از SQLite مرجع به PostgreSQL.
2. ماتریس دقیق Row/Column Projection برای منابع مشترک.
3. سیاست RLS و نقش‌های PostgreSQL برای Batch، API، Query و Audit.
4. قرارداد کامل مدل داخلی Insight Brief، Report و DecisionCard.
5. نگاشت رسمی `suppressed` بریف به `ongoing/open_items` در Schema عرضه‌شده.
6. حالت‌های مرزی Signal: تساوی Threshold، مخرج صفر، Reset، Recovery و Owner غیرفعال.
7. مالک هر Stage در سه Workflow و رفتار Stage فاقد SLA.
8. قرارداد Canonical نوع داده، Null، زمان و تغییر نام ستون‌ها.
9. اختیار تغییر Config، مرحله Approval، زمان فعال‌سازی و Rollback.
10. State Machine مربوط به Job، Retry، Timeout، Repair و Fallback.

### ۲۲.۲. P1؛ پیش از Replay کامل

1. Model Provider و مدل‌های مجاز.
2. تقسیم Budget میان تحلیل، گزارش، QA و Reserve.
3. سیاست Cache و عمر آن.
4. سیاست Last Valid Value و نمایش تاریخ واقعی آن.
5. قرارداد Restatement و اعلان اصلاح گزارش گذشته.
6. Retention، Backup interval و RPO/RTO.
7. فرمت‌های Upload مجاز و پشتیبانی PDF/Excel.
8. وزن Ranking حداکثر پنج مورد.
9. الگوریتم نسخه‌دار Confidence.
10. Index و Pool configuration پس از Benchmark.
11. روش Authentication و منبع Identity.
12. نسخه دقیق PostgreSQL.
13. Availability، SLO پاسخ گفت‌وگو، RPO و RTO.
14. نیاز یا عدم نیاز به HA در محیط هدف.
15. Stack مشاهده‌پذیری و محل نگهداری Artifactهای نمودار.

### ۲۲.۳. P2؛ پیش از تحویل نهایی

1. Visibility مخزن و دسترسی ارزیاب.
2. Hardware Profile نهایی.
3. حدود نهایی ۱۵ دقیقه، ۵ دلار و ۸۵٪ در صورت تغییر برگزارکننده.
4. قالب گزارش هزینه و چک‌لیست Demo Day.

## ۲۳. ریسک‌های اصلی

| ریسک | اثر | کنترل پیشنهادی |
|---|---|---|
| اختلاف SQL SQLite و PostgreSQL | عدد نادرست و شکست پذیرش | Parity suite برای هر ۵۵ تعریف. |
| دورزدن RLS در Text-to-SQL | نشت داده | Role جدا، FORCE RLS، AST validation و آزمون منفی. |
| Prompt Injection | تغییر رفتار Agent | ورودی به‌عنوان Data، Tool allowlist و کنترل خروجی. |
| پیچیدگی بیش از ظرفیت تیم | تأخیر در MVP | Modular Monolith و تعویق زیرساخت غیرضروری. |
| LLM کند یا گران | شکست زمان و هزینه | Budget reservation، Timeout و تحلیل محدود. |
| Data Issue به‌عنوان Signal | هشدار کاذب | جداسازی DQ از Signal eligibility. |
| گزارش ناقص ولی معتبر از نظر Schema | شکست معنایی | Validator داخلی سخت‌تر از JSON Schema. |
| Hardcode روی دیتاست توسعه | شکست دیتاست پنهان | Clock تزریقی، Configuration و hidden-like fixtures. |
| نشت آینده در Replay | نتیجه غیرواقعی | known_at، cutoff و Snapshot ثابت. |

## ۲۴. مسیر پیشنهادی پیاده‌سازی

### فاز ۰: بستن تصمیم‌های P0

خروجی: ADRهای تصویب‌شده، EvaluationProfile و Baseline این سند.

### فاز ۱: ستون فقرات داده

خروجی:

- Archive و Ingestion.
- PostgreSQL schema و Migration.
- Snapshot و Projection.
- Organization و RLS اولیه.
- Replay Clock.

### فاز ۲: یک روز کامل قطعی

خروجی:

- همه ۵۵ KPI در PostgreSQL.
- Parity suite.
- Signal پایه.
- یک Report end-to-end.
- سپس Report همه مدیران فعال.

### فاز ۳: Workflow و Agent

خروجی:

- سه Workflow.
- EvidenceBundle.
- Insight Brief.
- Validation و Publication مستقل.

### فاز ۴: تعامل و UI

خروجی:

- Assistant با Text-to-SQL امن.
- Dashboard نقش‌محور.
- Workflow Control Room.
- Decision tracking و Config input.

### فاز ۵: Replay و پذیرش

خروجی:

- Replay صبح‌های ۶۲ تا ۹۱.
- آزمون‌های امنیت، Prompt Injection، Missing Source و Org Change.
- Benchmark زمان و هزینه.
- Backup/Restore test.
- Docker و مستندات تحویل.

## ۲۵. آمادگی برای C4 و Structurizr

مدل C4 باید حداقل این Viewها را داشته باشد:

1. `SystemContext`: مدیران، ارزیاب، منابع، LLM و دیدراه.
2. `Containers`: Web، API، Worker، Scheduler، PostgreSQL، Archive و Model Provider.
3. `ApiComponents`: Identity، Authorization، Manager Input، Query Gateway، Report API و Decision Tracker.
4. `WorkerComponents`: Ingestion، Snapshot، KPI، Signal، Workflow، Evidence، Agent، Validator و Publisher.
5. `NightlyReporting`: جریان Drop تا Report.
6. `InteractiveAssistant`: جریان سؤال تا SQL و پاسخ.
7. `ManagerInput`: تغییر تنظیم، Upload و Decision.
8. `SecurityBoundaries`: Trust boundary، RLS، Agent و Archive.
9. `Deployment`: Docker Host، Containerها، Volumeها و ارتباط خارجی LLM.
10. `FailureAndPartialPublication`: شکست یک مدیر و ادامه انتشار دیگران.

### ۲۵.۱. رابطه‌های اصلی برای مدل C4

- Manager از WebApp استفاده می‌کند.
- WebApp فقط BackendApi را فراخوانی می‌کند.
- BackendApi AuthContext را می‌سازد.
- BackendApi QueryGateway را برای Query تعاملی فراخوانی می‌کند.
- QueryGateway با Role محدود به PostgreSQL متصل می‌شود.
- BackgroundWorker داده را از Source و Archive دریافت می‌کند.
- BackgroundWorker KPI و Workflow را در PostgreSQL محاسبه می‌کند.
- AgentOrchestrator فقط EvidenceService و ModelGateway را فراخوانی می‌کند.
- ModelGateway تنها جزء متصل به LLM Provider است.
- Publisher ReportVersion را در PostgreSQL ثبت می‌کند.
- WebApp گزارش منتشرشده را از BackendApi می‌خواند.
- ReplayRunner همان APIهای دامنه و Worker را با Clock شبیه‌سازی‌شده اجرا می‌کند.

## ۲۶. تصمیم پیشنهادی نهایی

معماری پیشنهادی برای دیدراه این است:

> یک Modular Monolith با Backend API و Worker جدا، PostgreSQL به‌عنوان تنها پایگاه داده محصول، Protected File Archive برای فایل خام، هسته قطعی برای KPI و Signal و Workflow، یک Agent محدود مبتنی بر LangGraph برای تحلیل و نگارش، Query Gateway با RLS اجباری برای Text-to-SQL، و انتشار مستقل و Validation‌شده گزارش هر مدیر.

این معماری با اندازه تیم، Docker، Replay، محدودیت زمان و هزینه و معیارهای امنیتی بریف سازگار است. اجرای آن پس از بستن تصمیم‌های P0 شروع می‌شود. تصمیم‌های باز بخشی از معماری هستند و نباید پنهان شوند.
