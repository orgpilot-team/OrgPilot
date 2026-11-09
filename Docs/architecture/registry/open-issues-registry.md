# فهرست مسائل باز

<a id="open-issues-registry-overview"></a>

محل مستند: رکورد حاکمیتی تعیین‌شده توسط تیم. وضعیت: **Draft / Pending Review**. رکوردهای کامل منبع و معیارهای زیر در قالب Markdown خوانا هستند. متن نمایه، راهنمای دسترسی به رکوردها است. تأیید ساختار، هیچ تصمیم، قاعده منبع، ارزیابی ریسک یا نتیجه پذیرش را تغییر نمی‌دهد.

وضعیت: **Draft / Pending Review**. همه رکوردها **Open** هستند. وضعیت شواهد لازم **Evidence Pending** است.

برای هر مسئله، یک رکورد اصلی وجود دارد. گونه‌های منبع، جنبه‌های همان رکورد هستند. نام نقش‌ها در Decision Log نقش‌های پیشنهادی هستند و انتصاب فرد را نشان نمی‌دهند. کلاس‌های مسیر، نوع کار را مشخص می‌کنند و مالک را تعیین نمی‌کنند. هیچ گزینه‌ای انتخاب نشده است.

<a id="dl-01"></a>

## DL-01: All-55 PostgreSQL equivalence

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

Exact conflict / missing evidence: موتور PostgreSQL دارای وضعیت Accepted است؛ درستی هر 55 تبدیل و نوع‌های ورودی اثبات نشده است.

Effect: See the exact source options and effects below.

Existing options: تبدیل نسخه‌دار، SQL منبع را حفظ می‌کند و به محیط آزمون مرجع نیاز دارد. بازنویسی بررسی‌نشده خطر اختلاف عددی دارد و الزام را نقض می‌کند. موتور دوم محصول بازگردانده نشود.

Decision owner: Proposed source role: مهندسی؛ ADR-01؛ AT-02,03,05,17

Closure criterion: Record the type/translation contract and compare complete results for all 55 definitions and replay mornings. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-01, AT-02, AT-03, AT-05, AT-17.

Additional Source Evidence: [Versioned input types and integer/empty-value behavior](../002-data-architecture.md#data-6).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-01 / Q03 | متن و نتیجه S16 Q03؛ رکوردهای 2-56 در S03؛ Viewهای S04؛ قرارداد KPI در S02. | موتور PostgreSQL دارای وضعیت Accepted است؛ درستی هر 55 تبدیل و نوع‌های ورودی اثبات نشده است. | تبدیل نسخه‌دار، SQL منبع را حفظ می‌کند و به محیط آزمون مرجع نیاز دارد. بازنویسی بررسی‌نشده خطر اختلاف عددی دارد و الزام را نقض می‌کند. موتور دوم محصول بازگردانده نشود. | مهندسی؛ ADR-01؛ AT-02,03,05,17 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



Preserved source facet: Versioned input types and integer/empty-value behavior. See [Source](../002-data-architecture.md#data-6).

<a id="dl-02"></a>

## DL-02: RAW versus exact-payload DEDUP

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.

Exact conflict / missing evidence: حالت‌های RAW و DEDUP دقیق Payload، نتیجه هشت تعریف KPI را تغییر می‌دهند.

Effect: See the exact source options and effects below.

Existing options: حالت RAW همه رخدادهای پذیرفته‌شده را حفظ می‌کند؛ DEDUP جمعیت Join را تغییر می‌دهد. تا عرضه سیاست محاسبه یا نتیجه مورد انتظار توسط برگزارکننده، هر دو Namespace مقایسه حفظ شوند. Idempotency مربوط به Retry جداست.

Decision owner: Proposed source role: برگزارکننده یا مالک داده؛ ADR-02؛ AT-02,05

Closure criterion: Obtain the official policy or expected result, then test the approved input mode. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-02, AT-02, AT-05.


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-02 / Q05 | S03؛ فایل day_076/orders.csv و Manifest؛ RCA ORD-01..03؛ بخش‌های 2-5 در KPI-VAL؛ S16 Q05. | حالت‌های RAW و DEDUP دقیق Payload، نتیجه هشت تعریف KPI را تغییر می‌دهند. | حالت RAW همه رخدادهای پذیرفته‌شده را حفظ می‌کند؛ DEDUP جمعیت Join را تغییر می‌دهد. تا عرضه سیاست محاسبه یا نتیجه مورد انتظار توسط برگزارکننده، هر دو Namespace مقایسه حفظ شوند. Idempotency مربوط به Retry جداست. | برگزارکننده یا مالک داده؛ ADR-02؛ AT-02,05 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



<a id="dl-03"></a>

## DL-03: Source closure, publication and dated prior values

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.

Exact conflict / missing evidence: قرارداد بسته‌شدن منبع و سیاست آزادسازی مقدار موجود نیستند. نمایش آخرین مقدار معتبر، داده جاری را معتبر نمی‌کند.

Effect: See the exact source options and effects below.

Existing options: نگهداری مقادیر جاری وابسته به‌صورت null؛ انتشار مشروط Snapshot؛ یا آزادسازی مبتنی بر بسته‌شدن منبع. هرکدام مجوز صریح نیاز دارد. زمینه قبلی تاریخ‌دار فقط با نگاشت مصوب قابل نمایش است. جای مقدار جاری هرگز با داده قدیمی پر نشود.

Decision owner: Proposed source role: برگزارکننده یا محصول؛ ADR-04؛ AT-04,23

Closure criterion: Obtain source-interval closure and release contracts, dated-context age/mapping, and test missing/empty/backfill cases. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-04, AT-04, AT-23.


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-03 / Q06 | قاعده مقدار ناموجود در S02؛ بخش‌های 3/6 در DQ؛ نتیجه S16 Q06؛ مؤلفه reportWriter در S17. | قرارداد بسته‌شدن منبع و سیاست آزادسازی مقدار موجود نیستند. نمایش آخرین مقدار معتبر، داده جاری را معتبر نمی‌کند. | نگهداری مقادیر جاری وابسته به‌صورت null؛ انتشار مشروط Snapshot؛ یا آزادسازی مبتنی بر بسته‌شدن منبع. هرکدام مجوز صریح نیاز دارد. زمینه قبلی تاریخ‌دار فقط با نگاشت مصوب قابل نمایش است. جای مقدار جاری هرگز با داده قدیمی پر نشود. | برگزارکننده یا محصول؛ ADR-04؛ AT-04,23 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



<a id="dl-04"></a>

## DL-04: Selective rebuild and restatement

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

Exact conflict / missing evidence: بازسازی کامل در برابر محاسبه انتخابی؛ اعلان و تصویب بازبیان.

Effect: See the exact source options and effects below.

Existing options: بازسازی کامل، مبنای صحت پیشنهادی است. محاسبه انتخابی به اثبات هم‌ارزی و وابستگی نیاز دارد. هر دو، نسخه‌های قبلی گزارش را حفظ می‌کنند.

Decision owner: Proposed source role: داده و محصول؛ ADR-03,05؛ AT-03,05

Closure criterion: Approve rebuild scope and restatement notice/version policy, then compare selective and full outputs. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-03, ADR-05, AT-03, AT-05.


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-04 / Q07 | Cutoff در S02؛ S04؛ S16 Q07؛ مؤلفه snapshots در S17؛ ADR-03/05. | بازسازی کامل در برابر محاسبه انتخابی؛ اعلان و تصویب بازبیان. | بازسازی کامل، مبنای صحت پیشنهادی است. محاسبه انتخابی به اثبات هم‌ارزی و وابستگی نیاز دارد. هر دو، نسخه‌های قبلی گزارش را حفظ می‌کنند. | داده و محصول؛ ADR-03,05؛ AT-03,05 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



<a id="dl-05"></a>

## DL-05: Conflicting payload precedence

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.

Exact conflict / missing evidence: تعارض Payload و اصلاح‌های هم‌رتبه در یک Drop، قاعده تقدم ندارند.

Effect: See the exact source options and effects below.

Existing options: قاعده تقدم منبع دریافت شود یا خروجی‌های متأثر با ثبت مسئله قرنطینه شوند. انتخاب آخرین ردیف، قاعده ساختگی است. وجود تعارض اصلاح هم‌رتبه در داده فعلی ادعا نمی‌شود.

Decision owner: Proposed source role: مالک منبع یا داده؛ ADR-11؛ AT-05

Closure criterion: Obtain valid precedence or approve quarantine, then test equal-rank conflict cases. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-11, AT-05.


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-05 / Q08 | عبارت lead_fact ORDER BY drop_day DESC و Payloadهای غیرتجمیعی در گروه‌بندی در S04؛ RCA CRM-03؛ S16 Q08. | تعارض Payload و اصلاح‌های هم‌رتبه در یک Drop، قاعده تقدم ندارند. | قاعده تقدم منبع دریافت شود یا خروجی‌های متأثر با ثبت مسئله قرنطینه شوند. انتخاب آخرین ردیف، قاعده ساختگی است. وجود تعارض اصلاح هم‌رتبه در داده فعلی ادعا نمی‌شود. | مالک منبع یا داده؛ ADR-11؛ AT-05 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



<a id="dl-06"></a>

## DL-06: Shared-source access projections

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required. Organizer / Source Clarification Required only if the documented manager-Q08 source-meaning ambiguity cannot be resolved from the supplied brief and access matrix.

Exact conflict / missing evidence: منابع مشترک، Projection کامل ردیف، ستون و هدف استفاده ندارند.

Effect: See the exact source options and effects below.

Existing options: Predicateهای منبع و حذف اطلاعات محدود بازبینی شوند یا دسترسی تعریف‌نشده رد شود. استفاده از جدول برای محاسبه، مجوز مشاهده منبع نیست. همه انتخاب‌ها باید سلسله‌مراتب عرضه‌شده را حفظ کنند.

Decision owner: Proposed source role: امنیت و داده؛ ADR-06؛ AT-06

Closure criterion: Review row/column/purpose predicates, historic scope and text redaction, then inspect negative access tests. Ask the organizer only about unresolved source meaning. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-06, AT-06.

Additional Source Evidence: [Historic marketplace access; raw text/customer redaction; shared-resource predicates](../001-system-blueprint.md#system-10).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-06 / Q09 | رکوردهای 2-12 مربوط به access_matrix در S05؛ S01/S18، صفحات 5,10,13؛ پرسش‌های مدیر Q03/Q08 در S07. | منابع مشترک، Projection کامل ردیف، ستون و هدف استفاده ندارند. | Predicateهای منبع و حذف اطلاعات محدود بازبینی شوند یا دسترسی تعریف‌نشده رد شود. استفاده از جدول برای محاسبه، مجوز مشاهده منبع نیست. همه انتخاب‌ها باید سلسله‌مراتب عرضه‌شده را حفظ کنند. | امنیت و داده؛ ADR-06؛ AT-06 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



Preserved source facet: Historic marketplace access; raw text/customer redaction; shared-resource predicates. See [Source](../001-system-blueprint.md#system-10).

<a id="dl-07"></a>

## DL-07: Capacity formula and privacy

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required. Source clarification is conditional on choosing an hours measure whose working-hours contract is absent. A headcount design does not itself require an organizer answer.

Exact conflict / missing evidence: فرمول ظرفیت، ساعت کاری، اندازه گروه و حذف اطلاعات محدود از متن آزاد حل نشده‌اند.

Effect: See the exact source options and effects below.

Existing options: معیار مصوب تعداد افراد یا معیار ساعتی با قرارداد تقویم کاری. ساعت ساخته نشود و مرخصی فردی افشا نشود. استنباط هویت در گروه کوچک به کنترل نیاز دارد.

Decision owner: Proposed source role: محصول و امنیت؛ ADR-06؛ AT-06,10

Closure criterion: Approve headcount or an hours measure with a valid hours contract, redaction and small-group controls; test them. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-06, AT-06, AT-10.

Additional Source Evidence: [Working hours, effective staff dates, small groups and free-text personal data](../002-data-architecture.md#data-9).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-07 / Q10 | S01/S18، صفحات 6,9,12-13؛ staff_availability/staff/calendar؛ S16 Q10. | فرمول ظرفیت، ساعت کاری، اندازه گروه و حذف اطلاعات محدود از متن آزاد حل نشده‌اند. | معیار مصوب تعداد افراد یا معیار ساعتی با قرارداد تقویم کاری. ساعت ساخته نشود و مرخصی فردی افشا نشود. استنباط هویت در گروه کوچک به کنترل نیاز دارد. | محصول و امنیت؛ ADR-06؛ AT-06,10 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



Preserved source facet: Working hours, effective staff dates, small groups and free-text personal data. See [Source](../002-data-architecture.md#data-9).

<a id="dl-08"></a>

## DL-08: Stage ownership and delay routing

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

Exact conflict / missing evidence: مالک هر Workflow برابر M01 است؛ مالکان مرحله و مسیر ارجاع تأخیر تعریف نشده‌اند.

Effect: See the exact source options and effects below.

Existing options: فهرست مصوب مرحله با تشدید یا ارجاع حل‌نشده. مالک حدس زده نشود و مالک Canonical KPI تغییر نکند.

Decision owner: Proposed source role: محصول و داده؛ ADR-15؛ AT-08,12

Closure criterion: Approve the stage mapping without changing M01 end-to-end ownership or canonical owners; test all 12 stages and unknown actors. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-15, AT-08, AT-12, AT-25.

Additional Source Evidence: [WF1.5 follow-up ticket category/time projection and missing SLA; unit-valued actor_team](../001-system-blueprint.md#system-7).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-08 / Q11 | رکوردهای 2-13 در workflow_definitions.csv؛ ردیف‌های Workflow در kpi_dictionary؛ S16 Q11. | مالک هر Workflow برابر M01 است؛ مالکان مرحله و مسیر ارجاع تأخیر تعریف نشده‌اند. | فهرست مصوب مرحله با تشدید یا ارجاع حل‌نشده. مالک حدس زده نشود و مالک Canonical KPI تغییر نکند. | محصول و داده؛ ADR-15؛ AT-08,12 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



Preserved source facet: WF1.5 follow-up ticket category/time projection and missing SLA; unit-valued actor_team. See [Source](../001-system-blueprint.md#system-7).

<a id="dl-09"></a>

## DL-09: Signal edge rules and state

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.

Exact conflict / missing evidence: تساوی با Threshold، مرجع مقایسه R4، نبود warn در R3، خط پایه کم‌نمونه، مخرج صفر، روزهای نامعلوم و Reset.

Effect: See the exact source options and effects below.

Existing options: قواعد نسخه‌دار صریح با حالت‌های مرزی نام‌گذاری‌شده. عبور Strict دارای وضعیت Proposed است. داده نامعلوم نمی‌تواند عادی تلقی شود.

Decision owner: Proposed source role: محصول یا برگزارکننده؛ ADR-07؛ AT-08,09

Closure criterion: Record equality, baseline, zero, missing-day and reset policy, then test every R1-R8 boundary. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-07, AT-08, AT-09, AT-24.

Additional Source Evidence: [Ranking, cause grouping, multilevel recipient clocks and confidence in unknown states](../001-system-blueprint.md#system-7).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-09 / Q12 | رکوردهای 2-9 در escalation_rules.csv؛ Metadata جهت و قاعده KPI؛ S01/S18، صفحه 8؛ S16 Q12. | تساوی با Threshold، مرجع مقایسه R4، نبود warn در R3، خط پایه کم‌نمونه، مخرج صفر، روزهای نامعلوم و Reset. | قواعد نسخه‌دار صریح با حالت‌های مرزی نام‌گذاری‌شده. عبور Strict دارای وضعیت Proposed است. داده نامعلوم نمی‌تواند عادی تلقی شود. | محصول یا برگزارکننده؛ ADR-07؛ AT-08,09 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



Preserved source facet: Ranking, cause grouping, multilevel recipient clocks and confidence in unknown states. See [Source](../001-system-blueprint.md#system-7).

<a id="dl-10"></a>

## DL-10: M11, same-day uploads and calendar known-at

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.

Exact conflict / missing evidence: شروع ثابت روز 75 با اثر ورودی در صبح بعد تعارض دارد. رسید Upload و زمان اطلاع از تقویم موجود نیستند.

Effect: See the exact source options and effects below.

Existing options: شروع M11 از صبح 75 به 317 گزارش و از صبح 76 به 316 گزارش منجر می‌شود. هیچ‌کدام انتخاب نشده است. دریافت و آمادگی پیوست ثبت شوند؛ استفاده از پیوست ناموجود پرسش مدیر Q09 به تعویق بیفتد. رویداد برنامه‌ریزی‌شده، علت مشاهده‌شده نیست.

Decision owner: Proposed source role: برگزارکننده یا معماری؛ ADR-08,16؛ AT-03,07,15,22

Closure criterion: Obtain precedence and receipt/readiness contracts. Test 316 and 317 scenarios until one is approved. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-08, ADR-16, AT-03, AT-07, AT-15, AT-22.

Additional Source Evidence: [Historical scope and calendar future-plan visibility; manager Q09 before upload IN07](../002-data-architecture.md#data-9).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-10 / Q13 | M11/T_MKT/E25/E26 از روز 75 در S05؛ IN05 و پرسش مدیر Q09/IN07 در S07؛ زمان‌بندی ورودی در S02. | شروع ثابت روز 75 با اثر ورودی در صبح بعد تعارض دارد. رسید Upload و زمان اطلاع از تقویم موجود نیستند. | شروع M11 از صبح 75 به 317 گزارش و از صبح 76 به 316 گزارش منجر می‌شود. هیچ‌کدام انتخاب نشده است. دریافت و آمادگی پیوست ثبت شوند؛ استفاده از پیوست ناموجود پرسش مدیر Q09 به تعویق بیفتد. رویداد برنامه‌ریزی‌شده، علت مشاهده‌شده نیست. | برگزارکننده یا معماری؛ ADR-08,16؛ AT-03,07,15,22 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



Preserved source facet: Historical scope and calendar future-plan visibility; manager Q09 before upload IN07. See [Source](../002-data-architecture.md#data-9).

<a id="dl-11"></a>

## DL-11: Suppressed/ongoing and internal Insight schema

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.

Exact conflict / missing evidence: مقدار suppressed در بریف در برابر ongoing در Schema؛ Schema داخلی Insight و نگاشت اعداد افزوده.

Effect: See the exact source options and effects below.

Existing options: نگاشت به Ledger داخلی و open_items تأیید شود یا قرارداد رسمی خروجی اصلاح‌شده دریافت شود. هیچ‌کدام مصوب نیست. تحلیل مشترک همچنان به کنترل Evidence مختص نقش نیاز دارد.

Decision owner: Proposed source role: برگزارکننده یا محصول؛ ADR-09؛ AT-10,11

Closure criterion: Obtain the status/wire mapping, internal Insight schema and authorized projection contract; test actual-date context and evidence review records. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-09, AT-10, AT-11.

Additional Source Evidence: [Evidence independence storage: groups, result, reason, review version and authorized Insight recipient](../002-data-architecture.md#data-8).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-11 / Q14 | S01/S18، صفحات 9-10,15-16؛ فیلد item.status و فیلدهای عدد و Query در S06؛ S16 Q14. | مقدار suppressed در بریف در برابر ongoing در Schema؛ Schema داخلی Insight و نگاشت اعداد افزوده. | نگاشت به Ledger داخلی و open_items تأیید شود یا قرارداد رسمی خروجی اصلاح‌شده دریافت شود. هیچ‌کدام مصوب نیست. تحلیل مشترک همچنان به کنترل Evidence مختص نقش نیاز دارد. | برگزارکننده یا محصول؛ ADR-09؛ AT-10,11 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



Preserved source facet: Evidence independence storage: groups, result, reason, review version and authorized Insight recipient. See [Source](../002-data-architecture.md#data-8).

<a id="dl-12"></a>

## DL-12: Decision follow-up and execution confirmation

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

Exact conflict / missing evidence: تصویب تصمیم، Evidence اجرای اقدام نیست. دامنه پیگیری اجرای واقعی تعیین نشده است.

Effect: See the exact source options and effects below.

Existing options: صرفاً پیگیری تصمیم و Draft یا وضعیت اجرای تأییدشده توسط انسان با Evidence. هیچ‌کدام اجرای خودکار را مجاز نمی‌کند.

Decision owner: Proposed source role: محصول؛ ADR-17؛ AT-14

Closure criterion: Approve the MVP confirmation scope, actor/time/subject links, decision-to-observation mapping and evidence; test human-only actions. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-17, AT-14, AT-29.

Additional Source Evidence: [Decision follow-up evidence and actor/time/subject history, separate from actual action execution](../002-data-architecture.md#data-8).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-12 / Q15 | S01/S18، صفحات 11-12,15؛ IN02/IN03 در S07؛ نمای HumanDecisionFollowUp در S17. | تصویب تصمیم، Evidence اجرای اقدام نیست. دامنه پیگیری اجرای واقعی تعیین نشده است. | صرفاً پیگیری تصمیم و Draft یا وضعیت اجرای تأییدشده توسط انسان با Evidence. هیچ‌کدام اجرای خودکار را مجاز نمی‌کند. | محصول؛ ADR-17؛ AT-14 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



Preserved source facet: Decision follow-up evidence and actor/time/subject history, separate from actual action execution. See [Source](../002-data-architecture.md#data-8).

<a id="dl-13"></a>

## DL-13: Retry, timeout, fallback and failure export

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

Exact conflict / missing evidence: انتشار مستقل دارای وضعیت Accepted است؛ Export شکست، Retry، Timeout و Fallback مشخص نیستند.

Effect: See the exact source options and effects below.

Existing options: Retry محدود و سپس شکست صریح یا Fallback مبتنی بر قالب معتبر. شکست پیش از Draft باید ثبت شود. پوشش جزئی هرگز پذیرش روز نیست.

Decision owner: Proposed source role: محصول و مهندسی؛ ADR-14؛ AT-15,21

Closure criterion: Approve bounded failure/export/replacement policy and inspect pre-draft and validation-failure receipts. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-14, AT-15, AT-21, AT-28.


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-13 / Q16 | جدول نتیجه S16 Q16؛ مؤلفه PartialPublication در S17؛ پوشش مدیران فعال در S02؛ Schemaهای خروجی S06. | انتشار مستقل دارای وضعیت Accepted است؛ Export شکست، Retry، Timeout و Fallback مشخص نیستند. | Retry محدود و سپس شکست صریح یا Fallback مبتنی بر قالب معتبر. شکست پیش از Draft باید ثبت شود. پوشش جزئی هرگز پذیرش روز نیست. | محصول و مهندسی؛ ADR-14؛ AT-15,21 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



<a id="dl-14"></a>

## DL-14: Agent, model, gateway and budget limits

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required. Final organizer hardware/profile confirmation is tracked in DL-16. Model, provider, gateway and internal limits remain team choices.

Exact conflict / missing evidence: حدود Agent، مدل، ارائه‌دهنده، Gateway، ردیابی و سهم‌های بودجه انتخاب نشده‌اند.

Effect: See the exact source options and effects below.

Existing options: از رابط مستقل از ارائه‌دهنده با حدود اندازه‌گیری‌شده استفاده شود. محصول Gateway فقط نامزد است. کل روز شامل QA و Retry در حدود USD 5 و 15 دقیقه Benchmark شود.

Decision owner: Proposed source role: مهندسی و محصول؛ ADR-10,13؛ AT-17,18,20

Closure criterion: Approve model/provider/product/limits/rates and budget allocation; obtain final organizer profile, then benchmark all work. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-10, ADR-13, AT-17, AT-18, AT-20, AT-28.


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-14 / Q01,Q17 | S16 Q01/Q17؛ مؤلفه requests/modelGateway در S17؛ S01/S18، صفحات 14,16,19. | حدود Agent، مدل، ارائه‌دهنده، Gateway، ردیابی و سهم‌های بودجه انتخاب نشده‌اند. | از رابط مستقل از ارائه‌دهنده با حدود اندازه‌گیری‌شده استفاده شود. محصول Gateway فقط نامزد است. کل روز شامل QA و Retry در حدود USD 5 و 15 دقیقه Benchmark شود. | مهندسی و محصول؛ ADR-10,13؛ AT-17,18,20 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



<a id="dl-15"></a>

## DL-15: Retention, backup, audit access and restore

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

Exact conflict / missing evidence: Retention، بازه Backup، مشاهده‌کنندگان Audit و روش Restore.

Effect: See the exact source options and effects below.

Existing options: همه Evidenceهای Replay برای ارزیابی حفظ شوند. Retention بعدی به سیاست مصوب و Restore بازتولیدپذیر نیاز دارد. Cache مشتق‌شده قابل بازسازی است.

Decision owner: Proposed source role: عملیات و معماری؛ ADR-12؛ AT-06,19

Closure criterion: Approve periods and audit viewers, then inspect consistent backup and reproducible restore evidence. Source gate: پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-12, AT-06, AT-19.


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-15 / موضوع فراگیر | مؤلفه rawFiles/postgres/audit در S17؛ پیشنهاد مهندسی ADR-12؛ قرارداد بازه عرضه نشده است. | Retention، بازه Backup، مشاهده‌کنندگان Audit و روش Restore. | همه Evidenceهای Replay برای ارزیابی حفظ شوند. Retention بعدی به سیاست مصوب و Restore بازتولیدپذیر نیاز دارد. Cache مشتق‌شده قابل بازسازی است. | عملیات و معماری؛ ADR-12؛ AT-06,19 | پاسخ ثبت‌شده درباره سیاست یا منبع، به‌همراه Evidence آزمون پذیرش نام‌برده لازم است. در اینجا موفقیتی ادعا نمی‌شود. |



<a id="dl-16"></a>

## DL-16: Final evaluation profile and missing contracts

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Organizer / Source Clarification Required; Engineering Evidence Required.

Exact conflict / missing evidence: پروفایل نهایی برگزارکننده، سخت‌افزار مرجع، برچسب‌های پنهان و فرهنگ کامل Raw در دسترس نیستند.

Effect: See the exact source options and effects below.

Existing options: حدود فعلی بریف حفظ شوند. پیش از پذیرش نهایی، تأیید برگزارکننده ثبت شود. از بررسی مستندات، کشف رویداد پنهان، دقت QA یا کارایی ادعا نشود.

Decision owner: Proposed source role: برگزارکننده؛ AT-02,09,16,17,18,19

Closure criterion: Obtain official hardware/profile, hidden evaluation results and a full raw dictionary or recorded disposition of missing contracts. Source gate: پروفایل و سخت‌افزار برگزارکننده و Evidence ارزیابی رسمی؛ فرهنگ داده یا تعیین تکلیف مستند قرارداد مفقود.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: AT-02, AT-09, AT-16, AT-17, AT-18, AT-19.

Additional Source Evidence: [Absent event occurrence IDs, customer/campaign registries and full raw dictionary](../002-data-architecture.md#data-4).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-16 / پذیرش | S01/S18، صفحات 14,16-19؛ ارزیابی پنهان S02؛ نبود فرهنگ رسمی ستون‌های Raw. | پروفایل نهایی برگزارکننده، سخت‌افزار مرجع، برچسب‌های پنهان و فرهنگ کامل Raw در دسترس نیستند. | حدود فعلی بریف حفظ شوند. پیش از پذیرش نهایی، تأیید برگزارکننده ثبت شود. از بررسی مستندات، کشف رویداد پنهان، دقت QA یا کارایی ادعا نشود. | برگزارکننده؛ AT-02,09,16,17,18,19 | پروفایل و سخت‌افزار برگزارکننده و Evidence ارزیابی رسمی؛ فرهنگ داده یا تعیین تکلیف مستند قرارداد مفقود. |



Preserved source facet: Absent event occurrence IDs, customer/campaign registries and full raw dictionary. See [Source](../002-data-architecture.md#data-4).

<a id="dl-17"></a>

## DL-17: NULL dimensions and added query numbers

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.

Exact conflict / missing evidence: Dimension دارای NULL در برابر نبود Dimension؛ شناسه‌های خروجی Query و Evidence افزوده.

Effect: See the exact source options and effects below.

Existing options: تمایزهای داخلی حفظ شوند؛ Serialization و نگاشت مرجع تأیید شوند. مقدار Sentinel که Dimension مرجع را تغییر دهد ساخته نشود.

Decision owner: Proposed source role: محصول یا برگزارکننده؛ ADR-09؛ AT-02، AT-30

Closure criterion: Approve no-dimension/NULL/empty/new-dimension and ad hoc serialization without an invented sentinel; test fixtures. Source gate: نگاشت مصوب و Fixtureهای نبود Dimension، NULL، رشته خالی، Dimensionهای جدید و نتایج Ad hoc.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-09, AT-02, AT-30.

Additional Source Evidence: [KPI-specific precision, query-number mapping and actual NULL versus no dimension](../002-data-architecture.md#data-2).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-17 / خروجی | نوع string برای number.dim و query_id اختیاری در S06؛ قاعده ردیابی عدد در S02؛ Metadata مربوط به Dimension در S03. | Dimension دارای NULL در برابر نبود Dimension؛ شناسه‌های خروجی Query و Evidence افزوده. | تمایزهای داخلی حفظ شوند؛ Serialization و نگاشت مرجع تأیید شوند. مقدار Sentinel که Dimension مرجع را تغییر دهد ساخته نشود. | محصول یا برگزارکننده؛ ADR-09؛ AT-02، AT-30 | نگاشت مصوب و Fixtureهای نبود Dimension، NULL، رشته خالی، Dimensionهای جدید و نتایج Ad hoc. |



Preserved source facet: KPI-specific precision, query-number mapping and actual NULL versus no dimension. See [Source](../002-data-architecture.md#data-2).

<a id="dl-18"></a>

## DL-18: Complete content, signal selection and history

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

Exact conflict / missing evidence: محتوای الزامی نمودار، کارت و وضعیت، Schema کامل تجویزشده داخلی و خروجی ندارد. برچسب بررسی `Open Decision`: تفاوت Candidate Signal، Open Item و Published Brief Item و دسترسی به تاریخچه Signalهای معتبر خارج از پنج مورد مهم، نگاشت کامل ندارد.

Effect: See the exact source options and effects below.

Existing options: از قرارداد محتوای داخلی Validationشده یا افزونه مستند سازگار استفاده شود. بازبودن Schema محتوای الزامی را اختیاری نمی‌کند. گزینه Proposed: نگهداری تاریخچه داخلی و نمایش مجاز موارد انتخاب‌نشده؛ محل نمایش و Wire Format انتخاب نشده است. Suppressed با خارج‌بودن از Top 5 یکسان فرض نشود؛ تعارض suppressed/ongoing همچنان DL-11 است.

Decision owner: Proposed source role: محصول؛ ADR-09، ADR-17؛ AT-26، AT-30 ؛ ارتباط با ADR-07 و AT-08. این نقش‌ها همان پیشنهادهای قبلی‌اند، نه انتصاب جدید.

Closure criterion: Approve full chart/card/content mapping and Candidate/Open/Published transitions; test >5 candidates, authorized history and separate suppression. Source gate: نگاشت فیلد بازبینی‌شده و Evidence مربوط به Validation کل محتوا. نگاشت مصوب مراحل انتخاب، Open و Suppression، دسترسی تاریخچه و نمونه بیش از پنج Candidate که items همچنان حداکثر پنج عضو دارد؛ Evidence مسیر مجاز مشاهده موارد باقی‌مانده.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-07, ADR-09, ADR-17, AT-08, AT-26, AT-30.

Additional Source Evidence: [Candidate/Open/Published selection and authorized history outside Top 5](open-issues-registry.md#decision-log).

Additional Source Evidence: [Qualitative cause confidence versus optional numeric 0..1; source-family aliases and complete internal content/wire mapping](../001-system-blueprint.md#system-9).

Additional Source Evidence: [Read/close/refer actor, time and subject history; no implied action execution](../002-data-architecture.md#data-8).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-18 / محتوا | S01/S18، صفحات 9-12؛ ساختار مجاز و باز decision_card/causes و فیلدهای اضافی در S06. تکمیل منبع: بریف صفحات ۸، ۱۰ و ۱۱؛ `brief_schema.json`، بخش‌های items/open_items؛ AT-08 و AT-26. | محتوای الزامی نمودار، کارت و وضعیت، Schema کامل تجویزشده داخلی و خروجی ندارد. برچسب بررسی `Open Decision`: تفاوت Candidate Signal، Open Item و Published Brief Item و دسترسی به تاریخچه Signalهای معتبر خارج از پنج مورد مهم، نگاشت کامل ندارد. | از قرارداد محتوای داخلی Validationشده یا افزونه مستند سازگار استفاده شود. بازبودن Schema محتوای الزامی را اختیاری نمی‌کند. گزینه Proposed: نگهداری تاریخچه داخلی و نمایش مجاز موارد انتخاب‌نشده؛ محل نمایش و Wire Format انتخاب نشده است. Suppressed با خارج‌بودن از Top 5 یکسان فرض نشود؛ تعارض suppressed/ongoing همچنان DL-11 است. | محصول؛ ADR-09، ADR-17؛ AT-26، AT-30 ؛ ارتباط با ADR-07 و AT-08. این نقش‌ها همان پیشنهادهای قبلی‌اند، نه انتصاب جدید. | نگاشت فیلد بازبینی‌شده و Evidence مربوط به Validation کل محتوا. نگاشت مصوب مراحل انتخاب، Open و Suppression، دسترسی تاریخچه و نمونه بیش از پنج Candidate که items همچنان حداکثر پنج عضو دارد؛ Evidence مسیر مجاز مشاهده موارد باقی‌مانده. |



Preserved source facet: Candidate/Open/Published selection and authorized history outside Top 5. See [Source](open-issues-registry.md#decision-log).

Preserved source facet: Qualitative cause confidence versus optional numeric 0..1; source-family aliases and complete internal content/wire mapping. See [Source](../001-system-blueprint.md#system-9).

Preserved source facet: Read/close/refer actor, time and subject history; no implied action execution. See [Source](../002-data-architecture.md#data-8).

<a id="dl-19"></a>

## DL-19: KPI changes, activation authority and rollback

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

Exact conflict / missing evidence: نقش‌های تأیید، اختیار نوشتن، فعال‌سازی نامزد و سیاست Rollback. برچسب بررسی `Open Decision`: تغییر مجاز KPI موجود در برابر حفظ Reference Definition ارزیابی هنوز قرارداد کامل ندارد؛ با افزودن KPI جدید یکسان نیست.

Effect: See the exact source options and effects below.

Existing options: نامزدهای غیرفعال نسخه‌دار شوند و به تأیید و Validation مجاز نیاز داشته باشند یا فعال‌سازی با حفظ الزام به تعویق بیفتد. اختیار نوشتن از Scope خواندن استنباط نشود. گزینه‌های Proposed برای بررسی: نسخه مدیریتی جدا از مرجع ثابت، یا تعریف مشتق با ارتباط صریح به مرجع؛ هیچ‌کدام مصوب نیست. روش تغییر، سطح اختیار، زمان اثر و Rollback انتخاب نشده‌اند.

Decision owner: Proposed source role: محصول، امنیت و داده؛ ADR-01، ADR-06، ADR-08؛ AT-27، AT-29 ؛ ارتباط با ADR-09. این نقش‌ها همان پیشنهادهای قبلی‌اند، نه انتصاب جدید.

Closure criterion: Approve the distinction between fixed reference definitions and allowed management changes, with write authority, effect time and rollback; test add and change independently. Source gate: چرخه حیات و اختیار مصوب و آزمون نامزدهای ردشده و تأییدشده بدون ویرایش مرجع. ثبت تصمیم تیم درباره تفکیک مرجع و تغییر مدیریتی و Evidence دو آزمون مستقل افزودن و تغییر KPI، مجوزسنجی، زمان اثر، Rollback و حفظ نتایج و نسخه‌های قبلی لازم است.

Source Evidence: [Source](open-issues-registry.md#decision-log).

Dependencies: ADR-01, ADR-06, ADR-08, ADR-09, AT-27, AT-29.

Additional Source Evidence: [Existing KPI formula/owner/target changes versus fixed 55 reference definitions; add and change are separate tests](decisions-registry.md#adr-01).


### Full source record and conditions

| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |
|---|---|---|---|---|---|
| DL-19 / پیکربندی | S01/S18، صفحه 13؛ قاعده توسعه KPI در S02؛ مؤلفه managerConfig/ManagerGovernance در S17. تکمیل منبع: بریف صفحه ۴، قابلیت ویرایش تعریف، فرمول، مالک و هدف، و صفحه ۱۳، پیکربندی بدون تغییر کد؛ ADR-01/09 و AT-27. | نقش‌های تأیید، اختیار نوشتن، فعال‌سازی نامزد و سیاست Rollback. برچسب بررسی `Open Decision`: تغییر مجاز KPI موجود در برابر حفظ Reference Definition ارزیابی هنوز قرارداد کامل ندارد؛ با افزودن KPI جدید یکسان نیست. | نامزدهای غیرفعال نسخه‌دار شوند و به تأیید و Validation مجاز نیاز داشته باشند یا فعال‌سازی با حفظ الزام به تعویق بیفتد. اختیار نوشتن از Scope خواندن استنباط نشود. گزینه‌های Proposed برای بررسی: نسخه مدیریتی جدا از مرجع ثابت، یا تعریف مشتق با ارتباط صریح به مرجع؛ هیچ‌کدام مصوب نیست. روش تغییر، سطح اختیار، زمان اثر و Rollback انتخاب نشده‌اند. | محصول، امنیت و داده؛ ADR-01، ADR-06، ADR-08؛ AT-27، AT-29 ؛ ارتباط با ADR-09. این نقش‌ها همان پیشنهادهای قبلی‌اند، نه انتصاب جدید. | چرخه حیات و اختیار مصوب و آزمون نامزدهای ردشده و تأییدشده بدون ویرایش مرجع. ثبت تصمیم تیم درباره تفکیک مرجع و تغییر مدیریتی و Evidence دو آزمون مستقل افزودن و تغییر KPI، مجوزسنجی، زمان اثر، Rollback و حفظ نتایج و نسخه‌های قبلی لازم است. |



Preserved source facet: Existing KPI formula/owner/target changes versus fixed 55 reference definitions; add and change are separate tests. See [Source](decisions-registry.md#adr-01).

<a id="reg-iss-001"></a>

## REG-ISS-001: دامنه نقطه عطف Workflow در P2/P3

Status: **Open**. Evidence state: **Evidence Pending**.

کار لازم: Team Decision Required؛ Engineering Evidence Required.

تعارض دقیق / شواهد مفقود: جدول فاز، Workflow را در P3 قرار می‌دهد. یادداشت روز کامل P2، خلاصه هر سه Workflow را الزامی می‌کند. وضعیت این یادداشت نیز Proposed است.

اثر: کامل‌بودن P2 و وابستگی‌های فاز مشخص نیستند. محتوای الزامی گزارش را نمی‌توان حذف کرد.

گزینه‌های موجود: حداقل خروجی Workflow در P2 و جزئیات تاریخی و حالت‌های مرزی در P3؛ یا تعریف‌های مصوب نقطه عطف که همه الزام‌ها را حفظ کنند.

مالک تصمیم: هیچ مالکی مشخص نشده است.

معیار بسته‌شدن: تصمیم تیم درباره دامنه و وابستگی ثبت شود؛ سپس خروجی‌های AT-12، AT-15، AT-25 و AT-26 بررسی شوند.

شواهد منبع: [فازهای Roadmap](../003-roadmap.md#roadmap-phases).

وابستگی‌ها: ADR-15، AT-12، AT-15، AT-25، AT-26، P2 و P3.



### Full source context for REG-ISS-001

برچسب بررسی `Open Decision`: جدول بخش ۶، Workflow را در P3 قرار داده، اما توضیح Full-day Milestone، خلاصه هر سه Workflow را برای P2 لازم می‌داند. بریف صفحات ۵، ۶، ۱۶ و ۱۸ خروجی الزامی را مشخص می‌کند، نه تقسیم کار P2/P3 را. توضیح بالا همچنان Proposed است. گزینه‌های قابل بررسی عبارت‌اند از حداقل Workflow لازم در P2 و تکمیل تاریخچه و Edge Caseها در P3، یا بازتعریف مصوب Milestoneها با حفظ همه الزامات. هیچ فعالیتی در جدول جابه‌جا نشده است. بسته‌شدن این ابهام به ثبت نظر تیم درباره دامنه و وابستگی مراحل و سپس Evidence خروجی‌های AT-12/15/25/26 نیاز دارد؛ P2 فاقد خروجی الزامی، کامل محسوب نمی‌شود. این موضوع شناسه ADR/DL مناسب مستقلی ندارد و برای انتقال به Registry مرکزی آینده ثبت می‌شود؛ مالک مشخصی تعیین نشده است.

<a id="reg-iss-002"></a>

## REG-ISS-002: زمینه و پیوندهای رکورد QA

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

تعارض دقیق / شواهد مفقود: Schema منبع QA فیلدهای الزامی را دارد، اما مدل داخلی پیوندهای میان مدیر احراز هویت‌شده، دامنه مجاز، پرسش، بازبینی Snapshot یا تعاملی و نتایج واقعی QueryRun را تعریف نمی‌کند.

اثر: زمینه پاسخ و امتناع را نمی‌توان از قرارداد رکورد اعلام‌شده بازسازی کرد.

گزینه‌های موجود: یک نگاشت منطقی بازبینی‌شده لازم است. در منبع، هیچ نام موجودیت یا کلید فیزیکی انتخاب نشده است.

مالک تصمیم: مستند نشده است.

معیار بسته‌شدن: نگاشت منطقی و نمونه‌های پاسخ و امتناع بازبینی شوند. امتناع‌ها نباید Query یا ردیف ساختگی ایجاد کنند.

شواهد منبع: [مدل مفهومی داده](../002-data-architecture.md#data-2).

وابستگی‌ها: ADR-06، ADR-09، AT-16 و AT-30.

<details><summary>Source extract (unchanged text)</summary>

```text
<a id="data-2"></a>

## ۲. مدل مفهومی

نماهای موجود Structurizr با نام‌های `DataIntake` و `Containers` در [Workspace](../../architecture/structurizr/workspace.dsl)، مرز مؤلفه‌ها و ذخیره‌سازی را نشان می‌دهند؛ این نماها ERD موجودیت‌ها نیستند. نبود نمودار تفصیلی موجودیت‌ها و روابط در [گزارش شکاف‌های Structurizr](audit-2026-11-09/structurizr-gap-report.md) ثبت شده است. قراردادهای منطقی زیر همچنان پیشنهاد مدل داده هستند. دریافت انجام‌نشده می‌تواند بدون SourceFile دارای مسئله DQ باشد.

`Proposed`: اگر طراحی فیزیکی به آن نیاز دارد، روابط چندبه‌چند را با رکوردهای ارتباطی صریح نمایش دهید. نمودار قبلی قید منبع نبود. مسئله DQ مربوط به دریافت انجام‌نشده، به ExpectedDelivery ارجاع می‌دهد و وجود فایل را الزامی نمی‌کند.

### ۲.۱. قرارداد موجودیت‌های زیرساختی

| موجودیت | کلید و grain | فیلدهای لازم و قید |
|---|---|---|
| `Dataset` | یک بستهٔ داده با `dataset_id` | namespace شناسه‌ها؛ جلوگیری از برخورد شناسهٔ توسعه و دادهٔ پنهان. |
| `SourceContract` | `source_id + contract_version` | فایل‌های مورد انتظار، schedule، schemaهای پذیرفته، mapping، سیاست empty و completion؛ محدودیت تأخیر فقط اگر منبع اعلام کند. |
| `IngestBatch` | یک تلاش پذیرش یک delivery version | `drop_day, manifest_hash, received_at_utc, commit_seq, status, previous_batch_id`؛ retry به receipt قبلی متصل می‌شود. |
| `SourceFile` | یک file occurrence در delivery | `relative_path, byte_hash, byte_size, original_header, schema_fingerprint, declared_rows, actual_rows, parse_status`؛ hash یکسان به‌تنهایی هویت delivery نیست. |
| `SourceRow` | `file_occurrence_id + csv_record_ordinal` | payload اصلی، payload hash، offset یا line span، parse state و canonical mapping version. multiline CSV با شمارهٔ record ردیابی می‌شود. |
| `EntityObservation` | یک مشاهدهٔ payload موجودیت | `entity_type, business_id, source_row_id, observed_fields, effective_time, known_at_seq`؛ اختلاف payload به overwrite تبدیل نمی‌شود. |
| `EventRecord` | یک occurrence رویداد | `event_record_id, entity_type, business_id, event_type, event_at_raw, event_at_local, delivered_drop, known_at_seq, source_row_id`؛ تکرار entity/event مجاز است. |
| `CorrectionLink` | رابطهٔ اصلاح با موضوع اصلاح | `corrects_entity, corrected_field, replacement_value, effective_at, delivered_drop, source_row_id, conflict_state`؛ delta فقط اگر قرارداد بگوید. |
| `Snapshot` | یک مجموعهٔ منجمد ورودی و policy | cutoff دریافت، commit ceiling، file/version set، input policy، config/org versions و content hash. |
| `FactVersion` | `snapshot_id + projection_id + business_id` | فیلدهای MIN/MAX منتخب، contributor references، projection hash؛ current lifecycle جداست. |
| `KpiDefinition` | `kpi_id + definition_version` | تمام ستون‌های dictionary، SQL اصلی و hash، engine contract و ارجاع source line. |
| `KpiObservation` | `snapshot_id + definition_version + entity_id + dim_key + business_date` | row state، value اصلی، value منتشرشدنی، reason، query و contributor hash؛ کلید باید یکتا باشد. |
| `ReportVersion` | `report_day + manager_id + run_id + version` | snapshot، JSON/text hashes، Insight refs، policy bundle، validation receipt، `supersedes` و publication mode. |

### 2.1a. رکوردهای داخلی مورد ارجاع

همه رکوردهای این جدول قراردادهای منطقی با وضعیت Proposed هستند؛ این رکوردها جدول‌های عرضه‌شده دیتاست یا کلیدهای فیزیکی مصوب نیستند. شناسه‌های منبع را جدا از شناسه‌های داخلی تولیدشده نگه دارید.

| رکورد | Grain و مرز منطقی |
|---|---|
| ExpectedDelivery / DQIncident | یک بازه مورد انتظار منبع و یک مسئله ثبت‌شده. نبود فایل به ساخت SourceFile فرضی نیاز ندارد. شواهد مسئله، وابستگی‌های متأثر، تاریخچه وضعیت و نامعلوم‌بودن بسته‌شدن مسئله حفظ شوند. |
| SourceSchema | یک نسخه شناخته‌شده از Header، نوع و نگاشت. نام‌های اصلی و رسیدهای Parse باید قابل بازیابی بمانند. |
| KpiDependency | یک قرارداد نسخه‌دار وابستگی برای تعریف KPI: رابطه، فیلدهای مقدار و جمعیت منتخب، مسیر Join، ساعت یا Window محاسبه و شرط‌های ساختاری. |
| QueryRun / RegisteredQueryResult | یک اجرای واقعی و نتیجه آن در Snapshot عملیاتی ثابت یا نسخه تعاملی مشخص. SQL/params/hash، نسخه‌های موتور، تعریف و نوع، principal/scope، ردیف‌ها، Hash نتیجه، خطا و اشاره‌گرهای منبع حفظ شوند. نتیجه Query سفارشی نباید با برچسب Canonical KPI عرضه شود. |
| EvidenceRef | یک ارجاع مجاز به Query یا نتیجه، گروه منبع یا قطعه‌ای از سند عملیاتی. محدودیت‌های مخاطب و هدف استفاده به ارجاع منتقل شوند. |
| SignalEpisode / SignalOccurrence | یک مسئله ادامه‌دار و یک رخداد ارزیابی‌شده. هویت سری Canonical، نسخه‌های قواعد و تنظیمات، ارتباط با کیفیت و مقادیر نخست و آخر و اعلان‌های مختص هر گیرنده حفظ شوند. قواعد Reset همچنان Open هستند. |
| InsightVersion | یک منبع تحلیلی مشترک برای هر مسئله و زمینه گزارش. هشت بخش محتوای الزامی و مخاطبان شواهد ذخیره شوند. فقط Projectionهای مجاز هر نقش به اشتراک گذاشته شوند. Schema داخلی همچنان Open است. |
| DecisionEvent / ActionDraft | یک تصمیم انسانی با هویت احرازشده و پیش‌نویس مرتبط با آن. مالک، مهلت، معیار موفقیت و گزارش مبدأ قابل ردیابی باشند. پیش‌نویس یا تصمیم، رویداد اجرای اقدام نیست. |
| OrgNode / OrgEdgeVersion | یک گره سازمانی و یک رابطه تاریخ‌دار والد و فرزند. زمان اطلاع و زمان اثر، در صورت عرضه از منبع، جدا حفظ شوند. سابقه جابه‌جایی کارکنان ساخته نشود. |
| AccessGrantVersion / AuthContext | یک نسخه مجوز کنترل‌شده برای Scope و هدف استفاده و یک هویت درخواست ساخته‌شده در Server. اطلاعات دسترسی هرگز از ادعای مدل گرفته نمی‌شود. |
| ManagerConfigurationRevision | یک تغییر مجاز در تنظیمات یا نامزد KPI. تاریخچه Validation، تأیید، فعال‌سازی و زمان اثر حفظ شود. فرمول‌های Canonical بدون تغییر می‌مانند. |
| InteractiveEvidenceRevision | یک مجموعه مصوب از نسخه‌های Upload، تنظیمات و شواهد، همراه با Cutoff عملیاتی مجاز. Namespace مربوط به Upload، رسید پردازش موفق و مخاطب حفظ شوند. بسته صبحگاهی منتشرشده هرگز بازنویسی نشود. |
| ExecutionGrant / BudgetLedger | یک درخواست والد با حدود مشخص و ثبت هزینه روزانه. فراخوانی‌های فرزند نمی‌توانند محدودیت‌ها را از نو تنظیم کنند. حدود دقیق و قیمت مدل‌ها همچنان Open هستند. |
| ManagerJobOutcome / DayRunOutcome | یک نتیجه گزارش یا Export برای هر مدیر الزامی و یک رکورد تجمیعی پوشش. شکست Job الزامی، روز را ناقص نگه می‌دارد؛ حتی اگر سایر بسته‌ها منتشر شوند. |
| WorkflowStageObservation | یک مشاهده پرونده و مرحله در یک Snapshot. شواهد شروع و پایان، وضعیت open/unknown، نوع SLA، هدف Median، نسخه نگاشت مالک و مسئولیت حل‌نشده حفظ شوند. این قرارداد از Canonical KPI مربوط به Workflow جداست. |

`Requirement`: خروجی QA باید شامل `question_id, manager_id, answer_status, answer_fa` باشد (`dataset/output_contract/qa_answer_schema.json`، بخش `required`). پنج وضعیت پاسخ و قواعد امتناع در [سند 001، بخش 9.1](001-system-blueprint.md#system-9) تعریف شده‌اند. `Open`: این مدل قرارداد صریحی برای ارتباط پرسش و پاسخ با مدیر احرازهویت‌شده، Scope مجاز، Snapshot یا نسخه تعاملی و نتایج واقعی QueryRun ندارد. S07 فیلدهای `input_id, day, date, manager_id, type, content_fa` را عرضه می‌کند، اما این ارتباط‌های داخلی را عرضه نمی‌کند. قرارداد داده باید این زمینه و فیلدهای الزامی پاسخ را حفظ کند. امتناع نباید Query یا نتیجه فرضی ایجاد کند. بسته‌شدن این مورد به نگاشت منطقی بازبینی‌شده و نمونه‌های پاسخ و امتناع نیاز دارد (بریف، صفحات 3,11,13,17). ADR-06 و ADR-09 دسترسی و خروجی را پوشش می‌دهند؛ قرارداد اختصاصی رکورد QA دارای ADR/DL نیست. این یافته به ثبت مرکزی در آینده نیاز دارد. در اینجا نام موجودیت یا کلید فیزیکی انتخاب نمی‌شود.

`Open`: قرارداد WorkflowStageObservation شواهد پرونده را پوشش می‌دهد، اما روش نگهداری جمعیت محاسبه، پرونده‌های مشمول و حذف‌شده، صورت و مخرج SLA، Query محاسبه یا نتیجه گلوگاه در خلاصه هر مرحله را مشخص نمی‌کند. خروجی‌های مرحله دارای وضعیت `Requirement` هستند (بریف، صفحات 5-6,16). به [سند 001، بخش 7.2](001-system-blueprint.md#system-7)، فیلدهای `from_event, to_event, sla_hours, stage_target_median_h` در `dataset/config/workflow_definitions.csv` و `reference_views.sql` مراجعه کنید. بسته‌شدن این مورد به نگاشت بازبینی‌شده خلاصه به پرونده و Query نیاز دارد؛ پرونده‌های باز و نامعلوم باید متمایز بمانند. Canonical KPI مربوط به Workflow را جایگزین معیار مرحله نکنید. ADR-15/DL-08 مسئولیت را پیگیری می‌کنند، اما این رکورد محاسبه را تعریف نمی‌کنند. این شکاف تکمیلی قرارداد به ثبت مرکزی در آینده نیاز دارد.

`dim_key` در ذخیره‌سازی، نام بعد و مقدار آن را نگه می‌دارد. رشتهٔ خالی خروجی S06 به معنی «بدون بعد» است. NULL واقعی یک مقدار بعد، نباید با «بدون بعد» مخلوط شود. تبدیل آن به schema خروجی نیازمند قاعدهٔ صریح است.

### ۲.۲. grain دادهٔ کسب‌وکار

| خانواده | grain و ارتباط | قید طراحی |
|---|---|---|
| `orders` | مشاهدهٔ سفارش با `order_id` | raw دارای تکرار دقیق است. primary key خام نباید فقط order_id باشد. |
| `order_events` | رخداد سفارش؛ `actor_team` موجود است | از order_id به‌تنهایی برای dedup استفاده نشود. paid/refund تاریخ و اثر جدا دارند. |
| `tickets` | مشاهدهٔ تیکت؛ `ticket_id` و `order_id` | دستهٔ تیکت با دستهٔ کالا یکسان نیست. متن، دادهٔ غیرقابل اعتماد است. |
| `ticket_events` | رخداد تیکت با staff_id احتمالی | first_response از MIN و inspected/resolved از MAX در reference ساخته می‌شود. staff_id فیلد محدود است. |
| `csat` | occurrence پاسخ نظرسنجی | ticket_id تنها کلید جهانیِ تضمین‌شده برای هر پاسخ نیست. بدون قرارداد، پاسخ جدید حذف نشود. |
| `crm_leads` / `crm_lead_events` | سرنخ و رویدادهای آن | `drop_day` در فایل رویداد وجود ندارد؛ از metadata دریافت ساخته می‌شود. |
| `tasks` / `task_events` | وظیفه و رخداد آن | owner_id و blocker ممکن است دادهٔ فردی داشته باشند. reference برای done از MAX استفاده می‌کند. |
| `mkt_daily` | مشاهدات date/source | date/source نامزد grain تجاری است؛ occurrence خام همیشه حفظ می‌شود. |
| `web_sessions` | مشاهدات date/channel | تعداد session از منبع می‌آید؛ نبود فایل صفر session نیست. |
| `staff_availability` | مشاهده در سطح date/staff_id/team_id | فقط برای هدف داخلی مدیریت ظرفیت. نمایش یا پایش حضور و مرخصی فردی مجاز نیست. استثنای بار کاری تیم مستقیم، مجوز مشاهده حضور نیست. فرمول و کنترل‌های استنباط همچنان Open هستند. |

فرزند قبل از والد در مدل مجاز است. رویداد با `unresolved_parent` حفظ می‌شود و پس از ورود والد دوباره ارزیابی می‌شود. نبود orphan در دادهٔ کامل فعلی، تضمین ترتیب دریافت در دادهٔ پنهان نیست. constraint خام نباید دریافت را به دلیل نبود موقت والد حذف کند.
```

</details>


<a id="reg-iss-003"></a>

## REG-ISS-003: شواهد محاسبه مرحله Workflow

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

تعارض دقیق / شواهد مفقود: WorkflowStageObservation جمعیت‌های نگهداری‌شده، موارد مشمول یا مستثنا، صورت و مخرج SLA، Query محاسبه یا نتیجه خلاصه گلوگاه را تعریف نمی‌کند.

اثر: خلاصه‌های مرحله را نمی‌توان تا موارد و محاسبات واقعی ردیابی کرد. مالکیت در [DL-08](#dl-08) مسئله‌ای جدا است.

گزینه‌های موجود: نگاشت ذخیره‌سازی خلاصه به مورد و Query بازبینی شود. هیچ گزینه طراحی فیزیکی ارائه نشده است.

Decision owner: Not documented.

معیار بسته‌شدن: نگاشت منطقی ثبت شود و شواهد مورد و Query، از جمله موارد باز و نامعلوم، بررسی شوند. سنجه‌های مرحله با فرمول‌های Canonical Workflow KPI جایگزین نشوند.

Source Evidence: [Source](../002-data-architecture.md#data-2).

وابستگی‌ها: ADR-15، [DL-08](#dl-08)، AT-12 و AT-25.

<details><summary>Source extract (unchanged text)</summary>

```text
<a id="data-2-reg-iss-003-source-extract"></a>

## ۲. مدل مفهومی

نماهای موجود Structurizr با نام‌های `DataIntake` و `Containers` در [Workspace](../../architecture/structurizr/workspace.dsl)، مرز مؤلفه‌ها و ذخیره‌سازی را نشان می‌دهند؛ این نماها ERD موجودیت‌ها نیستند. نبود نمودار تفصیلی موجودیت‌ها و روابط در [گزارش شکاف‌های Structurizr](audit-2026-11-09/structurizr-gap-report.md) ثبت شده است. قراردادهای منطقی زیر همچنان پیشنهاد مدل داده هستند. دریافت انجام‌نشده می‌تواند بدون SourceFile دارای مسئله DQ باشد.

`Proposed`: اگر طراحی فیزیکی به آن نیاز دارد، روابط چندبه‌چند را با رکوردهای ارتباطی صریح نمایش دهید. نمودار قبلی قید منبع نبود. مسئله DQ مربوط به دریافت انجام‌نشده، به ExpectedDelivery ارجاع می‌دهد و وجود فایل را الزامی نمی‌کند.

### ۲.۱. قرارداد موجودیت‌های زیرساختی

| موجودیت | کلید و grain | فیلدهای لازم و قید |
|---|---|---|
| `Dataset` | یک بستهٔ داده با `dataset_id` | namespace شناسه‌ها؛ جلوگیری از برخورد شناسهٔ توسعه و دادهٔ پنهان. |
| `SourceContract` | `source_id + contract_version` | فایل‌های مورد انتظار، schedule، schemaهای پذیرفته، mapping، سیاست empty و completion؛ محدودیت تأخیر فقط اگر منبع اعلام کند. |
| `IngestBatch` | یک تلاش پذیرش یک delivery version | `drop_day, manifest_hash, received_at_utc, commit_seq, status, previous_batch_id`؛ retry به receipt قبلی متصل می‌شود. |
| `SourceFile` | یک file occurrence در delivery | `relative_path, byte_hash, byte_size, original_header, schema_fingerprint, declared_rows, actual_rows, parse_status`؛ hash یکسان به‌تنهایی هویت delivery نیست. |
| `SourceRow` | `file_occurrence_id + csv_record_ordinal` | payload اصلی، payload hash، offset یا line span، parse state و canonical mapping version. multiline CSV با شمارهٔ record ردیابی می‌شود. |
| `EntityObservation` | یک مشاهدهٔ payload موجودیت | `entity_type, business_id, source_row_id, observed_fields, effective_time, known_at_seq`؛ اختلاف payload به overwrite تبدیل نمی‌شود. |
| `EventRecord` | یک occurrence رویداد | `event_record_id, entity_type, business_id, event_type, event_at_raw, event_at_local, delivered_drop, known_at_seq, source_row_id`؛ تکرار entity/event مجاز است. |
| `CorrectionLink` | رابطهٔ اصلاح با موضوع اصلاح | `corrects_entity, corrected_field, replacement_value, effective_at, delivered_drop, source_row_id, conflict_state`؛ delta فقط اگر قرارداد بگوید. |
| `Snapshot` | یک مجموعهٔ منجمد ورودی و policy | cutoff دریافت، commit ceiling، file/version set، input policy، config/org versions و content hash. |
| `FactVersion` | `snapshot_id + projection_id + business_id` | فیلدهای MIN/MAX منتخب، contributor references، projection hash؛ current lifecycle جداست. |
| `KpiDefinition` | `kpi_id + definition_version` | تمام ستون‌های dictionary، SQL اصلی و hash، engine contract و ارجاع source line. |
| `KpiObservation` | `snapshot_id + definition_version + entity_id + dim_key + business_date` | row state، value اصلی، value منتشرشدنی، reason، query و contributor hash؛ کلید باید یکتا باشد. |
| `ReportVersion` | `report_day + manager_id + run_id + version` | snapshot، JSON/text hashes، Insight refs، policy bundle، validation receipt، `supersedes` و publication mode. |

### 2.1a. رکوردهای داخلی مورد ارجاع

همه رکوردهای این جدول قراردادهای منطقی با وضعیت Proposed هستند؛ این رکوردها جدول‌های عرضه‌شده دیتاست یا کلیدهای فیزیکی مصوب نیستند. شناسه‌های منبع را جدا از شناسه‌های داخلی تولیدشده نگه دارید.

| رکورد | Grain و مرز منطقی |
|---|---|
| ExpectedDelivery / DQIncident | یک بازه مورد انتظار منبع و یک مسئله ثبت‌شده. نبود فایل به ساخت SourceFile فرضی نیاز ندارد. شواهد مسئله، وابستگی‌های متأثر، تاریخچه وضعیت و نامعلوم‌بودن بسته‌شدن مسئله حفظ شوند. |
| SourceSchema | یک نسخه شناخته‌شده از Header، نوع و نگاشت. نام‌های اصلی و رسیدهای Parse باید قابل بازیابی بمانند. |
| KpiDependency | یک قرارداد نسخه‌دار وابستگی برای تعریف KPI: رابطه، فیلدهای مقدار و جمعیت منتخب، مسیر Join، ساعت یا Window محاسبه و شرط‌های ساختاری. |
| QueryRun / RegisteredQueryResult | یک اجرای واقعی و نتیجه آن در Snapshot عملیاتی ثابت یا نسخه تعاملی مشخص. SQL/params/hash، نسخه‌های موتور، تعریف و نوع، principal/scope، ردیف‌ها، Hash نتیجه، خطا و اشاره‌گرهای منبع حفظ شوند. نتیجه Query سفارشی نباید با برچسب Canonical KPI عرضه شود. |
| EvidenceRef | یک ارجاع مجاز به Query یا نتیجه، گروه منبع یا قطعه‌ای از سند عملیاتی. محدودیت‌های مخاطب و هدف استفاده به ارجاع منتقل شوند. |
| SignalEpisode / SignalOccurrence | یک مسئله ادامه‌دار و یک رخداد ارزیابی‌شده. هویت سری Canonical، نسخه‌های قواعد و تنظیمات، ارتباط با کیفیت و مقادیر نخست و آخر و اعلان‌های مختص هر گیرنده حفظ شوند. قواعد Reset همچنان Open هستند. |
| InsightVersion | یک منبع تحلیلی مشترک برای هر مسئله و زمینه گزارش. هشت بخش محتوای الزامی و مخاطبان شواهد ذخیره شوند. فقط Projectionهای مجاز هر نقش به اشتراک گذاشته شوند. Schema داخلی همچنان Open است. |
| DecisionEvent / ActionDraft | یک تصمیم انسانی با هویت احرازشده و پیش‌نویس مرتبط با آن. مالک، مهلت، معیار موفقیت و گزارش مبدأ قابل ردیابی باشند. پیش‌نویس یا تصمیم، رویداد اجرای اقدام نیست. |
| OrgNode / OrgEdgeVersion | یک گره سازمانی و یک رابطه تاریخ‌دار والد و فرزند. زمان اطلاع و زمان اثر، در صورت عرضه از منبع، جدا حفظ شوند. سابقه جابه‌جایی کارکنان ساخته نشود. |
| AccessGrantVersion / AuthContext | یک نسخه مجوز کنترل‌شده برای Scope و هدف استفاده و یک هویت درخواست ساخته‌شده در Server. اطلاعات دسترسی هرگز از ادعای مدل گرفته نمی‌شود. |
| ManagerConfigurationRevision | یک تغییر مجاز در تنظیمات یا نامزد KPI. تاریخچه Validation، تأیید، فعال‌سازی و زمان اثر حفظ شود. فرمول‌های Canonical بدون تغییر می‌مانند. |
| InteractiveEvidenceRevision | یک مجموعه مصوب از نسخه‌های Upload، تنظیمات و شواهد، همراه با Cutoff عملیاتی مجاز. Namespace مربوط به Upload، رسید پردازش موفق و مخاطب حفظ شوند. بسته صبحگاهی منتشرشده هرگز بازنویسی نشود. |
| ExecutionGrant / BudgetLedger | یک درخواست والد با حدود مشخص و ثبت هزینه روزانه. فراخوانی‌های فرزند نمی‌توانند محدودیت‌ها را از نو تنظیم کنند. حدود دقیق و قیمت مدل‌ها همچنان Open هستند. |
| ManagerJobOutcome / DayRunOutcome | یک نتیجه گزارش یا Export برای هر مدیر الزامی و یک رکورد تجمیعی پوشش. شکست Job الزامی، روز را ناقص نگه می‌دارد؛ حتی اگر سایر بسته‌ها منتشر شوند. |
| WorkflowStageObservation | یک مشاهده پرونده و مرحله در یک Snapshot. شواهد شروع و پایان، وضعیت open/unknown، نوع SLA، هدف Median، نسخه نگاشت مالک و مسئولیت حل‌نشده حفظ شوند. این قرارداد از Canonical KPI مربوط به Workflow جداست. |

`Requirement`: خروجی QA باید شامل `question_id, manager_id, answer_status, answer_fa` باشد (`dataset/output_contract/qa_answer_schema.json`، بخش `required`). پنج وضعیت پاسخ و قواعد امتناع در [سند 001، بخش 9.1](001-system-blueprint.md#system-9) تعریف شده‌اند. `Open`: این مدل قرارداد صریحی برای ارتباط پرسش و پاسخ با مدیر احرازهویت‌شده، Scope مجاز، Snapshot یا نسخه تعاملی و نتایج واقعی QueryRun ندارد. S07 فیلدهای `input_id, day, date, manager_id, type, content_fa` را عرضه می‌کند، اما این ارتباط‌های داخلی را عرضه نمی‌کند. قرارداد داده باید این زمینه و فیلدهای الزامی پاسخ را حفظ کند. امتناع نباید Query یا نتیجه فرضی ایجاد کند. بسته‌شدن این مورد به نگاشت منطقی بازبینی‌شده و نمونه‌های پاسخ و امتناع نیاز دارد (بریف، صفحات 3,11,13,17). ADR-06 و ADR-09 دسترسی و خروجی را پوشش می‌دهند؛ قرارداد اختصاصی رکورد QA دارای ADR/DL نیست. این یافته به ثبت مرکزی در آینده نیاز دارد. در اینجا نام موجودیت یا کلید فیزیکی انتخاب نمی‌شود.

`Open`: قرارداد WorkflowStageObservation شواهد پرونده را پوشش می‌دهد، اما روش نگهداری جمعیت محاسبه، پرونده‌های مشمول و حذف‌شده، صورت و مخرج SLA، Query محاسبه یا نتیجه گلوگاه در خلاصه هر مرحله را مشخص نمی‌کند. خروجی‌های مرحله دارای وضعیت `Requirement` هستند (بریف، صفحات 5-6,16). به [سند 001، بخش 7.2](001-system-blueprint.md#system-7)، فیلدهای `from_event, to_event, sla_hours, stage_target_median_h` در `dataset/config/workflow_definitions.csv` و `reference_views.sql` مراجعه کنید. بسته‌شدن این مورد به نگاشت بازبینی‌شده خلاصه به پرونده و Query نیاز دارد؛ پرونده‌های باز و نامعلوم باید متمایز بمانند. Canonical KPI مربوط به Workflow را جایگزین معیار مرحله نکنید. ADR-15/DL-08 مسئولیت را پیگیری می‌کنند، اما این رکورد محاسبه را تعریف نمی‌کنند. این شکاف تکمیلی قرارداد به ثبت مرکزی در آینده نیاز دارد.

`dim_key` در ذخیره‌سازی، نام بعد و مقدار آن را نگه می‌دارد. رشتهٔ خالی خروجی S06 به معنی «بدون بعد» است. NULL واقعی یک مقدار بعد، نباید با «بدون بعد» مخلوط شود. تبدیل آن به schema خروجی نیازمند قاعدهٔ صریح است.

### ۲.۲. grain دادهٔ کسب‌وکار

| خانواده | grain و ارتباط | قید طراحی |
|---|---|---|
| `orders` | مشاهدهٔ سفارش با `order_id` | raw دارای تکرار دقیق است. primary key خام نباید فقط order_id باشد. |
| `order_events` | رخداد سفارش؛ `actor_team` موجود است | از order_id به‌تنهایی برای dedup استفاده نشود. paid/refund تاریخ و اثر جدا دارند. |
| `tickets` | مشاهدهٔ تیکت؛ `ticket_id` و `order_id` | دستهٔ تیکت با دستهٔ کالا یکسان نیست. متن، دادهٔ غیرقابل اعتماد است. |
| `ticket_events` | رخداد تیکت با staff_id احتمالی | first_response از MIN و inspected/resolved از MAX در reference ساخته می‌شود. staff_id فیلد محدود است. |
| `csat` | occurrence پاسخ نظرسنجی | ticket_id تنها کلید جهانیِ تضمین‌شده برای هر پاسخ نیست. بدون قرارداد، پاسخ جدید حذف نشود. |
| `crm_leads` / `crm_lead_events` | سرنخ و رویدادهای آن | `drop_day` در فایل رویداد وجود ندارد؛ از metadata دریافت ساخته می‌شود. |
| `tasks` / `task_events` | وظیفه و رخداد آن | owner_id و blocker ممکن است دادهٔ فردی داشته باشند. reference برای done از MAX استفاده می‌کند. |
| `mkt_daily` | مشاهدات date/source | date/source نامزد grain تجاری است؛ occurrence خام همیشه حفظ می‌شود. |
| `web_sessions` | مشاهدات date/channel | تعداد session از منبع می‌آید؛ نبود فایل صفر session نیست. |
| `staff_availability` | مشاهده در سطح date/staff_id/team_id | فقط برای هدف داخلی مدیریت ظرفیت. نمایش یا پایش حضور و مرخصی فردی مجاز نیست. استثنای بار کاری تیم مستقیم، مجوز مشاهده حضور نیست. فرمول و کنترل‌های استنباط همچنان Open هستند. |

فرزند قبل از والد در مدل مجاز است. رویداد با `unresolved_parent` حفظ می‌شود و پس از ورود والد دوباره ارزیابی می‌شود. نبود orphan در دادهٔ کامل فعلی، تضمین ترتیب دریافت در دادهٔ پنهان نیست. constraint خام نباید دریافت را به دلیل نبود موقت والد حذف کند.
```

</details>


<a id="reg-iss-004"></a>

## REG-ISS-004: رکورد صلاحیت DQ برای Signal

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

تعارض دقیق / شواهد مفقود: مدل وضعیت‌های کیفیت و ابطال را دارد، اما هیچ پیوند ارزیابی نسخه‌دار و صریحی میان DQIncident، KpiObservation متأثر و صلاحیت Signal وجود ندارد.

اثر: ممکن است خطای داده یا بازبینی مقدار تاریخی با Signal کسب‌وکار اشتباه شود.

گزینه‌های موجود: نگاشت وضعیت به صلاحیت بازبینی شود. منبع هیچ سیاست انتشار یا قاعده داده نامعلوم را انتخاب نمی‌کند.

Decision owner: Not documented.

معیار بسته‌شدن: نگاشت و رسیدهای ورودی‌های مفقود، دیررس، اصلاح‌شده، تکراری و دارای تغییر Schema، به‌همراه یک کنترل مثبت انحراف کسب‌وکار، ثبت شوند.

شواهد منبع: [وضعیت کیفیت، قابلیت محاسبه و انتشار](../002-data-architecture.md#data-5).

وابستگی‌ها: ADR-04، ADR-07، [DL-03](#dl-03)، [DL-09](#dl-09)، AT-04، AT-05، AT-08 و AT-24.

<details><summary>Source extract (unchanged text)</summary>

```text
<a id="data-5"></a>

## ۵. وضعیت کیفیت، قابلیت محاسبه و انتشار

یک enum کلی برای همهٔ وضعیت‌ها کافی نیست. حالت‌های زیر مستقل ذخیره می‌شوند:

| محور | مقادیر پیشنهادی | پرسش پاسخ‌داده‌شده |
|---|---|---|
| `delivery_state` | expected، present، empty، missing، invalid | چه چیزی دریافت شد؟ |
| `completeness_state` | not_asserted، open_incident، observed_backfill، source_closed، closure_revoked | آیا منبع تکمیل بازه را اثبات کرده است؟ |
| `calculation_state` | success، blocked، failed | آیا query اجرا شد؟ |
| `row_state` | numeric، sql_null، no_reference_row | SQL چه نوع نتیجه‌ای داشت؟ |
| `publication_state` | eligible_snapshot، held، qualified، not_applicable، future | آیا و چگونه نمایش مجاز است؟ |
| `impact_state` | independent، changed_by_observed_input، potentially_affected، unresolved | ارتباط خروجی با incident چیست؟ |

`numeric=0` یک مقدار است، نه حالت missing. `sql_null` یعنی ردیف برگشته ولی value NULL است. `no_reference_row` یعنی گروه/کلید اصلاً برگشته نیست. این دو در ذخیره‌سازی و ارزیابی جدا می‌مانند، حتی اگر خروجی محدود JSON برای هر دو `null` نشان دهد و دلیل را در `data_issues` توضیح دهد.

`empty` فقط فایل معتبر با header و row count صفر است. این وضعیت، بسته‌شدن منبع را ثابت نمی‌کند. یک manifest درست فقط اعلام دریافت را اثبات می‌کند. `source_closed` نیاز به سند مستقل شامل source، بازه، coverage، صادرکننده و known_at دارد. اگر بعداً رکورد نقض‌کننده برسد، closure version پیشین حفظ و incident جدید ثبت می‌شود.

### ۵.۱. سه سیاست قابل پشتیبانی بدون بازطراحی

| policy | انتشار مقدار در منبع مسئله‌دار | محدودیت |
|---|---|---|
| `HOLD_UNRESOLVED_INCIDENT` | مقدار اصلی SQL داخلی حفظ؛ نتیجهٔ وابسته و نامعلوم در گزارش `null` | پیشنهاد محافظه‌کارانه تا تعیین پذیرش. ممکن است دادهٔ مفید زیادی نمایش داده نشود. |
| `QUALIFIED_DELIVERED_SNAPSHOT` | مقدار دقیق snapshot با برچسب صریح عدم تأیید تکمیل | نیازمند پذیرش برگزارکننده؛ schema فعلی فیلد استاندارد confidence منبع ندارد، پس detail و metadata داخلی لازم است. |
| `CLOSURE_BACKED_RELEASE` | نتیجه فقط با closure یا اثبات استقلال وابستگی آزاد می‌شود | دادهٔ فعلی closure مستقل ندارد؛ نمی‌توان آن را از دریافت روز بعد ساخت. |

در وضعیت عادی بدون incident، نتیجه می‌تواند طبق قرارداد «دادهٔ تحویل‌شده در آن صبح» منتشر شود و `not_asserted` باقی بماند. این کار ادعای کامل‌بودن واقعی جهان نیست. چگونگی انتشار پس از incident حل‌نشده موضوع ADR-04 است. نبود closure نباید بی‌توضیح به معنی تعطیلی دائمی کل سامانه باشد.

پیشنهاد اولیه برای incident شناخته‌شده، نگهداری unresolvedها و انتشار نتایج مستقل است. عدد صفر بازگشتی از `COUNT` یا `COALESCE` منبع غایب، گواه نبود رخداد نیست. backfill دریافت‌شده نیز incident را خودکار closed نمی‌کند.

در S10، هفت کلید پشتیبانی به علت نبود گروه denominator سفارش، مستقل و `no_reference_row` بودند. آن‌ها هفت عدد قابل بازگرداندن نیستند. ۱٬۷۳۳ مقدار تاریخی ثابت، از نظر کامل‌بودن همچنان نامعلوم بودند. معماری هیچ‌یک را صرفاً به دلیل ثابت‌ماندن عدد کامل اعلام نمی‌کند.

### 5.2. تفکیک معناهای اطمینان

`calculation_confidence` از اجرای موفق، parity و provenance به دست می‌آید؛ ترجیحاً با وضعیت و دلیل ثبت شود. `source_completeness` از شواهد منبع می‌آید. `cause_confidence` ارزیابی یک فرضیه است. هیچ‌کدام با یک امتیاز ساختگی جای دیگری را نمی‌گیرد.

`Requirement`: خطای داده به‌تنهایی نباید Signal کسب‌وکار ایجاد کند (بریف، صفحه 14، بخش خطاهای داده). `Open`: بخش‌های 4، 5 و 7 وضعیت‌های کیفیت و Invalidation را تعریف می‌کنند، اما رکورد ارزیابی ارتباط DQIncident، KpiObservation متأثر و مجوز ایجاد Signal را مشخص نمی‌کنند. قرارداد داده به نسخه‌های مرتبط مسئله و مشاهده، دلیل ارزیابی و نسخه قاعده و سیاست نیاز دارد. به [ADR-04](decisions-registry.md#adr-04)، [ADR-07](decisions-registry.md#adr-07)، DL-03 و DL-09 مراجعه کنید. بسته‌شدن این مورد به نگاشت مصوب وضعیت به مجوز ایجاد Signal و شواهد ورودی‌های غایب، دیررسیده و اصلاح‌شده نیاز دارد. این یادداشت سیاست انتشار یا قاعده‌ای برای داده نامعلوم انتخاب نمی‌کند.
```

</details>


<a id="reg-iss-005"></a>

## REG-ISS-005: ادعای حدود 70 خروجی KPI

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Engineering Evidence Required.

تعارض دقیق / شواهد مفقود: برای ادعای پیشین تیم درباره حدود 70 خروجی، خروجی محاسباتی قابل بررسی وجود ندارد. Dictionary دارای 55 تعریف است. عدد حدود 150 در بریف، تخمین است.

اثر: ممکن است تعداد تعریف، سری و مشاهده با یکدیگر اشتباه شوند و ادعای پذیرش نادرست ایجاد کنند.

گزینه‌های موجود: از فهرست بازتولیدپذیر سری‌ها استفاده شود. هیچ KPI، Dimension یا تعداد هدف جدیدی مجاز نیست.

Decision owner: Not documented.

معیار بسته‌شدن: فهرست Definition، Entity، Dimension، تاریخ، Snapshot و Query و یک روش شمارش بازتولیدپذیر ارائه شود.

شواهد منبع: [اندازه‌گیری Roadmap](../003-roadmap.md#roadmap-measurement).

وابستگی‌ها: AT-02 و AT-10.

<details><summary>Source extract (unchanged text)</summary>

```text
<a id="decisions-8"></a>

## ۸. اندازه‌گیری عملکرد و هزینه

در هر روز، زمان واقعی سپری‌شده مراحل ingest، snapshot، facts، KPI، signal، workflow، evidence، LLM و validation ثبت شود. زمان bootstrap روزهای۱ تا۶۰ جدا از زمان هر روز ارزیابی گزارش شود. برای روز کامل، تعداد مدیر واقعی، تعداد پرسش و cache state ثبت شوند.

برای هر فراخوانی مدل، `day, purpose, model_version, input_tokens, output_tokens, cached_tokens, price_version, reserved_cost, actual_cost, retry_of` نگهداری شود. ledger روز با run receipt آشتی داده شود. نرخ ثابتِ بدون تاریخ یا تخمین LLM از هزینه پذیرفته نیست.

گزارش benchmark شامل همهٔ ۳۰ روز، بیشینه، میانه و توزیع زمان باشد. حد پذیرش هر روز کنترل می‌شود؛ میانگین خوب شکست یک روز را پنهان نمی‌کند. مصرف حافظه و حجم archive/snapshot نیز ثبت شود. هدف عددی برای این دو پس از baseline سخت‌افزار تعیین شود.

برای صحت، آمار زیر لازم است: تعداد تعریف و سری، شکست SQL، اختلاف عددی، اختلاف در نبود ردیف، امتناع به دلیل Scope، نشت کشف‌شده، پوشش گزارش، شکست Schema، مسئله باز و تعداد suppressed/escalated. این آمار نباید به سهمیه مصنوعی تعداد Signal تبدیل شود.

تفکیک شمارش با برچسب `Already Covered`: `KPI Definition` تعریف ثبت‌شده در Dictionary است؛ `KPI Series` سری مشخص با Entity و Dimension؛ `KPI Observation` مقدار آن سری در تاریخ و Snapshot معین است. Grain مشاهده و هویت سری در [سند 002، بخش ۲](002-data-architecture.md#data-2) ثبت شده‌اند. فایل `dataset/config/kpi_dictionary.csv` دارای ۵۵ تعریف با شناسه یکتا است. حدود ۱۵۰ در بریف صفحه ۱ تخمین است، نه Acceptance Threshold. عدد حدود ۷۰ خروجی، گزارش بررسی قبلی تیم در درخواست این بازبینی است و با برچسب `Evidence Pending` ثبت می‌شود؛ خروجی محاسباتی قابل بازرسی برای تأیید آن ارائه نشده است. بسته‌شدن این مورد به فهرست سری‌ها با Definition، Entity، Dimension، تاریخ، Snapshot و Query و روش شمارش بازتولیدپذیر نیاز دارد؛ AT-02 صحت تعریف و AT-10 ردیابی را کنترل می‌کنند. Breakdown شهر، کانال یا محصول فقط با منبع و Dimension و Query پشتیبان معتبر است؛ Ad hoc Query بدون قرارداد، Canonical KPI Definition محسوب نمی‌شود. برای رسیدن به ۱۵۰، KPI یا Dimension ساخته نشود و تعداد هدف جدیدی انتخاب نشود.
```

</details>


<a id="reg-iss-006"></a>

## REG-ISS-006: شکاف شواهد تحویل P5

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Engineering Evidence Required.

تعارض دقیق / شواهد مفقود: جدول P5 به‌تنهایی چک‌لیست کامل تحویل را که در ضمیمه آمده است، شامل نمی‌شود.

اثر: موفقیت Docker به‌تنهایی نمی‌تواند تحویل کامل را اثبات کند.

گزینه‌های موجود: چک‌لیست کامل فعلی حفظ شود: سه UI، تاریخچه کامل Git، راهنماهای نصب و KPI و Source و سطح مدیریت، گزارش هزینه مدل و API و زیرساخت، و ارائه 10 دقیقه‌ای Demo Day.

Decision owner: Not documented.

معیار بسته‌شدن: مسیر و نسخه اقلام، لاگ‌های Docker و Replay، شواهد سه UI و گزارش‌های هزینه بررسی شوند. این کار هیچ Commit یا Push را مجاز نمی‌کند.

شواهد منبع: [فازهای Roadmap](../003-roadmap.md#roadmap-phases).

وابستگی‌ها: AT-11، AT-12، AT-18، AT-19 و P5.

<a id="reg-iss-007"></a>

## REG-ISS-007: قراردادهای فیزیکی و شواهد تفصیلی مدل

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

تعارض دقیق / شواهد مفقود: قراردادهای مدل منطقی همچنان Proposed هستند. کلیدهای فیزیکی، کلیدهای خارجی Nullable، Indexها و رکوردهای چندبه‌چند تأیید نشده‌اند. نماهای فعلی Structurizr جزئیات کامل موجودیت، Row Lineage یا مجوز تاریخ‌دار را نشان نمی‌دهند.

اثر: ممکن است یک نمودار با Schema اعتبارسنجی‌شده یا اثبات کامل مقدار و دسترسی اشتباه شود.

گزینه‌های موجود: قراردادهای فیزیکی و پیشنهادهای فعلی SG-04، SG-05 و SG-13 در کار مجاز بعدی مدل بازبینی شوند. کلید یا Grant منبع ساخته نشود.

مالک تصمیم: تیم معماری داده در VQ08 نقش بازبینی دارد؛ هیچ فرد منصوبی نام برده نشده است.

معیار بسته‌شدن: قراردادهای بازبینی‌شده ثبت شوند؛ جزئیات لازم و پس از مجوز جداگانه، Syntax و Layout مدل بررسی شوند. فهرست‌های متنی فعلی این بررسی‌ها را اثبات نمی‌کنند.

شواهد منبع: [مدل مفهومی داده](../002-data-architecture.md#data-2).

وابستگی‌ها: [DL-15](#dl-15) و [DL-16](#dl-16).

<a id="reg-iss-008"></a>

## REG-ISS-008: گزاره‌های تاریخی Workspace و ابزارها

Status: **Open**. Evidence state: **Evidence Pending**.

کار لازم: Engineering Evidence Required. این مورد، پیگیری نگهداری مستندات است. زمینه تاریخی Git یک انتخاب معماری حل‌نشده را ایجاد نمی‌کند.

تعارض دقیق / شواهد مفقود: سند 003 می‌گوید این Workspace مخزن Git ندارد؛ سند 004 می‌گوید Git در دسترس نیست. این گزاره‌ها مربوط به ممیزی تاریخی هستند. مخزن محلی و Baseline فعلی وجود دارند. SG-01 نیز توضیحات قدیمی درباره مرجع و تعداد Viewها را ثبت می‌کند؛ SG-14 یک مولد نمودار بازنشسته را ثبت می‌کند.

اثر: خواننده یا مولد بعدی ممکن است از زمینه قدیمی استفاده کند یا مستندات اصلاح‌شده را بازنویسی کند.

گزینه‌های موجود: شواهد ممیزی تاریخی حفظ شوند. یادداشت‌های زمینه فعلی بازبینی شوند و مولد قدیمی در کار بعدی با دامنه مشخص بازنشسته یا سازگار شود.

Decision owner: Not documented.

معیار بسته‌شدن: نتیجه بازبینی ثبت شود و هر تغییر مجاز بعدی در مرجع یا ابزار بررسی شود. فایل‌های حفاظت‌شده در این کار تغییر نکنند.

شواهد منبع: [بخش Verification](../004-reconciliation-review.md#verification).

وابستگی‌ها: هیچ شناسه صریحی ارائه نشده است.

<a id="reg-iss-009"></a>

## REG-ISS-009: قالب‌های Upload زمان اجرا و بازیابی

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Team Decision Required; Engineering Evidence Required.

تعارض دقیق / شواهد مفقود: در بریف به Excel اشاره شده است، اما قالب‌ها و Validation دقیق Excel، پشتیبانی اختیاری PDF، محدودیت فایل و بازیابی انتخاب نشده‌اند. Fixtureهای فعلی CSV، JSON و MD این قرارداد را تعیین نمی‌کنند.

اثر: دامنه دریافت، Parsing و بازیابی را نمی‌توان فقط بر اساس پوشش Fixture پذیرفت. زمان‌بندی Receipt در [DL-10](#dl-10) باقی می‌ماند.

گزینه‌های موجود: ثبت سند و دریافت ساخت‌یافته از هم جدا شوند؛ بازیابی متن PostgreSQL دارای وضعیت Proposed است. پشتیبانی اضافی PDF و RAG وابستگی‌های تأییدشده نیستند.

مالک تصمیم: محصول و مهندسی نقش‌های مستند هستند؛ هیچ فردی منصوب نشده است.

معیار بسته‌شدن: قرارداد قالب، اندازه و بازیابی ثبت شود و موارد Upload معتبر، پشتیبانی‌نشده، ناموفق و تزریق‌شده بررسی شوند.

شواهد منبع: [ADR-16](decisions-registry.md#adr-16).

وابستگی‌ها: ADR-16، [DL-10](#dl-10)، AT-03، AT-13 و AT-22.

<a id="reg-iss-010"></a>

## REG-ISS-010: شواهد مقایسه محتوای تاریخی S01

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Engineering Evidence Required.

بخش حل‌شده: کاربر PDF رسمی فعلی S01 را در بخش 1 از ARCH-REG-002 تأیید می‌کند. فایل در مسیر اعلام‌شده مخزن وجود دارد. SHA-256 فعلی آن `f6761b4fc37145d152f2b9793b298e35f48db666d5205c4d02be0f5f13e4863b` است. شناسایی منبع به پاسخ دیگری از برگزارکننده نیاز ندارد.

پرسش باقی‌مانده: بازبینی قبلی SHA-256 برابر با `6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8` را ثبت کرده است. بایت‌های PDF تاریخی برای مقایسه محتوا بازیابی نشده‌اند. نتیجه بازبینی قدیمی نمی‌تواند برابری معنایی با بایت‌های فعلی را اثبات کند.

اثر: هویت منبع فعلی از تطابق تأییدنشده محتوای تاریخی جدا نگه داشته شود. تفاوت Hash بایت‌ها، تغییر الزام‌ها را اثبات نمی‌کند.

گزینه‌های موجود: PDF شناسایی‌شده تاریخی بازیابی و محتوای آن مقایسه شود؛ یا تعیین تکلیف مجاز برای مقایسه تاریخی بازیابی‌ناپذیر ثبت شود. هیچ‌یک در اینجا انتخاب نشده است.

مالک تصمیم: هیچ فردی مستند نشده است. این مورد، کار شواهد و Provenance است و انتخاب معماری جدید نیست.

معیار بسته‌شدن: مقایسه تاریخی یا تعیین تکلیف مجاز و ثبت‌شده ارائه شود. بخش هویت فعلی حل شده است. کل رکورد همچنان Open می‌ماند.

شواهد منبع: [فهرست منبع](../001-system-blueprint.md#system-2)، [بازبینی قبلی](../004-reconciliation-review.md#verification)، [دستور فعلی کاربر](audit-ARCH-REG-002/request.txt) و [یافته‌های ممیزی](semantic-audit-report.md).

وابستگی‌ها: [DL-16](#dl-16) یک Proposed / Inferred Relationship برای بازبینی Provenance است. این رابطه، وابستگی به برگزارکننده ایجاد نمی‌کند.


<a id="decision-log"></a>

<a id="decisions-10"></a>

## 10. Decision Log

همه ردیف‌های زیر `Open` هستند. گزینه‌ها ورودی بازبینی‌اند، نه قواعد پذیرفته‌شده. نقش‌های فهرست‌شده مالکان پیشنهادی هستند، نه افراد منصوب. ردیف فقط با منبع یا رکورد تصمیم تیم و Evidence آزمون پذیرش مرتبط بسته شود.



رکوردهای کامل DL-01 تا DL-19 را در بالا بخوانید. ردیف‌های منبع آن‌ها همه گزینه‌ها، نقش‌ها و Gateهای اصلی را حفظ می‌کنند. نقش‌ها همچنان نقش‌های پیشنهادی هستند و افراد منصوب را نشان نمی‌دهند.
