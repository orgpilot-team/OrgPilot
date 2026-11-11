# تصمیم‌های معماری To-Be دیدراه

## A. Document Control

| Field | Value |
|---|---|
| عنوان | تصمیم‌های معماری To-Be دیدراه |
| نسخه | 2.0 |
| تاریخ بازبینی | ۱۴۰۵/۰۸/۱۹ (2026-11-10) |
| وضعیت | Draft — Ready for Team Review |
| دامنه | معماری To-Be و قراردادهای تصمیم‌گیری |
| نسخه پشتیبان | [نسخه پیش از Refactor](architecture-decisions.pre-refactor-2026-11-10.md) |

این سند مرجع واحد تصمیم‌های معماری To-Be است. این سند Requirement، تصمیم Accepted، راهکار Proposed و سؤال Open را از هم جدا می‌کند.

### منابع مرجع

| منبع | وضعیت | کاربرد |
|---|---|---|
| [بریف رسمی دیدراه](../دیدراه-بریف-دستیار-ایجنتیک-مدیران.md) و PDF هم‌نام | در دسترس | Requirement، Acceptance، Replay و تحویل |
| [Decisions Registry](../architecture/registry/decisions-registry.md) | در دسترس | تصمیم‌ها و Evidence |
| [Open Issues Registry](../architecture/registry/open-issues-registry.md) | در دسترس | Issueهای `DL-01` تا `DL-19` |
| [Adr.md](../architecture/sources/Adr.md) | در دسترس | سؤال‌های معماری و تصمیم تیم |
| [Dataset README](../../DataSet/arka_dataset/README_FA.md) | در دسترس | قرارداد Dataset و KPI |
| [KPI Dictionary](../../DataSet/arka_dataset/config/kpi_dictionary.csv) و [Reference Views](../../DataSet/arka_dataset/config/reference_views.sql) | در دسترس | تعریف و SQL مرجع KPI |
| [Brief Schema](../../DataSet/arka_dataset/output_contract/brief_schema.json) و [QA Schema](../../DataSet/arka_dataset/output_contract/qa_answer_schema.json) | در دسترس | قرارداد رسمی خروجی |
| [Acceptance Register](../architecture/registry/acceptance-register.md) | در دسترس | معیار و Evidence پذیرش |

یک فایل مستقل با عنوان Replay پیدا نشد. قرارداد Replay در بریف و Acceptance Register موجود است. این سند فقط به همان قراردادها استناد می‌کند.

### تعریف وضعیت‌ها

- **Requirement:** الزام قطعی منبع رسمی است. Requirement تصمیم تیم نیست.
- **Accepted:** تصمیم صریح و قابل ردیابی تیم است.
- **Proposed:** راهکار پیشنهادی است. Proposed به معنی Accepted نیست.
- **Open:** پاسخ نهایی ثبت نشده است.
- **External clarification:** فقط برگزارکننده یا مالک رسمی Dataset می‌تواند پاسخ معتبر بدهد.
- **Closed:** پاسخ، Owner، Evidence و Closure Criteria ثبت و تأیید شده‌اند.

هیچ Issue با متن این سند بسته نمی‌شود. تغییر وضعیت باید در Registry ثبت شود و Evidence داشته باشد.

## B. Executive Decision Summary

| مورد | نتیجه |
|---|---|
| تصمیم Accepted | **۶** |
| Issue Open اولیه | **۲۰** |
| Issue Open جدید | **۳** (`DL-21` تا `DL-23`) |
| Issue Open نهایی | **۲۳** |
| Issue بسته‌شده | **۰** |
| سؤال Peer در Crosswalk | **۱۵** |

هشت Issue با اولویت `P0` بخش متأثر را مسدود می‌کنند: `DL-02`، `DL-03`، `DL-06`، `DL-07`، `DL-09`، `DL-11`، `DL-18` و `DL-20`.

- پاسخ برگزارکننده یا مالک Dataset لازم است: `DL-02`، بخش‌های منبع‌محور `DL-03` و `DL-09`، `DL-11`، `DL-16`، `DL-21` و بخش Expected output در `DL-23`.
- تصمیم تیم لازم است: `DL-01`، `DL-04`، `DL-06` تا `DL-08`، بخش اجرایی `DL-09`، `DL-12` تا `DL-15`، `DL-17` تا `DL-20`، `DL-22` و بخش Policy در `DL-23`.
- `DL-05` و `DL-10` ابتدا به Evidence منبع و سپس به تصمیم پیاده‌سازی نیاز دارند.

## C. Accepted Architecture Decisions

### ADR-01 — موتور پایگاه داده محصول

- **Question:** موتور پایگاه داده محصول چیست؟
- **Status:** Accepted.
- **Requirement:** SQL، تعریف و نتیجه مرجع Dataset برای آزمون حفظ شوند.
- **Accepted Team Decision:** SQLite تنها موتور پایگاه داده محصول و مرجع است. همه ۵۵ KPI و Queryهای تعاملی روی SQLite اجرا می‌شوند.
- **Boundary:** PostgreSQL و ترجمه بین دو موتور در محصول استفاده نمی‌شوند.
- **Impact:** تصمیم موتور در `DL-01` بسته است. صحت نتیجه SQLite همچنان با آزمون‌های پذیرش بررسی می‌شود.
- **Evidence / Sources:** [ADR-01](../architecture/registry/decisions-registry.md#adr-01)، [Adr.md، Q03](../architecture/sources/Adr.md)، Dataset README و بریف.

### ADR-13-S01 — یک Agent محدود

- **Question:** سیستم چند AI Agent دارد؟
- **Status:** Accepted.
- **Accepted Team Decision:** سیستم یک AI Agent محدود دارد. ماژول‌های قطعی مستقل Agent نیستند.
- **Boundary:** Multi-Agent و delegation پذیرفته نشده‌اند.
- **Impact:** کنترل هزینه، Trace و ارزیابی در یک Agent runtime انجام می‌شود.
- **Evidence / Sources:** [ADR-13](../architecture/registry/decisions-registry.md#adr-13)، [Adr.md، Q01](../architecture/sources/Adr.md).

### ADR-13-S02 — مرز منطق قطعی

- **Question:** کدام منطق نباید به LLM واگذار شود؟
- **Status:** Accepted.
- **Accepted Team Decision:** محاسبه KPI، تشخیص Signal، Authorization و Validation نهایی قطعی هستند.
- **Boundary:** LLM فقط Evidence مجاز را تحلیل می‌کند و متن می‌نویسد.
- **Impact:** عدد، مجوز، Signal و پذیرش خروجی به نتیجه احتمالی مدل وابسته نیستند.
- **Evidence / Sources:** [ADR-13](../architecture/registry/decisions-registry.md#adr-13)، [Adr.md، Q01، Q04 و Q12](../architecture/sources/Adr.md)، بریف.

### ADR-14-S01 — انتشار مستقل گزارش معتبر

- **Question:** شکست یک گزارش چه اثری بر گزارش‌های دیگر دارد؟
- **Status:** Accepted.
- **Accepted Team Decision:** هر گزارش معتبر مدیر مستقل منتشر می‌شود. شکست یک گزارش مانع انتشار گزارش معتبر دیگر نیست.
- **Requirement:** شکست و پوشش ناقص روز ثبت شوند.
- **Impact:** Policy مربوط به Retry و Fallback در `DL-13` Open است.
- **Evidence / Sources:** [ADR-14](../architecture/registry/decisions-registry.md#adr-14)، [Adr.md، Q16](../architecture/sources/Adr.md).

### ADR-17 — کنترل انسانی تصمیم و اقدام

- **Question:** آیا سیستم اقدام سازمانی را اجرا می‌کند؟
- **Status:** Accepted.
- **Accepted Team Decision:** مدیر تصمیم می‌گیرد. سیستم فقط گزینه، Draft و پیگیری اثر را تولید می‌کند.
- **Boundary:** سیستم نیرو را جابه‌جا نمی‌کند، هدف را خودکار تغییر نمی‌دهد و پیام را خودکار ارسال نمی‌کند.
- **Impact:** اثبات اجرای واقعی در `DL-12` Open است.
- **Evidence / Sources:** [ADR-17](../architecture/registry/decisions-registry.md#adr-17)، بریف بخش ۸ و Dataset README.

### ADR-18 — LangGraph برای Orchestration Agent

- **Question:** Orchestration جریان Agent با چه Framework انجام می‌شود؟
- **Status:** Accepted.
- **Accepted Team Decision:** LangGraph برای Orchestration جریان‌های Agent استفاده می‌شود.
- **Boundary:** LangGraph مرجع KPI، Signal، Authorization یا Validation نهایی نیست.
- **Impact:** مرز اجرایی دقیق در `DL-20` Open است.
- **Evidence / Sources:** تصمیم صریح تیم در درخواست «DIDRAH — Execute To-Be Architecture Finalization». نسخه پیش از Refactor نیز این Evidence را ثبت کرده است.

## D. Open Decision Register

ترتیب Register بر اساس `P0`، سپس `P1` و سپس `P2` است. شناسه‌های قبلی تغییر نکرده‌اند. Ownerها پیشنهادی هستند.

### P0

#### DL-02 — سیاست RAW یا DEDUP

- **ID:** `DL-02`
- **Question:** Payloadهای تکراری سفارش RAW محاسبه شوند یا exact-payload DEDUP؟
- **Status:** Open.
- **What We Know:** RAW باید حفظ شود. Policy روی ۸ KPI اثر دارد. Idempotency دریافت با DEDUP کسب‌وکار یکسان نیست.
- **Unresolved Gap:** Policy رسمی و مقدار Canonical مشخص نیست.
- **Options:** RAW؛ DEDUP؛ Policy جدا برای هر Source.
- **Recommended Approach:** هر دو نتیجه با `input_policy_id` جدا بمانند. هیچ نتیجه‌ای Canonical نامیده نشود.
- **Decision Owner:** برگزارکننده یا مالک Dataset.
- **Impact:** درستی عدد و Acceptance.
- **Priority:** P0؛ بدون تغییر.
- **Evidence / Sources:** [DL-02](../architecture/registry/open-issues-registry.md#dl-02)، بریف و ممیزی Dataset.
- **Closure Criteria:** پاسخ رسمی، Fixture مرجع و آزمون ۸ KPI ثبت شوند.

#### DL-03 — Missing Source و انتشار

- **ID:** `DL-03`
- **Question:** Source چه زمانی بسته است و مقدار وابسته به داده ناقص چه زمانی منتشر می‌شود؟
- **Status:** Open.
- **What We Know:** Pipeline نباید کامل متوقف شود. Missing یک Data Issue است. مقدار جاری نامعتبر با مقدار قبلی جایگزین نمی‌شود.
- **Unresolved Gap:** مدت Incident، Closure، حداکثر سن Context و Eligibility مشخص نیستند. Q06 در این Issue ادغام شد.
- **Options:** `null` و Data Issue؛ Snapshot ناقص؛ انتظار تا Closure.
- **Recommended Approach:** خروجی مستقل ادامه یابد. مقدار متأثر `null` بماند. مقدار قبلی فقط با تاریخ واقعی نمایش داده شود.
- **Decision Owner:** برگزارکننده یا محصول.
- **Impact:** گزارش و Signal eligibility.
- **Priority:** P0؛ بدون تغییر.
- **Evidence / Sources:** [DL-03](../architecture/registry/open-issues-registry.md#dl-03)، [Adr.md، Q06](../architecture/sources/Adr.md)، بریف.
- **Closure Criteria:** Closure event، Wire mapping، حداکثر سن و Fixture چندروزه تأیید شوند.

#### DL-06 — Projection دسترسی

- **ID:** `DL-06`
- **Question:** ردیف، ستون، Purpose و Predicate مجاز هر نقش چیست؟
- **Status:** Open.
- **What We Know:** دسترسی سلسله‌مراتبی و deny-by-default Requirement هستند. سؤال مدیر Grant جدید ایجاد نمی‌کند.
- **Unresolved Gap:** Projection منابع مشترک، متن حساس، Historical scope و رفتار پاسخ جزئی Q12 مشخص نیستند.
- **Options:** Policy Catalog؛ View مجزا؛ رد دسترسی تعریف‌نشده.
- **Recommended Approach:** Policy Catalog نسخه‌دار با scoped SQLite views، Query Gateway، allowlist و Redaction استفاده شود. RLS مربوط به PostgreSQL نیست.
- **Decision Owner:** امنیت و داده.
- **Impact:** Query، Evidence، QA و صفر نشت.
- **Priority:** P0؛ بدون تغییر.
- **Evidence / Sources:** [DL-06](../architecture/registry/open-issues-registry.md#dl-06)، `access_matrix.csv` و بریف.
- **Closure Criteria:** Matrix کامل و آزمون مثبت و منفی سه سطح تأیید شوند.

#### DL-07 — ظرفیت و حریم خصوصی

- **ID:** `DL-07`
- **Question:** ظرفیت تیم چگونه محاسبه و برای گروه کوچک محافظت می‌شود؟
- **Status:** Open.
- **What We Know:** مرخصی فقط Context ظرفیت تجمیعی است. رتبه‌بندی فردی ممنوع است. Contract ساعت کامل وجود ندارد.
- **Unresolved Gap:** Formula، آستانه گروه کوچک و Redaction مشخص نیستند.
- **Options:** نسبت افراد؛ نسبت ساعت؛ مقدار عرضه‌شده.
- **Recommended Approach:** در MVP فقط مقدار تجمیعی عرضه‌شده استفاده شود.
- **Decision Owner:** محصول و امنیت.
- **Impact:** Evidence و داده فردی.
- **Priority:** P0؛ بدون تغییر.
- **Evidence / Sources:** [DL-07](../architecture/registry/open-issues-registry.md#dl-07)، `staff_availability.csv` و بریف.
- **Closure Criteria:** Formula، Grain، Threshold و Fixture گروه کوچک تأیید شوند.

#### DL-09 — قواعد مرزی Signal

- **ID:** `DL-09`
- **Question:** Equality، جهت Baseline، صفر، نمونه ناکافی، Reset و هم‌زمانی `new` و `escalated` چگونه ارزیابی شوند؟
- **Status:** Open.
- **What We Know:** Escalation تابع زمان، بدترشدن و اثر بین‌واحدی است. Critical به‌تنهایی Escalation نیست. Unknown نباید Normal شود.
- **Unresolved Gap:** Q09 و Q10 به Gap موجود اضافه شدند. Direction، Equality، Clock، Recovery و مخاطب هم‌زمان مشخص نیستند.
- **Options:** Truth table هر Rule؛ تفسیر عمومی؛ توقف نتیجه مرزی.
- **Recommended Approach:** `direction` هر KPI و Edge behavior هر Rule نسخه‌دار شوند. مورد مرزی `unknown` بماند.
- **Decision Owner:** محصول یا برگزارکننده.
- **Impact:** Detection، recurrence و escalation.
- **Priority:** P0؛ بدون تغییر.
- **Evidence / Sources:** [DL-09](../architecture/registry/open-issues-registry.md#dl-09)، `escalation_rules.csv` و بریف.
- **Closure Criteria:** Truth table برای R1 تا R8 و Fixtureهای جهت و مخاطب تأیید شوند.

#### DL-11 — `suppressed` و `ongoing`

- **ID:** `DL-11`
- **Question:** `suppressed` بریف چگونه با Enum رسمی `ongoing` نگاشت می‌شود؟
- **Status:** Open.
- **What We Know:** Schema فقط `new`، `escalated` و `ongoing` دارد. بریف Suppression را الزام می‌کند.
- **Unresolved Gap:** Wire mapping و محل State داخلی مشخص نیستند.
- **Options:** Ledger داخلی؛ نگاشت به `ongoing`؛ Schema جدید.
- **Recommended Approach:** Schema تغییر نکند. Suppression در Ledger داخلی ثبت شود.
- **Decision Owner:** برگزارکننده یا محصول.
- **Impact:** JSON، History و recurrence.
- **Priority:** P0؛ بدون تغییر.
- **Evidence / Sources:** [DL-11](../architecture/registry/open-issues-registry.md#dl-11)، Brief Schema و بریف.
- **Closure Criteria:** Mapping رسمی، نمونه JSON و آزمون recurrence تأیید شوند.

#### DL-18 — مدل کامل گزارش

- **ID:** `DL-18`
- **Question:** محتوای الزامی بریف که Field رسمی ندارد کجا نگه‌داری می‌شود؟
- **Status:** Open.
- **What We Know:** Insight Brief مرجع گزارش است. Schema همه مفهوم‌های بریف را Field مجزا نمی‌دهد.
- **Unresolved Gap:** مدل Item، Evidence، Chart، Decision Card، انتخاب پنج مورد و History مشخص نیست.
- **Options:** مدل داخلی؛ Field آزاد؛ Schema رسمی جدید.
- **Recommended Approach:** مدل داخلی کوچک و نسخه‌دار ساخته شود. Schema رسمی تغییر نکند.
- **Decision Owner:** محصول.
- **Impact:** متن، JSON و Validation.
- **Priority:** P0؛ بدون تغییر.
- **Evidence / Sources:** [DL-18](../architecture/registry/open-issues-registry.md#dl-18)، بریف و Brief Schema.
- **Closure Criteria:** Content model، Projection و Fixture سه نقش تأیید شوند.

#### DL-20 — مرز LangGraph

- **ID:** `DL-20`
- **Question:** کدام جریان‌ها، Nodeها و Stateها در LangGraph قرار می‌گیرند؟
- **Status:** Open.
- **What We Know:** LangGraph Accepted است. منطق قطعی بیرون مرز Agent می‌ماند. یک Agent داریم.
- **Unresolved Gap:** Graph boundary، Checkpoint، State sensitivity، Retry و Interrupt مشخص نیستند.
- **Options:** تحلیل و نگارش؛ Job کامل؛ Graphهای Nightly و Interactive جدا.
- **Recommended Approach:** دو Graph ساده در یک runtime استفاده شوند. State فقط ID و Reference داشته باشد.
- **Decision Owner:** تیم معماری.
- **Impact:** بازیابی، امنیت و استقلال انتشار.
- **Priority:** P0؛ بدون تغییر.
- **Evidence / Sources:** ADR-13، ADR-14، ADR-18 و نسخه پشتیبان. این ID در Registry خارجی ثبت نشده بود و از نسخه قبل حفظ شد.
- **Closure Criteria:** Diagram، State schema، Node contracts و Failure path تأیید شوند.

### P1

#### DL-01 — موتور و صحت ۵۵ KPI

- **ID:** `DL-01`
- **Question:** موتور محصول چیست و صحت KPIها چگونه اثبات می‌شود؟
- **Status:** Closed for engine decision; tests pending.
- **What We Know:** SQLite تنها موتور محصول و مرجع است.
- **Unresolved Gap:** فقط شواهد اجرای صحیح همه ۵۵ KPI و حالت‌های مرزی باقی مانده است.
- **Options:** تصمیم موتور نهایی است و گزینه موتور دوم وجود ندارد.
- **Recommended Approach:** SQL مرجع SQLite بدون ترجمه برای همه روزها اجرا و نتیجه آن ثبت شود.
- **Decision Owner:** تصمیم کاربر؛ اجرای آزمون با مهندسی.
- **Impact:** پذیرش عددی.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-01](../architecture/registry/open-issues-registry.md#dl-01)، ADR-01 و KPI sources.
- **Closure Criteria:** Engine اعلام و Receipt همه ۵۵ KPI ثبت شود.

#### DL-04 — Rebuild

- **ID:** `DL-04`
- **Question:** اصلاح تاریخی Full rebuild باشد یا Selective rebuild؟
- **Status:** Open.
- **What We Know:** Snapshot و گزارش قبلی حفظ می‌شوند.
- **Unresolved Gap:** Dependency algorithm و Scope بهینه‌سازی مشخص نیستند.
- **Options:** Full؛ Selective با Proof.
- **Recommended Approach:** Full rebuild مبنای MVP باشد.
- **Decision Owner:** داده و محصول.
- **Impact:** کارایی و پیچیدگی.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-04](../architecture/registry/open-issues-registry.md#dl-04)، بریف.
- **Closure Criteria:** Benchmark و آزمون Restatement تأیید شوند.

#### DL-05 — تعارض Payload

- **ID:** `DL-05`
- **Question:** اصلاح‌های متعارض و هم‌رتبه چگونه حل می‌شوند؟
- **Status:** Open.
- **What We Know:** انتخاب بی‌مدرک آخرین رکورد معتبر نیست.
- **Unresolved Gap:** Source precedence رسمی وجود ندارد.
- **Options:** تقدم رسمی؛ Quarantine؛ آخرین رکورد.
- **Recommended Approach:** Quarantine و Data Issue.
- **Decision Owner:** مالک Source یا داده.
- **Impact:** KPI متأثر.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-05](../architecture/registry/open-issues-registry.md#dl-05)، بریف.
- **Closure Criteria:** Precedence و Fixture تعارض ثبت شوند.

#### DL-08 — مالک Stage

- **ID:** `DL-08`
- **Question:** مالک Stage و مسیر ارجاع تأخیر چیست؟
- **Status:** Open.
- **What We Know:** مالک KPI لزوماً مالک Stage نیست. Actor معتبر یا Mapping لازم است.
- **Unresolved Gap:** Mapping کامل و Fallback مشخص نیستند. Q11 ادغام شد.
- **Options:** Mapping رسمی؛ Actor؛ unresolved route.
- **Recommended Approach:** مالک Stage فقط از Actor معتبر یا Mapping تأییدشده تعیین شود.
- **Decision Owner:** محصول و داده.
- **Impact:** مالک Signal و Bottleneck.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-08](../architecture/registry/open-issues-registry.md#dl-08)، `workflow_definitions.csv` و بریف.
- **Closure Criteria:** Mapping همه Stageها و Fixture تأخیر تأیید شوند.

#### DL-10 — زمان اثر M11 و Upload

- **ID:** `DL-10`
- **Question:** تغییر سازمان و ورودی هم‌روز چه زمانی اثر می‌گذارند؟
- **Status:** Open.
- **What We Know:** valid time، received time و ready time جدا هستند.
- **Unresolved Gap:** صبح شروع M11، تقدم ورودی و readiness پیوست مشخص نیستند.
- **Options:** صبح ۷۵ یا ۷۶؛ receipt/readiness صریح.
- **Recommended Approach:** زمان دریافت و آماده‌شدن جدا ثبت شوند. گزارش صبح Immutable بماند.
- **Decision Owner:** برگزارکننده یا معماری.
- **Impact:** Coverage و QA.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-10](../architecture/registry/open-issues-registry.md#dl-10)، Dataset README.
- **Closure Criteria:** Fixture روز ۷۵/۷۶ و Upload contract تأیید شوند.

#### DL-12 — اثر تصمیم و اجرای واقعی

- **ID:** `DL-12`
- **Question:** اجرای واقعی و اثر تصمیم چگونه ثبت و سنجیده می‌شوند؟
- **Status:** Open.
- **What We Know:** اثر در روزهای بعد بررسی می‌شود. تغییر مشاهده‌شده اثر علّی قطعی نیست. قانون عمومی بهبود ۱۰٪ وجود ندارد.
- **Unresolved Gap:** Window، KPI، Success، Confounder، uncertainty و Evidence اجرا مشخص نیستند. Q14 و Q15 ادغام شدند.
- **Options:** فقط Draft؛ تأیید انسانی اجرا؛ Observation تصمیم‌ویژه.
- **Recommended Approach:** هر تصمیم KPI، Window، Threshold و Owner معیار موفقیت داشته باشد.
- **Decision Owner:** محصول و مدیر تصمیم‌گیر.
- **Impact:** تاریخچه تصمیم و ادعای اثر.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-12](../architecture/registry/open-issues-registry.md#dl-12)، ADR-17 و بریف.
- **Closure Criteria:** Decision contract، روش مقایسه و Evidence اجرا تأیید شوند.

#### DL-13 — Failure policy

- **ID:** `DL-13`
- **Question:** Retry، Timeout و Fallback چیست؟
- **Status:** Open.
- **What We Know:** انتشار مستقل Accepted است. Fallback باید Validation شود.
- **Unresolved Gap:** اعداد Retry، Repair، Timeout و Failure export مشخص نیستند.
- **Options:** Retry؛ Template؛ Failure صریح.
- **Recommended Approach:** Retry خطای موقت، یک Repair، سپس Failure.
- **Decision Owner:** محصول و مهندسی.
- **Impact:** هزینه، زمان و Coverage.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-13](../architecture/registry/open-issues-registry.md#dl-13)، ADR-14 و بریف.
- **Closure Criteria:** اعداد و Fixtureهای Failure تأیید شوند.

#### DL-14 — Provider و بودجه

- **ID:** `DL-14`
- **Question:** Provider، Model، API Key و سهم بودجه چگونه تعیین می‌شوند؟
- **Status:** Open.
- **What We Know:** سقف ۵ دلار برای کل LLM روز است و از Token log محاسبه می‌شود.
- **Unresolved Gap:** Provider، Price list، Secret delivery و Limitها مشخص نیستند. Q03 ادغام شد.
- **Options:** Provider مستقیم؛ Gateway؛ چند Model.
- **Recommended Approach:** رابط مستقل، Secret injection و Cost ledger استفاده شوند.
- **Decision Owner:** مهندسی و محصول؛ API Key با برگزارکننده.
- **Impact:** هزینه، امنیت و عملیات.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-14](../architecture/registry/open-issues-registry.md#dl-14)، بریف.
- **Closure Criteria:** Provider، قیمت، Secret delivery و Benchmark تأیید شوند.

#### DL-17 — NULL و اعداد Ad hoc

- **ID:** `DL-17`
- **Question:** NULL، Dimension ناموجود و عدد Query موردی چگونه Serialize می‌شوند؟
- **Status:** Open.
- **What We Know:** Schema رسمی مرجع است. Sentinel نباید معنی داده را تغییر دهد.
- **Unresolved Gap:** Wire mapping و Pairing عدد مشخص نیستند.
- **Options:** Mapping صریح؛ Sentinel؛ Schema جدید.
- **Recommended Approach:** تمایز داخلی حفظ و Wire mapping با Fixture تأیید شود.
- **Decision Owner:** محصول یا برگزارکننده.
- **Impact:** JSON و مقایسه عدد.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-17](../architecture/registry/open-issues-registry.md#dl-17)، Brief Schema و بریف.
- **Closure Criteria:** Fixture و Validator رسمی تأیید شوند.

#### DL-19 — تغییر KPI و Rollback

- **ID:** `DL-19`
- **Question:** چه کسی KPI یا تنظیم را فعال می‌کند؟
- **Status:** Open.
- **What We Know:** ۵۵ تعریف مرجع بازنویسی نمی‌شوند. تنظیم بدون تغییر کد Requirement است.
- **Unresolved Gap:** Authority، زمان اثر و Rollback مشخص نیستند.
- **Options:** Candidate نسخه‌دار؛ فعال‌سازی مستقیم؛ فقط افزودن.
- **Recommended Approach:** Candidate نسخه‌دار با تأیید انسانی و زمان اثر ثبت شود.
- **Decision Owner:** محصول، امنیت و داده.
- **Impact:** Configuration، Audit و Replay.
- **Priority:** P1؛ بدون تغییر.
- **Evidence / Sources:** [DL-19](../architecture/registry/open-issues-registry.md#dl-19)، Dataset README و بریف.
- **Closure Criteria:** Lifecycle، Authority و Rollback تأیید شوند.

#### DL-21 — GitHub Delivery

- **ID:** `DL-21`
- **Question:** Repository باید Public باشد یا Private با دسترسی Evaluator؟
- **Status:** Open — New.
- **What We Know:** کد کامل و Git history Requirement هستند. Visibility تعیین نشده است.
- **Unresolved Gap:** Visibility، حساب Evaluator، Deadline و LFS/Submodule مشخص نیستند.
- **Options:** Public؛ Private با Invite؛ Mirror.
- **Recommended Approach:** Private بماند مگر Public الزام شود. Clone test قبل از Freeze انجام شود.
- **Decision Owner:** برگزارکننده.
- **Impact:** دریافت و ارزیابی تحویل.
- **Priority:** P1؛ قبل از Final Delivery.
- **Evidence / Sources:** بریف بخش ۱۲ و Q05. پاسخ رسمی دیگری پیدا نشد.
- **Closure Criteria:** Visibility رسمی و Clone test ثبت شوند.

#### DL-22 — CRM Lead lifecycle

- **ID:** `DL-22`
- **Question:** Lead بدون `Qualified` یا `Lost`، `Stalled` است یا `Abandoned`؟
- **Status:** Open — New.
- **What We Know:** نبود وضعیت نهایی، Abandonment را اثبات نمی‌کند.
- **Unresolved Gap:** State، Timeout، Terminality و KPI effect مشخص نیستند.
- **Options:** Stalled با Timeout؛ Abandoned فقط با Event؛ State رسمی جدید.
- **Recommended Approach:** بدون Contract، `Abandoned` استنتاج نشود.
- **Decision Owner:** محصول و مالک داده CRM.
- **Impact:** Funnel KPI، Aging و Signal.
- **Priority:** P1؛ Gate CRM.
- **Evidence / Sources:** CRM files، KPI Dictionary و Q08. پاسخ رسمی پیدا نشد.
- **Closure Criteria:** State machine، Event mapping و Fixture تأیید شوند.

#### DL-23 — QA answer status

- **ID:** `DL-23`
- **Question:** `data_unavailable`، `refused_out_of_scope` و رد داده غیرمجاز چگونه جدا می‌شوند؟
- **Status:** Open — New.
- **What We Know:** Schema پنج Enum دارد. سؤال کاربر Grant جدید نمی‌سازد.
- **Unresolved Gap:** پاسخ جزئی، Status نهایی Q03 و مرز سه حالت مشخص نیستند.
- **Options:** Status واحد؛ پاسخ مجاز با Redaction؛ Clarification.
- **Recommended Approach:** داده مجاز ولی ناموجود `data_unavailable`؛ قابلیت خارج محصول `refused_out_of_scope`؛ داده فردی غیرمجاز `refused_individual_data`.
- **Decision Owner:** برگزارکننده برای Expected output؛ امنیت و محصول برای Policy.
- **Impact:** QA Acceptance و امنیت.
- **Priority:** P1؛ Gate QA.
- **Evidence / Sources:** [QA Schema](../../DataSet/arka_dataset/output_contract/qa_answer_schema.json)، DL-06، Q12 و Q13.
- **Closure Criteria:** Truth table، Expected Q03 و Fixture هر Enum تأیید شوند.

#### DL-24 — تغییر نام ستون‌های زمان

- **ID:** `DL-24`
- **Question:** دو نسخه نام ستون‌های زمان چگونه به Schema داخلی نگاشت شوند؟
- **Status:** Open — New.
- **What We Know:** از روز ۰۸۲، `tickets.created_at` با نام `tickets.create_time` و `ticket_events.at` با نام `ticket_events.event_time` عرضه شده‌اند.
- **Unresolved Gap:** نام Canonical و رفتار فایل دارای هر دو نام یا نام ناشناخته مشخص نیست.
- **Recommended Approach:** Adapter هر دو Header شناخته‌شده را بپذیرد و Header اصلی را در رسید حفظ کند. این پیشنهاد هنوز تصویب نشده است.
- **Decision Owner:** مهندسی داده و معماری.
- **Impact:** Ingestion، Schema evolution و Dataset پنهان.
- **Priority:** P1؛ قبل از تثبیت Ingestion.
- **Evidence / Sources:** [DL-24](open-issues-registry.md#dl-24) و Headerهای Dropهای ۰۸۱ و ۰۸۲.
- **Closure Criteria:** نگاشت مصوب و آزمون نسخه قدیمی، نسخه جدید و تعارض Header ثبت شوند.

#### DL-25 — قرارداد و نرمال‌سازی نوع داده

- **ID:** `DL-25`
- **Question:** نوع Canonical، قالب، واحد، NULL و رفتار خطای هر ستون چیست؟
- **Status:** Open — New.
- **What We Know:** ورودی CSV نوع صریح ندارد. SQLهای مرجع از زمان، مبلغ، شمارنده، امتیاز و شناسه استفاده می‌کنند.
- **Unresolved Gap:** Data Dictionary کامل و نتیجه بررسی همه Dropها موجود نیست.
- **Recommended Approach:** داده خام حفظ شود و Parser نسخه‌دار آن را به نوع Canonical تبدیل کند. مقدار نامعتبر Data Issue باشد. این پیشنهاد هنوز تصویب نشده است.
- **Decision Owner:** مهندسی داده و مالک Dataset.
- **Impact:** صحت KPI، Join، Sort، مقایسه زمان و Dataset پنهان.
- **Priority:** P1؛ قبل از اعلام صحت محاسبات.
- **Evidence / Sources:** [DL-25](open-issues-registry.md#dl-25)، Dataset و `config/kpi_dictionary.csv`.
- **Closure Criteria:** Data Dictionary مصوب و آزمون همه Dropها ثبت شوند.

### P2

#### DL-15 — Retention و Restore

- **ID:** `DL-15`
- **Question:** دوره نگه‌داری، Backup، Audit access و Restore چیست؟
- **Status:** Open.
- **What We Know:** Evidence ارزیابی و Replay باید بازسازی شود.
- **Unresolved Gap:** دوره، حجم، RTO و RPO مشخص نیستند.
- **Options:** حفظ کامل؛ دوره محدود؛ Archive.
- **Recommended Approach:** برای ارزیابی همه Evidenceها حفظ شوند.
- **Decision Owner:** عملیات و معماری.
- **Impact:** ذخیره‌سازی و عملیات.
- **Priority:** P2؛ بدون تغییر.
- **Evidence / Sources:** [DL-15](../architecture/registry/open-issues-registry.md#dl-15)، بریف.
- **Closure Criteria:** Retention matrix و Restore drill تأیید شوند.

#### DL-16 — پروفایل ارزیابی و Docker

- **ID:** `DL-16`
- **Question:** سخت‌افزار، Network، Docker command، Mountها و `submission` چیست؟
- **Status:** Open.
- **What We Know:** اجرای یک‌فرمانی، سقف ۱۵ دقیقه و Dataset پنهان Requirement هستند.
- **Unresolved Gap:** CPU، RAM، API، Command، Mount، output و Evaluator مشخص نیستند. Q01، Q02 و Q04 ادغام شدند.
- **Options:** حدود بریف؛ پروفایل رسمی و Harness نمونه.
- **Recommended Approach:** پذیرش نهایی تا دریافت Profile ادعا نشود. Input و output جدا باشند.
- **Decision Owner:** برگزارکننده.
- **Impact:** Benchmark و پذیرش نهایی.
- **Priority:** P2؛ بدون تغییر.
- **Evidence / Sources:** [DL-16](../architecture/registry/open-issues-registry.md#dl-16)، بریف بخش‌های ۱۰ تا ۱۲.
- **Closure Criteria:** Machine، Network، Run command، Mount و output layout اعلام شوند.

## E. External Clarifications

1. Evaluator برای اعداد مرجع از چه Engine و نسخه‌ای استفاده می‌کند؟
2. ماشین Docker چه CPU و RAM دارد؟ Network و API خارجی مجاز هستند؟
3. Provider مجاز، روش تحویل API Key و Price list سقف ۵ دلار چیست؟
4. دستور Run، Mount داده پنهان و Layout `submission` چیست؟
5. Repository باید Public باشد یا Private؟ حساب Evaluator چیست؟
6. Policy رسمی Duplicate order، RAW است یا DEDUP؟
7. Missing Source چه زمانی Closed می‌شود؟ Context قبلی تا چند روز مجاز است؟
8. Truth table رسمی R1 تا R8 برای Equality، جهت، صفر و Reset چیست؟
9. `suppressed` چگونه به `ongoing` نگاشت می‌شود؟
10. پاسخ جزئی QA چه Status دارد؟ Expected status سؤال Q03 چیست؟

## F. Peer Questions Crosswalk

| Question ID | Existing ADR/DL | Known Answer | Remaining Open Point | Action |
|---|---|---|---|---|
| Q01 | ADR-01؛ DL-01؛ DL-16 | SQLite موتور محصول و مرجع است. | شواهد اجرای صحیح | ادغام در DL-01/DL-16 |
| Q02 | DL-16 | Runtime برابر ۱۵ دقیقه است. | CPU، RAM و Network | ادغام در DL-16 |
| Q03 | DL-14؛ DL-16 | سقف ۵ دلار برای کل روز است. | Provider، قیمت و Key | ادغام در DL-14/DL-16 |
| Q04 | DL-16 | Docker یک‌فرمانی لازم است. | Command، Mount و output | ادغام در DL-16 |
| Q05 | DL-21 | کد و Git history لازم است. | Public یا Private | Issue جدید DL-21 |
| Q06 | DL-03 | Pipeline ادامه دارد؛ Missing یک Data Issue است. | مدت و Closure | ادغام در DL-03 |
| Q07 | DL-02 | Policy روی ۸ KPI اثر دارد. | RAW یا DEDUP | ادغام در DL-02 |
| Q08 | DL-22 | نبود وضعیت نهایی Abandonment نیست. | State و Timeout | Issue جدید DL-22 |
| Q09 | DL-09 | Critical به‌تنهایی Escalation نیست. | مخاطب و Clock | ادغام در DL-09 |
| Q10 | DL-09 | جهت KPI باید اعمال شود. | Truth table | ادغام در DL-09 |
| Q11 | DL-08 | مالک KPI مالک Stage نیست. | Mapping و Fallback | ادغام در DL-08 |
| Q12 | DL-06؛ DL-23 | سؤال Grant نمی‌سازد. | پاسخ جزئی و Status | تفکیک در DL-06/DL-23 |
| Q13 | DL-23 | Enum رسمی موجود است. | Semantics دقیق | Issue جدید DL-23 |
| Q14 | DL-12 | اثر در روزهای بعد سنجیده می‌شود. | Window و uncertainty | ادغام در DL-12 |
| Q15 | DL-12 | قانون عمومی ۱۰٪ وجود ندارد. | معیار تصمیم‌ویژه | ادغام در DL-12 |

هر سؤال Q01 تا Q15 دقیقاً یک‌بار در این جدول آمده است.

## G. Decision Dependencies

| Issue | وابستگی | مرحله مسدودشده |
|---|---|---|
| DL-01، DL-02 | ADR-01 و KPI Oracle | درستی عدد |
| DL-03، DL-05 | قرارداد کیفیت داده | انتشار KPI متأثر |
| DL-04 | Snapshot | Historical correction |
| DL-06، DL-07، DL-23 | Authorization | صفر نشت و QA |
| DL-08، DL-22 | Workflow/CRM semantics | مالک و Funnel KPI |
| DL-09، DL-11 | Rule و Schema | کشف و Escalation |
| DL-10 | Temporal contract | Coverage و Upload |
| DL-12 | ADR-17 | پیگیری و اثر تصمیم |
| DL-13، DL-14 | ADR-14 و Budget | Runtime و Cost |
| DL-15 | عملیات | Restore |
| DL-16، DL-21 | قرارداد برگزارکننده | اجرای نهایی و تحویل |
| DL-17، DL-18 | Schema | سازگاری متن و JSON |
| DL-19 | Governance | تغییر تنظیم |
| DL-20 | ADR-13 و ADR-18 | Agent orchestration |

## H. Change Log

### نسخه 2.0 — 2026-11-10

- ساختار قبلی چهار بخشی به ساختار A تا H تبدیل شد.
- هر ۶ تصمیم Accepted حفظ شد.
- هر ۲۰ Issue Open اولیه حفظ شد.
- `DL-20` در نسخه قبل بود، ولی در Open Issues Registry نبود. این Issue با Provenance روشن حفظ شد.
- سه Issue مستقل ساخته شد: `DL-21`، `DL-22` و `DL-23`.
- Q01 تا Q04 در Issueهای موجود ادغام شدند. Q05 به `DL-21` تبدیل شد.
- Q06 و Q07 در `DL-03` و `DL-02` ادغام شدند. Q08 به `DL-22` تبدیل شد.
- Q09 و Q10 در `DL-09` و Q11 در `DL-08` ادغام شدند.
- Q12 بین `DL-06` و `DL-23` تفکیک شد. Q13 به `DL-23` پیوست.
- Q14 و Q15 در `DL-12` ادغام شدند.
- هیچ Accepted تغییر نکرد. هیچ Open بسته نشد. هیچ اولویت قبلی تغییر نکرد.
- تعارض قطعی جدیدی پیدا نشد. تفاوت `suppressed` و `ongoing` در `DL-11` Open ماند.

### نتیجه اعتبارسنجی

- Accepted اولیه: **۶ از ۶ حفظ شد**.
- Open اولیه: **۲۰ از ۲۰ حفظ شد**.
- Open نهایی: **۲۳**.
- Crosswalk: **۱۵ سؤال یکتا**.
- Issue جدید تکراری: **۰**.
- Proposed تبدیل‌شده به Accepted: **۰**.
- تغییر محصول، Dataset، SQL یا Schema رسمی: **۰**.
