# ARCH-001: طرح معماری سیستم ARKA

کلید سند: `001-system-blueprint`. عبارت `ARCH-001` برچسب حفظ‌شده خانواده معماری است. این عبارت شناسه یکتای سند نیست.

تاریخ بازبینی: 2026-11-09. منطقه زمانی: `Asia/Tehran`.

وضعیت: requirements، تصمیم‌های Accepted تیم، جزئیات Proposed و مسائل Open. هیچ ادعایی درباره پیاده‌سازی محصول یا نتیجه پذیرش وجود ندارد. [بازبینی Q01-Q17](004-reconciliation-review.md) و [Decision Log](003-decisions-and-roadmap.md#decision-log) را ببینید.

<a id="system-1"></a>

## 1. معماری Accepted و جزئیات Proposed

ARKA از یک AI Agent محدود و ماژول‌های deterministic استفاده می‌کند. PostgreSQL تنها موتور پایگاه داده محصول است. این موارد تصمیم‌های `Accepted` تیم در S16 Q01/Q03 هستند. S17 نیز همین هدف را بیان می‌کند. [ADR-13](003-decisions-and-roadmap.md#adr-13) و [ADR-01](003-decisions-and-roadmap.md#adr-01) را ببینید.

برنامه modular در یک codebase شامل API، رابط فارسی RTL و background worker است. فایل‌های اصلی را همراه با hashهای SHA-256 در file storage محافظت‌شده نگه دارید. File storage پایگاه داده دوم نیست. Queue و وضعیت اجرا می‌توانند از PostgreSQL استفاده کنند. جزئیات Framework و استقرار فیزیکی همچنان Proposed هستند.

`ReferenceCalculator` برای 55 تعریف canonical مربوط به KPI، SQL سازگار با PostgreSQL را اجرا می‌کند. SQL و viewهای اصلی SQLite را به‌عنوان Evidence مربوط به Requirement حفظ کنید. SQL ترجمه‌شده و نسخه آن را جدا نگه دارید. هر 55 تعریف پیش از پذیرش به بررسی هم‌ارزی عددی نیاز دارند. SQLite می‌تواند به‌عنوان test oracle مجزا عمل کند. این ابزار calculator محصول یا موتور query تعاملی نیست. تصمیم ثبت‌شده تیم جایگزین پیشنهاد قبلی dual-engine شده است. هیچ ادعایی درباره نتیجه هم‌ارزی وجود ندارد.

Agent برای تحلیل و نگارش از Evidence مجاز استفاده می‌کند. محاسبه، تشخیص Signal، کنترل Authorization و بررسی خروجی deterministic هستند. Agent هیچ credential پایگاه داده یا ابزار اقدام سازمانی ندارد. همان Agent می‌تواند از تحلیل و نگارش ویژه نقش پشتیبانی کند. ماژول‌های جداگانه Writer و Validator، AI Agent اضافی ایجاد نمی‌کنند.

هر گزارش معتبر مدیر به‌صورت مستقل منتشر می‌شود. هر نتیجه و وضعیت روز را ثبت کنید. روزی که گزارش الزامی آن ناموفق باشد، ناقص است. Template fallback، تعداد retry و timeout همچنان Proposed هستند. [ADR-14](003-decisions-and-roadmap.md#adr-14) را ببینید.

استفاده از Python برای API/worker و TypeScript برای رابط همچنان در حد پیشنهاد است. تحویل Docker با یک دستور یک Requirement است. Model، provider، framework و محصول gateway انتخاب نشده‌اند.

<a id="system-2"></a>

## ۲. منابع و درجهٔ اعتبار

از این چهار وضعیت تصمیم استفاده کنید:

| وضعیت | معنا | Evidence لازم |
|---|---|---|
| `Requirement` | یک قانون صریح brief یا قرارداد dataset. | منبع، صفحه یا Field و نسخه قابل‌اعمال. |
| `Accepted` | یک تصمیم ثبت‌شده تیم. | متن تصمیم و محل منبع. در صورت ارائه، تأییدکننده و تاریخ را ثبت کنید. |
| `Proposed` | یک گزینه طراحی بدون Evidence تأیید. | پیشنهاد، گزینه‌ها و مسئول بازبینی. |
| `Open` | یک قانون، تعارض یا انتخاب حل‌نشده. | منابع، اثرها، مسئول و Evidence مربوط به بسته‌شدن. |

`Observation` یک دسته Evidence است، نه وضعیت پنجم تصمیم. توصیه Codex تأیید تیم نیست. S16 تصمیم‌ها را ثبت می‌کند و جایگزین Requirementهای S01-S07 نمی‌شود. S17 مدل هدف موجود را تأیید می‌کند. جزئیات طراحی آن، تأیید یا پیاده‌سازی را اثبات نمی‌کنند. تعارض‌های حل‌نشده منابع را در [Decision Log](003-decisions-and-roadmap.md#decision-log) نگه دارید.

### ۲.۱. فهرست منابع بررسی‌شده

مسیرهای جدول نسبت به این سند هستند. شناسهٔ منبع در دو سند دیگر نیز همین معنا را دارد.

| شناسه | منبع | نتیجهٔ بررسی و کاربرد |
|---|---|---|
| S01 | [بریف اصلی DIDRAH](../بریف%20پروژه%20بوتکمپ%20_%20دستیار%20ایجنتیک%20مدیران%20سازمانی%20_%20دیدراه.pdf) | PDF کنونی: 19 صفحه در 2026-11-09 خوانده شد. صفحه‌های 13 و 16 نیز به‌صورت تصویر بررسی شدند. Requirementهای محصول و پذیرش. |
| S02 | [README_FA.md](../../DataSet/arka_dataset/README_FA.md) | زمان دسترسی، ساختار drop، قرارداد محاسبه و ورودی مدیر را مشخص می‌کند. |
| S03 | [kpi_dictionary.csv](../../DataSet/arka_dataset/config/kpi_dictionary.csv) | ۵۵ تعریف؛ شناسه، مالک، واحد، SQL، ابعاد و آستانه‌ها. |
| S04 | [reference_views.sql](../../DataSet/arka_dataset/config/reference_views.sql) | پنج view مرجع: `order_fact`، `ticket_fact`، `lead_fact`، `task_fact` و `revenue_daily`. |
| S05 | [org](../../DataSet/arka_dataset/org/) و [access_matrix.csv](../../DataSet/arka_dataset/org/access_matrix.csv) | واحدها، تیم‌ها، مدیران، کارکنان، تاریخ شروع و محدودیت دادهٔ فردی. |
| S06 | [brief_schema.json](../../DataSet/arka_dataset/output_contract/brief_schema.json)، [qa_answer_schema.json](../../DataSet/arka_dataset/output_contract/qa_answer_schema.json)، [example_brief.json](../../DataSet/arka_dataset/output_contract/example_brief.json) | قالب واقعی خروجی؛ مثال، مرجع مقدار یا تاریخ صحیح نیست. |
| S07 | [scripted_inputs.json](../../DataSet/arka_dataset/manager_inputs/scripted_inputs.json) و [uploads](../../DataSet/arka_dataset/uploads/) | ۲۳ ورودی شامل ۱۶ پرسش؛ تغییر اولویت، آستانه، سازمان، تصمیم و فایل. ترتیب آرایه کاملاً زمانی نیست. |
| S08 | [RCA-001](../review/rca-001-report.md) و [شواهد آن](../review/rca-001-evidence.json) | تقویم، `drop_day`، median، تکرار سفارش و تغییر schema. |
| S09 | [KPI-VAL-001](../review/kpi-val-001-report.md)، [شواهد](../review/kpi-val-001-evidence.json)، [مقایسهٔ CSV](../review/kpi-val-001-results.csv) | مقایسهٔ RAW و DEDUP برای همهٔ تعریف‌ها و ۳۰ صبح. CSV دارای ۱۷۶٬۰۰۲ ردیف است. |
| S10 | [DQ-001](../review/dq-001-report.md)، [شواهد](../review/dq-001-evidence.json)، [اثر KPI در CSV](../review/dq-001-kpi-impact.csv) | تفکیک اثر دیررسیدن، وضعیت نامعلوم و نبود ردیف SQL؛ CSV دارای ۲۳٬۰۳۹ ردیف است. |
| S11 | [escalation_rules.csv](../../DataSet/arka_dataset/config/escalation_rules.csv)، [workflow_definitions.csv](../../DataSet/arka_dataset/config/workflow_definitions.csv)، [monthly_targets.csv](../../DataSet/arka_dataset/config/monthly_targets.csv) | هشت قاعده، سه Workflow با ۱۲ مرحله و سه هدف ماهانه. |
| S12 | [calendar_days.csv](../../DataSet/arka_dataset/calendar/calendar_days.csv)، [events_calendar.csv](../../DataSet/arka_dataset/calendar/events_calendar.csv) | تاریخ کسب‌وکار، ماه شمسی، روز هفته، تعطیلی و زمینهٔ رویداد. |
| S13 | [history](../../DataSet/arka_dataset/history/) | حافظهٔ تصمیم و گزارش قدیمی با تعریف متفاوت. |
| S14 | [drops](../../DataSet/arka_dataset/drops/) | ۹۱ manifest و ۱٬۰۷۹ فایل CSV؛ نمونه‌های روزهای ۰۰۰، ۰۶۶، ۰۶۷، ۰۷۰، ۰۷۶، ۰۸۱ و ۰۸۲ مستقیماً بررسی شدند. |
| S15 | [نقشهٔ اکتشافی](../review/exploration/DATA_MAP_FA.md) و [نتایج اکتشاف](../review/exploration/) | مدرک کمکی دربارهٔ جدول‌ها و روابط؛ جایگزین قرارداد رسمی نیست. |
| S16 | [رکورد بازبینی معماری](sources/Adr.md) | نسخه دقیق `C:/Users/ashkriz/Desktop/Adr.md` که کاربر ارائه کرده است. Q01-Q17 و جدول نتیجه خوانده شدند. تصمیم‌های صریح تیم از پیشنهادها جدا شده‌اند. |
| S17 | [مدل موجود Structurizr](../../architecture/structurizr/workspace.dsl) | یادداشت‌های Authority و قراردادهای component مرتبط بررسی شدند. یک Agent، اجرای صرفاً مبتنی بر PostgreSQL و انتشار مستقل را تأیید می‌کند. فایل مدل تغییر نکرده است. |
| S18 | [brief با Markdown](../دیدراه-بریف-دستیار-ایجنتیک-مدیران.md) | منبع متنی کنار S01. commentهای صفحه، شماره صفحه‌های PDF را حفظ می‌کنند. بخش‌های مهم با S01 بررسی شدند. Highlight و ذخیره مجدد، Requirement تغییریافته را اثبات نمی‌کنند. |
| S19 | [درخواست audit کنونی](audit-2026-11-09/request.txt) | تأیید کاربر درباره پنج مرز Accepted و Scope صرفاً مستندسازی. این مورد محاسبه جدید dataset یا قرارداد خروجی نیست. |

S16 در دسترس است. Data Dictionary رسمی و کامل برای ستون‌های raw، قرارداد بسته‌شدن منبع و labelهای پنهان Evaluation یافت نشدند. ستون‌های مشاهده‌شده و نتایج audit جایگزین این قراردادها نیستند.

یافته‌های audit قبلی، Evidence تاریخی هستند. این بازبینی 55 query مربوط به SQL را دوباره اجرا نکرد و همه ادعاهای audit قبلی را تأیید نکرد. رکورد Verification کنونی را در سند 004 ببینید.

hash منشأ S01: `6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8`. PDF کنونی و S18 درباره Requirementهای بررسی‌شده هم‌خوان هستند. تفاوت قبلی file-hash هیچ تعارضی در Requirement را اثبات نمی‌کند.

### ۲.۲. مشاهده‌هایی که طراحی را محدود می‌کنند

| مشاهده | اثر بر معماری |
|---|---|
| ۲۶۲ تکرار دقیق در `day_076/orders.csv`؛ ۶۹۹ ردیف خام و ۴۳۷ payload متمایز | idempotency دریافت با حذف تکرار تجاری یکسان نیست. هر دو سیاست ورودی باید قابل اجرا و نسخه‌دار باشند. |
| در S09، هشت KPI دارای ۴۱ اختلاف در snapshot نهایی و ۴۱۸ اختلاف در replay هستند | انتخاب RAW/DEDUP شرط پذیرش است؛ نمی‌توان آن را بهینه‌سازی بی‌اثر نامید. |
| سه فایل پشتیبانی در روز ۰۶۶ هم در پوشه و هم در manifest غایب‌اند | مقایسهٔ فایل با manifest کافی نیست؛ قرارداد منبع مورد انتظار نیز لازم است. |
| دادهٔ روز ۰۶۷، ۳۲ کلید تاریخی پشتیبانی را تغییر می‌دهد؛ هفت مورد متعلق به روز ۰۶۵ است | invalidation یک‌روزه یا محدودیت ثابت تأخیر کافی نیست. |
| ۳۵ مجموعهٔ مشارکت‌کننده عوض شده‌اند، ولی سه خروجی گرد‌شده ثابت مانده‌اند | تساوی مقدار، گواه تساوی شواهد یا کامل‌بودن نیست. |
| اصلاح `L02045` در drop 070 می‌رسد و فقط از صبح ۷۱ مجاز است | فیلتر دریافت باید قبل از ساخت fact اعمال شود. |
| از روز ۰۸۲ دو نام ستون پشتیبانی عوض می‌شود | adapter باید بر اساس schema شناخته‌شده کار کند، نه شمارهٔ روز ثابت. |
| تغییر روش محاسبهٔ مدت زمان، هشت مقدار گرد‌شده را در S08 تغییر داده است | معادل ریاضی PostgreSQL بدون آزمون، معادل محاسباتی قرارداد نیست. |

<a id="system-3"></a>

## ۳. ردیابی نیازمندی‌ها

| ID | الزام و مرجع | مسئول طراحی | آزمون پذیرش در سند 003 |
|---|---|---|---|
| <a id="req-01"></a>REQ-01 | دریافت ماژولار و ادامهٔ گزارش هنگام نبود منبع؛ S01 ص۱۳-۱۴، S02 | Ingestion، DQ، Orchestrator | AT-01، AT-04 |
| <a id="req-02"></a>REQ-02 | محاسبه با SQL ثبت‌شده و صفر عدد نادرست؛ S01 ص۱۳ و ۱۶، S03-S04 | Semantic، ReferenceCalculator، Validator | AT-02، AT-03 |
| <a id="req-03"></a>REQ-03 | سلسله‌مراتب قابل تغییر بدون تغییر کد؛ S01 ص۲ و ۱۷، S05 و S07 | Organization، Authorization | AT-07 |
| <a id="req-04"></a>REQ-04 | حداکثر پنج مورد، مالک درست، حذف تکرار و تشدید؛ S01 ص۷-۸، S11 | Signal، Workflow، Report | AT-08، AT-09 |
| <a id="req-05"></a>REQ-05 | دو شاهد مستقل برای هر علت و کوئری برای هر عدد؛ S01 ص۹-۱۰ | Evidence، Analysis، Validator | AT-10 |
| <a id="req-06"></a>REQ-06 | گزارش فارسی و RTL، داشبورد، گفتگو و اتاق کنترل؛ S01 ص۱۱-۱۲ و ۱۵ | Interface، Brief Publisher | AT-11 |
| <a id="req-07"></a>REQ-07 | سه Workflow از لاگ واقعی، SLA و گلوگاه؛ S01 ص۵-۶ و ۱۶، S11 | Process Projection | AT-12 |
| <a id="req-08"></a>REQ-08 | دسترسی ردیفی برای همهٔ کوئری‌های کاربر؛ S01 ص۱۳، S05 | Query Gateway، RLS | AT-06 |
| <a id="req-09"></a>REQ-09 | دادهٔ فردی فقط برای سرپرست مستقیم و مدیریت کار؛ S01 ص۱۳ و ۱۷ | Authorization، Privacy Filter | AT-06 |
| <a id="req-10"></a>REQ-10 | متن تیکت و فایل دستور نیست؛ S01 ص۱۳ و ۱۷ | Input Boundary، Tool Gateway | AT-13 |
| <a id="req-11"></a>REQ-11 | تصمیم با مدیر؛ فقط پیش‌نویس و پیگیری؛ S01 ص۱۱-۱۲، S02 | Decision Registry | AT-14 |
| <a id="req-12"></a>REQ-12 | تاریخچهٔ ۶۰ روز و replay سی روز، صبح ۶۲ تا ۹۱؛ S01 ص۱۴، S02 | ReplayClock، Snapshot Builder | AT-03، AT-15 |
| <a id="req-13"></a>REQ-13 | کشف حداقل ۹۰٪ در ۲۴ ساعت و دقت گفتگو حداقل ۸۵٪؛ S01 ص۱۶-۱۷ | Evaluation Harness | AT-09، AT-16 |
| <a id="req-14"></a>REQ-14 | هر روز حداکثر ۱۵ دقیقه روی ماشین مرجع؛ گزارش پیش از ۰۷:۳۰ شبیه‌سازی؛ S01 ص۱۴ | Orchestrator، Metrics | AT-17 |
| <a id="req-15"></a>REQ-15 | مجموع هزینهٔ LLM حداکثر ۵ دلار در روز، شامل گفتگو؛ S01 ص۱۶ | Budget Ledger | AT-18 |
| <a id="req-16"></a>REQ-16 | اجرای بدون تغییر کد روی دادهٔ پنهان؛ بستهٔ Docker با یک دستور؛ S01 ص۱۴ و ۱۸ | Configuration، Packaging | AT-19 |
| <a id="req-17"></a>REQ-17 | اصلاح تاریخی، رکورد دیررس، تکرار و schema change به‌عنوان مسئلهٔ داده؛ S01 ص۱۴ و ۱۷ | Ingestion، DQ، Versioning | AT-04، AT-05 |

اعداد حدود ۱۵۰ شاخص روزانه، ۲۵ سیگنال و هشت تحلیل در بریف، اندازهٔ تقریبی هستند. آن‌ها حداقل خروجی اجباری نیستند. ۵۵ تعریف می‌توانند چندین سری بعددار تولید کنند. صفحهٔ ۱۹ نیز نهایی‌شدن حدود پذیرش را به برگزارکننده واگذار می‌کند؛ اجرای آینده باید نسخهٔ حدود را ثبت کند.

<a id="system-4"></a>

## ۴. نمای ماژول‌ها و مرز اعتماد

از [workspace موجود Structurizr](../../architecture/structurizr/workspace.dsl) و کلیدهای view شامل `IntegratedOverview`، `Containers`، `DataIntake`، `DeterministicAnalytics` و `EvidenceAndAnalysis` استفاده کنید. این کلیدها در DSL وجود دارند. آن‌ها viewهای هدف را مشخص می‌کنند، نه componentهای نصب‌شده را. [فهرست viewها و شکاف‌ها](audit-2026-11-09/structurizr-gap-report.md) را ببینید.

منابع، متن آزاد و LLM قابل اعتماد اجرایی نیستند. worker محاسبهٔ ثبت‌شده و Query Gateway مرزهای مجزا دارند. worker می‌تواند با هویت خدماتی، snapshot سازمان را برای KPIهای ثبت‌شده محاسبه کند. این مجوز به LLM، مدیر یا مسیر Text-to-SQL منتقل نمی‌شود. دادهٔ خروجی worker نیز قبل از هر استفادهٔ کاربری، کنترل دسترسی می‌شود.

### ۴.۱. مسئولیت و رابط هر ماژول

نام رابط‌ها قرارداد طراحی است؛ endpoint یا کد موجود نیست.

| ماژول | ورودی | خروجی | مرز و رفتار خطا |
|---|---|---|---|
| A: `SourceAdapter` | `DeliveryEnvelope`، bytes و schema fingerprint | `ParsedBatch` با raw pointers، رکوردهای معتبر و ردشده | فقط parse و نگاشت مصوب؛ تغییر فرمول یا تصمیم دربارهٔ تکرار تجاری ممنوع. خطا با source/file/row ثبت می‌شود. |
| A: `IngestionCoordinator` | manifest، SourceContract، idempotency key | `BatchReceipt` و `SourceStatus` | ثبت فایل و metadata اتمی؛ فایل خراب به quarantine می‌رود. منابع سالم ادامه می‌یابند. |
| B: `SnapshotService` | `KnowledgeCutoff`، policy/config versions | `SnapshotRef` و روابط مجاز reference | فقط batchهای committed؛ زمان رویداد جای cutoff دریافت را نمی‌گیرد. |
| B: `ProjectionService` | snapshot و تغییرات entity/event | factهای نسخه‌دار و `ProjectionDelta` | projection قابل بازسازی است. raw و گزارش گذشته تغییر نمی‌کنند. |
| C: `SemanticRegistry` | S03-S04 و تنظیمات نسخه‌دار | `KpiSpec`، `DependencySpec`، units و query hash | SQL و metadata اصلی حفظ می‌شوند. شاخص جدید شناسهٔ جدید دارد. |
| C: `ReferenceCalculator` | Snapshot ثابت، تعریف canonical، نسخه PostgreSQL مربوط به SQL، policy ورودی | نتیجه KPI، QueryRun، Lineage | فقط SQL ثبت‌شده. هم‌ارزی با SQL اصلی الزامی است. failureها را با صفر جایگزین نکنید. |
| D: `SignalEngine` | KPIهای واجد شرایط، rule version و سابقه | signal occurrence، incident link و وضعیت مخاطب | بدون LLM؛ DQ به‌تنهایی business signal نمی‌سازد. |
| D: `WorkflowEngine` | event history، stage definitions و clock | case/stage وضعیت، SLA، bottleneck evidence | مرحلهٔ بدون SLA، وضعیت unknown دارد؛ عدد نمایشی بریف استفاده نمی‌شود. |
| E: `EvidenceService` | signal، scope، snapshot و پرسش محدود | `EvidenceBundle` با query و source pointers | قبل از ورود به LLM، row/column filtering و بررسی مقصد انجام می‌شود. |
| E: `AnalysisCoordinator` | evidence، محدودیت ابزار و بودجه | `InsightBrief` با facts، hypotheses، گزینه‌ها | ادعای بی‌شاهد حذف یا به نیاز بررسی تبدیل می‌شود؛ عدد توسط ابزار تولید می‌شود. |
| F: `ManagementInputService` | پرسش، تصمیم یا تغییر تنظیم احراز‌شده | input event، config revision یا QA job | متن فایل نمی‌تواند دستور مدیر بسازد. تغییر مجاز از زمان اثر مشخص فعال می‌شود. |
| F: `Publisher` | یک package مجاز و Validation‌شده مدیر | نسخه JSON/text و رسید انتشار | packageهای معتبر را مستقل منتشر کنید. packageهای ناموفق یا غایب و وضعیت روز ناقص را ثبت کنید. |
| G: `QueryGateway` | AuthContext، QuerySpec و snapshot | نتیجهٔ محدود، query receipt یا refusal | read-only، deny by default و RLS؛ LLM هیچ credential پایگاه داده ندارد. |
| H: `ReplayRunner` | dataset root، clock و EvaluationProfile | run receipts، خروجی‌ها، معیار زمان/هزینه/صحت | هیچ شاخهٔ رفتاری به شمارهٔ حادثه یا شناسهٔ نمونه وابسته نیست. |

### مالکیت Configuration و اجرا

`Requirement`: مدیران مجاز می‌توانند بدون تغییر کد، هدف‌ها، اولویت‌ها، targetها، آستانه‌های هشدار، قوانین escalation و سازمان را تغییر دهند. افزودن مورد به dictionary مربوط به KPI مجاز است. 55 تعریف موجود بدون تغییر می‌مانند. یک preference نمی‌تواند دسترسی را گسترش دهد یا نتیجه عددی را تغییر دهد.

`Proposed mechanism`، سازگار با DSL `managerConfig`: یک نسخه غیرفعال جدید KPI را ثبت کنید؛ ایمنی SQL، ورودی‌ها، واحدها، rounding مرجع، scope، rollupها و اجرای deterministic را اعتبارسنجی کنید؛ تأیید انسانی را ثبت کنید؛ سپس نسخه تأییدشده را در زمان اثرگذاری کنترل‌شده فعال کنید. نسخه قبلی را حفظ کنید. نقش‌های تأیید و قوانین دقیق فعال‌سازی همچنان Open هستند. درخواست تغییر فرمول canonical را به overwrite ثبت‌نشده تبدیل نکنید. ADR-01، ADR-06، ADR-08 و AT-27 را ببینید.

controller مربوط به DSL `requests` مالک کل ExecutionGrant است. این مالکیت گام‌های بررسی، ابزارها، زمان سپری‌شده، retryها، لغو و درخواست والد را پوشش می‌دهد. DSL `modelGateway` مالک callهای جداگانه Model و اعمال هزینه روزانه مشترک است. هیچ‌یک از این مرزها نمی‌تواند محدودیت‌های والد را reset کند. محدودیت‌های دقیق طبق ADR-10 همچنان Open هستند. AT-20 و AT-28 را ببینید.

| اصطلاح سند | شناسه موجود DSL | مرز |
|---|---|---|
| SourceAdapter / IngestionCoordinator | `ingestion`, `quality` | دریافت ساخت‌یافته و مسائل داده. |
| SnapshotService / ProjectionService | `snapshots` | ورودی‌های واجد شرایط نسخه‌دار و Observationهای مشتق‌شده. |
| SemanticRegistry / ReferenceCalculator | `managerConfig`, `kpi` | حاکمیت تعریف و محاسبه deterministic با PostgreSQL. |
| SignalEngine / WorkflowEngine | `signals`, `workflows` | قوانین deterministic جداگانه و بازسازی فرایند. |
| AnalysisCoordinator | `requests`, `agent`, `evidence`, `insights` | یک Agent محدود و تحلیل مشترک کنترل‌شده. |
| ManagementInputService | `requests`, `managerConfig`, `documents`, `decisions` | تنظیمات، uploadها، تصمیم‌ها و lifecycle مجاز. |
| Publisher / QueryGateway | `publication`, `reportWriter`, `outputValidator`, `queryGateway` | محتوای نقش، Validation، تحویل مستقل و queryهای کنترل‌شده. |
| ReplayRunner | `jobs`, `audit` | اجرای زمان‌بندی‌شده و Evidence نتایج. |

این نگاشت‌ها elementهای موجود را حفظ می‌کنند. آن‌ها component جدیدی به runtime اضافه نمی‌کنند. API هر دو مسیر runtime را مدیریت می‌کند. worker پردازش deterministic را در همان codebase ماژولار انجام می‌دهد.

### مرز ورودی و سند

`Requirement`: منابع شبانه و ورودی‌های مدیر، از جمله uploadها، را بپذیرید. brief، Excel را به‌عنوان نمونه upload ذکر می‌کند. S07 پیوست‌های CSV و Markdown را فراهم می‌کند. مجموعه fixture، Requirement مربوط به upload را حذف نمی‌کند. formatهای دقیق، Validation مربوط به Excel، پشتیبانی PDF، بازیابی متن و RAG طبق [ADR-16](003-decisions-and-roadmap.md#adr-16) همچنان Open یا Proposed هستند. اسناد developer، فایل‌های معماری، auditها یا labelهای پنهان را به‌عنوان Evidence محصول دریافت نکنید. upload عملیاتی Markdown همچنان داده غیرقابل‌اعتماد است.

### ۴.۲. قرارداد مشترک پیام‌ها

هر درخواست داخلی دارای `request_id`، `run_id`، `schema_version`، `snapshot_id` و `policy_bundle_id` است. عملیات کاربر، `principal_id`، `auth_context_id` و `purpose` نیز دارند. `AuthContext` را سرور از هویت معتبر می‌سازد؛ این فیلد از متن LLM یا `manager_id` ارسالی کاربر پذیرفته نمی‌شود.

| قرارداد | فیلدهای اصلی و قید |
|---|---|
| `DeliveryEnvelope` | `dataset_id, source_id, drop_day, manifest_hash, file_hash, source_schema_version, received_at, batch_id`؛ `received_at` واقعی است. |
| `SnapshotRef` | `knowledge_drop_max, commit_seq_max, business_date_max, source_version_set, config_version_set, org_version, input_policy_id`؛ پس از ساخت تغییر نمی‌کند. |
| `KpiObservation` | `kpi_id, entity_id, dim, business_date, row_state, reference_value, publication_state, completeness_state, query_id, contributor_hash`؛ نبود ردیف از NULL جداست. |
| `SignalOccurrence` | `signal_id, episode_id, series_key, rule_version, occurrence_day, baseline_refs, owner_id, severity, dq_links`؛ وضعیت انتشار به مخاطب وابسته است. |
| `EvidenceBundle` | `scope_fingerprint, facts, queries, source_groups, contradictions, limitations, data_issues`؛ هر fact به query و snapshot متصل است. |
| `InsightBrief` | `summary, impact, metric_refs, drilldowns, causes, alternatives, options, history, proposed_owner, query_refs`؛ شرط پذیرش هر علت جدا بررسی می‌شود. |
| `QueryReceipt` | SQL واقعی اجراشده، params، hash، principal، purpose، snapshot، policy، زمان، تعداد ردیف، نتیجه یا خطا؛ log خودش مشمول دسترسی است. |
| `DecisionEvent` | `decision_id, actor_id, brief_version, selected_option, decided_at, effective_from, success_metric_refs`؛ هیچ اجرای خارجی ضمنی ندارد. |
| `ExecutionGrant` | قرارداد داخلی Proposed: درخواست والد، principal قابل‌اعتماد، ابزارهای مجاز، revision ثابت Snapshot/Evidence، رزرو هزینه، محدودیت‌های step/token/time/retry، deadline و وضعیت لغو. محدودیت‌های دقیق همچنان Open هستند. |
| `InteractiveEvidenceRevision` | قرارداد داخلی Proposed: cutoff عملیاتی drop به‌همراه revisionهای موفق و مجاز upload/config و وضعیت رسید/آمادگی آن‌ها. این قرارداد هرگز گزارش صبحگاهی immutable را تغییر نمی‌دهد. |
| `ManagerJobOutcome` | قرارداد داخلی Proposed: کلید manager/report، وضعیت، نتیجه Validation/export، علت امن failure و referenceهای retry/version. حتی اگر draft وجود ندارد، failure را ثبت کنید. پوشش روز نتیجه‌ای جداگانه است. |

کدهای خطای پایدار پیشنهادی: `SOURCE_MISSING`، `SCHEMA_UNSUPPORTED`، `CORRECTION_CONFLICT`، `REFERENCE_QUERY_FAILED`، `ACCESS_DENIED`، `BUDGET_EXHAUSTED` و `OUTPUT_VALIDATION_FAILED`. پاسخ خطا، دادهٔ خارج از scope یا نام فایل محرمانه را آشکار نمی‌کند.

<a id="system-5"></a>

## ۵. جریان اجرای شبانه و replay

viewهای موجود Structurizr شامل `NightlyReporting`، `NightlyData` و `NightlyBrief` مسیر زمان‌بندی‌شده را نشان می‌دهند. `InteractiveAssistant` و `ManagerUpload` مسیر تعاملی را نشان می‌دهند. `PartialPublication` نتایج مستقل failure را نشان می‌دهد. برای یافتن هر declaration از [فهرست viewها](audit-2026-11-09/structurizr-gap-report.md) استفاده کنید.

۱. `day_000` بار اولیهٔ CRM است. نبود سایر منابع در آن روز حادثه نیست. روزهای ۱ تا ۶۰ برای تاریخچه و baseline وارد می‌شوند.

۲. گزارش صبح `R` فقط dropهای `000..R-1` را می‌بیند. پرسش روز `D` نیز فقط دادهٔ dropهای تا `D-1` را می‌بیند. تغییرهای مدیریتی روز `D` از گزارش `D+1` اثر می‌گذارند. `commit_seq` از ورود تصادفی فایل جدید به snapshot در حال اجرا جلوگیری می‌کند.

۳. رویدادهای ورودی بر اساس روز و ترتیب ثبت معتبر زمان‌بندی می‌شوند. ترتیب فعلی آرایهٔ S07 نباید clock را عقب ببرد. ترتیب چند ورودی هم‌روز و دریافت attachment باید صریح ثبت شود؛ ابهام manager Q09/IN07 در ADR-08 آمده است.

۴. missing source و schema failure مانع گزارش کل سازمان نمی‌شوند. گزارش هر مدیر با داده‌های مجاز و سالم و با بخش `data_issues` تولید می‌شود. مقدار ناموجود `null` است. «هیچ هشدار تأییدشده‌ای نیست» جایگزین «همه‌چیز سالم است» می‌شود، اگر داده کافی نباشد.

5. نسخه‌های محاسبه و Configuration را ثابت کنید. گزارش را فقط پس از Validation منتشر کنید. یک package مدیر را به‌صورت atomic ثبت کنید. packageها را مستقل منتشر کنید. Retry نباید گزارش یا Signal را تکراری کند. پوشش روز را جداگانه ثبت کنید.

۶. تغییر تاریخی، نسخهٔ جدید KPI می‌سازد. گزارش صبح گذشته با دادهٔ جدید بازنویسی نمی‌شود. مسیر `restated` از مسیر `as_reported` جداست.

<a id="system-6"></a>

## ۶. Semantic Layer و محاسبه

همهٔ ۵۵ تعریف از S03 خوانده شوند. SQL، شناسه، entity، مالک، unit، direction، rule، target، warn، crit، dim و مهلت تشدید در registry نسخه‌دار قرار گیرند. فهرست کامل پوشش و وابستگی در سند 002 است.

`cal` همان calendar عرضه‌شده است و فقط `date` به `d` نگاشت می‌شود. `crm_lead_events.drop_day` از manifest معتبر اضافه می‌شود. نگاشت شناخته‌شدهٔ `create_time -> created_at` و `event_time -> at` در adapter انجام می‌شود. فایل و SQL اصلی دست‌نخورده می‌مانند.

گردکردن در خود SQL مرجع انجام می‌شود. LLM، رابط و serializer نباید مقدار را دوباره گرد کنند. واحد «میلیون تومان»، «هزار تومان»، «تومان»، «ساعت»، «روز»، درصد و امتیاز از پنج یکسان نیستند. اختلاف دو درصد در توضیح، «واحد درصد» است. هر محاسبهٔ اضافه باید query و تعریف ثبت‌شدهٔ مستقل داشته باشد.

تجمیع سلسله‌مراتبی به معنی جمع‌زدن همهٔ خروجی‌های فرزند نیست. نرخ از صورت و مخرج، میانگین از sum/count و median از نمونه‌های مجاز محاسبه می‌شود. median تیم‌ها یا درصدهای گرد‌شده میانگین‌گیری نمی‌شوند. KPIهای تکراری در چند سطح، مانند FRT، شواهد مستقل نیستند. برای ۵۵ تعریف موجود، SQL همان سطح مرجع است؛ rollup جدید با شناسهٔ جدید ثبت می‌شود.

<a id="system-7"></a>

## ۷. موتور سیگنال و Workflow

### 7.1. قرارداد کامل R1-R8

منبع `../../DataSet/arka_dataset/config/escalation_rules.csv` و رکوردهای R1-R8 است. هر قانون زیر یک Requirement است. نام‌های Field مربوط به state و سازوکار storage، Proposed هستند. مسیریابی قانون هرگز access grant جدید ایجاد نمی‌کند.

از metadata canonical مربوط به KPI، Snapshot واجد شرایط، Fieldهای تقویم و سابقه گیرنده به‌عنوان ورودی استفاده کنید. کیفیت منبع را از وضعیت کسب‌وکار جدا نگه دارید. مسئله داده یک Signal کسب‌وکار نیست. R7 هشدار برای metricهای `info` را ممنوع می‌کند. R8 پیش از ارزیابی آستانه، `threshold_from_day8` را gate می‌کند.

| Rule / رکورد منبع | معنای دقیق منبع و trigger | ورودی‌ها | خروجی و مسیریابی | State و gateهای برنامه‌ریزی‌شده |
|---|---|---|---|---|
| R1 / 2 | هر Signal ابتدا به پایین‌ترین سطح مسئول که در `owner_manager_id` نام‌گذاری شده است می‌رسد. | مالک canonical، سازمان فعال، Signal واجد شرایط. | به آن مالک مسیریابی کنید. مالک غیرفعال یا حل‌نشده مسئله مسیریابی است؛ جایگزین را حدس نزنید. | Proposed: از unrouted به owned. مالک canonical را حفظ کنید. AT-08، AT-24. |
| R2 / 3 | اگر `crit` رد شود، هشدار **بیش از** `escalate_after_days` ادامه یابد یا افت نسبت به اولین گزارش **حداقل 20%** باشد، به سطح بالاتر escalation انجام دهید. | جهت، warn/crit، مدت، اولین مقدار گزارش‌شده، سابقه گیرنده، سلسله‌مراتب. | یک رخداد escalated با علت و سابقه صریح. از سطح بالاتر استفاده کنید؛ زمان‌بندی دقیق چندسطحی همچنان Open است. | Proposed: برای گیرنده از owned/open به escalated. سابقه قبلی گیرنده را نگه دارید. AT-08، AT-24. |
| R3 / 4 | وقتی یک شاخص در سطح Workflow یا سازمان از warn عبور می‌کند، آن را به M01 escalation دهید. | نوع/entity شاخص، warn عددی در صورت ارائه، مقدار واجد شرایط، جهت. | escalation مدیریتی همراه با علت آن. این مورد افشای Evidence محدود منبع را مجاز نمی‌کند. | سابقه مالک قبلی را حفظ کنید. رفتار در زمانی که Rule انتخاب‌شده warn عددی ندارد همچنان Open است. AT-08، AT-24. |
| R4 / 5 | Signal با تغییر معنادار کمتر از 10% نباید دوباره به‌عنوان مورد جدید گزارش شود؛ این Signal در فهرست Open باقی می‌ماند. | همان Signal، سابقه گیرنده، مقادیر قابل‌مقایسه. | تکرار جدید را برای همان گیرنده suppress کنید. State مربوط به Open را حفظ کنید. نمایش wire همچنان تابع ADR-09 است. | سابقه را حفظ کنید، نه episode جدید را. مرجع مقایسه، denominator صفر و جزئیات recovery/reset همچنان Open هستند. AT-08، AT-24. |
| R5 / 6 | `dow_baseline:N` مقدار را با median همان روز هفته در چهار هفته قبل مقایسه می‌کند. انحراف **بیشتر از N%** یک Signal است. تعطیلات رسمی مستثنا هستند. | Observationهای واجد شرایط همان روز هفته، `N`، روز هفته/تعطیلی تقویم ارائه‌شده، Snapshot. | یک انحراف و رسید baseline پشتیبانی‌شده، یا Evaluation صریحاً ناموجود. مسیریابی اولیه از R1 استفاده می‌کند. | baseline ناموجود/صفر، حداقل Observationها، تفسیر جهت و نحوه برخورد با نمونه‌های تاریخی تعطیلات همچنان Open هستند. وضعیت ناشناخته را عادی ننامید. AT-03، AT-09، AT-24. |
| R6 / 7 | حداکثر پنج مورد مهم در هر گزارش. Signalهایی با علت یکسان در teamها/systemها یک مورد را تشکیل می‌دهند. | Signalهای واجد شرایط، Evidence علت، context اولویت، scope گیرنده. | حداکثر پنج مورد مجاز برای گیرنده. series گروه‌بندی‌شده و مالکان را به‌صورت داخلی حفظ کنید. | گروه‌بندی و ranking پیشنهادی به Evidence نیاز دارند؛ علت حدس‌زده‌شده نمی‌تواند مالکان را حذف کند. وزن‌های دقیق همچنان Open هستند. AT-08، AT-10، AT-11، AT-24. |
| R7 / 8 | metricهای `info` فقط برای نمایش هستند و هرگز alert ایجاد نمی‌کنند. | `rule=info` canonical، مقدار، scope. | اطلاعات واجد شرایط را نمایش دهید. هیچ رخداد alert یا escalation از این metric ایجاد نمی‌شود. | مقدار نمایش‌داده‌شده وارد episode مربوط به alert نمی‌شود. metricهای واجد شرایط دیگر همچنان می‌توانند alert ایجاد کنند. AT-02، AT-24. |
| R8 / 9 | `threshold_from_day8` منطق آستانه‌ای است که فقط از روز 8 هر ماه جلالی ارزیابی می‌شود. | `cal.day_in_month` ارائه‌شده، metadata آستانه، مقدار واجد شرایط. | پیش از روز 8: بدون alert آستانه. از روز 8: از مسیر آستانه و مالکیت عادی استفاده کنید. | نسخه‌های ماه/دانش را نگه دارید. از روز ماه Gregorian یا اصلاحات حدس‌زده‌شده تقویم استفاده نکنید. AT-03، AT-07، AT-24. |

تمایزهای منبع ثابت هستند: R2 از `> escalate_after_days` و `>=20%` استفاده می‌کند؛ R5 از `>N%` استفاده می‌کند؛ R4 تکرار جدید برای `<10%` را حذف می‌کند. منبع همه حالت‌های equality یا baseline صفر را حل نمی‌کند. ADR-07 فقط آن انتخاب‌های باقی‌مانده را حفظ می‌کند. فرمول‌های candidate، قوانین نمونه baseline، recovery مربوط به episode و حالت missing-warn در R3 باید پیش از استفاده نام‌گذاری و تأیید شوند.

brief در p.8 بررسی recurrence/escalation را در سه نقطه الزامی می‌کند: detection، ساخت گزارش و Validation نهایی. در هر سه نقطه از همان نسخه‌های Rule و سابقه گیرنده استفاده کنید. بررسی بعدی نباید رخداد دوم ایجاد کند. AT-24 هر Rule و هر نقطه کنترل را پوشش می‌دهد.

`series_key = kpi_id + entity_id + dimension` است. تاریخ هر occurrence جدا ثبت می‌شود. episode با استمرار مسئله مرتبط است، نه با یک مقدار گرد‌شده. هر مخاطب `first_seen, last_sent, first_value, last_value, escalation_reason` جدا دارد. افزایش سطح، تاریخچهٔ گزارش مالک را پاک نمی‌کند.

اولویت‌بندی پیشنهادی: شدت، اثر مشتری، اثر مالی مستند، وابستگی بین‌واحدی، اطمینان شواهد و اولویت اعلام‌شدهٔ مدیر. وزن‌ها تنظیمات نسخه‌دار هستند؛ عددهای نمایشی بریف وزن مصوب نیستند. اولویت مدیر نمی‌تواند دادهٔ غایب یا قید دسترسی را نادیده بگیرد.

تغییر مقدار ناشی از اصلاح، backfill، dedup یا schema repair به `knowledge_revision` متصل می‌شود. خود این تغییر، علت تجاری جدید نیست. وضعیت تجاری جاری فقط با شواهد واجد شرایط جداگانه ارزیابی می‌شود. گزارش‌های قدیمی و تشدیدهای واقعاً ارسال‌شده حفظ می‌شوند.

### ۷.۲. سه Workflow و Process Mining سبک

| Workflow | case و مراحل اصلی | خروجی و محدودیت |
|---|---|---|
| `WF1` | `order_id`: created، paid، picked، handed_over، delivered؛ سپس اتصال تیکت از `tickets.order_id` | SLA مراحل ۱، ۱۲ و ۶ ساعت؛ تحویل نسبت به `promised_by`. مرحلهٔ پیگیری SLA عددی ندارد. `K_WF1_SLA` فقط فرمول خود dictionary را اجرا می‌کند. |
| `WF2` | `ticket_id` مربوط به `T_CMP`: created، first_response، inspected، resolved | مراحل ۸، ۳۶ و ۲۴ ساعت از config. KPI کلی `K_WF2_SLA` حل در ۴۸ ساعت است؛ جمع مهلت مراحل جای آن را نمی‌گیرد. |
| `WF3` | `lead_id`: created، first_contact، qualified، proposal_sent، won/lost | مهلت مراحل ۲۴، ۷۲، ۱۲۰ و ۷۲۰ ساعت. KPI هفت‌روزهٔ WF3 همهٔ همین مراحل را عیناً نمی‌سنجد؛ SQL معیار نهایی است. |

#### همه stageهای ارائه‌شده Workflow

12 رکورد زیر از `workflow_definitions.csv` می‌آیند. مالک end-to-end هر Workflow برابر `M01` است. این واقعیت مالک stage را تعیین نمی‌کند. targetهای مدت‌زمان، targetهای median هستند و جایگزین SLA نمی‌شوند. مسئولیت stage-to-team طبق ADR-15 همچنان Open است.

| Stage / رکورد CSV | از | به | SLA | target مربوط به Median، ساعت |
|---|---|---|---|---|
| WF1.1 / 2 | `created_at` | `paid` | 1 ساعت | 0.25 |
| WF1.2 / 3 | `paid` | `picked` | 12 ساعت | 4 |
| WF1.3 / 4 | `picked` | `handed_over` | 6 ساعت | 3 |
| WF1.4 / 5 | `handed_over` | `delivered` | مرجع deadline مربوط به `promised_by` | 24 |
| WF1.5 / 6 | `delivered` | ticket با دسته follow-up | ارائه نشده | ارائه نشده |
| WF2.1 / 7 | `created_at` | `first_response` | 8 ساعت | 4 |
| WF2.2 / 8 | `first_response` | `inspected` | 36 ساعت | 18 |
| WF2.3 / 9 | `inspected` | `resolved` | 24 ساعت | 8 |
| WF3.1 / 10 | `created_at` | `first_contact` | 24 ساعت | 8 |
| WF3.2 / 11 | `first_contact` | `qualified` | 72 ساعت | 48 |
| WF3.3 / 12 | `qualified` | `proposal_sent` | 120 ساعت | 96 |
| WF3.4 / 13 | `proposal_sent` | `won/lost` | 720 ساعت | 400 |

WF1.5 از label منبع `ticket پیگیری سفارش` استفاده می‌کند، نه نوع order-event ارائه‌شده. projection دقیق ticket-category/time آن همچنان یک قرارداد پیاده‌سازی است که باید مشخص شود. SLA مفقود برابر صفر نیست. `promised_by` یک Field مربوط به deadline است، نه مدت‌زمان 24 ساعت.

KPIهای canonical مربوط به Workflow جدا هستند: WF1 چهار شرط SQL خود را بررسی می‌کند؛ WF2 اختلاف resolved-minus-created را در 48 ساعت بررسی می‌کند؛ WF3 از population مربوط به closed-lead در rolling هفت‌روزه استفاده می‌کند و first contact، qualified-to-proposal و proposal-to-close را بررسی می‌کند. SQL آن شامل آزمون 72 ساعته WF3.2 نیست. آن آزمون stage را به فرمول canonical اضافه نکنید. Observationهای سطح stage همچنان هر چهار stage مربوط به WF3 را شامل می‌شوند. AT-12 و AT-25 را ببینید.

projection فرآیند، مسیرها، مراحل طی‌شده، تکرار مرحله، ترتیب نامعتبر، case باز و زمان انتظار را ثبت می‌کند. case باز، نمونهٔ تکمیل‌شده برای median نیست؛ مدت انتظار آن در series جداست. نبود مرحله، شکست SLA یا صفر زمان فرض نمی‌شود.

نقشهٔ `directly-follows`، تعداد case، مدت مرحله، درصد SLA و backlog برای تشخیص گلوگاه کافی است. فعلاً موتور BPM، کشف فرایند با مدل پیچیده یا زیرساخت مستقل لازم نیست. گلوگاه از دادهٔ واقعی و هدف همان مرحله به دست می‌آید. آستانهٔ نمونهٔ کم و رتبه‌بندی گلوگاه پیشنهاد طراحی هستند.

روابط `order_id` و `ticket_id` شواهد اتصال پرونده‌اند. `mkt_daily` شناسهٔ lead ندارد؛ اتصال تک‌به‌تک تبلیغ به قرارداد از آن قابل اثبات نیست. مسیر بازاریابی به CRM فقط در سطح source و بازهٔ زمانی بررسی می‌شود، مگر رابطهٔ معتبر دیگری ارائه شود.

مالک انتهابه‌انتهای هر Workflow از ستون `owner` در S11 می‌آید. برای انتساب گلوگاه به مرحله، `order_events.actor_team` یا رابطهٔ مجاز staff/team در زمان رخداد بررسی می‌شود. نبود actor معتبر، مجوز حدس‌زدن مالک مرحله نیست؛ mapping تکمیلی stage-to-team در policy catalog تأیید شود. این metadata با مالک KPI موجود جایگزین نمی‌شود.

fact مرجع با projection چرخهٔ جاری یکی نیست. برای مثال `ticket_fact.resolved_at` برابر MAX است و `reopened` را جدا نگه می‌دارد. نمایش پروندهٔ بازشدهٔ مجدد نباید فرمول backlog مرجع را بی‌صدا تغییر دهد.

<a id="system-8"></a>

## ۸. تحلیل مبتنی بر شواهد و Insight Brief

برای هر مورد، ابتدا `EvidenceBundle` قطعی ساخته می‌شود: query مربوط به KPI، شکست مجاز بر حسب زمان/کانال/شهر/دسته، دادهٔ Workflow، رویداد زمینه‌ای، ظرفیت تجمیعی و تصمیم‌های گذشته. شناسهٔ evidence تا فایل و ردیف منبع قابل پیگیری است.

`Requirement`: هر علت منتشرشده به حداقل دو شاهد مستقل، confidence و علت‌های جایگزین نیاز دارد (brief p.9). `Proposed`: برای پیاده‌سازی این بررسی از گروه‌های Evidence آگاه از Lineage استفاده کنید. خود آزمون استقلال به‌عنوان algorithm تأییدشده ارائه نشده است. دو KPI مشتق از یک جمعیت، دو شاهد مستقل نیستند. نمونهٔ مناسب، تغییر صف تیکت و دادهٔ ظرفیت تجمیعی از منبع جداست. استقلال مسیر مشاهده، استقلال آماری یا اثبات علیت نیست؛ S02 تصریح می‌کند که کل داده از یک شبیه‌سازی مشترک ساخته شده است.

| نوع گزاره | شرط |
|---|---|
| `observed_fact` | نتیجهٔ query ثبت‌شده، snapshot معلوم، مقدار و scope تأییدشده. |
| `supported_hypothesis` | حداقل دو گروه شاهد، ترتیب زمانی سازگار، محدودیت‌ها و علت جایگزین؛ متن با زبان احتمالی. |
| `needs_evidence` | کمتر از شواهد لازم یا تعارض؛ علت قطعی در گزارش ساخته نمی‌شود. اقدام بعدی برای جمع‌آوری شاهد پیشنهاد می‌شود. |
| `decision_option` | مالک، هزینه/اثر در صورت وجود evidence، ریسک، مهلت و معیار موفقیت؛ عدد تخمینی بدون روش و query ممنوع. |

`cause_confidence` با `source_completeness` یا صحت عدد یک فیلد نیست. روش امتیازدهی اطمینان باید نسخه‌دار و قابل توضیح باشد؛ عدد ۰ تا ۱ احتمال آماری کالیبره‌شده فرض نمی‌شود. برچسب کم/متوسط/زیاد و دلیل آن در متن بیاید. ادعای اثر تصمیم نیز مشاهدهٔ قبل/بعد است؛ هم‌زمانی، اثبات اثر علّی نیست.

ابزارهای مجاز تحلیل محدودند: `read_kpi`، `query_scoped_data`، `read_workflow`، `read_calendar_context`، `read_decision_history` و `propose_action_draft`. ابزار ویرایش منبع، ارسال پیام، جابه‌جایی نیرو و تغییر خودکار هدف وجود ندارد. درخواست tool دوباره مجوز، snapshot، row limit و بودجه را بررسی می‌کند.

ابزار `propose_action_draft` فقط با `DecisionEvent` معتبر و تأییدشدهٔ مدیر فعال می‌شود. پیش از آن، مدل فقط گزینهٔ تصمیم را در Insight Brief پیشنهاد می‌کند. هیچ فرمان داخل فایل، مدرک تأیید مدیر محسوب نمی‌شود.

یک `InsightBrief` نسخه‌دار منبع مشترک گزارش‌هاست. projection هر نقش فقط evidence مجاز همان نقش را شامل می‌شود. Brief حاوی اطلاعات فردی تیم به Writer مدیر بالاتر داده نمی‌شود. هم‌معنابودن تحلیل نباید به اشتراک‌گذاری خام prompt میان مدیران منجر شود.

مجوز نتیجهٔ مشتق نیز از شواهد آن پیروی می‌کند. مخاطب یک علت باید مجوز همهٔ شواهد لازم برای همان علت را داشته باشد. حذف یک جدول محرمانه و نگه‌داشتن نتیجه‌ای که از آن به دست آمده، کنترل دسترسی کافی نیست. برای مخاطب محدود، علت حذف یا با شواهد مجاز دوباره ساخته شود. انتشار خلاصهٔ بین‌واحدی فقط با grant صریح و خروجی تجمیعی مصوب مجاز است.

### Confidence و ادعاهای عددی

`Requirement`: confidence و گزینه‌های جایگزین را بیان کنید و هر ادعای عددی را تا یک query ثبت‌شده و اجراشده ردیابی کنید. DSL موجود F01 این مرز را برای confidence، ظرفیت، baselineها، هزینه و اثر تخمینی حفظ می‌کند. `Proposed`: تا زمانی که تعریف scoring تأییدشده و نتیجه query ثبت‌شده وجود ندارد، از cause confidence کیفی استفاده کنید. عدد 0 تا 1 تولیدشده توسط Model، Evidence اجرا یا احتمال calibrated نیست.

Schema خروجی یک `causes[].confidence` عددی و اختیاری بین 0 و 1 را مجاز می‌داند. این Schema به score ساختگی نیاز ندارد. اگر confidence کیفی است، هنگام بازبینی نگاشت دقیق internal/wire، آن را در متن مجاز گزارش نگه دارید. در property عددی string تولید نکنید. ADR-09، DL-18، AT-10 و AT-30 را ببینید.

### ۸.۱. بودجه و رفتار هنگام خرابی LLM

سقف الزام‌شده ۵ دلار برای مجموع گزارش، تحلیل، پرسش‌های همان روز و retryهاست. `BudgetLedger` پیش از هر فراخوانی، هزینهٔ حداکثری آن را رزرو و پس از پاسخ با مصرف واقعی تسویه می‌کند. نرخ مدل از price config دارای تاریخ می‌آید. مدل یا قیمت مشخص در این طرح تثبیت نشده است.

پیشنهاد اولیه: تحلیل عمیق فقط برای موارد مهم، حداکثر دو دور تکمیل شواهد در هر تحلیل و سهم ذخیرهٔ بودجه برای QA. حدود دقیق در ADR-10 تصویب و با تست بار سنجیده شوند. عدد تقریبی هشت تحلیل در بریف سهمیهٔ اجباری نیست.

`Proposed`: cacheها را با Snapshot، hash مربوط به query/result، scope، policy، Model، prompt و revision مربوط به Evidence کلیدگذاری کنید. template fallback فقط می‌تواند از عددهای Validation‌شده و محتوای پشتیبانی‌شده استفاده کند. انتخاب fallback، timeout و محدودیت‌های repair همچنان Open هستند. اگر نتواند Validation را بگذراند، failure گزارش را ثبت کنید. انتشار مستقل Accepted است؛ این وضعیت تضمین نمی‌کند که هر call ناموفق Model با موفقیت جایگزین شود.

<a id="system-9"></a>

## ۹. رابط‌های مدیریت و خروجی

`Requirement`: یک assistant مکالمه‌ای فارسی RTL، یک dashboard مبتنی بر نقش BI و یک اتاق کنترل Workflow ویژه مدیر ارشد فراهم کنید. `Proposed`: این موارد می‌توانند frontend و layout صفحه مشترک داشته باشند. دقیقاً سه صفحه، Requirement منبع نیست. سابقه تصمیم/action و drill-down مجاز query باید در دسترس بماند.

| نقش | محتوای مجاز |
|---|---|
| مدیر ارشد | سلامت سازمان، پنج KPI اصلی، سه Workflow، موارد تشدیدشده و اثر تصمیم‌ها؛ دادهٔ کارکنان فقط تجمیعی. |
| مدیر واحد | شاخص‌ها و تیم‌های زیرمجموعه، ریسک وابستگی و گزینهٔ تخصیص منابع؛ بدون نام و بارکاری فردی. |
| سرپرست | KPI تیم، کارهای باز، موانع و بارکاری اعضای مستقیم برای مدیریت کار؛ بدون رتبه‌بندی یا معرفی مقصر. |

تعداد تیم و مدیر در UI ثابت نوشته نمی‌شود. `M11/T_MKT` آزمون تغییر سازمان است، نه استثنای کدنویسی. ابهام زمان فعال‌شدن آن در ADR-08 ثبت شده است.

### محتوای کامل گزارش

محتوای زیر طبق brief در pp.9-12 الزامی است. Schema ارائه‌شده JSON همه Fieldهای زیر را تعریف نمی‌کند. `Proposed`: این Fieldها را در یک مدل محتوای داخلی Validation‌شده نگه دارید. در مواردی که Schema محل را تعیین نمی‌کند، جای‌گذاری نهایی wire همچنان Open است. Schemaهای منبع را تغییر ندهید.

| خروجی | Fieldها یا رفتار الزامی | منبع / gate |
|---|---|---|
| مورد صبحگاهی | عنوان، عدد و target، علت احتمالی، مالک و پرسش پیشنهادی. | p.10; AT-26 |
| مشخصات Chart | نوع Chart، metric، بازه زمانی، breakdown و خط target. Chartها خروجی الزامی هستند، نه diagramهای اختیاری معماری. | pp.10-11; AT-26 |
| کارت تصمیم مهم/escalated | مسئله، گزینه‌ها، اثر تخمینی پشتیبانی‌شده، هزینه، ریسک، confidence، مالک اجرا، deadline، معیار موفقیت و Evidence پشتیبان. تخمین ساختگی مجاز نیست. | pp.10-12; AT-10, AT-14, AT-26 |
| package مشترک | سلامت scope، حداکثر پنج مورد مهم، تصمیم‌های در انتظار، actionهای Open و deadlineها، اثرهای مشاهده‌شده تصمیم و لینک dashboard. | pp.10-11; AT-11, AT-26 |
| وضعیت و عملیات | وضعیت خواندن، تصمیم ثبت‌شده و ارجاع؛ عملیات مجاز بستن/ارجاع در مکالمه. این موارد action سازمانی را اجرا نمی‌کنند. | pp.3,11-12; AT-14, AT-29 |
| محتوای مدیر ارشد | پنج شاخص کلیدی سلامت، هر سه Workflow و bottleneckهای stage، escalationها، تصمیم‌های در انتظار و اثر تصمیم‌های قبلی. | pp.5,11; AT-12, AT-26 |
| محتوای واحد/supervisor | سلامت مجاز واحد/team؛ کار و blockerهای team مستقیم فقط در مواردی که به‌صورت فردی مجاز است. نقش‌های بالاتر aggregateها را دریافت می‌کنند. | pp.5,10,13; AT-06, AT-26 |
| خلاصه ماهانه هیئت‌مدیره | در پایان ماه اختیاری است. این مورد dependency پذیرش روزانه نیست. | p.10; AT-26 scope check |

Fieldهای داخلی Insight باید هر هشت بخش brief را پوشش دهند: summary/impact؛ metric/deviation؛ breakdown؛ possible causes/confidence؛ decision options؛ history/prior decisions؛ proposed owner؛ registered queries. از projectionهای مجاز منبع تحلیلی مشترک استفاده کنید. تحلیل عمیق بدون محدودیت را برای هر مدیر تکرار نکنید. Schema داخلی دقیق طبق ADR-09 همچنان Open است.

### ۹.۱. قرارداد خروجی و کنترل پیش از انتشار

`submission/briefs/day_XXX/<manager_id>.json` از `brief_schema.json` ساخته می‌شود. `report_day, manager_id, items, numbers, data_issues, text_fa` الزامی‌اند. `items` حداکثر پنج مورد دارد. هر عدد، KPI/entity/dim/date/value و `query_id` قابل ردیابی دارد. اگر schema فیلدی را اختیاری بداند ولی بریف آن را برای ردیابی لازم بداند، Validator داخلی آن را الزامی می‌کند.

متن و JSON از یک مدل محتوای تأییدشده تولید می‌شوند. بازنویسی فارسی فقط ظاهر رقم و جمله را تغییر می‌دهد. استخراج عدد از متن، کنترل واحد، تطبیق evidence و کنترل دسترسی پیش از انتشار انجام می‌شود. مقدارهای ساختگی `example_brief.json` و تاریخ ناسازگار آن در محاسبه استفاده نمی‌شوند.

`Requirement`: مقدار `data_issues.source` یکی از `orders, tickets, crm, tasks, marketing, sessions, availability` است. مقدار `data_issues.type` یکی از `missing, late_arrival, duplicate, schema_change, late_correction, other` است. `Proposed`: مسائل csat/ticket-event را به خانواده tickets نگاشت کنید و فایل واقعی را در جزئیات مجاز نگه دارید. این alias mapping قرارداد per-file ارائه‌شده نیست. مقدار جدید به Enum اضافه نکنید. AT-30 را ببینید.

برای دادهٔ ناموجود، `value=null` و issue ثبت شود. `open_items` محل موارد بدون تغییر است. وضعیت‌های item فقط `new, escalated, ongoing` هستند. بریف ص۱۵ از `suppressed` نام می‌برد؛ proposed mapping, pending organizer confirmation، نگهداری suppression در ledger داخلی و `open_items` است، نه فرستادن enum نامعتبر. این نگاشت نیازمند تأیید ADR-09 است.

پاسخ پرسش در `submission/qa/<input_id>.json` ذخیره می‌شود. وضعیت فقط یکی از `answered, refused_out_of_scope, refused_individual_data, data_unavailable, clarification_requested` است. query واقعاً اجراشده، rows و تعریف استفاده‌شده همراه پاسخ می‌آید. SQL پیشنهادی اجرا‌نشده به‌عنوان SQL اجراشده ثبت نمی‌شود.

در پرسش مبهم «فروش»، تعریف روشن شود: ثبت سفارش، فروش ناخالص، خالص B2C یا درآمد شامل قرارداد. گزارش قدیمی و فایل بیرونی تا تعیین تعریف و بازه وارد KPI مرجع نمی‌شوند. تفاوت، با reconciliation ثبت‌شده توضیح داده می‌شود؛ برابرسازی عددها هدف نیست.

### مرزهای دقیق wire-schema

برای همه Fieldهای ارائه‌شده، [رکورد کامل property/pointer](audit-2026-11-09/output-schema-contracts.csv) را بخوانید. این قوانین Schema جایگزین Requirementهای روایی، عددی یا دسترسی نمی‌شوند.

| Scope | محدودیت دقیق منبع | مرز معنایی اضافی |
|---|---|---|
| ریشه Brief | الزامی: `report_day, manager_id, items, numbers, data_issues, text_fa`. | roster فعال، cutoff، محتوای فارسی و بخش‌های الزامی گزارش را بررسی کنید. مقدار integer مربوط به report_day به‌تنهایی روز معتبر Replay را اثبات نمی‌کند. |
| هر item | الزامی: `item_id, status, kpi_id, entity_id, dim, kpi_date, value, causes, owner_manager_id`. حداکثر پنج item. | مالک درست، پشتیبانی علت و recurrence بررسی‌های جداگانه هستند. array خالی causes می‌تواند Schema را بگذراند، اما علت پشتیبانی‌شده یا تشخیص رسمی event را اثبات نمی‌کند. |
| ورودی Number / Evidence | الزامی: `kpi_id, entity_id, dim, kpi_date, value`. مقدار `value` عددی یا null است. `query_id` در Schema اختیاری است. | brief همچنان برای هر عدد گزارش‌شده به query ثبت‌شده نیاز دارد. تاریخ، واحد، precision، Snapshot/revision و Scope را بررسی کنید. |
| وضعیت item | `new, escalated, ongoing`. | تعارض `suppressed` در brief همچنان Open است. Enum چهارم wire نسازید و برچسب item را بدون اعلام تغییر ندهید. |
| Confidence علت | `confidence` عددی اختیاری، حداقل 0 و حداکثر 1. | این مقدار نمی‌تواند شامل string کیفی یا ادعای احتمال ساختگی/calibrated باشد. از مرز Confidence بازبینی‌شده بالا استفاده کنید. |
| اثر follow-up تصمیم | `improved, worsened, no_change, too_early`. | Evidence باید Observation بیان‌شده را پشتیبانی کند. Enum اثبات اجرا یا علیت نیست. |
| ریشه/وضعیت QA | الزامی: `question_id, manager_id, answer_status, answer_fa`. وضعیت: `answered, refused_out_of_scope, refused_individual_data, data_unavailable, clarification_requested`. | refusalها به row یا SQL ساختگی نیاز ندارند. failure فنی job یک Enum جدید QA نیست. rowها/SQL/تعریف واقعی در صورت اعتبار و مجازبودن نشان داده می‌شوند. |
| ساختارهای اختیاری | `open_items`، `decision_followups`، `mentioned_staff_ids`، محتوای مرتبط با chart/card و rowهای QA دارای قوانین property/type ارائه‌شده هستند. | Fieldهای اختیاری wire، محتوای الزامی brief یا ثبت کارکنان نام‌برده را حذف نمی‌کنند. Fieldهای اضافی مجاز در Schema به‌صورت خودکار تأیید evaluator نیستند. |

### آخرین مقدار معتبر و failure گزارش

S16 Q06 نمایش آخرین مقدار معتبر را با تاریخ واقعی آن ثبت می‌کند. S17 این رفتار را حفظ می‌کند. این context تاریخی را حفظ کنید. هرگز مقدار قبلی را در Field مربوط به KPI با تاریخ کنونی قرار ندهید. مقدار کنونی ناموجود همراه با مسئله داده به‌صورت `null` باقی می‌ماند. عدد تاریخی به تاریخ واقعی KPI، query، Snapshot و بررسی دسترسی کنونی نیاز دارد. Eligibility، حداکثر عمر و نگاشت دقیق خروجی در [ADR-04](003-decisions-and-roadmap.md#adr-04) همچنان Open هستند.

انتشار مستقل Accepted است. package الزامی ناموفق یا مفقود را حتی در صورت نبود draft ثبت کنید. تا زمانی که آن failure باقی است، روز نمی‌تواند بررسی coverage را بگذراند. fallback باید همه بررسی‌ها را بگذراند و نباید علت بسازد. policy تفصیلی آن طبق ADR-14 همچنان Proposed است.

<a id="system-10"></a>

## ۱۰. امنیت و حاکمیت

دامنهٔ دسترسی تصمیم باز نیست: بریف ص۱۰ و ص۱۳ و `../../DataSet/arka_dataset/org/access_matrix.csv` مرجع الزام‌اند. مدیران M01 تا M04 فقط دادهٔ تجمیعی زیرمجموعه را می‌بینند. سرپرستان M05 تا M11 فقط در تیم مستقیم خود دادهٔ فردی برای مدیریت بار کار دارند. مرخصی فقط ظرفیت تجمیعی تیم است؛ مجوز فردی این محدودیت را حذف نمی‌کند. جدول کامل دامنه‌ها و تفکیک الزام از جزئیات اجرای باز در ADR-06 سند 003 ثبت شده است. فهرست ستون‌های مجاز منابع مشترک باید از این قواعد استخراج و آزموده شود؛ بریف فهرست تک‌تک ستون‌ها را تعیین نکرده است.

`visible_entities` با سلسله‌مراتب فعال و مجوز منبع ترکیب می‌شود. فقط داشتن نقش مدیر بالاتر، مجوز دادهٔ فردی نمی‌دهد. `individual_level_data_team` استثنای محدود برای سرپرست مستقیم است. `staff_availability.status` نباید به فهرست حضور و مرخصی اشخاص تبدیل شود؛ ظرفیت برای تحلیل بالاتر تجمیعی است.

کنترل فیلد فردی به ستون staff_id محدود نیست. نام کارکنان یا اطلاعات فردی داخل `text_fa`، title و blocker نیز پیش از ورود به LLM بررسی و در صورت نامجازبودن حذف شوند. ذکر نام مجاز در گزارش باید با `mentioned_staff_ids` منطبق باشد. حذف شناسهٔ ساختارمند، متن آزاد را خودکار مجاز نمی‌کند.

| مسیر | کنترل لازم |
|---|---|
| KPI ذخیره‌شده | RLS بر entity، active roster، snapshot و sensitivity؛ ارجاع از report نیز دوباره مجوز می‌خواهد. |
| raw و event | فقط هویت ingestion/calculation محدود؛ مدیر و LLM مجوز مستقیم روی مخزن خام ندارند. |
| ad hoc SQL | انتخاب schema مجاز، AST validation، transaction فقط‌خواندنی، محدودیت زمان/حجم و RLS پیش از نتیجه. |
| evidence و فایل | مجوز در retrieval، حذف فیلد فردی نامجاز و ثبت مقصد؛ متن آزاد untrusted است. |
| cache و log | کلید scope و policy؛ لاگ کامل تنها برای نقش audit؛ خطا و query plan نیز ممکن است داده افشا کنند. |
| تغییر تنظیم و تصمیم | هویت actor، دامنهٔ اختیار، نسخهٔ قبل/بعد و زمان اثر؛ پیشنهاد LLM تغییر معتبر نیست. |

در PostgreSQL نقش کاربری نباید owner جدول، superuser یا دارای `BYPASSRLS` باشد. `FORCE ROW LEVEL SECURITY` و تست owner bypass برای جدول‌های مربوط بررسی شوند. سیاست‌های permissive با OR ترکیب می‌شوند؛ ترکیب مجوز عمومی و فردی باید آزمون منفی داشته باشد. این ویژگی‌ها در [مستندات رسمی Row Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) توضیح داده شده‌اند.

`principal_id` و scope در context سرور ثبت می‌شوند. SQL تولیدی اجازهٔ `SET ROLE`، `set_config`، دسترسی به schema داخلی یا function دارای اثر جانبی ندارد. connection pool در پایان transaction context را پاک می‌کند. view دارای امتیاز مالک نباید RLS را دور بزند.

SQL تعاملی فقط در PostgreSQL و از طریق QueryGateway اجرا می‌شود. از relationهای تأییدشده، هویت server قابل‌اعتماد، نقش‌های read-only، کنترل‌های row و column، Validation مربوط به statement و محدودیت‌های resource استفاده کنید. Agent هیچ credential مستقیمی ندارد. privilegeهای Batch نباید به privilegeهای user-query تبدیل شوند. context مربوط به Pool، functionها، errorها، logها، cacheها و exportها به بررسی امنیتی نیاز دارند. این کنترل‌ها قراردادهای طراحی هستند. آن‌ها در اینجا پیاده‌سازی نشده‌اند.

بعضی جدول‌ها مانند orders فاقد team_id هستند. دسترسی آن‌ها از `resource_scope_policy` تأییدشده می‌آید؛ به همهٔ مدیران صرفاً به علت مصرف مشترک جدول داده نمی‌شود. `T_MKT` می‌تواند policy کانال marketplace داشته باشد؛ عملیات، policy مرحلهٔ عملیاتی؛ این نگاشت‌ها باید پیش از Text-to-SQL در ADR-06 تصویب شوند. KPI سازمان به KPI واحد تغییر نام داده نمی‌شود.

در متن upload روز ۷۳، دستور پنهان برای حذف عددهای منفی و ارسال گزارش به همه وجود دارد. این متن فقط دادهٔ غیرقابل اعتماد است. parser یا LLM حق تغییر policy، مقصد، عدد یا tool از روی آن ندارد. کنترل مقصد و عدد بعد از تولید نیز مستقل اجرا می‌شود.

<a id="system-11"></a>

## ۱۱. توسعه‌پذیری و حدود نسخهٔ اول

افزودن منبع، adapter و SourceContract جدید می‌خواهد. افزودن KPI، registry entry، dependency spec و parity fixture می‌خواهد. افزودن سطح سازمان، node و policy می‌خواهد. هیچ‌یک نباید بازطراحی جریان روزانه را لازم کند.

`Accepted`: از یک AI Agent محدود استفاده کنید. `Proposed`: broker، Kubernetes، پایگاه‌های داده graph/vector و زیرساخت‌های دیگر را تا زمانی به تعویق بیندازید که یک نیاز اندازه‌گیری‌شده از ADR جداگانه پشتیبانی کند. منبع این فناوری‌ها را ممنوع نمی‌کند. PostgreSQL تنها موتور پایگاه داده محصول باقی می‌ماند.

مرز توقف این تحویل، همین طراحی است. پیاده‌سازی، نصب package، تغییر dataset، تغییر SQL، تغییر ممیزی، commit و push در این کار انجام نمی‌شود.

Audit trail: [یافته‌های تفصیلی](audit-2026-11-09/audit-report.md)، [ماتریس ردیابی](audit-2026-11-09/requirements-traceability.csv) و [شکاف‌های Structurizr](audit-2026-11-09/structurizr-gap-report.md). همه gateهای پذیرش محصول همچنان برنامه‌ریزی‌شده هستند.
