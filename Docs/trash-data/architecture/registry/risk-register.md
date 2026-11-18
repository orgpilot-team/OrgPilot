# ثبت ریسک‌ها

<a id="risk-register-overview"></a>

محل مستندات: سابقهٔ حاکمیتی تعیین‌شده توسط تیم. وضعیت: **Draft / Pending Review**. سوابق کامل منبع و معیارهای زیر در قالب Markdown خوانا هستند. متن انگلیسی نقش نمایه را دارد. تأیید ساختار، هیچ تصمیم، قاعدهٔ منبع، ارزیابی ریسک یا نتیجهٔ پذیرش را تغییر نمی‌دهد.

وضعیت: **Draft / Pending Review**.

شدت همهٔ سوابق: **Not Assessed**. منابع، روش امتیازدهی ریسک را مشخص نمی‌کنند. شدت یافتهٔ ممیزی، امتیاز ریسک نیست.

وضعیت کنترل: **Evidence Pending / Not Executed**. الزامات منبع همچنان الزام هستند. کنترل‌های مهندسی تا زمانی که منبع آن‌ها را به‌صراحت تأیید نکند، Proposed می‌مانند. هیچ ادعایی دربارهٔ اثربخشی کنترل وجود ندارد.

دو ریسک تبدیل SQL و Oracle در بخش ۵، یک سابقهٔ اصلی را تشکیل می‌دهند. دو ردیف منبع آن‌ها در ادامه حفظ شده است. سایر اثرهای متمایز، جدا می‌مانند.

<a id="reg-rsk-001"></a>

## REG-RSK-001: افشای داده‌های آینده

Cause: Facts or preloaded files can include knowledge beyond the cutoff.

Consequence: A historical report can look correct but be invalid.

Control: Filter before projection; use future-data injection fixtures and snapshot hashes.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

شاهد منبع: [بخش ۵، ریسک‌های عمده و اقدام کنترل](#decisions-5).

ADR / DL / AT مرتبط: [ADR-08](decisions-registry.md#adr-08)، [DL-10](open-issues-registry.md#dl-10)، [AT-03](acceptance-register.md#at-03).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| نشت آینده از fact یا فایل preloadشده | گزارش تاریخی ظاهراً درست ولی غیرقابل قبول | cutoff قبل از projection؛ آزمون تزریق داده آینده؛ snapshot hash. |



<a id="reg-rsk-002"></a>

## REG-RSK-002: دانه‌بندی نامشخص ورودی

Cause: RAW and DEDUP can feed different populations to joins.

Consequence: Canonical values can differ from evaluator results.

Control: Keep separate modes and obtain the official input answer.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-02](decisions-registry.md#adr-02)، [DL-02](open-issues-registry.md#dl-02)، [AT-02](acceptance-register.md#at-02)، [AT-05](acceptance-register.md#at-05).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| input grain نامشخص | عدد مرجع متفاوت با evaluator | دو policy جدا و پاسخ رسمی ADR-02. |



<a id="reg-rsk-003"></a>

## REG-RSK-003: اشتباه‌گرفتن manifest با کامل‌بودن

Cause: A manifest can omit a missing source.

Consequence: False zero values or early incident closure can be reported.

Control: Use expected-source contracts, separate closure and missing/empty tests.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-04](decisions-registry.md#adr-04)، [DL-03](open-issues-registry.md#dl-03)، [AT-04](acceptance-register.md#at-04)، [AT-23](acceptance-register.md#at-23).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| اعتماد به manifest برای completeness | صفر جعلی یا رفع incident زودهنگام | expected source registry، closure جدا و آزمون missing/empty. |



<a id="reg-rsk-004"></a>

## REG-RSK-004: انحراف در تبدیل SQL

Cause: PostgreSQL and the reference oracle can differ in time, types, rounding and selected row sets.

Consequence: Even a hundredth-hour difference can break acceptance.

Control: Use one PostgreSQL product path, versioned translations, original hashes and an independent reference oracle.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-01](decisions-registry.md#adr-01)، [DL-01](open-issues-registry.md#dl-01)، [AT-02](acceptance-register.md#at-02)، [AT-05](acceptance-register.md#at-05).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| تغییر محاسبات در تبدیل SQL | اختلاف حتی در صدم ساعت | Test Oracle مرجع SQLite، نسخه تبدیل PostgreSQL و هم‌ارزی در مرزها. |
| نگهداری تبدیل و Oracle مرجع | تفاوت رفتار SQL می‌تواند مقادیر گرد‌شده یا مجموعه ردیف‌ها را تغییر دهد. | یک مسیر محصول PostgreSQL؛ Test Oracle نسخه‌دار مستقل و رسیدهای تبدیل. |



<a id="reg-rsk-005"></a>

## REG-RSK-005: افشای query خام یا cache

Cause: Results, query context, cache or logs can carry another manager scope.

Consequence: Restricted data can reach a manager or the LLM.

Control: Apply RLS, scoped cache keys, separate worker identity and adversarial query tests.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-06](decisions-registry.md#adr-06)، [DL-06](open-issues-registry.md#dl-06)، [AT-06](acceptance-register.md#at-06)، [AT-13](acceptance-register.md#at-13).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| دسترسی خام در query یا cache | نشت به مدیر دیگر یا LLM | RLS، scope در cache key، worker جدا و مجموعه آزمون Query خصمانه. |



<a id="reg-rsk-006"></a>

## REG-RSK-006: اشتباه‌گرفتن اصلاح تاریخی با Signal تجاری

Cause: A knowledge revision can change an old value.

Consequence: False alerts and escalation can follow.

Control: Keep knowledge_revision and incident links separate from business eligibility.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-04](decisions-registry.md#adr-04)، [ADR-07](decisions-registry.md#adr-07)، [DL-03](open-issues-registry.md#dl-03)، [DL-09](open-issues-registry.md#dl-09)، [AT-04](acceptance-register.md#at-04)، [AT-05](acceptance-register.md#at-05)، [AT-24](acceptance-register.md#at-24).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| اصلاح تاریخی به شکل سیگنال تجاری | هشدار و تشدید نادرست | `knowledge_revision` جدا و incident linkage. |



<a id="reg-rsk-007"></a>

## REG-RSK-007: رویدادهای توسعهٔ hardcoded

Cause: Runtime logic can depend on known incident dates or IDs.

Consequence: The product can fail on hidden data.

Control: Vary dates, identifiers, dimensions and delivery order in separate fixtures.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-08](decisions-registry.md#adr-08)، [DL-16](open-issues-registry.md#dl-16)، [AT-19](acceptance-register.md#at-19).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| hardcode حوادث توسعه | شکست روی دادهٔ پنهان | تغییر تاریخ، شناسه، dimension و ترتیب delivery در fixtureهای مصنوعی. |



<a id="reg-rsk-008"></a>

## REG-RSK-008: تکرار بدون وضعیت گیرنده

Cause: One state shared among recipients can erase or repeat their history.

Consequence: The owner can miss a warning or a parent can receive a duplicate.

Control: Keep episode and recipient state separate and test the escalation chain.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-07](decisions-registry.md#adr-07)، [DL-09](open-issues-registry.md#dl-09)، [AT-08](acceptance-register.md#at-08)، [AT-24](acceptance-register.md#at-24).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| قاعدهٔ تکرار بدون recipient state | حذف هشدار مالک یا تکرار برای والد | state جدا برای episode و recipient؛ تست escalation chain. |



<a id="reg-rsk-009"></a>

## REG-RSK-009: علت‌های بدون پشتوانه

Cause: Two dependent measurements can look like two independent witnesses.

Consequence: A fabricated cause can receive high confidence.

Control: Use lineage-aware evidence review and deterministic validation outside the LLM.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-09](decisions-registry.md#adr-09)، [DL-11](open-issues-registry.md#dl-11)، [DL-18](open-issues-registry.md#dl-18)، [AT-10](acceptance-register.md#at-10).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| نبود دو شاهد مستقل | علت ساختگی با confidence بالا | lineage groups و validator مستقل از LLM. |



<a id="reg-rsk-010"></a>

## REG-RSK-010: ادعای علّی بر پایهٔ تصمیم شبیه‌سازی‌شده

Cause: A decision record and later change can be mistaken for proof of execution or effect.

Consequence: The report can attribute an effect without evidence.

Control: Compare observations with calendar context and stated limits; preserve fixed replay data.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-17](decisions-registry.md#adr-17)، [DL-12](open-issues-registry.md#dl-12)، [AT-14](acceptance-register.md#at-14)، [AT-29](acceptance-register.md#at-29).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| برداشت علّی از تصمیم شبیه‌سازی‌شده | نسبت‌دادن اثر بدون مدرک | قبل و بعد با کنترل تقویم و محدودیت؛ عدم تغییر دادهٔ replay پس از تصمیم. |



<a id="reg-rsk-011"></a>

## REG-RSK-011: افزایش تعداد مدیران یا پرسش‌ها

Cause: More reports, QA and retries consume shared daily resources.

Consequence: Time or cost limits can fail.

Control: Consider template writing, reservations and authorized cache; measure the worst day.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-10](decisions-registry.md#adr-10)، [ADR-13](decisions-registry.md#adr-13)، [ADR-14](decisions-registry.md#adr-14)، [DL-13](open-issues-registry.md#dl-13)، [DL-14](open-issues-registry.md#dl-14)، [AT-17](acceptance-register.md#at-17)، [AT-18](acceptance-register.md#at-18)، [AT-28](acceptance-register.md#at-28).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| رشد تعداد مدیران یا سؤالات | شکست زمان یا هزینه | template writer، reservation، cache مجاز و اندازه‌گیری بدترین روز. |



<a id="reg-rsk-012"></a>

## REG-RSK-012: جایگزینی واقعیت‌های مرجع با چرخهٔ عمر جاری

Cause: An operational state can be substituted for canonical MIN/MAX selections.

Consequence: Backlog or SLA can change without source authority.

Control: Keep operational projections separate and retain the formula hash.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](risk-register.md#decisions-5).

ADR / DL / AT مرتبط: [ADR-11](decisions-registry.md#adr-11)، [DL-05](open-issues-registry.md#dl-05)، [AT-02](acceptance-register.md#at-02)، [AT-05](acceptance-register.md#at-05).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


### سابقهٔ کامل منبع و شرایط

| ریسک | اثر | اقدام و نشانهٔ کنترل |
|---|---|---|
| وضعیت فعلی entity جایگزین reference شود | تغییر backlog/SLA بدون مجوز | projection عملیاتی جدا، formula hash ثابت. |



<a id="reg-rsk-013"></a>

## REG-RSK-013: تزریق prompt از متن عملیاتی

Cause: A ticket or upload contains instructions.

Consequence: Policy, numbers, recipients or actions can be changed.

Control: Treat text as untrusted data and check destination, number and tool authority independently.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

شاهد منبع: [امنیت و حاکمیت](../001-system-blueprint.md#system-10).

ADR / DL / AT مرتبط: [ADR-06](decisions-registry.md#adr-06)، [ADR-16](decisions-registry.md#adr-16)، [ADR-17](decisions-registry.md#adr-17)، [DL-06](open-issues-registry.md#dl-06)، [AT-13](acceptance-register.md#at-13)، [AT-22](acceptance-register.md#at-22).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.

<a id="reg-rsk-014"></a>

## REG-RSK-014: استفادهٔ زودهنگام از شاهد پیوست

Cause: A question can precede receipt or readiness of its attachment.

Consequence: The answer can use evidence unavailable at question time.

Control: Record attachment dependency, receipt and readiness; use clarification/data-unavailable when needed.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

شاهد منبع: [جریان اجرای شبانه و replay](../001-system-blueprint.md#system-5).

ADR / DL / AT مرتبط: [ADR-08](decisions-registry.md#adr-08)، [ADR-16](decisions-registry.md#adr-16)، [DL-10](open-issues-registry.md#dl-10)، [AT-03](acceptance-register.md#at-03)، [AT-22](acceptance-register.md#at-22).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.

<a id="reg-rsk-015"></a>

## REG-RSK-015: اشتباه‌گرفتن روز ناقص با موفقیت

Cause: A required manager job can fail before a draft exists.

Consequence: Successful independent packages can hide missing daily coverage.

Control: Track job/export/day outcomes separately and record failure even without a draft.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

شاهد منبع: [عملیات، کارایی و بازیابی](../002-data-architecture.md#data-11).

ADR / DL / AT مرتبط: [ADR-14](decisions-registry.md#adr-14)، [DL-13](open-issues-registry.md#dl-13)، [AT-15](acceptance-register.md#at-15)، [AT-21](acceptance-register.md#at-21)، [AT-28](acceptance-register.md#at-28).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.

<a id="reg-rsk-016"></a>

## REG-RSK-016: serialization تأییدنشدهٔ وضعیت

Cause: The brief uses suppressed and the schema uses ongoing.

Consequence: Output can violate schema or silently lose suppression meaning.

Control: Preserve history and obtain a valid output mapping without changing the source schema.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

شاهد منبع: [رابط‌های مدیریت و خروجی](../001-system-blueprint.md#system-9).

ADR / DL / AT مرتبط: [ADR-09](decisions-registry.md#adr-09)، [DL-11](open-issues-registry.md#dl-11)، [AT-11](acceptance-register.md#at-11)، [AT-30](acceptance-register.md#at-30).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.

<a id="reg-rsk-017"></a>

## REG-RSK-017: اولویت مبهم اصلاح

Cause: Equal-rank conflicting corrections have no supplied secondary order.

Consequence: An arbitrary payload can be reported as valid.

Control: Record conflict; obtain source precedence or review quarantine. No current correction tie is claimed.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

شاهد منبع: [زمان، snapshot و تاریخچه](../002-data-architecture.md#data-3).

ADR / DL / AT مرتبط: [ADR-11](decisions-registry.md#adr-11)، [DL-05](open-issues-registry.md#dl-05)، [AT-05](acceptance-register.md#at-05).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.

<a id="reg-rsk-018"></a>

## REG-RSK-018: تاریخچهٔ بازیابی‌ناپذیر

Cause: Inconsistent archive/database backup or early retention removal can break replay.

Consequence: Historical reports and their source evidence cannot be reconstructed.

Control: Approve retention/backup policy and test file hashes, snapshot rebuild and sample reports after restore.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](../002-data-architecture.md#data-11).

ADR / DL / AT مرتبط: [ADR-12](decisions-registry.md#adr-12)، [DL-15](open-issues-registry.md#dl-15)، [AT-19](acceptance-register.md#at-19).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.

<a id="reg-rsk-019"></a>

## REG-RSK-019: شناسایی از گروه کوچک یا متن آزاد

Cause: Aggregate capacity or title/blocker text can identify a person.

Consequence: A higher manager can receive restricted individual or leave data.

Control: Review redaction, purpose and group-size controls; test derived claims and text paths.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

Source Evidence: [Source](../001-system-blueprint.md#system-10).

ADR / DL / AT مرتبط: [ADR-06](decisions-registry.md#adr-06)، [DL-06](open-issues-registry.md#dl-06)، [DL-07](open-issues-registry.md#dl-07)، [AT-06](acceptance-register.md#at-06)، [AT-10](acceptance-register.md#at-10).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.

<a id="reg-rsk-020"></a>

## REG-RSK-020: بازنویسی KPI مرجع با تغییر مدیریتی

Cause: Configurable formula/owner/target changes can be confused with changes to the fixed 55 reference definitions.

Consequence: Canonical evaluation and previous versions can change without authority.

Control: Obtain the DL-19 lifecycle policy; preserve the reference and separately test add/change, effect time and rollback.

وضعیت کنترل: **Evidence Pending**. کنترل محصول اجرا نشده است.

شدت: **Not Assessed**.

شاهد منبع: [DL-19: تغییرهای KPI، اختیار فعال‌سازی و rollback](open-issues-registry.md#dl-19).

ADR / DL / AT مرتبط: [ADR-01](decisions-registry.md#adr-01)، [ADR-06](decisions-registry.md#adr-06)، [ADR-08](decisions-registry.md#adr-08)، [DL-19](open-issues-registry.md#dl-19)، [AT-27](acceptance-register.md#at-27)، [AT-29](acceptance-register.md#at-29).

شاهد لازم: پاسخ منبع یا خط‌مشی مرتبط، قرارداد کنترل تأییدشده و رسیدهای واقعی آزمون‌های مرتبط. پیش از هر ادعای کاهش ریسک، موارد مثبت و منفی را بررسی کنید.


<a id="decisions-5"></a>

## ۵. ریسک‌های عمده و اقدام کنترل

۱۳ ردیف اصلی ریسک منبع در ۲۰ سابقهٔ ریسک بالا حفظ شده‌اند. دو ردیف SQL/Oracle در REG-RSK-004 مشترک هستند. هیچ کنترلی اجرا نشده است و شدت همهٔ موارد Not Assessed باقی می‌ماند.
