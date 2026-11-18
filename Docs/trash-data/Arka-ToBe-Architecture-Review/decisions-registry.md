# دفتر ثبت تصمیم‌ها

<a id="decisions-registry-overview"></a>

محل مستند: سابقهٔ حاکمیتی تعیین‌شده توسط تیم. وضعیت: **Draft / Pending Review**. سوابق کامل منبع و معیارهای زیر در قالب Markdown خوانا هستند. متن فهرست، راهنمای این سوابق است. تأیید ساختار، هیچ تصمیم، قاعدهٔ منبع، ارزیابی ریسک یا نتیجهٔ پذیرشی را تغییر نمی‌دهد.

وضعیت: **Draft / Pending Review**. وظیفه: `ARCH-REG-001`. تاریخ: 2026-11-09.

[قواعد دفتر ثبت](README.md) را بخوانید. وضعیت به هر گزارهٔ شماره‌دار مربوط است. یک سابقه می‌تواند چند وضعیت داشته باشد. گزیدهٔ منبع همهٔ شرایط و گزینه‌های اصلی را حفظ می‌کند. متن فهرست، راهنمای این گزیده است.

برای خط مبنای Accepted، نام مالک تصمیم یا تاریخ تأیید اولیه ارائه نشده است. نقش‌های زیر همان نقش‌های منبع هستند و انتصاب جدید نیستند. دروازهٔ پذیرش Open، مرز Accepted را دوباره باز نمی‌کند.

<a id="adr-01"></a>

## ADR-01: SQLite as the product and reference engine

Problem / Context: The supplied canonical SQL and results use SQLite. The team no longer uses PostgreSQL.

Decision owner: User decision recorded on 2026-11-11. Engineering verifies the SQLite implementation.

Closure condition: The engine decision is complete. Inspect SQLite receipts for all 55 definitions and replay mornings. DL-19 separately controls changes to existing KPIs.

Source Evidence: [ADR-01](decisions-registry.md#adr-01). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-01-S01 | Superseded | The earlier PostgreSQL-only decision is replaced by the user decision dated 2026-11-11. |
| ADR-01-S01A | Accepted | SQLite is the only product and reference database engine for all 55 KPIs and custom queries. |
| ADR-01-S02 | Requirement | Preserve the original source data, SQL, views, definitions and canonical results. |
| ADR-01-S03 | Rejected | Do not create or maintain PostgreSQL translations. |
| ADR-01-S04 | Accepted | Run the canonical SQLite SQL in the product path. |
| ADR-01-S05 | Closed | No cross-engine translation strategy is required. |
| ADR-01-S06 | Closed | Cross-engine equivalence is not required; SQLite result validation remains in the acceptance tests. |

Accepted decision: See the Accepted statement rows.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [DL-19](open-issues-registry.md#dl-19)، [AT-02](acceptance-register.md#at-02)، [AT-03](acceptance-register.md#at-03)، [AT-05](acceptance-register.md#at-05)، [AT-17](acceptance-register.md#at-17)، [AT-27](acceptance-register.md#at-27).


### Full source record and conditions

### ADR-01: اجرای SQLite به‌عنوان موتور محصول و مرجع

**تصمیم پذیرفته‌شده:** طبق تصمیم کاربر در ۲۰۲۶-۱۱-۱۱، SQLite تنها موتور پایگاه داده محصول و مرجع محاسبه هر ۵۵ KPI و همه Queryهای سفارشی است. تصمیم قدیمی PostgreSQL کنار گذاشته شد.

**الزام:** تعریف‌ها و نتایج S03-S04 حفظ شوند. SQL اصلی و داده منبع تغییر نکنند. اجرای محصول باید همان رفتار و نتیجه مرجع SQLite را حفظ کند.

**ردشده:** تبدیل SQL به PostgreSQL، نگهداری دو موتور و استفاده از SQLite فقط به‌عنوان محیط آزمون انجام نمی‌شوند.

**آزمون باقی‌مانده:** صحت نتیجه SQLite برای NULL، نبود ردیف، تقسیم صحیح، زمان، گردکردن، Joinها، Dimensionها و همه صبح‌های بازپخش بررسی شود. این آزمون، مقایسه با PostgreSQL نیست.

**آزمون پذیرش:** AT-02، AT-03، AT-05 و AT-17. تا زمان اجرای این آزمون‌ها، صحت کامل هر ۵۵ شاخص یا کارایی SQLite ادعا نمی‌شود.

تغییر تعریف، فرمول، مالک و هدف KPI همچنان در DL-19 پیگیری می‌شود. افزودن KPI و تغییر KPI موجود در AT-27 دو آزمون جدا هستند. این موضوع تصمیم SQLite را تغییر نمی‌دهد.



<a id="adr-02"></a>

## ADR-02: Accepted orders input

Problem / Context: Day 076 has 699 raw rows and 437 distinct payloads. RAW/DEDUP changes eight KPIs. The net B2C difference is 332,060,000 toman; it is not gross revenue.

Decision owner: The project supporter/organizer supplies the answer. The team then approves the policy implementation.

Closure condition: Obtain the recorded source answer and relevant test receipts. Do not deduplicate events by order_id.

Source Evidence: [ADR-02](decisions-registry.md#adr-02). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-02-S01 | Requirement | Preserve source occurrences and canonical definitions. |
| ADR-02-S02 | Proposed | Compare versioned RAW and exact-payload DEDUP modes with separate lineage and result namespaces. |
| ADR-02-S03 | Open | Obtain the accepted orders input policy or an official expected result. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: در متن این ADR شناسهٔ صریحی وجود ندارد؛ ارجاع‌های ورودی DL را در ماتریس ببینید.


### Full source record and conditions

### ADR-02: ورودی پذیرفته‌شدهٔ orders

**وضعیت:** Open: سیاست پذیرفته‌شده ورودی RAW/DEDUP. Proposed: دو حالت مقایسه نسخه‌دار. Requirement: حفظ منابع و تعریف‌های Canonical.

**مسئله:** drop 076 دارای ۶۹۹ ردیف خام و ۴۳۷ payload متمایز است. RAW/DEDUP در S09 هشت KPI را عوض می‌کند. اختلاف B2C خالص در تشخیص خام، ۳۳۲٬۰۶۰٬۰۰۰ تومان است؛ با gross برابر نیست.

**پیشنهاد معماری:** هر دو input policy با نسخه، lineage و result namespace جدا پشتیبانی شوند. هیچ policy نهایی پیش‌فرض فرض نشود. حذف براساس order_id، به‌ویژه روی event، ممنوع است.

**تصمیم پذیرش لازم:** آیا رابطهٔ `orders` باید RAW باشد یا تکرارهای دقیق Payload را حذف کند؟ یک نتیجه مورد انتظار رسمی نیز می‌تواند این ابهام را حل کند.

**مالک پاسخ:** پشتیبان پروژه/برگزارکننده؛ تیم سپس پیاده‌سازی policy را تصویب می‌کند. این پرسش در S08-S09 باز مانده است. تا پاسخ، مقایسهٔ هر دو mode مجاز است، ولی نتیجهٔ نهایی accepted اعلام نمی‌شود.



<a id="adr-03"></a>

## ADR-03: Dependencies and selective recalculation

Problem / Context: Table dependencies and equal values do not prove the minimum affected set.

Decision owner: Data engineering and the test role are named as decision roles. No person is appointed.

Closure condition: Compare selective and full rebuild results for late data, corrections and repeated events. Invalidate changed contributors even when values are equal.

Source Evidence: [ADR-03](decisions-registry.md#adr-03). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-03-S01 | Requirement | Preserve cutoff and canonical results. |
| ADR-03-S02 | Proposed | Start with full snapshot rebuilds; then recalculate affected KPIs and, if needed, exact keys. |
| ADR-03-S03 | Proposed | Separate value dependencies from execution dependencies; use wider recomputation when evidence is incomplete. |
| ADR-03-S04 | Open | Approve the optimization scope and dependency algorithm. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: در متن این ADR شناسهٔ صریحی وجود ندارد؛ ارجاع‌های ورودی DL را در ماتریس ببینید.


### Full source record and conditions

### ADR-03: dependency و selective recalculation

**وضعیت:** Proposed: محاسبه مجدد مرحله‌ای. Open: دامنه بهینه‌سازی و تصویب آن. Requirement: حفظ Cutoff و نتایج Canonical.

**مسئله:** field، event selector، join، gate و window دامنهٔ اثر را تعیین می‌کنند. تساوی خروجی یا وابستگی سطح جدول برای تعیین حداقل اثر کافی نیست.

**پیشنهاد:** ابتدا full rebuild بر snapshot، سپس recompute در سطح KPIهای متأثر و بعد در صورت نیاز کلیدهای دقیق. DependencySpec شامل value dependencies و execution dependencies جدا باشد. اطلاعات ناکافی، fallback به recomputation گسترده‌تر می‌دهد.

**شرط تصویب:** selective و full rebuild برای همهٔ fixtureهای late/correction/repeated event برابر باشند؛ تغییر contributor بدون تغییر مقدار نیز invalidate شود. برای منبع غایب با تاریخ‌های نامعلوم، ادعای دامنهٔ دقیق ممنوع است.

**مالک تصمیم:** مهندسی داده و مسئول آزمون. انتخاب الگوریتم وابستگی، مجوز انتشار مقدار ناقص نیست.



<a id="adr-04"></a>

## ADR-04: Source completeness and publication

Problem / Context: A valid manifest or observed backfill does not prove source closure.

Decision owner: The organizer/source owner answers contract questions. Data and product roles handle design.

Closure condition: Record closure evidence and publication policy, then test them. Prior context must retain its actual date, query, snapshot, unit and current access. It must never replace current null.

Source Evidence: [ADR-04](decisions-registry.md#adr-04). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-04-S01 | Requirement | Continue reports; report missing current values as null with a data issue. |
| ADR-04-S02 | Proposed | Keep reference values internally and hold unresolved dependent current values while independent outputs continue. |
| ADR-04-S03 | Open | Define source-interval closure and release of values after unresolved incidents. |
| ADR-04-S04 | Open | Approve eligibility, maximum age and wire mapping for dated last-valid context. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [DL-02](open-issues-registry.md#dl-02)، [DL-03](open-issues-registry.md#dl-03).


### Full source record and conditions

### ADR-04: کامل‌بودن منبع و انتشار مقدار ناقص

**وضعیت:** Requirement: ادامه گزارش‌دهی و اعلام داده ناموجود. Open: بسته‌شدن منبع، سیاست آزادسازی مقدار و نگاشت زمینه تاریخی تاریخ‌دار.

**مسئله:** manifest درست و backfill مشاهده‌شده، closure را ثابت نمی‌کنند. دادهٔ فعلی کران تأخیر یا expected total مستقل ندارد. S10 هیچ مقدار عددی نگه‌داشته‌شده‌ای را به‌عنوان «قطعاً بی‌دلیل withheld» اثبات نکرده است.

**پیشنهاد اولیه:** مقدار reference داخلی حفظ شود. خروجی مستقل منتشر شود. خروجی وابسته به incident حل‌نشده تا تعیین سیاست، `null` و issue داشته باشد. نبود SQL row از missing value جدا بماند. عدم closure کلی، برچسب `not_asserted` است؛ لزوماً تمام نتایج عادی بدون incident را مسدود نمی‌کند.

**گزینه‌ها:** hold برای unresolved incident؛ انتشار delivered-snapshot با برچسب صریح؛ یا release مبتنی بر closure معتبر. data model هر سه را پشتیبانی می‌کند.

**دو پاسخ لازم:** چه سند یا قرارداد، source interval را کامل می‌داند؟ آیا نمایش مقدار دقیق snapshot ناقص با برچسب روشن برای ارزیابی پذیرفته است؟

**مالک پاسخ:** برگزارکننده/مالک منبع. **مالک طراحی:** تیم داده و محصول. threshold تأخیر دلخواه، پاسخ این پرسش نیست.

**نتیجه Q06 و مرز مقدار جاری:** خلاصه S16 نمایش آخرین مقدار معتبر با تاریخ واقعی را ثبت می‌کند. Report Writer در S17 آن را حفظ می‌کند. رفتار نمایشی موجود حفظ شود. شروط آزادسازی آن Open هستند. مقدار قبلی نباید جای مقدار جاری ناموجود را بگیرد. خروجی جاری همچنان `null` با مسئله داده است. زمینه تاریخی فقط با تاریخ واقعی KPI، Query، Snapshot، واحد و مجوز فعلی نمایش داده شود. حداکثر قدمت و نگاشت خروجی به تصمیم نیاز دارند. این مورد، انتخاب میان نگهداری مقدار، انتشار مشروط یا آزادسازی مبتنی بر بسته‌شدن منبع را نمی‌بندد. به DL-02 و DL-03 مراجعه کنید.



<a id="adr-05"></a>

## ADR-05: Restatement and report versions

Problem / Context: Later knowledge can change an old business date without changing the actual report sent that morning.

Decision owner: Product and architecture roles.

Closure condition: Approve restatement and notification rules and inspect version/cutoff evidence. Historical corrections do not cancel past human decisions.

Source Evidence: [ADR-05](decisions-registry.md#adr-05). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-05-S01 | Proposed | Preserve immutable reports and separate as_reported, restated and counterfactual modes. |
| ADR-05-S02 | Proposed | Create a restated version with a new cutoff and explicit link to the first report. |
| ADR-05-S03 | Open | Select which changes require notice, who approves republication and which version a stable URL shows first. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: در متن این ADR شناسهٔ صریحی وجود ندارد؛ ارجاع‌های ورودی DL را در ماتریس ببینید.


### Full source record and conditions

### ADR-05: restatement و نسخهٔ گزارش

**وضعیت:** Proposed: سازوکار بازبیان گزارش. Open: اعلان و تصویب. طراحی موجود نسخه گزارش تغییرناپذیر حفظ شود.

**پیشنهاد:** گزارش منتشرشده immutable بماند. محاسبهٔ جدید روی تاریخ قدیمی نسخهٔ `restated` با cutoff جدید ایجاد کند. `as_reported`، `restated` و `counterfactual` در API، storage و UI جدا باشند.

**تصمیم باز:** چه تغییرهایی به مدیر اعلام شوند؟ چه کسی انتشار مجدد را تأیید کند؟ آیا نسخهٔ اولیه در URL ثابت اول نمایش داده شود یا آخرین نسخه با هشدار و پیوند به اولیه؟

**محدودیت ثابت:** گزارش صبح گذشته نباید از آینده داده بگیرد. آمار تاریخی و نسخهٔ گزارش می‌توانند متفاوت باشند ولی برچسبشان باید روشن باشد. اصلاح سابقه، تصمیم انسانی گذشته را خودکار لغو نمی‌کند.

**مالک تصمیم:** تیم محصول و معماری. پیشنهاد اولیه، نسخهٔ اولیه به‌عنوان گزارش واقعی و دسترسی صریح به نسخهٔ اصلاح‌شده است.



<a id="adr-06"></a>

## ADR-06: اجرای دسترسی مصوب و امنیت Query

**زمینه:** جدول‌های مشترک، مجوز کامل ردیف، ستون و هدف استفاده را عرضه نمی‌کنند.

**مالک تصمیم:** تیم امنیت و معماری. ابهام معنای پرسش Q08 مدیر، در صورت نیاز، با برگزارکننده حل می‌شود.

**شرط بسته‌شدن:** Projectionهای باقی‌مانده بازبینی شوند. آزمون‌های منفی Join، Subquery، UNION، CTE، خطا، Export، Log، Cache و تغییر نقش اجرا و قبول شوند. سلسله‌مراتب منبع ثابت می‌ماند.

**شواهد منبع:** [ADR-06](decisions-registry.md#adr-06) و [نقشه وضعیت Q01 تا Q17](../004-reconciliation-review.md#question-map).

| شناسه گزاره | وضعیت | گزاره |
|---|---|---|
| ADR-06-S01 | الزام | سلسله‌مراتب و کنترل ردیف عرضه‌شده باید روی همه Queryهای کاربر اعمال شوند. |
| ADR-06-S02 | الزام | داده بار کاری فردی فقط برای سرپرست مستقیم مجاز است. مرخصی فقط ظرفیت تجمیعی است و نباید برای رتبه‌بندی فردی استفاده شود. |
| ADR-06-S03 | پذیرفته‌شده | Policy Catalog مشترک برای منبع، ستون، هدف استفاده و Predicate به‌کار رود. Backend و Query Gateway آن را با scoped viewهای SQLite اجرا کنند. |
| ADR-06-S04 | پذیرفته‌شده | فقط Queryهای SELECT/CTE خواندنی و معتبر اجرا شوند. allowlist جدول و تابع و default deny اعمال شوند. نقش پایگاه داده و ردیف خام به مدیر نمایش داده نشوند. |
| ADR-06-S05A | پذیرفته‌شده | `customer_id` فقط برای محاسبه داخلی و KPI مرتبط استفاده شود. مدیر، مدیر کل و سرپرست نباید آن را مستقیم ببینند. |
| ADR-06-S05B | پذیرفته‌شده | `city` یک بعد مجاز KPI است. نتیجه تجمیعی مانند `K_SHP_ONTIME_BY_CITY` در Scope مجاز نمایش داده شود. Drill-down آماری مجاز است، اما شناسه مشتری نباید نمایش داده شود. |
| ADR-06-S05C | پذیرفته‌شده | سیاست اطلاعات مشتری در Chatbot، Daily Report، Dashboard، Drill-down، JSON و Export یکسان اعمال شود. فقط سرویس محاسباتی می‌تواند داده خام لازم برای KPI را پردازش کند. |
| ADR-06-S05D | پذیرفته‌شده | Chatbot و Daily Report از Shared Authorization Policy استفاده کنند. داده غیرمجاز باید قبل از ساخت Prompt و قبل از خروجی قابل مشاهده مدیر حذف شود. |
| ADR-06-S06 | باز | Predicate منابع مشترک، Scope تاریخی، حذف متن حساس و Projection شواهد مشتق‌شده تعریف شوند. |
| ADR-06-S07 | باز | روش تجمیع ظرفیت و کنترل بازشناسی افراد در گروه کوچک تعریف شود. |

**جمع‌بندی وضعیت:** سیاست اطلاعات مشتری و اجرای آن با SQLite، Backend و Query Gateway پذیرفته شده است. Projection ردیف‌ها و ستون‌های سایر منابع مشترک هنوز باز است.

**الزامات پایه، ثبت‌شده در ۲۰۲۶-۱۱-۰۳:** اصل دامنهٔ دسترسی، الزام موجود است و تصمیم باز نیست. بریف ص۱۰ دسترسی را به زیرمجموعهٔ مدیر محدود می‌کند و دادهٔ فردی را فقط برای سرپرست مستقیم مجاز می‌داند. ص۱۳ کنترل ردیفی در لایهٔ داده را برای همهٔ Queryها، از جمله گفتگو، الزامی می‌کند. دادهٔ فردی فقط برای مدیریت بار کار است؛ ارزیابی و رتبه‌بندی افراد مجاز نیست. طبق ص۶، ص۱۲ و ص۱۳، مرخصی فقط به شکل ظرفیت تجمیعی تیم وارد تحلیل می‌شود. `dataset/org/access_matrix.csv` دامنهٔ دقیق مدیران را ثبت کرده است:

| مدیر | دامنهٔ دادهٔ تجمیعی مجاز | دادهٔ فردی مجاز برای مدیریت بار کار |
|---|---|---|
| M01، مدیر ارشد | سازمان، هر سه واحد و تمام تیم‌های ماتریس | ندارد |
| M02، مدیر کل فروش | U_SAL، T_ENT، T_DIG، T_MKT | ندارد |
| M03، مدیر کل عملیات | U_OPS، T_WH، T_SHP | ندارد |
| M04، مدیر کل پشتیبانی | U_SUP، T_RSP، T_CMP | ندارد |
| M05، سرپرست فروش سازمانی | T_ENT | فقط T_ENT |
| M06، سرپرست بازاریابی دیجیتال | T_DIG | فقط T_DIG |
| M07، سرپرست انبار | T_WH | فقط T_WH |
| M08، سرپرست ارسال | T_SHP | فقط T_SHP |
| M09، سرپرست پاسخ‌گویی | T_RSP | فقط T_RSP |
| M10، سرپرست شکایات و مرجوعی | T_CMP | فقط T_CMP |
| M11، سرپرست مارکت‌پلیس | T_MKT | فقط T_MKT |

این جدول grant تازه نیست؛ بازنویسی ماتریس منبع است. زمان فعال‌شدن مدیر و تیم باید اعمال شود؛ اختلاف صبح شروع M11 در ADR-08 جدا باقی است. مجوز فردی، مجوز نمایش وضعیت مرخصی اشخاص نیست. بریف و ماتریس، فهرست مجاز تک‌تک ستون‌های خام را عرضه نکرده‌اند؛ نگاشت جدول/ستون و predicate باید همین قواعد موجود را اجرا کند.

**مسئله:** access_matrix دامنهٔ entityها را تعیین می‌کند؛ تمام جدول‌ها team_id ندارند. مشترک‌بودن orders میان فروش و عملیات مجوز کل اطلاعات فروش نمی‌سازد.

**تصمیم پذیرفته‌شده:** policy catalog مشترک برای resource، column، purpose و predicate ایجاد شود. Backend و Query Gateway با scoped viewهای SQLite محدودیت ردیف و ستون را پیش از LLM اعمال کنند. Query Gateway فقط SELECT/CTE خواندنی معتبر با function/table allowlist اجرا کند و default deny را اعمال کند. SQLite به‌تنهایی مرجع مجوز کاربر نیست.

**سیاست اطلاعات مشتری:** `customer_id` فقط برای محاسبات داخلی و KPIهای مرتبط مجاز است. هیچ مدیر، مدیر کل یا سرپرست اجازه مشاهده مستقیم آن را ندارد. `city` برای محاسبه و گروه‌بندی KPI مجاز است. KPI تجمیعی شهری، مانند `K_SHP_ONTIME_BY_CITY` در M08، در محدوده مجاز قابل نمایش است. Drill-down فقط جزئیات آماری مجاز را نشان می‌دهد و نباید شناسه مشتری را نشان دهد. این قاعده در Chatbot، Daily Report، Dashboard، Drill-down، JSON و Export یکسان است. سرویس محاسباتی می‌تواند داده خام لازم را پردازش کند؛ این مجوز به مدیر منتقل نمی‌شود. داده نامجاز نباید وارد Prompt مدل یا خروجی مدیر شود.

**جزئیات اجرای باز:** نگاشت دامنهٔ مصوب به ردیف‌ها و ستون‌های سایر منابع مشترک؛ دامنهٔ دادهٔ گذشته برای تیم جدید؛ حذف دادهٔ نامجاز از evidence ارجاع بین‌واحدی؛ روش تجمیع ظرفیت و جلوگیری از بازشناسی افراد در تیم کوچک. این موارد، مجوز بازتعریف سلسله‌مراتب یا گسترش دسترسی نیستند. default برای مجوز تعریف‌نشده deny است.

**آزمون‌های لازم:** آزمون منفی روی Join، Subquery، UNION، CTE، خطا، Export، Log، Cache و تغییر نقش اجرا شود. تغییر Principal از پارامتر یا Prompt نباید Scope را عوض کند. موفقیت فقط پس از اجرای واقعی آزمون‌ها ثبت شود.

**نکته دامنه:** وجود KPI `K_ORG_ORDERS` به M03 مجوز سازمان نمی‌دهد. Query عملیاتی مجاز باید تعریف و Policy مستقل داشته باشد.



<a id="adr-07"></a>

## ADR-07: Signal and escalation edge cases

Problem / Context: R1-R8 are fixed requirements; some comparisons and state transitions are incomplete.

Decision owner: Product/analysis roles; organizer confirmation is needed for score-sensitive interpretations.

Closure condition: Record the edge policy and rule-version fixtures. Do not invent a numeric warn for R3 or an epsilon denominator.

Source Evidence: [ADR-07](decisions-registry.md#adr-07). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-07-S01 | Requirement | Apply all R1-R8, including > escalation duration, >=20% deterioration, <10% repeat suppression, >N% baseline deviation, no info alerts and the Jalali day-8 gate. |
| ADR-07-S02 | Requirement | Check recurrence at detection, report construction and final validation. |
| ADR-07-S03 | Proposed | Use named, versioned edge interpretations; strict threshold crossing is a proposal. |
| ADR-07-S04 | Open | Define equality, baseline direction, missing/holiday samples, zero denominators and minimum sample counts. |
| ADR-07-S05 | Open | Define unknown warning days, recovery/reset, multilevel escalation clocks, ranking weights and evidence-based grouping. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [AT-24](acceptance-register.md#at-24).


### Full source record and conditions

### ADR-07: جزئیات مرزی signal و escalation

**وضعیت:** Requirement: R1-R8. Open: حالت‌های مرزی. Proposed: فقط تفسیرهای نام‌گذاری‌شده پیشنهادی.

[قرارداد کامل R1-R8](../001-system-blueprint.md#system-7) و [ردیابی قواعد](../audit-2026-11-09/requirements-traceability.csv) را بخوانید. R2 صریحاً ماندگاری بیش از مدت تشدید و بدترشدن حداقل 20% نسبت به اولین گزارش را به کار می‌برد. R5 صریحاً انحراف بیشتر از N% را ملاک می‌داند. R4 تکرار جدید با تغییر کمتر از 10% را صریحاً منع می‌کند. R7 هرگز هشدار نمی‌سازد. R8 ارزیابی را به روز 8 ماه شمسی محدود می‌کند. این موارد انتخاب باز نیستند.

ابهام باقی‌مانده شامل مرجع مقایسه R4، بازیابی و Reset و رفتار R3 برای KPI دارای قاعده خط پایه و فاقد warn عددی است. برای این حالت آستانه هشدار نسازید. مقایسه‌های تعریف‌شده در منبع و سه نقطه کنترل باید بدون تغییر بمانند. AT-24 را ببینید.

قواعد اصلی R1-R8 از config الزام‌اند. موارد زیر در منبع به اندازهٔ کافی دقیق نیستند و نباید پنهانی انتخاب شوند:

| موضوع باز | پیشنهاد قابل آزمون، نه قاعدهٔ مصوب |
|---|---|
| تساوی با warn/crit | مقایسهٔ strict بر اساس عبارت عبور؛ تست equality جدا؛ تأیید برگزارکننده پیش از ارزیابی نهایی. |
| baseline دوطرفه یا نامطلوب | جهت نامطلوب از `direction` برای هشدار؛ رشد/افت مطلوب در نمایش؛ R5 می‌تواند تفسیر دوطرفه داشته باشد و باید روشن شود. |
| چهار هفته با missing/holiday | فقط نقاط مجاز؛ baseline ناقص با reason؛ حداقل نمونه و حذف تعطیلی گذشته صریح در config. |
| مخرج صفر در تغییر ۱۰٪/۲۰٪ | وضعیت undefined و rule تصمیم جدا؛ تقسیم بر epsilon یا عدد بی‌نهایت ممنوع. |
| روزهای پیوستهٔ هشدار با دادهٔ غایب | روز نامعلوم نه سالم و نه هشدار قطعی؛ پیشنهاد توقف شمارش تا تعیین وضعیت، بدون پاک‌کردن سابقه. |
| Reset دوره Signal | recovery با معیار مصوب و ثبت علت؛ تغییر rule version به‌تنهایی سیگنال جدید نسازد. |
| ادامهٔ تشدید چند سطح | تقویم هر recipient و reason مستقل؛ مهلت سطح بعد اگر در config نیست نیازمند سیاست صریح است. |
| تجمیع هم‌علت | گروه‌بندی فقط با evidence؛ حدس علّی مدل نباید چند مالک مستقل را حذف کند. |

مدت R2 «بیش از» `escalate_after_days` است؛ `>=` جایگزین بی‌توضیح آن نشود. مالک، scope و سابقه از داده تعیین می‌شوند. وزن‌های رتبه‌بندی و آستانهٔ sample کم پارامتر طراحی هستند.

**مالک تصمیم:** تیم محصول/تحلیل؛ برای موارد اثرگذار بر امتیاز، تأیید برگزارکننده. تا آن زمان تست‌ها هر تفسیر را نام‌گذاری می‌کنند، نه اینکه یکی را قانون قطعی بنامند.



<a id="adr-08"></a>

## ADR-08: Management calendar and input precedence

Problem / Context: Static day-75 activation conflicts with next-morning manager-input effect.

Decision owner: The organizer answers evaluation timing. Architecture roles handle event ordering.

Closure condition: Obtain a recorded precedence contract and time fixtures. Keep M01-M10 for all 30 mornings. Neither 316 nor 317 is approved.

Source Evidence: [ADR-08](decisions-registry.md#adr-08). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-08-S01 | Requirement | Apply the supplied cutoff and next-report input-effect rules. |
| ADR-08-S02 | Proposed | Use valid time, known time and an explicit report_population_policy. |
| ADR-08-S03 | Open | Select M11 first-report precedence: morning 75 gives 317 briefs; morning 76 gives 316. |
| ADR-08-S04 | Open | Define same-day question/upload ordering and attachment receipt/readiness. |
| ADR-08-S05 | Open | Define calendar known-at and future-plan visibility. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: در متن این ADR شناسهٔ صریحی وجود ندارد؛ ارجاع‌های ورودی DL را در ماتریس ببینید.


### Full source record and conditions

### ADR-08: تقویم مدیریت و تقدم ورودی‌ها

**وضعیت:** Requirement: Cutoff و زمان اثر ورودی مدیر. Open: تقدم منابع، شروع M11، آمادگی پیوست و زمان اطلاع از تقویم.

**اختلاف مستند:** بریف از ۱۰ گزارش روزانه می‌گوید. S05 مدیر M11 و تیم T_MKT را از روز ۷۵ فعال می‌کند. S07 تغییر سازمان را روز ۷۵ می‌فرستد، در حالی که S02 اثر ورودی را صبح بعد قرار می‌دهد.

**پیشنهاد:** roster با valid time و known time ساخته شود. `report_population_policy` تقدم تاریخ اثر ثابت یا فرمان runtime را مشخص کند. M01 تا M10 در هر ۳۰ صبح پوشش داده شوند؛ مدیر فعال اضافه حذف نشود.

با فعال‌شدن M11 از صبح ۷۶، خروجی ۳۰ روز شامل ۳۱۶ brief است. با تقدم مستقیم effective day و شروع صبح ۷۵، ۳۱۷ brief می‌شود. این دو تعداد، محاسبهٔ دو policy هستند؛ تعداد accepted هنوز تأیید نشده است. ۳۰۰ گزارش ثابت نباید بدون توجه به تغییر سازمان هدف کد شود.

**ورودی هم‌روز:** S07 پرسش manager Q09 را پیش از upload IN07 روز ۸۰ نوشته است. محتوای پرسش به پیوست اشاره دارد، ولی زمان دقیق دریافت آن در روز مشخص نیست. پیشنهاد، ثبت dependency صریح attachment و زمان دریافت است. اگر فایل هنوز مجاز/دریافت‌شده نیست، پاسخ `clarification_requested` or `data_unavailable` بدهد؛ صرف وجود آن در filesystem مجوز خواندن زودهنگام نیست.

**سایر زمینه‌ها:** calendar رویدادها known_at ندارد. نمایش رخداد آینده به‌عنوان علت جاری ممنوع باشد. استفاده از برنامهٔ کمپین آینده نیازمند visibility policy جداست.

**مالک پاسخ:** برگزارکننده برای زمان‌بندی ارزیابی؛ تیم معماری برای event ordering و registry.



<a id="adr-09"></a>

## ADR-09: Output status, precision and registered numbers

Problem / Context: The brief and schema have different status terms; the internal Insight schema is incomplete.

Decision owner: The organizer resolves output contracts. Product/data roles handle internal presentation.

Closure condition: Record the approved mapping and inspect numerical, scope and content fixtures. Shared analysis creates no access grant.

Source Evidence: [ADR-09](decisions-registry.md#adr-09). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-09-S01 | Requirement | Use KPI-specific canonical rounding with zero tolerance after reference rounding. |
| ADR-09-S02 | Requirement | Allow registered scoped ad hoc queries; every published number needs actual SQL/result, definition, snapshot, scope and query reference. |
| ADR-09-S03 | Requirement | Use one shared Insight Brief as the report source with authorized role projections. |
| ADR-09-S04 | Proposed | Validate query_id for every published number even where the wire schema makes it optional. |
| ADR-09-S05 | Proposed | Keep suppression history in an internal ledger and open_items, pending approval. |
| ADR-09-S06 | Open | Resolve brief suppressed versus schema ongoing without changing the supplied schema. |
| ADR-09-S07 | Open | Define added-query/estimate wire mapping and the internal Insight projection contract. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [AT-02](acceptance-register.md#at-02)، [AT-10](acceptance-register.md#at-10)، [AT-11](acceptance-register.md#at-11)، [AT-23](acceptance-register.md#at-23).


### Full source record and conditions

### ADR-09: وضعیت خروجی، گردکردن و اعداد ثبت‌شده

**Requirement:** منبع S01 در صفحه 16، فرهنگ KPI را مرجع گردکردن می‌داند. S02 مقدار درست را نتیجه SQL مرجع تعریف می‌کند. مثال‌های عمومی با یک رقم اعشار جای Precision اختصاصی KPI را نمی‌گیرند. Precision مرجع حفظ شود. تلرانس پس از گردکردن مرجع صفر است. گردکردن یکسان و اضافی مجاز نیست.

**Requirement:** منبع S01 در صفحات 9 و 13، Queryهای Ad hoc ثبت‌شده را مجاز می‌داند. تفکیک جدید یا برآورد پشتیبانی‌شده صرفاً به دلیل خارج‌بودن از 55 تعریف اصلی ممنوع نیست. SQL اجراشده، نتیجه، تعریف، Snapshot، Scope و query_id ثبت شوند. LLM نمی‌تواند مقدار آن را بسازد.

**تعارض Open:** منبع S01 در صفحه 15، `new/escalated/suppressed` را مشخص می‌کند. S06 مقدارهای `new/escalated/ongoing` را مجاز می‌داند. تاریخچه Suppression حفظ شود. نگاشت پیشنهادی به تاریخچه داخلی و `open_items` مصوب نیست. Enum نامعتبر تولید نشود و `suppressed` بی‌اعلام به `ongoing` تغییر نکند. برگزارکننده باید نگاشت خروجی را تأیید کند. Schema عرضه‌شده بدون تغییر است.

**Open:** نگاشت ماشین‌خوان نتایج Query افزوده یا برآوردها، زمانی که ارزیاب به ارجاع KPI نیاز دارد. Schema، فیلد query_id را اختیاری می‌داند، اما بریف ردیابی هر عدد را الزامی می‌کند. Validation با وضعیت Proposed، آن را برای اعداد منتشرشده الزامی می‌کند. تا وجود نگاشت معتبر، اعداد بدون پشتیبان وارد گزارش نشوند.

**Requirement:** یک Insight Brief مشترک، منبع گزارش نقش‌ها است (S01، صفحات 9-10). **Open:** Schema داخلی و قرارداد Projection مجاز. این قرارداد از `brief_schema.json` جداست. تحلیل مشترک هرگز مجوز شواهد محدود خود را به مدیر دیگر نمی‌دهد.

**آزمون‌های پذیرش:** AT-02، AT-10، AT-11، AT-23. برگزارکننده مسئول حل قرارداد خروجی است. تیم‌های محصول و داده مسئول نمایش داخلی هستند.



<a id="adr-10"></a>

## ADR-10: Budget, models and execution limits

Problem / Context: The daily limits cover all reports, analysis, conversation and retry.

Decision owner: Engineering/product roles. The organizer must supply the reference machine, rates and final limit profile.

Closure condition: Approve the policy and measure all work, QA, retry, repair and extra model services. Report infrastructure cost separately.

Source Evidence: [ADR-10](decisions-registry.md#adr-10). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-10-S01 | Requirement | Keep total daily LLM cost at or below USD 5, daily runtime at or below 15 minutes on the stated machine, and simulated publication before 07:30. |
| ADR-10-S02 | Proposed | Use a provider-neutral gateway, atomic cost reservations, scoped cache and bounded tools/tokens. |
| ADR-10-S03 | Proposed | Test USD 3.5 for analysis/reports, USD 1 for QA and USD 0.5 reserve within the same USD 5 limit. |
| ADR-10-S04 | Open | Choose model, provider, gateway, tracing, exact limits and allocation rules. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: در متن این ADR شناسهٔ صریحی وجود ندارد؛ ارجاع‌های ورودی DL را در ماتریس ببینید.


### Full source record and conditions

### ADR-10: بودجه، مدل و محدودیت اجرا

**وضعیت:** Requirement: حدود هزینه و زمان کل روز. Proposed: Gateway مستقل از ارائه‌دهنده، Ledger و سهم‌های بودجه. Open: مدل، محصولات و حدود دقیق.

**الزام فعلی:** حداکثر ۵ دلار LLM در هر روز شامل تمام گزارش‌ها، تحلیل‌ها، گفتگو و retry. حداکثر ۱۵ دقیقه اجرای یک روز روی ماشین مرجع؛ ساعت شبیه‌سازی گزارش پیش از ۰۷:۳۰.

**پیشنهاد:** ledger رزرو هزینه پیش از call، سقف token و tool-call، cache با scope و سهم ذخیره برای QA. یک مدل کم‌هزینه برای کار معمول و مدل قوی‌تر فقط در صورت نیاز و بودجه؛ مدل و قیمت در این سند انتخاب نشده‌اند.

**پیشنهاد بودجهٔ اولیه برای آزمون، نه حد پذیرش جدید:** ۳٫۵ دلار تحلیل/گزارش، ۱ دلار QA و ۰٫۵ دلار reserve؛ این ارقام تضمین هزینه نیستند. انتقال سهم تنها در همان سقف ۵ دلار و با reservation اتمی مجاز باشد. embedding یا خدمت مدل اضافی نیز در ledger بیاید.

**آزمون پذیرش:** همه گزارش‌های روزانه، تحلیل‌های منتخب، QA اسکریپت‌شده، Retryها و اصلاح‌های محدود در اندازه‌گیری هزینه و زمان منظور شوند. اگر Fallback مبتنی بر قالب انتخاب شود، باید از همه Validatorها عبور کند. در غیر این صورت، شکست Job مدیر صریح ثبت شود. موفقیت Fallback تأییدنشده الزامی نشود. هزینه زیرساخت جدا از سقف LLM گزارش می‌شود.

**مالک تصمیم:** تیم مهندسی/محصول؛ ماشین مرجع، نرخ‌ها و نسخهٔ حدود نهایی از برگزارکننده دریافت شود.



<a id="adr-11"></a>

## ADR-11: Correction conflicts and entity lifecycle

Problem / Context: Some reference selections have no full ordering. No current correction tie was observed.

Decision owner: Data roles handle detection/quarantine. The contract owner handles precedence.

Closure condition: Record precedence or quarantine policy and inspect conflict fixtures. Last-row, latest timestamp and greatest value are not supplied rules.

Source Evidence: [ADR-11](decisions-registry.md#adr-11). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-11-S01 | Proposed | Track conflicting corrections and payloads separately; quarantine affected uncertain outputs. |
| ADR-11-S02 | Open | Obtain a valid source precedence rule for equal-rank conflicts. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: در متن این ADR شناسهٔ صریحی وجود ندارد؛ ارجاع‌های ورودی DL را در ماتریس ببینید.


### Full source record and conditions

### ADR-11: correction conflict و چرخهٔ موجودیت

**وضعیت:** Proposed: وضعیت تعارض و قرنطینه. Open: تقدم منابع. الگوریتم حل تعارض مصوب تیم ثبت نشده است.

**پیشنهاد:** اصلاح‌های متعارض در یک Drop و payload متفاوت با business_id یکسان، state مستقل داشته باشد. reference view روی دادهٔ مبهم به‌صورت خروجی قطعاً معتبر منتشر نشود. رویدادهای تکرارشونده یا reopening حفظ شوند.

**محدودیت:** SQL موجود برای بعضی انتخاب‌ها ترتیب کامل ندارد. اضافه‌کردن last-row-wins، آخرین Timestamp یا بزرگ‌ترین value قاعدهٔ کسب‌وکار تازه است. در دادهٔ فعلی correction tie مشاهده نشده است؛ این مورد ریسک دادهٔ پنهان است، نه خطای اثبات‌شدهٔ فعلی.

**مالک تصمیم:** تیم داده برای تشخیص و quarantine؛ مالک قرارداد برای precedence در صورت مشاهدهٔ واقعی یا الزام آزمون.



<a id="adr-12"></a>

## ADR-12: Retention, backup and audit

Problem / Context: Replay evidence and restricted logs need a recoverable preservation policy.

Decision owner: Architecture and operations roles.

Closure condition: Approve periods and access, then prove file hashes, snapshot rebuild and sample reports after restore. Derived cache need not be retained forever.

Source Evidence: [ADR-12](decisions-registry.md#adr-12). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-12-S01 | Proposed | Retain raw/config/query/report evidence for evaluation and use consistent archive/database backups with restore checks. |
| ADR-12-S02 | Open | Define post-evaluation retention, volume limits, backup periods, audit viewers and restore policy. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: در متن این ADR شناسهٔ صریحی وجود ندارد؛ ارجاع‌های ورودی DL را در ماتریس ببینید.


### Full source record and conditions

### ADR-12: نگهداری، backup و audit

**وضعیت:** Proposed: سازوکار Backup و Retention. Open: بازه‌ها، دسترسی ممیزی و سیاست Restore.

**پیشنهاد:** برای ارزیابی، raw، config، query و همهٔ report versionهای لازم برای replay حفظ شوند. backup سازگار archive/DB و restore test لازم است. log حاوی دادهٔ فردی در خروجی عمومی benchmark قرار نگیرد.

**تصمیم باز:** دورهٔ retention پس از ارزیابی، محدودیت حجم، مدت backup و نقش مشاهدهٔ audit. حذف تاریخچه برای کاهش هزینه پیش از تعیین این موارد انجام نشود.

**مالک تصمیم:** تیم معماری و مسئول عملیات. این طراحی به نگهداری نامحدود همهٔ فایل‌های cache نیاز ندارد؛ cache مشتق قابل بازسازی است.



<a id="adr-13"></a>

## ADR-13: One bounded AI Agent

Problem / Context: Writer and Validator modules do not imply extra autonomous Agents.

Decision owner: Engineering handles the execution controller. S16 supplies no original approver name or approval date.

Closure condition: Record limits and inspect AT-20/28 evidence. Do not reopen the one-Agent choice.

Source Evidence: [ADR-13](decisions-registry.md#adr-13). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-13-S01 | Accepted | Use one bounded AI Agent with deterministic support modules. |
| ADR-13-S02 | Accepted | Keep KPI calculation, Signal detection, authorization and final validation deterministic. |
| ADR-13-S03 | Open | Approve tool calls, tokens, time, cancellation and evidence-review rounds. |

Accepted decision: See the Accepted statement rows.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [AT-20](acceptance-register.md#at-20).


### Full source record and conditions

### ADR-13: یک AI Agent با حدود مشخص

**Accepted:** یک AI Agent با حدود مشخص و ماژول‌های قطعی استفاده شود. Evidence: جدول نتیجه S16 Q01 صریحاً تصمیم تیم را ثبت می‌کند. S17 یک Agent را مشخص می‌کند. منبع، نام تأییدکننده یا تاریخ تصویب اولیه را عرضه نمی‌کند.

Agent می‌تواند شواهد مجاز را بررسی و پیش‌نویس تحلیل، پاسخ و متن گزارش را تهیه کند. محاسبه KPI، Signalها، Projectionهای Workflow، بررسی مجوز و Validation نهایی قطعی می‌مانند. ماژول‌های Writer و Validator به معنی Agentهای خودمختار اضافی نیستند. معماری چند Agent جایگزین مصوب نیست.

**Open:** حدود فراخوانی ابزار، Token، زمان، لغو و دورهای بررسی. **آزمون پذیرش:** AT-20 و ADR-10. مهندسی مسئول کنترل‌گر اجرا است.



<a id="adr-14"></a>

## ADR-14: Independent valid-report publication

Problem / Context: A failed manager job does not invalidate another manager package. A partial day is still incomplete.

Decision owner: Product and engineering roles. Original approver names and dates are not supplied.

Closure condition: Approve failure policies and inspect before-draft and validation-failure tests. A failure file is not a successful report.

Source Evidence: [ADR-14](decisions-registry.md#adr-14). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-14-S01 | Accepted | Publish each valid manager report independently and record failed reports and partial-day outcomes. |
| ADR-14-S02 | Proposed | Commit one manager text/JSON package atomically. |
| ADR-14-S03 | Proposed | Use bounded retry and a deterministic validated template fallback. |
| ADR-14-S04 | Open | Define timeout, retry bounds, fallback content, failure/status export and replacement-version rules. |

Accepted decision: See the Accepted statement rows.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [AT-11](acceptance-register.md#at-11)، [AT-15](acceptance-register.md#at-15)، [AT-18](acceptance-register.md#at-18)، [AT-21](acceptance-register.md#at-21).


### Full source record and conditions

### ADR-14: انتشار مستقل گزارش

**Accepted:** گزارش معتبر هر مدیر مستقل منتشر شود. گزارش‌های ناموفق و وضعیت شکست جزئی روز ثبت شوند. Evidence: جدول نتیجه S16 Q16 صریحاً تصمیم تیم را ثبت می‌کند؛ قراردادهای Publication و Schedule در S17 هم‌خوان هستند. نام تأییدکننده و تاریخ تصویب اولیه عرضه نشده‌اند.

**سازوکار انتشار Proposed:** متن فارسی و JSON یک بسته مدیر به‌صورت اتمی ثبت شوند. شکست گزارش مدیر B نباید بسته معتبر مدیر A را پس بگیرد. خطاها حتی در صورت ساخته‌نشدن Draft ثبت شوند. روز فقط زمانی پوشش کامل دارد که هر مدیر فعال الزامی بسته معتبر داشته باشد. انتشار مستقل، AT-15 را تضعیف نمی‌کند.

**Proposed:** Retry محدود و Fallback قطعی مبتنی بر قالب با اعداد معتبر و متکی به Query. **Open:** Timeout، حدود Retry، محتوای Fallback، قرارداد Export شکست و وضعیت و قواعد نسخه جایگزین. Fallback باید کنترل Scope، Schema، عدد و شواهد را بگذراند. وجود فایل خطا، گزارش ناموفق را موفق نمی‌کند.

**آزمون‌های پذیرش:** AT-11، AT-15، AT-18، AT-21. محصول و مهندسی مسئول سیاست شکست هستند.



<a id="adr-15"></a>

## ADR-15: Workflow stage ownership

Problem / Context: All three end-to-end owners are M01; this does not determine stage owners.

Decision owner: Product and data roles must approve the mapping.

Closure condition: Record the mapping and test all stages, missing owners and unit-valued actors. Do not infer team-only foreign keys or change canonical KPI owners.

Source Evidence: [ADR-15](decisions-registry.md#adr-15). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-15-S01 | Requirement | Reconstruct WF1-WF3 from actual logs and preserve M01 ownership and the separate supplied stage and KPI contracts. |
| ADR-15-S02 | Proposed | Use a versioned stage responsibility catalog. |
| ADR-15-S03 | Open | Approve stage-to-team ownership and stage-delay routing, or retain explicit unresolved routing. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [AT-08](acceptance-register.md#at-08)، [AT-12](acceptance-register.md#at-12)، [AT-25](acceptance-register.md#at-25).


### Full source record and conditions

### ADR-15: مالکیت مراحل Workflow

**Requirement:** مسیرهای WF1-WF3 از Logهای واقعی بازسازی شوند. S11، مالک سرتاسری هر سه Workflow را M01 تعیین می‌کند. مقادیر SLA مرحله و فرمول‌های KPI، قراردادهای مستقل عرضه‌شده خود را حفظ می‌کنند.

**Open:** نگاشت مرحله به تیم و ارجاع تأخیر مرحله. مالک سرتاسری، مالک هر مرحله را اثبات نمی‌کند. `order_events.actor_team` می‌تواند تیم یا واحد را مشخص کند. ارتباط کارکنان و رویداد به تاریخ و مجوز معتبر نیاز دارد. FK محدود به تیم ساخته نشود و مالک از ترتیب Workflow حدس زده نشود.

**Proposed:** فهرست نسخه‌دار مسئولیت مراحل. گزینه‌ها عبارت‌اند از مالک مصوب مرحله با تشدید به M01 یا ارجاع صریحاً حل‌نشده تا زمان وجود نگاشت. گزینه دوم وضعیت را صادقانه حفظ می‌کند، اما پذیرش ارجاع به مالک مرحله را برآورده نمی‌کند. تغییر مالک Canonical KPI بدون اختیار منبع گزینه مجاز نیست.

**آزمون پذیرش:** AT-08، AT-12 و AT-25، شامل همه مراحل عرضه‌شده، مرحله فاقد نگاشت و عامل از نوع واحد. مالکان محصول و داده باید نگاشت را تصویب کنند.



<a id="adr-16"></a>

## ADR-16: Runtime files and operational documents

Problem / Context: Uploads are required. Current CSV/JSON/MD fixtures do not define the full format requirement.

Decision owner: Product and engineering roles handle the format contract.

Closure condition: Approve formats and inspect authorized/failed/injected uploads. Developer documents, audits and hidden labels are not product evidence. RAG/vector storage is not an approved dependency.

Source Evidence: [ADR-16](decisions-registry.md#adr-16). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-16-S01 | Requirement | Support structured nightly sources, authenticated manager input and file upload; the brief names Excel. |
| ADR-16-S02 | Proposed | Separate structured intake from untrusted document registration and preserve originals, receipt, audience, validation and lineage. |
| ADR-16-S03 | Proposed | Use SQLite text retrieval for operational documents. |
| ADR-16-S04 | Open | Define exact Excel formats/validation, extra PDF support, file limits, retrieval and same-day readiness. |

Accepted decision: No explicit Accepted statement is recorded for this ADR.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [AT-03](acceptance-register.md#at-03)، [AT-13](acceptance-register.md#at-13)، [AT-22](acceptance-register.md#at-22).


### Full source record and conditions

### ADR-16: فایل‌های زمان اجرا و اسناد عملیاتی

**Requirement:** منابع ساختاریافته شبانه و ورودی‌های مدیر از طریق API یا پوشه ورودی پشتیبانی شوند. Upload الزامی است. بریف Excel را نام می‌برد؛ Fixtureهای فعلی شامل CSV و Markdown هستند. JSON نیز Manifestها، ورودی‌ها و قراردادهای خروجی را نگه می‌دارد.

**Proposed:** ورود داده ساختاریافته از ثبت سند غیرقابل اعتماد جدا شود. اصل فایل‌ها، زمان دریافت، مخاطب، بررسی Schema و نوع و Data Lineage حفظ شوند. نسخه‌های Upload از Dropهای مرجع جدا بمانند. مستندات توسعه، خروجی‌های Audit، Notebookها یا برچسب‌های پنهان وارد شواهد محصول نشوند.

**Open:** قالب‌های دقیق Excel و Validation آن‌ها، پشتیبانی اضافی PDF، حدود فایل، روش بازیابی و آمادگی Upload همان روز. بازیابی متنی SQLite یک پیشنهاد است. RAG و پایگاه داده برداری وابستگی مصوب نیستند. محدودبودن Fixtureها به CSV/JSON/MD به‌تنهایی قالب‌های الزامی Upload را تعیین نمی‌کند.

**آزمون پذیرش:** AT-03، AT-13، AT-22؛ تقدم ورودی همان روز همچنان ADR-08 است. محصول و مهندسی مسئول قرارداد قالب هستند.



<a id="adr-17"></a>

## ADR-17: Human decisions and actual execution

Problem / Context: A decision or draft does not prove that an organizational action occurred.

Decision owner: Product handles these details.

Closure condition: Approve the confirmation contract and inspect AT-14/29 evidence. Fixed replay data must stay unchanged.

Source Evidence: [ADR-17](decisions-registry.md#adr-17). [Q01-Q17 status map](../004-reconciliation-review.md#question-map).

| Statement ID | Decision Status | Statement |
|---|---|---|
| ADR-17-S01 | Accepted | Humans control organizational decisions; the system cannot execute organizational actions. |
| ADR-17-S02 | Requirement | Create only drafts after a valid human decision; do not send messages or move staff. |
| ADR-17-S03 | Proposed | Separate decision, draft, human execution confirmation and observed follow-up states. |
| ADR-17-S04 | Open | Decide whether MVP stores execution confirmation, its authorized confirmer and its required evidence. |

Accepted decision: See the Accepted statement rows.

Proposed options and Open details: See the statement rows and the full extract.

Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.

وابستگی‌های DL / AT در ADR: [AT-14](acceptance-register.md#at-14)، [AT-29](acceptance-register.md#at-29).


### Full source record and conditions

### ADR-17: تصمیم انسانی و واقعیت اجرای اقدام

**Requirement:** سیستم پیشنهاد می‌دهد؛ انسان تصمیم می‌گیرد. پس از تصمیم معتبر، سیستم می‌تواند Draft وظیفه و پیام بسازد و شواهد بعدی را پیگیری کند. سیستم نباید پیام بفرستد، نیرو جابه‌جا کند یا اقدام سازمانی اجرا کند (S01، صفحات 11-12؛ S02).

**Proposed:** وضعیت تصمیم، Draft، تأیید اجرا و پیگیری مشاهده‌شده جدا باشند. رکورد تصمیم، شواهد اجرای اقدام نیست. داده ثابت Replay از قبل اثر تصمیم‌های اسکریپت‌شده را دارد و در واکنش به اقدام تیم تغییر نمی‌کند.

**Open:** آیا MVP تأیید انسانی اجرای اقدام را ذخیره می‌کند، چه کسی می‌تواند آن را تأیید کند و چه شواهدی لازم است. گزینه‌ها، صرفاً پیگیری تصمیم و Draft یا پیگیری اجرای صریحاً تأییدشده توسط انسان هستند. گزینه دوم وظایف وضعیت و ممیزی اضافه می‌کند، اما مجوز ابزار اجرا نمی‌دهد.

**آزمون پذیرش:** AT-14 و AT-29. نمای موجود HumanDecisionFollowUp مسیر وضعیت گزارش‌شده توسط انسان را حفظ می‌کند. فیلدهای دقیق تأیید، اختیار و شواهد همچنان Open هستند. محصول مسئول این جزئیات است. تصمیم یا وظیفه نوشته‌شده هرگز اجرای سازمانی اقدام را اثبات نمی‌کند.



<a id="decisions-3"></a>

## 3. سوابق تصمیم معماری
