# تصمیم‌های معماری To-Be دیدراه

وضعیت سند: **Draft - Ready for Team Review**  
تاریخ بازبینی: ۱۴۰۵/۰۸/۱۹ (2026-11-10)  
مرجع نیازمندی: `Docs/دیدراه-بریف-دستیار-ایجنتیک-مدیران.md`  

این فایل مرجع واحد تصمیم‌های معماری To-Be است. `Accepted` یعنی تصمیم صریح تیم یا الزام قطعی منبع. `Open` یعنی پاسخ نهایی هنوز ثبت نشده است. پیشنهاد فنی در یک تصمیم Open، به‌تنهایی تصمیم تیم نیست.

در فیلد Source، شناسه `DL-xx` به بخش هم‌نام در `Docs/architecture/registry/open-issues-registry.md` و شناسه `ADR-xx` به بخش هم‌نام در `Docs/architecture/registry/decisions-registry.md` ارجاع می‌دهد. ارجاع «بریف خطوط» به شماره خط نسخه فعلی فایل مرجع Markdown مربوط است.

## ۱. تصمیم‌های Accepted

### ADR-01 - موتور پایگاه داده محصول

- **Question:** موتور پایگاه داده محصول چیست؟
- **Status:** Accepted
- **Decision:** PostgreSQL تنها موتور پایگاه داده محصول است. همه ۵۵ KPI مرجع و Queryهای تعاملی باید در مسیر محصول روی PostgreSQL اجرا شوند. SQL و نتیجه مرجع Dataset باید برای آزمون هم‌ارزی حفظ شوند.
- **Impact:** مسیر محاسبه و Query یک موتور دارد. SQLite فقط می‌تواند Oracle آزمون خارج از محصول باشد.
- **Priority:** Critical
- **Source:** تصمیم تیم در `Docs/architecture/sources/Adr.md`، Q03 و جدول خلاصه خطوط 208-224؛ قرارداد Dataset در `DataSet/arka_dataset/README_FA.md`، بخش «شاخص‌ها»؛ بریف خطوط 378-387 و 487-491.

### ADR-13-S01 - یک Agent محدود

- **Question:** سیستم چند AI Agent دارد؟
- **Status:** Accepted
- **Decision:** سیستم یک AI Agent محدود دارد. ماژول‌های قطعی می‌توانند مستقل باشند، اما Agent مستقل دیگری ایجاد نمی‌شود.
- **Impact:** معماری از Multi-Agent، delegation و هماهنگی غیرضروری پرهیز می‌کند.
- **Priority:** Critical
- **Source:** تصمیم تیم در `Docs/architecture/sources/Adr.md`، Q01؛ تصمیم ثبت‌شده در `Docs/architecture/registry/decisions-registry.md`، ADR-13-S01.

### ADR-13-S02 - مرز منطق قطعی

- **Question:** کدام تصمیم‌ها نباید به LLM واگذار شوند؟
- **Status:** Accepted
- **Decision:** محاسبه KPI، تشخیص Signal، Authorization و Validation نهایی قطعی هستند. LLM فقط از Evidence مجاز برای تحلیل و نگارش استفاده می‌کند.
- **Impact:** عدد، مجوز، Signal و پذیرش خروجی از نتیجه احتمالی مدل مستقل می‌مانند.
- **Priority:** Critical
- **Source:** تصمیم تیم در `Docs/architecture/sources/Adr.md`، Q01، Q04 و Q12؛ بریف خطوط 183-188، 312-318 و 378-387.

### ADR-14 - انتشار مستقل گزارش معتبر

- **Question:** شکست گزارش یک مدیر چه اثری بر گزارش مدیران دیگر دارد؟
- **Status:** Accepted
- **Decision:** هر گزارش معتبر مدیر مستقل منتشر می‌شود. شکست یک گزارش مانع انتشار گزارش معتبر مدیر دیگر نیست. شکست و پوشش ناقص روز باید ثبت شود.
- **Impact:** واحد انتشار، بسته متن و JSON یک مدیر است. وضعیت کل روز جدا ثبت می‌شود.
- **Priority:** Critical
- **Source:** تصمیم تیم در `Docs/architecture/sources/Adr.md`، Q16؛ تصمیم ثبت‌شده در `Docs/architecture/registry/decisions-registry.md`، ADR-14-S01.

### ADR-17 - کنترل انسانی تصمیم و اقدام

- **Question:** آیا سیستم می‌تواند اقدام سازمانی را اجرا کند؟
- **Status:** Accepted
- **Decision:** مدیر تصمیم می‌گیرد. سیستم فقط گزینه، پیش‌نویس وظیفه یا پیام و پیگیری اثر را تولید می‌کند. سیستم نیرو جابه‌جا نمی‌کند، هدف را خودکار تغییر نمی‌دهد و پیام را خودکار ارسال نمی‌کند.
- **Impact:** همه اقدام‌های سازمانی به Actor انسانی و تأیید قابل ردیابی نیاز دارند.
- **Priority:** Critical
- **Source:** بریف خطوط 339-366؛ قرارداد Dataset در `DataSet/arka_dataset/README_FA.md`، بخش «ورودی‌های مدیران»؛ تصمیم تیم در `Docs/architecture/sources/Adr.md`، Q15.

### ADR-18 - LangGraph برای Orchestration Agent

- **Question:** هماهنگی جریان Agent با چه Framework انجام می‌شود؟
- **Status:** Accepted
- **Decision:** LangGraph برای Orchestration جریان‌های مربوط به Agent استفاده می‌شود. LangGraph مرجع محاسبه، Signal، مجوز یا Validation نهایی نیست.
- **Impact:** State، Checkpoint، Retry و Human-in-the-Loop جریان Agent در LangGraph طراحی می‌شوند. منطق قطعی در ماژول‌های مستقل باقی می‌ماند.
- **Priority:** Critical
- **Source:** دستور صریح تیم در درخواست «DIDRAH - Execute To-Be Architecture Finalization»، بخش تصمیم‌های تأییدشده. این تصمیم از بریف استخراج نشده است.

## ۲. تصمیم‌های Open ضروری برای تأیید معماری

پاسخ این تصمیم‌ها باید در جلسه تیم ثبت شود. معماری فعلی مرز امن پیشنهادی را نشان می‌دهد، اما پیشنهاد، Accepted نیست.

### DL-02 - سیاست RAW یا DEDUP برای محاسبه

- **Question:** رخدادهای تکراری Payload در ورودی KPI به‌صورت RAW محاسبه شوند یا با exact-payload DEDUP؟
- **Status:** Open
- **Options:** ۱) RAW مطابق همه رخدادهای پذیرفته‌شده؛ ۲) exact-payload DEDUP؛ ۳) سیاست رسمی جدا برای هر Source.
- **Recommendation:** تا پاسخ رسمی، هر دو نتیجه با `input_policy_id` جدا قابل محاسبه باشند و هیچ‌کدام «مقدار پذیرفته‌شده» نامیده نشود. Idempotency دریافت از DEDUP کسب‌وکار جدا بماند.
- **Impact:** نتیجه ۸ KPI و پذیرش «صفر عدد نادرست» تغییر می‌کند.
- **Priority:** P0 - تصمیم منبع؛ فقط پذیرش عدد و خروجی متأثر را مسدود می‌کند.
- **Source:** `Docs/architecture/registry/open-issues-registry.md`، DL-02؛ شواهد S09؛ بریف خطوط 406-420 و 493-507.

### DL-03 - انتشار هنگام داده ناقص

- **Question:** چه زمانی Source بسته تلقی می‌شود و مقدار KPI ناقص چه زمانی قابل انتشار است؟
- **Status:** Open
- **Options:** ۱) مقدار جاری `null` و Data Issue؛ ۲) انتشار Snapshot ناقص با برچسب؛ ۳) انتشار فقط پس از closure رسمی Source.
- **Recommendation:** مقدار جاری نامعتبر `null` بماند. آخرین مقدار معتبر فقط با تاریخ واقعی نمایش داده شود. Eligibility و حداکثر سن مقدار قبلی باید از برگزارکننده دریافت شود.
- **Impact:** محتوای گزارش، Signal eligibility و ادعای سلامت حوزه را محدود می‌کند.
- **Priority:** P0 - پاسخ منبع؛ معماری را متوقف نمی‌کند، اما انتشار مقدار متأثر را متوقف می‌کند.
- **Source:** DL-03؛ بریف خطوط 382-387، 416-420، 499-507؛ تصمیم نسبی Q06 در `Docs/architecture/sources/Adr.md`.

### DL-06 - Projection دسترسی منابع مشترک

- **Question:** ردیف، ستون و Purpose مجاز هر نقش برای Sourceهای مشترک چیست؟
- **Status:** Open
- **Options:** ۱) Policy catalog صریح برای هر Source؛ ۲) رد دسترسی تعریف‌نشده؛ ۳) Viewهای جدا برای هر Scope.
- **Recommendation:** Policy catalog نسخه‌دار با deny-by-default، RLS، allowlist ستون و حذف متن حساس. Query تعاملی و Evidence retrieval باید همان Policy را اجرا کنند.
- **Impact:** مرز Query Gateway، Evidence و امکان اثبات «صفر نشت» را تعیین می‌کند.
- **Priority:** P0 - تصمیم تیم امنیت و داده.
- **Source:** DL-06؛ `DataSet/arka_dataset/org/access_matrix.csv`؛ بریف خطوط 120-149، 378-387 و 493-505.

### DL-07 - تعریف ظرفیت و حریم خصوصی

- **Question:** ظرفیت تجمیعی تیم چگونه محاسبه و چگونه در گروه کوچک محافظت شود؟
- **Status:** Open
- **Options:** ۱) نسبت افراد در دسترس؛ ۲) نسبت ساعت با قرارداد ساعت کاری؛ ۳) فقط مقدار عرضه‌شده بدون استنتاج.
- **Recommendation:** در MVP از ظرفیت تجمیعی عرضه‌شده استفاده شود. ساعت یا حضور فردی ساخته نشود. برای مدیران بالاتر، گروه کوچک و متن آزاد Redact شود.
- **Impact:** Evidence تحلیل، نمایش بار کاری و کنترل داده فردی را تعیین می‌کند.
- **Priority:** P0 - انتخاب تیم؛ پاسخ برگزارکننده فقط برای مدل ساعتی لازم است.
- **Source:** DL-07؛ بریف خطوط 183-188، 264-272، 378-387؛ Dataset `staff_availability.csv`.

### DL-09 - حالت‌های مرزی Signal و Episode

- **Question:** Equality، baseline ناکافی، مقدار صفر، روز نامعلوم و Reset چگونه ارزیابی شوند؟
- **Status:** Open
- **Options:** ۱) قواعد سخت‌گیرانه با Unknown؛ ۲) قواعد ساده با suppression؛ ۳) پاسخ رسمی برای هر Rule.
- **Recommendation:** Unknown هرگز Normal تلقی نشود. Equality و Reset در Rule version ثبت شوند. تا پاسخ منبع، نتیجه مرزی Signal قابل انتشار نباشد.
- **Impact:** Detection، recurrence، escalation و هدف کشف ۹۰٪ را تغییر می‌دهد.
- **Priority:** P0 - پاسخ منبع برای Ruleهای مبهم؛ معماری Engine را متوقف نمی‌کند.
- **Source:** DL-09؛ `DataSet/arka_dataset/config/escalation_rules.csv`؛ بریف خطوط 206-245 و 474-506.

### DL-11 - نگاشت `suppressed` و `ongoing`

- **Question:** وضعیت `suppressed` بریف چگونه با Enum رسمی `ongoing` در JSON نگاشت شود؟
- **Status:** Open
- **Options:** ۱) suppression فقط در Ledger داخلی و `open_items`؛ ۲) نگاشت رسمی به `ongoing`؛ ۳) اصلاح رسمی Schema.
- **Recommendation:** Schema تغییر نکند. suppression در Ledger داخلی ثبت شود و فقط با تأیید منبع به `ongoing` نگاشت شود.
- **Impact:** JSON، history و آزمون recurrence را تعیین می‌کند.
- **Priority:** P0 - پاسخ منبع؛ طراحی داخلی می‌تواند ادامه یابد.
- **Source:** DL-11؛ بریف خطوط 438-465؛ `DataSet/arka_dataset/output_contract/brief_schema.json`.

### DL-18 - مدل محتوای کامل گزارش

- **Question:** محتوای الزامی بریف که در Schema رسمی Field مشخص ندارد کجا نگهداری شود؟
- **Status:** Open
- **Options:** ۱) مدل محتوای داخلی و projection به Schema؛ ۲) استفاده از Fieldهای آزاد سازگار؛ ۳) درخواست Schema جدید.
- **Recommendation:** یک مدل داخلی کوچک برای Item، Evidence، ChartSpec و DecisionCard تعریف شود. Schema رسمی بدون تغییر بماند. فقط Fieldهای لازم بریف در مدل داخلی باشند.
- **Impact:** سازگاری متن و JSON، Validation و محتوای نقش‌ها را تعیین می‌کند.
- **Priority:** P0 - تصمیم تیم محصول.
- **Source:** DL-18؛ بریف خطوط 274-337 و 438-465؛ Schema رسمی Brief.

### DL-20 - مرز اجرایی LangGraph

- **Question:** کدام جریان‌ها و Stateها در LangGraph قرار گیرند؟
- **Status:** Open
- **Options:** ۱) فقط تحلیل و نگارش؛ ۲) کل Job گزارش با Nodeهای قطعی و Agent؛ ۳) Graphهای جدا برای Nightly و Interactive.
- **Recommendation:** دو Graph ساده در یک Agent runtime: Graph گزارش هر مدیر و Graph تعامل مدیر. Ingestion، KPI، Signal و Workflow قبل از Graph اجرا شوند. Graph فقط Evidence مجاز، تحلیل، Draft، Validation call، repair محدود و نتیجه انتشار را هماهنگ کند. State شامل ID و reference باشد، نه Raw data یا Credential. Checkpoint پایدار در PostgreSQL باشد. Nightly Graph هیچ Interrupt انسانی نداشته باشد.
- **Impact:** بازیابی، امنیت State، Retry و استقلال انتشار را تعیین می‌کند.
- **Priority:** P0 - تصمیم تیم معماری.
- **Source:** ADR-18؛ ADR-13-S01/S02؛ ADR-14؛ بریف خطوط 83-100، 247-318 و 322-366.

## ۳. تصمیم‌های Open قابل تعویق با Gate

### DL-01 - روش تبدیل و اثبات هم‌ارزی ۵۵ KPI

- **Question:** ترجمه SQL مرجع و اثبات هم‌ارزی چگونه انجام شود؟
- **Status:** Open
- **Options:** ترجمه دستی نسخه‌دار؛ Translation layer محدود؛ بازنویسی کنترل‌شده همراه Oracle.
- **Recommendation:** SQL PostgreSQL نسخه‌دار و Oracle مستقل SQLite. مقایسه کل Relation برای همه روزهای Replay.
- **Impact:** پذیرش عددی. مرز معماری PostgreSQL را تغییر نمی‌دهد.
- **Priority:** P1 - Gate پیاده‌سازی محاسبه.
- **Source:** DL-01؛ ADR-01؛ Dataset README بخش شاخص‌ها.

### DL-04 - Full rebuild یا Selective rebuild

- **Question:** اصلاح تاریخی با بازسازی کامل یا محاسبه انتخابی پردازش شود؟
- **Status:** Open
- **Options:** Full rebuild؛ Selective rebuild با dependency proof.
- **Recommendation:** Full rebuild مبنای صحت MVP باشد. Selective rebuild فقط پس از اثبات هم‌ارزی اضافه شود.
- **Impact:** کارایی و پیچیدگی، نه قرارداد خروجی.
- **Priority:** P1 - تصمیم پیاده‌سازی.
- **Source:** DL-04؛ بریف خطوط 406-420.

### DL-05 - تقدم اصلاح‌های هم‌رتبه

- **Question:** رکوردهای اصلاحی متعارض و هم‌رتبه چگونه حل شوند؟
- **Status:** Open
- **Options:** تقدم رسمی Source؛ quarantine؛ انتخاب آخرین رکورد.
- **Recommendation:** quarantine و Data Issue تا دریافت قاعده رسمی. انتخاب آخرین رکورد ممنوع است.
- **Impact:** فقط داده و KPI متأثر را مسدود می‌کند.
- **Priority:** P1 - پاسخ منبع.
- **Source:** DL-05؛ بریف خطوط 416-420 و 499-507.

### DL-08 - مالک Stage و مسیر تأخیر

- **Question:** مالک هر Workflow stage و مسیر ارجاع تأخیر چیست؟
- **Status:** Open
- **Options:** mapping رسمی stage-to-team؛ actor event؛ unresolved routing.
- **Recommendation:** مالک end-to-end از config حفظ شود. مالک Stage فقط از actor معتبر یا mapping تأییدشده تعیین شود.
- **Impact:** مالک Signal و نمایش گلوگاه.
- **Priority:** P1 - Gate Workflow attribution.
- **Source:** DL-08؛ `workflow_definitions.csv`؛ بریف خطوط 151-175.

### DL-10 - M11، Upload و known-at

- **Question:** M11 چه صبحی فعال است و ورودی هم‌روز چه زمانی قابل استفاده است؟
- **Status:** Open
- **Options:** شروع صبح ۷۵ یا ۷۶؛ receipt/readiness صریح برای Upload؛ تقدم ثبت‌شده ورودی‌ها.
- **Recommendation:** زمان دریافت و آماده‌شدن جدا ثبت شود. فقط ورودی آماده و مجاز در revision تعاملی استفاده شود. گزارش صبح immutable بماند.
- **Impact:** Coverage و QA چند روز خاص.
- **Priority:** P1 - پاسخ منبع.
- **Source:** DL-10؛ Dataset README بخش زمان و ورودی مدیر.

### DL-12 - تأیید اجرای واقعی اقدام

- **Question:** MVP فقط تصمیم و Draft را پیگیری کند یا اجرای واقعی تأییدشده را نیز ثبت کند؟
- **Status:** Open
- **Options:** تصمیم و Draft؛ ثبت تأیید انسانی اجرای واقعی.
- **Recommendation:** MVP تصمیم، Draft و Observation اثر را نگه دارد. اجرای واقعی فقط با Evidence انسانی جدا ثبت شود.
- **Impact:** مدل Decision history و ادعای اثر.
- **Priority:** P1 - تصمیم محصول.
- **Source:** DL-12؛ بریف خطوط 339-366.

### DL-13 - Retry، Timeout و Fallback

- **Question:** Failure policy برای LLM و تولید گزارش چیست؟
- **Status:** Open
- **Options:** Retry محدود و failure؛ template fallback معتبر؛ repair loop محدود.
- **Recommendation:** Retry فقط برای خطای موقت، یک repair محدود برای خروجی نامعتبر، سپس failure صریح. Fallback فقط در صورت عبور از تمام Validationها.
- **Impact:** هزینه، زمان و پوشش گزارش.
- **Priority:** P1 - عدد دقیق پس از Benchmark.
- **Source:** DL-13؛ ADR-14؛ بریف خطوط 312-318 و 474-481.

### DL-14 - مدل، Provider و بودجه داخلی

- **Question:** مدل، Provider، Gateway و سهم بودجه چگونه انتخاب شوند؟
- **Status:** Open
- **Options:** Provider مستقیم؛ Gateway مستقل؛ چند مدل پشت رابط واحد.
- **Recommendation:** رابط مستقل از Provider با Ledger هزینه. انتخاب مدل با آزمون کیفیت، زمان و هزینه انجام شود.
- **Impact:** هزینه و عملیات. مرز Agent را تغییر نمی‌دهد.
- **Priority:** P1 - Gate Benchmark.
- **Source:** DL-14؛ بریف خطوط 378-387 و 474-491.

### DL-15 - Retention، Backup و Restore

- **Question:** دوره نگهداری و روش Restore چیست؟
- **Status:** Open
- **Options:** حفظ کامل Replay؛ دوره عملیاتی محدود؛ archive بلندمدت.
- **Recommendation:** برای ارزیابی، همه Source، Snapshot metadata، Decision و Report version حفظ شوند. دوره بعدی پس از نیاز عملیاتی تعیین شود.
- **Impact:** ذخیره‌سازی و عملیات.
- **Priority:** P2 - قبل از استقرار واقعی.
- **Source:** DL-15؛ الزام Replay و تحویل در بریف خطوط 406-436 و 521-536.

### DL-16 - پروفایل نهایی ارزیابی

- **Question:** سخت‌افزار مرجع، Dataset پنهان و قراردادهای مفقود چیست؟
- **Status:** Open
- **Options:** فقط حدود فعلی بریف؛ دریافت پروفایل رسمی برگزارکننده.
- **Recommendation:** حدود بریف حفظ شود و پذیرش نهایی تا دریافت پروفایل رسمی ادعا نشود.
- **Impact:** نتیجه Benchmark و پذیرش نهایی.
- **Priority:** P2 - پاسخ برگزارکننده.
- **Source:** DL-16؛ بریف خطوط 422-436، 470-507 و 559.

### DL-17 - NULL، نبود Dimension و اعداد Ad hoc

- **Question:** NULL، بدون Dimension، رشته خالی و عدد Query موردی چگونه Serialize شوند؟
- **Status:** Open
- **Options:** mapping داخلی صریح؛ Sentinel؛ تغییر Schema.
- **Recommendation:** تمایز داخلی حفظ شود. Sentinel ساختگی و تغییر Schema ممنوع باشد. mapping Wire با Fixture تأیید شود.
- **Impact:** سازگاری JSON و مقایسه عدد.
- **Priority:** P1 - Gate خروجی موارد متأثر.
- **Source:** DL-17؛ Schema Brief؛ بریف خطوط 438-490.

### DL-19 - تغییر KPI و Rollback

- **Question:** چه کسی KPI جدید یا تغییر تنظیم را فعال می‌کند؟
- **Status:** Open
- **Options:** candidate نسخه‌دار با تأیید؛ فعال‌سازی مستقیم مدیر مجاز؛ فقط افزودن و بدون تغییر ۵۵ تعریف.
- **Recommendation:** ۵۵ تعریف مرجع immutable بمانند. KPI جدید یا Threshold جدید candidate نسخه‌دار با Validation، تأیید انسانی، زمان اثر و Rollback باشد.
- **Impact:** Configuration، Audit و Replay.
- **Priority:** P1 - Gate قابلیت مدیریت تنظیمات.
- **Source:** DL-19؛ Dataset README بخش شاخص‌ها و ورودی مدیر؛ بریف خطوط 106-116 و 378-387.

## ۴. نتیجه تصمیم‌ها

- تصمیم‌های Accepted: **۶**
- تصمیم‌های Open: **۲۰**
- Open ضروری برای جلسه معماری: **۸** (`DL-02`, `DL-03`, `DL-06`, `DL-07`, `DL-09`, `DL-11`, `DL-18`, `DL-20`؛ DL-02/03/09/11 پاسخ منبع می‌خواهند و می‌توانند با Gate محدود باقی بمانند.)
- وضعیت: **Ready for Team Review**؛ هیچ Open به‌صورت پنهان Accepted نشده است.
