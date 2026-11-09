# تطبیق معماری ARKA

کلید سند: `004-reconciliation-review`. خانوادهٔ مشترک معماری: `ARCH-001`.

تاریخ بازبینی: 2026-11-09. منطقهٔ زمانی: `Asia/Tehran`.

این بازبینی، چهار سند شماره‌دار معماری و اسناد وابسته را با شرح رسمی، قراردادهای مجموعه‌داده و سابقهٔ بازبینی Q01-Q17 تطبیق می‌دهد. این بازبینی فقط اسناد را تغییر می‌دهد. این بازبینی مدعی پیاده‌سازی محصول، هم‌ارزی عددی، امنیت، کارایی یا نتیجهٔ پذیرش نیست.

مبنای `Accepted` شامل یک AI Agent با حدود مشخص، ماژول‌های پشتیبان قطعی، اجرای محصول فقط با PostgreSQL، انتشار مستقل گزارش‌های معتبر مدیران، مرزهای قطعی KPI، سیگنال، مجوز و اعتبارسنجی نهایی، و تصمیم‌های سازمانی تحت کنترل انسان است. کاربر این مرزها را در درخواست ممیزی فعلی (S19) تأیید می‌کند. محاسبه‌گر قبلی محصول که SQLite را در خود داشت منسوخ است. استفاده از SQLite فقط به‌عنوان oracle آزمون مرجع و مجزا مجاز است. SQLite خارج از مسیر اجرای محصول است.

## منابع و اعتبار

برای S01-S19، [فهرست منابع](001-system-blueprint.md#system-2) را بخوانید. شرح رسمی و قراردادهای مجموعه‌داده نیازمندی‌ها را تعریف می‌کنند. تصمیم تیم، معماری را در محدودهٔ این نیازمندی‌ها انتخاب می‌کند. پیشنهاد Codex به‌تنهایی تأیید را اثبات نمی‌کند.

کاربر `C:/Users/ashkriz/Desktop/Adr.md` را فایل درخواستی بازبینی معرفی کرد. [نسخهٔ بدون تغییر منبع](sources/Adr.md) در این مجموعه اسناد نگهداری می‌شود. متن پرسش‌ها و جدول نتیجهٔ نهایی آن بررسی شدند. تأییدکنندگان تصمیم‌های اصلی و تاریخ‌های تأیید ارائه نشده‌اند. این بازبینی آن‌ها را جعل نمی‌کند.

[مدل موجود Structurizr](../../architecture/structurizr/workspace.dsl) از این مرزهای هدف پشتیبانی می‌کند. یادداشت‌های اعتبار و قراردادهای مرتبط اجزای آن بررسی شدند. این مدل، مدل هدف موجود است و پیاده‌سازی را اثبات نمی‌کند. این مدل تغییر نکرد.

| منبع | SHA-256 در این بازبینی |
|---|---|
| سابقهٔ بازبینی S16 و نسخهٔ دقیق منبع | `0c7cea554016930366100cb1138ada6ace7f05e918e274ee24f0a89e465639df` |
| PDF فعلی شرح رسمی S01 که در ARCH-REG-002 تأیید شده است | `f6761b4fc37145d152f2b9793b298e35f48db666d5205c4d02be0f5f13e4863b` |
| hash تاریخی S01 که بازبینی پیشین ثبت کرده است | `6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8` |

فرادادهٔ منشأ S01 در ARCH-REG-002: کاربر PDF محلی موجود را به‌عنوان منبع ثبت فعلی تأیید می‌کند. گزاره‌های بازبینی PDF در ادامه، کار بازبینی تاریخی را شرح می‌دهند. این گزاره‌ها مقایسهٔ محتوایی جدید برای هویت بایتی فعلی نیستند. نسخهٔ تاریخی PDF برای مقایسه بازیابی نشده است. تفاوت hash به‌تنهایی تغییر نیازمندی را اثبات نمی‌کند. REG-ISS-010 برای این کمبود شواهد در وضعیت `Open` می‌ماند.

S01 نشانه‌گذاری و دوباره ذخیره شد. S18 تبدیل Markdown آن است. محتوای PDF فعلی در صفحه‌های 8، 10 و 15 با متن متناظر به‌صورت دیداری بررسی شد. این بررسی‌ها کنترل‌های تکرار، محتوای الزامی گزارش و عبارت وضعیت suppressed را تأیید می‌کنند. صفحه‌های 13 و 16 نیز در بازبینی پیشین همین PDF فعلی بررسی شدند. تفاوت hash قبلی هیچ تغییر نیازمندی را اثبات نکرد. ممیزی‌های عددی قبلی، شواهد تاریخی منتسب باقی می‌مانند.

دقیقاً از چهار وضعیت تصمیم زیر استفاده کنید:

- `Requirement`: قاعدهٔ صریح شرح یا قرارداد مجموعه‌داده.
- `Accepted`: تصمیم ثبت‌شدهٔ تیم.
- `Proposed`: انتخاب طراحی بدون شاهد تأیید.
- `Open`: انتخاب حل‌نشده یا تعارض منبع.

`Observation` منبع راستی‌آزمایی‌شده یا شاهد ممیزی است. این مورد وضعیت تأیید نیست.

یک پرسش می‌تواند بیش از یک وضعیت داشته باشد. برای نمونه، Q03 یک انتخاب موتور با وضعیت `Accepted` و یک دروازهٔ هم‌ارزی با وضعیت `Open` دارد. به کل پرسش یک وضعیت ندهید که این تفاوت را پنهان کند. تعداد پاسخ‌های صریح، جزئی و موجودنبودن پاسخ در منبع بازبینی، خلاصهٔ منبع است. این تعداد، شمار تأییدها نیست.

<a id="question-map"></a>

## نگاشت Q01-Q17

این شناسه‌ها فقط به بازبینی معماری در S16 ارجاع می‌دهند. [پرسش‌های مدیران Q01-Q16](registry/acceptance-register.md#manager-question-map) متعلق به S07 هستند. پرسش‌های بازبینی نمودار در [فهرست پرسش‌های باز](visualizations/open-questions.md#open-questions-and-review-points) پیشوند `VQ` دارند.

همهٔ دروازه‌های پذیرش زیر برنامه‌ریزی شده‌اند. این دروازه‌ها در این کار مستندسازی اجرا نشدند.

| پرسش بازبینی | نیازمندی و وضعیت تصمیم | ADRها | بخش‌های سند | دروازه‌های پذیرش و فهرست موارد باز |
|---|---|---|---|---|
| <a id="review-q01"></a>Q01: توپولوژی Agent | `Accepted`: یک AI Agent با حدود مشخص به‌همراه ماژول‌های قطعی؛ جدول نتیجهٔ Q01 در S16 تصمیم تیم را صریح ثبت می‌کند. `Open`: محدودیت‌های اجرا. | [ADR-13](registry/decisions-registry.md#adr-13)، [ADR-10](registry/decisions-registry.md#adr-10) | [001: سیستم](001-system-blueprint.md#system-1)، [ماژول‌ها](001-system-blueprint.md#system-4) | [AT-20](registry/acceptance-register.md#at-20)، [AT-17](registry/acceptance-register.md#at-17)/[AT-18](registry/acceptance-register.md#at-18)؛ [DL-14](registry/open-issues-registry.md#dl-14)؛ [AT-28](registry/acceptance-register.md#at-28) |
| <a id="review-q02"></a>Q02: فایل‌ها و دریافت | `Requirement`: منابع ساخت‌یافته، ورودی مدیر و بارگذاری‌ها؛ S01 pp.3,12-14 و S02/S07. `Proposed`: ثبت جداگانهٔ سند و دریافت ساخت‌یافته. `Open`: قالب‌های دقیق، از جمله Excel، و بازیابی. | [ADR-16](registry/decisions-registry.md#adr-16)، [ADR-08](registry/decisions-registry.md#adr-08) | [001: ماژول‌ها](001-system-blueprint.md#system-4)، [002: دریافت](002-data-architecture.md#data-4) | [AT-22](registry/acceptance-register.md#at-22)، [AT-03](registry/acceptance-register.md#at-03)/[AT-13](registry/acceptance-register.md#at-13)؛ [DL-10](registry/open-issues-registry.md#dl-10)؛ [AT-29](registry/acceptance-register.md#at-29) |
| <a id="review-q03"></a>Q03: تعداد 55 KPI در PostgreSQL | `Accepted`: فقط PostgreSQL؛ متن و نتیجهٔ Q03 در S16 و S17. `Requirement`: نتیجه‌های canonical بدون تغییر؛ S02-S04 و S01 p.16. `Proposed`: ترجمه‌های نسخه‌بندی‌شده. `Open`: اثبات برای همهٔ 55 تعریف. | [ADR-01](registry/decisions-registry.md#adr-01) | [002: محاسبه](002-data-architecture.md#data-6)، [مرز موتور](002-data-architecture.md#data-10) | [AT-02](registry/acceptance-register.md#at-02)، [AT-03](registry/acceptance-register.md#at-03)/[AT-05](registry/acceptance-register.md#at-05)/[AT-17](registry/acceptance-register.md#at-17)؛ [DL-01](registry/open-issues-registry.md#dl-01)؛ [AT-27](registry/acceptance-register.md#at-27) |
| <a id="review-q04"></a>Q04: کوئری‌های زبان طبیعی | `Requirement`: SQL فقط‌خواندنی و ثبت‌شده با کنترل ردیف در لایهٔ داده؛ S01 pp.9,13. `Proposed`: ابتدا ابزارهای ازپیش‌تعریف‌شده و سپس SQL سفارشی اعتبارسنجی‌شده. `Open`: فهرست‌های مجاز و محدودیت‌های دقیق. SQL آزاد با مرز الزامی سازگار نیست. | [ADR-06](registry/decisions-registry.md#adr-06)، [ADR-10](registry/decisions-registry.md#adr-10) | [001: امنیت](001-system-blueprint.md#system-10)، [002: مسیر کوئری](002-data-architecture.md#data-10) | [AT-06](registry/acceptance-register.md#at-06)، [AT-10](registry/acceptance-register.md#at-10)/[AT-16](registry/acceptance-register.md#at-16)/[AT-20](registry/acceptance-register.md#at-20)؛ [DL-06](registry/open-issues-registry.md#dl-06)/[DL-14](registry/open-issues-registry.md#dl-14)؛ [AT-28](registry/acceptance-register.md#at-28) |
| <a id="review-q05"></a>Q05: سفارش‌های تکراری | `Requirement`: موارد تکراری به‌عنوان مسئلهٔ داده گزارش شوند؛ مجموعه‌داده و SQL اصلی حفظ شوند. `Open`: سیاست محاسبهٔ پذیرفته‌شدهٔ RAW/DEDUP. مقایسهٔ دوحالتهٔ S16، `Proposed` است و تأیید برگزارکننده نیست. | [ADR-02](registry/decisions-registry.md#adr-02) | [002: دریافت](002-data-architecture.md#data-4)، [محاسبه](002-data-architecture.md#data-6) | [AT-02](registry/acceptance-register.md#at-02)، [AT-05](registry/acceptance-register.md#at-05)؛ [DL-02](registry/open-issues-registry.md#dl-02) |
| <a id="review-q06"></a>Q06: دادهٔ ناقص | `Requirement`: ادامهٔ گزارش‌ها، شناسایی منابع مفقود و استفاده از null برای مقدارهای فعلی موجودنبوده؛ S01 pp.13-14,17 و S02. خلاصهٔ S16/S17 زمینهٔ تاریخ‌دار آخرین مقدار معتبر را حفظ می‌کند. `Open`: شرایط انتشار، سن، بسته‌شدن و نگاشت wire. | [ADR-04](registry/decisions-registry.md#adr-04) | [002: کیفیت](002-data-architecture.md#data-5)، [001: خروجی](001-system-blueprint.md#system-9) | [AT-04](registry/acceptance-register.md#at-04)، [AT-23](registry/acceptance-register.md#at-23)؛ [DL-03](registry/open-issues-registry.md#dl-03) |
| <a id="review-q07"></a>Q07: اصلاح تاریخی | `Requirement`: واجدشرایط‌بودن cutoff و نتیجه‌های canonical؛ S02-S04. طراحی نسخه‌بندی‌شدهٔ موجود snapshot/report حفظ شود. `Proposed`: بازسازی کامل به‌عنوان مبنای صحت. `Open`: محاسبهٔ انتخابی و اعلان‌های restatement. | [ADR-03](registry/decisions-registry.md#adr-03)، [ADR-05](registry/decisions-registry.md#adr-05) | [002: زمان](002-data-architecture.md#data-3)، [محاسبهٔ دوباره](002-data-architecture.md#data-7)، [lineage](002-data-architecture.md#data-8) | [AT-02](registry/acceptance-register.md#at-02)/[AT-03](registry/acceptance-register.md#at-03)/[AT-05](registry/acceptance-register.md#at-05)؛ [DL-04](registry/open-issues-registry.md#dl-04) |
| <a id="review-q08"></a>Q08: رکوردهای متعارض | `Requirement`: واقعیت‌های منبع حفظ و مسائل داده گزارش شوند. `Proposed`: وضعیت تعارض و قرنطینه. `Open`: قاعدهٔ معتبر تقدم. هیچ قاعدهٔ last-row-wins ارائه نشده است. | [ADR-11](registry/decisions-registry.md#adr-11) | [002: زمان](002-data-architecture.md#data-3)، [دریافت](002-data-architecture.md#data-4) | [AT-05](registry/acceptance-register.md#at-05)؛ [DL-05](registry/open-issues-registry.md#dl-05) |
| <a id="review-q09"></a>Q09: دسترسی | `Requirement`: سلسله‌مراتب ارائه‌شده، کنترل ردیف برای هر کوئری و دادهٔ کار فردی فقط برای سرپرست مستقیم؛ S01 pp.5,10,13 و S05. `Proposed`: کاتالوگ سیاست. `Open`: شرط‌ها و ستون‌های منبع مشترک. | [ADR-06](registry/decisions-registry.md#adr-06) | [001: امنیت](001-system-blueprint.md#system-10)، [002: سازمان](002-data-architecture.md#data-9) | [AT-06](registry/acceptance-register.md#at-06)/[AT-07](registry/acceptance-register.md#at-07)/[AT-13](registry/acceptance-register.md#at-13)؛ [DL-06](registry/open-issues-registry.md#dl-06)؛ [AT-30](registry/acceptance-register.md#at-30) |
| <a id="review-q10"></a>Q10: ظرفیت و دادهٔ شخصی | `Requirement`: ظرفیت تجمیعی تیم و ممنوعیت پایش حضور فردی؛ S01 pp.6,9,12-13. `Proposed`: معیار تعداد افراد. `Open`: فرمول، قرارداد ساعت‌ها، استنتاج گروه کوچک و حذف متن حساس. | [ADR-06](registry/decisions-registry.md#adr-06) | [001: تحلیل](001-system-blueprint.md#system-8)، [002: سازمان](002-data-architecture.md#data-9) | [AT-06](registry/acceptance-register.md#at-06)/[AT-10](registry/acceptance-register.md#at-10)؛ [DL-07](registry/open-issues-registry.md#dl-07) |
| <a id="review-q11"></a>Q11: سه Workflow | `Requirement`: بازسازی رویداد واقعی، SLA مرحله و مالکیت Workflow ارائه‌شدهٔ M01؛ S01 pp.5-6,16 و S11. `Proposed`: کاتالوگ مرحله. `Open`: مالکان مرحله و مسیریابی. | [ADR-15](registry/decisions-registry.md#adr-15)، [ADR-07](registry/decisions-registry.md#adr-07) | [001: Workflowها](001-system-blueprint.md#system-7)، [002: موجودیت‌ها](002-data-architecture.md#data-2) | [AT-12](registry/acceptance-register.md#at-12)، [AT-08](registry/acceptance-register.md#at-08)؛ [DL-08](registry/open-issues-registry.md#dl-08)؛ [AT-25](registry/acceptance-register.md#at-25) |
| <a id="review-q12"></a>Q12: سیگنال‌ها و escalation | `Requirement`: تشخیص قطعی و R1-R8؛ S01 pp.6-8,13 و S11. `Proposed`: عبور سخت‌گیرانه و وضعیت‌های ناشناختهٔ نام‌گذاری‌شده. `Open`: برابری، baseline، مخرج صفر، تعداد روز هشدار و reset. | [ADR-07](registry/decisions-registry.md#adr-07) | [001: سیگنال‌ها](001-system-blueprint.md#system-7)، [002: کیفیت](002-data-architecture.md#data-5) | [AT-08](registry/acceptance-register.md#at-08)، [AT-09](registry/acceptance-register.md#at-09)؛ [DL-09](registry/open-issues-registry.md#dl-09)؛ [AT-24](registry/acceptance-register.md#at-24) |
| <a id="review-q13"></a>Q13: سازمان و زمان دریافت | `Requirement`: زمان تهران، cutoff، اثر ورودی بر گزارش بعدی و ساختار پویا؛ S01 p.14، S02/S05/S07. `Open`: صبح M11 در 75/76، دامنهٔ تاریخی، دریافت همان روز و known-at تقویم. صبح 76 در S16 در وضعیت `Proposed` است. | [ADR-08](registry/decisions-registry.md#adr-08)، [ADR-16](registry/decisions-registry.md#adr-16) | [001: replay](001-system-blueprint.md#system-5)، [002: زمان](002-data-architecture.md#data-3)، [سازمان](002-data-architecture.md#data-9) | [AT-03](registry/acceptance-register.md#at-03)/[AT-07](registry/acceptance-register.md#at-07)/[AT-15](registry/acceptance-register.md#at-15)/[AT-22](registry/acceptance-register.md#at-22)؛ [DL-10](registry/open-issues-registry.md#dl-10)؛ [AT-29](registry/acceptance-register.md#at-29) |
| <a id="review-q14"></a>Q14: گزارش‌های نقش و تحلیل مشترک | `Requirement`: یک Insight Brief به‌عنوان منبع گزارش و دسترسی ویژهٔ نقش؛ S01 pp.9-10. `Open`: schema داخلی و نگاشت suppressed/ongoing. شواهد مشترک هیچ‌گاه مجوز جدید نیست. | [ADR-09](registry/decisions-registry.md#adr-09)، [ADR-06](registry/decisions-registry.md#adr-06) | [001: تحلیل](001-system-blueprint.md#system-8)، [خروجی](001-system-blueprint.md#system-9)، [002: نسخه‌های گزارش](002-data-architecture.md#data-8) | [AT-06](registry/acceptance-register.md#at-06)/[AT-10](registry/acceptance-register.md#at-10)/[AT-11](registry/acceptance-register.md#at-11)؛ [DL-11](registry/open-issues-registry.md#dl-11)؛ [AT-26](registry/acceptance-register.md#at-26)، [AT-30](registry/acceptance-register.md#at-30) |
| <a id="review-q15"></a>Q15: تصمیم‌ها و اقدام | `Requirement`: تصمیم انسانی، فقط پیش‌نویس و بدون اجرای خودکار؛ S01 pp.11-12 و S02. `Proposed`: وضعیت‌های جداگانهٔ تصمیم، پیش‌نویس و تأیید اجرا. `Open`: ردیابی اجرای واقعی در MVP. | [ADR-17](registry/decisions-registry.md#adr-17) | [001: ماژول‌ها](001-system-blueprint.md#system-4)، [تحلیل](001-system-blueprint.md#system-8)، [002: تاریخچهٔ گزارش](002-data-architecture.md#data-8) | [AT-14](registry/acceptance-register.md#at-14)؛ [DL-12](registry/open-issues-registry.md#dl-12)؛ [AT-29](registry/acceptance-register.md#at-29) |
| <a id="review-q16"></a>Q16: خرابی LLM | `Accepted`: انتشار مستقل گزارش معتبر و رکوردهای گزارش ناموفق؛ جدول نتیجهٔ Q16 در S16 و S17. `Requirement`: هر مدیر فعال همچنان به گزارش معتبر نیاز دارد. `Proposed`: fallback مبتنی بر template. `Open`: retry، timeout، صدور وضعیت و قواعد جایگزینی. | [ADR-14](registry/decisions-registry.md#adr-14)، [ADR-10](registry/decisions-registry.md#adr-10) | [001: replay](001-system-blueprint.md#system-5)، [خروجی](001-system-blueprint.md#system-9)، [002: عملیات](002-data-architecture.md#data-11) | [AT-21](registry/acceptance-register.md#at-21)، [AT-11](registry/acceptance-register.md#at-11)/[AT-15](registry/acceptance-register.md#at-15)/[AT-18](registry/acceptance-register.md#at-18)؛ [DL-13](registry/open-issues-registry.md#dl-13)؛ [AT-28](registry/acceptance-register.md#at-28) |
| <a id="review-q17"></a>Q17: مدل‌ها و محدودیت‌ها | `Requirement`: USD 5 برای کل روز، 15 minutes و مهلت گزارش؛ S01 pp.14,16,19. `Proposed`: gateway مستقل از provider، رزروها، محدودیت‌های tool/token، tracing و سهم QA. `Open`: مدل، provider، محصولات، قیمت‌ها و محدودیت‌های دقیق. | [ADR-10](registry/decisions-registry.md#adr-10)، [ADR-13](registry/decisions-registry.md#adr-13) | [001: تحلیل](001-system-blueprint.md#system-8)، [003: اندازه‌گیری](003-roadmap.md#roadmap-measurement) | [AT-17](registry/acceptance-register.md#at-17)، [AT-18](registry/acceptance-register.md#at-18)، [AT-20](registry/acceptance-register.md#at-20)؛ [DL-14](registry/open-issues-registry.md#dl-14)/[DL-16](registry/open-issues-registry.md#dl-16)؛ [AT-28](registry/acceptance-register.md#at-28) |

## تعارض‌های مهم و تعیین تکلیف

[Decision Log](registry/open-issues-registry.md#decision-log) گزینه‌ها، اثرها، مالکان و دروازه‌ها را نگه می‌دارد. این بازبینی هیچ ردیف `Open` را بدون ثبت صریح نمی‌بندد.

| تعارض | تعیین تکلیف |
|---|---|
| پیشنهاد قدیمی دو موتور در برابر تصمیم ثبت‌شدهٔ فقط PostgreSQL | تصمیم صریح Q03 در S16 که S17 آن را تأیید می‌کند، تعارض را حل می‌کند. مسیرهای محصول و تعاملی به‌روزرسانی شوند. SQL اصلی و oracle آزمون مجزا حفظ شوند. اثبات عددی در وضعیت `Open` می‌ماند. |
| عنوان کلی Proposed/Open در برابر تصمیم‌های ثبت‌شدهٔ تیم | وضعیت‌های سطح گزاره تعارض را حل می‌کنند. [ADR-13](registry/decisions-registry.md#adr-13) و [ADR-14](registry/decisions-registry.md#adr-14) اضافه شوند. جزئیات طراحی تأییدنشده در وضعیت `Proposed` حفظ شوند. |
| عبارت atomic روزانه در برابر انتشار مستقل | `Accepted`: نتیجه‌های مدیران مستقل هستند. `Proposed`: متن/JSON یک مدیر در مرز package با هم commit شوند. پوشش الزامی ناقص نمی‌تواند روز را موفق کند. retry و fallback در وضعیت `Open` می‌مانند. |
| مقدار قبلی Q06 در برابر قرارداد null فعلی | نمایش تاریخی همراه با تاریخ واقعی حفظ شود. آن مقدار هرگز دوباره به‌عنوان مقدار فعلی استفاده نشود. نگاشت دقیق wire، واجدشرایط‌بودن و سن در [DL-03](registry/open-issues-registry.md#dl-03) باقی می‌مانند. |
| صبح موقت 76 در Q13 در برابر فرادادهٔ ایستای متعارض | هر دو سناریو حفظ شوند. نه پیشنهاد Codex و نه تعداد محاسبه‌شدهٔ گزارش، تقدم را تأیید نمی‌کند. [DL-10](registry/open-issues-registry.md#dl-10) در وضعیت `Open` می‌ماند. |
| نمونه‌های عمومی دقت در برابر SQL ویژهٔ KPI | از تعریف و گردکردن canonical استفاده شود. کوئری‌های ad hoc ثبت‌شده مجاز هستند. نمایش wire عدد افزوده‌شده در وضعیت `Open` می‌ماند. |
| suppressed در شرح در برابر ongoing در schema | هر دو منبع و تاریخچهٔ suppression حفظ شوند. schema مجموعه‌داده تغییر نکند و نگاشت جعل نشود. [DL-11](registry/open-issues-registry.md#dl-11) در وضعیت `Open` می‌ماند. |
| Insight مشترک در برابر دسترسی گیرنده | منبع تحلیلی با projectionهای مجاز دوباره استفاده شود. شواهد محدود و ادعاهای مشتق‌شده از آن نباید از prompt یا cache مشترک نشت کنند. schema داخلی در وضعیت `Open` می‌ماند. |

## تصمیم‌های لازم پیش از پیاده‌سازی

این ممیزی کاستی‌های مستندی را اصلاح می‌کند که با مقایسهٔ منبع پیدا شدند. [دامنه و روش گزارش ممیزی](audit-2026-11-09/audit-report.md#scope-and-method) و [دفتر بازبینی واحدها](audit-2026-11-09/document-review-ledger.csv) شواهد و محدودیت‌های آن را بیان می‌کنند. تصمیم‌های `Open` و دروازه‌های اجرا‌نشدهٔ محصول همچنان قابل مشاهده هستند. پیاده‌سازی محصول خارج از این کار است. تیم باید پیش از شروع کار متأثر، این انتخاب‌های طراحی P0 را حل کند یا سیاست‌های موقت نام‌گذاری‌شده را صریح تأیید کند:

1. Q03: قرارداد translation/type و برنامهٔ هم‌ارزی همهٔ 55 مورد. اثبات، دروازهٔ پذیرش پیاده‌سازی است و اکنون نتیجه‌ای در دسترس نیست.
2. Q05/Q06/Q08: حالت ورودی محاسبه، انتشار دادهٔ نامعتبر، نگاشت مقدار قبلی تاریخ‌دار و مدیریت تعارض. در بخش‌هایی که قرارداد منبع ناقص است، پاسخ برگزارکننده لازم است.
3. Q04/Q09/Q10: مجوزهای ردیف/ستون منبع مشترک، قواعد حریم خصوصی، تعریف ظرفیت و محدودیت‌های کوئری سفارشی.
4. Q11/Q12/Q13: مالکان مرحله، قواعد مرزی سیگنال و تقدم زمانی تغییرهای سازمان و پیوست‌ها.
5. Q14/Q16/Q17: قرارداد وضعیت خروجی، نمایش Insight مشترک، سیاست خرابی/وضعیت و اجرای مدل با حدود مشخص.

جزئیات نگهداری و تأیید اجرا در [DL-12](registry/open-issues-registry.md#dl-12)/[DL-15](registry/open-issues-registry.md#dl-15) باقی می‌مانند. سخت‌افزار نهایی، برچسب‌های پنهان و محدودیت‌های برگزارکننده، پذیرش نهایی را مسدود می‌کنند، نه مستندسازی مستقل یا کار مجاز حفظ منبع را. مرزهای معماری با وضعیت `Accepted` نیاز به انتخاب دوباره ندارند.

## خروجی‌های ممیزی فعلی و تغییرهای فایل

- [یافته‌های گزارش تفصیلی ممیزی](audit-2026-11-09/audit-report.md#findings-and-the-retained-source-observation): شناسهٔ مسئله، محل دقیق پیش از ویرایش، ادعای اصلی، شاهد، شدت، وضعیت اصلاح و عدم‌قطعیت باقی‌مانده.
- [ماتریس ردیابی نیازمندی](audit-2026-11-09/requirements-traceability.csv): منبع -> نیازمندی ریزدانه -> جزء موجود -> قرارداد/قاعده -> ADR -> دروازهٔ پذیرش برنامه‌ریزی‌شده.
- [قراردادهای KPI](audit-2026-11-09/kpi-contracts.csv)، [قراردادهای Workflow](audit-2026-11-09/workflow-contracts.csv) و [قراردادهای ورودی مدیر](audit-2026-11-09/manager-input-contracts.csv): معناهای تفصیلی منبع.
- [بازبینی نیازمندی نسبت به مدل در گزارش شکاف Structurizr](audit-2026-11-09/structurizr-gap-report.md#requirement-to-model-review): عناصر واقعی، رابطه‌ها، کلیدهای view و تغییرهای پیشنهادی بعدی. DSL بدون تغییر است.
- [بررسی‌ها و محدودیت‌های گزارش تغییر](audit-2026-11-09/change-report.md#checks-and-limits): تغییرهای هر فایل، بررسی‌ها، محدودیت‌های دامنه و مانع‌های باقی‌مانده.
- [diff یکپارچهٔ فعلی](audit-2026-11-09/reconciliation.diff)، [نسخهٔ پشتیبان پیش از ویرایش](audit-2026-11-09/pre-edit.zip) و [manifest مبنا](audit-2026-11-09/pre-edit-manifest.json).

فایل `reconciliation.diff` در ریشه متعلق به تطبیق قبلی است و بدون تغییر نگهداری می‌شود. برای این کار از diff ممیزی فعلی در بالا استفاده کنید. رکورد منبع `sources/Adr.md` بدون تغییر است. هیچ شرح اصلی، مجموعه‌داده، SQL، قرارداد منبع، گزارش بازبینی یا فایل Structurizr ویرایش نشد.

<a id="verification"></a>

## سابقهٔ راستی‌آزمایی

تطبیق قبلی از بررسی‌های پیوند/تعداد استفاده کرد. آن نتایج تاریخی هستند و صحت معنایی مبنای فعلی را اثبات نمی‌کنند. این ممیزی معنای منبع، رفتار قاعده، همهٔ فراداده‌های canonical، مراحل Workflow، ورودی‌های مدیر، قراردادهای JSON و مدل هدف موجود را مقایسه می‌کند. [نتیجهٔ راستی‌آزمایی فعلی](audit-2026-11-09/verification.json) فقط بررسی‌های اجراشدهٔ سند/منبع را گزارش می‌کند.

همهٔ دروازه‌های AT در حالت برنامه‌ریزی‌شده باقی می‌مانند. هیچ آزمون KPI SQL، هم‌ارزی PostgreSQL، امنیت محصول، replay، مدل، کارایی، restore یا هزینه اجرا نشد. هیچ dependency نصب نشد. هیچ renderer نمودار معماری اجرا نشد. کلیدهای view موجود Structurizr در متن DSL بررسی شدند؛ هیچ view جعل یا render نشد.

Git در این workspace در دسترس نیست. ممیزی از ZIP راستی‌آزمایی‌شدهٔ پیش از ویرایش و manifest hash منبع/فایل استفاده می‌کند. هیچ commit یا push انجام نشد. تصمیم‌های `Open`، به‌جای پاسخ‌های جعلی، در [Decision Log](registry/open-issues-registry.md#decision-log) باقی می‌مانند.


## متن تاریخی راستی‌آزمایی نگه‌داری‌شده از سند 003 پیشین

The following is historical source evidence from the former combined document. Statements about Git refer to that review context. They do not describe the current repository. Only navigation destinations are updated. No audit conclusion is rewritten.

<a id="decisions-9"></a>

## 9. تحویل مستندات و راستی‌آزمایی

چهار سند شماره‌دار معماری مشمول ممیزی فعلی مبتنی بر منبع هستند. پیش از کامل‌دانستن پوشش مستندات، یافته‌های تفصیلی و شواهد ردیابی خوانده شوند. سند 004 شامل نگاشت Q01-Q17، بررسی‌های منبع، تغییر فایل‌ها و حدود راستی‌آزمایی است. Decision Log زیر انتخاب‌های حل‌نشده را حفظ می‌کند. هیچ کد محصول، تبدیل SQL، اجرای KPI، آزمون امنیت، آزمون کارایی یا نتیجه پذیرش ادعا نمی‌شود.

این Workspace مخزن Git ندارد. [نسخه پشتیبان بازتولیدپذیر پیش از ویرایش](audit-2026-11-09/pre-edit.zip) و [Manifest مبنا](audit-2026-11-09/pre-edit-manifest.json)، پشتوانه [Diff یکپارچه فعلی](audit-2026-11-09/reconciliation.diff) هستند. فایل reconciliation.diff در ریشه، سابقه تاریخی است. در این کار Commit یا Push انجام نمی‌شود.
