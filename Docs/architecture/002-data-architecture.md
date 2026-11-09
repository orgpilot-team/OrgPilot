# ARCH-001: معماری داده، تاریخچه و محاسبه

مسئولیت مستندسازی در ARCH-DOC-004: مدل داده، دریافت، Snapshotها، محاسبات Canonical و Data Lineage در این سند باقی می‌مانند. برای رکوردهای حاکمیتی به [Registry](registry/README.md#current-document-responsibilities) و برای مراحل اجرا به [نقشه راه 003](003-roadmap.md#roadmap-phases) مراجعه کنید. این تغییر در مسیرهای راهبری، هیچ قرارداد یا وضعیتی را تغییر نمی‌دهد.

شناسه سند: `002-data-architecture`. خانواده مشترک معماری: `ARCH-001`.

تاریخ بازبینی: 2026-11-09. منطقه زمانی: `Asia/Tehran`. اجرای محصول فقط با PostgreSQL دارای وضعیت Accepted است. قراردادهای فیزیکی و سیاست‌های حل‌نشده همچنان Proposed یا Open هستند.

فهرست منابع `S01..S19` و درجهٔ اعتبار در [طرح سیستم](001-system-blueprint.md#system-2) آمده است. تعریف‌های زیر قرارداد طراحی هستند؛ هیچ جدول، adapter یا pipeline در این کار پیاده‌سازی نشده است.

از [قواعد وضعیت](001-system-blueprint.md#system-2)، [نگاشت Q01-Q17](004-reconciliation-review.md#question-map) و [Decision Log](registry/open-issues-registry.md#decision-log) استفاده کنید. این قراردادها طراحی هدف را توصیف می‌کنند؛ بیانگر جدول‌های نصب‌شده یا Pipelineهای اجراشده نیستند.

<a id="data-1"></a>

## ۱. اصل نگهداری و لایه‌های داده

فایل اصلی مرجع اثبات دریافت است. رویداد و payload اصلی حذف یا اصلاح نمی‌شوند. دادهٔ استاندارد، fact، KPI و گزارش، محصول نسخه‌دار این منابع‌اند. بازسازی هر خروجی باید با منابع و نسخه‌های همان زمان ممکن باشد.

| لایه | محتوای اصلی | اختیار تغییر |
|---|---|---|
| `source_archive` | bytes فایل، manifest، upload و hash | فقط افزودن؛ دسترسی مدیریتی مستقیم ندارد. |
| `ingestion` | batch، file receipt، source row، schema version، parse result | وضعیت job قابل تغییر است؛ سابقهٔ transition حفظ می‌شود. پذیرش payload با نسخهٔ جدید انجام می‌شود. |
| `history` | entity observations، events، correction links، org/config revisions | append-only؛ projection قدیمی حذف نمی‌شود. |
| `reference` | روابط ورودی و پنج view مرجع برای snapshot معین | مشتق و قابل بازسازی؛ دسترسی فقط calculator. |
| `semantic` | KPI observation، dependency، contributor set و QueryRun | نسخهٔ جدید درج می‌شود؛ مقدار گذشته overwrite نمی‌شود. |
| `management` | signal، Insight Brief، report، decision و action draft | رویداد تصمیم و نسخهٔ انتشار حفظ می‌شود. |
| `security_audit` | grant، AuthContext، query/access log و budget ledger | سرویس‌های مشخص می‌نویسند؛ دسترسی audit محدود است. |

این نام‌ها مرز منطقی‌اند. برای نسخهٔ اول، schemaها در یک PostgreSQL و فایل‌های حفاظت‌شده در یک volume کافی هستند. مجزا بودن منطقی به معنی نیاز به سرویس جدا نیست.

<a id="data-2"></a>

## ۲. مدل مفهومی

نماهای موجود Structurizr با نام‌های `DataIntake` و `Containers` در [Workspace](../../architecture/structurizr/workspace.dsl)، مرز مؤلفه‌ها و ذخیره‌سازی را نشان می‌دهند؛ این نماها ERD موجودیت‌ها نیستند. نبود نمودار تفصیلی موجودیت‌ها و روابط در [بازبینی نگاشت نیازمندی‌ها به مدل در گزارش شکاف‌های Structurizr](audit-2026-11-09/structurizr-gap-report.md#requirement-to-model-review) ثبت شده است. قراردادهای منطقی زیر همچنان پیشنهاد مدل داده هستند. دریافت انجام‌نشده می‌تواند بدون SourceFile دارای مسئله DQ باشد.

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

`Requirement`: خروجی QA باید شامل `question_id, manager_id, answer_status, answer_fa` باشد (`dataset/output_contract/qa_answer_schema.json`، بخش `required`). پنج وضعیت پاسخ و قواعد امتناع در [سند 001، بخش 9.1](001-system-blueprint.md#system-9) تعریف شده‌اند. `Open`: این مدل قرارداد صریحی برای ارتباط پرسش و پاسخ با مدیر احرازهویت‌شده، Scope مجاز، Snapshot یا نسخه تعاملی و نتایج واقعی QueryRun ندارد. S07 فیلدهای `input_id, day, date, manager_id, type, content_fa` را عرضه می‌کند، اما این ارتباط‌های داخلی را عرضه نمی‌کند. قرارداد داده باید این زمینه و فیلدهای الزامی پاسخ را حفظ کند. امتناع نباید Query یا نتیجه فرضی ایجاد کند. بسته‌شدن این مورد به نگاشت منطقی بازبینی‌شده و نمونه‌های پاسخ و امتناع نیاز دارد (بریف، صفحات 3,11,13,17). [ADR-06](registry/decisions-registry.md#adr-06) و [ADR-09](registry/decisions-registry.md#adr-09) دسترسی و خروجی را پوشش می‌دهند؛ قرارداد اختصاصی رکورد QA دارای ADR/DL نیست. این یافته به ثبت مرکزی در آینده نیاز دارد. در اینجا نام موجودیت یا کلید فیزیکی انتخاب نمی‌شود.

`Open`: قرارداد WorkflowStageObservation شواهد پرونده را پوشش می‌دهد، اما روش نگهداری جمعیت محاسبه، پرونده‌های مشمول و حذف‌شده، صورت و مخرج SLA، Query محاسبه یا نتیجه گلوگاه در خلاصه هر مرحله را مشخص نمی‌کند. خروجی‌های مرحله دارای وضعیت `Requirement` هستند (بریف، صفحات 5-6,16). به [سند 001، بخش 7.2](001-system-blueprint.md#system-7)، فیلدهای `from_event, to_event, sla_hours, stage_target_median_h` در `dataset/config/workflow_definitions.csv` و `reference_views.sql` مراجعه کنید. بسته‌شدن این مورد به نگاشت بازبینی‌شده خلاصه به پرونده و Query نیاز دارد؛ پرونده‌های باز و نامعلوم باید متمایز بمانند. Canonical KPI مربوط به Workflow را جایگزین معیار مرحله نکنید. [ADR-15](registry/decisions-registry.md#adr-15) و [DL-08](registry/open-issues-registry.md#dl-08) مسئولیت را پیگیری می‌کنند، اما این رکورد محاسبه را تعریف نمی‌کنند. این شکاف تکمیلی قرارداد به ثبت مرکزی در آینده نیاز دارد.

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

<a id="data-3"></a>

## ۳. زمان، snapshot و تاریخچه

چهار مفهوم زمان جدا هستند:

| زمان | معنا | نمونه |
|---|---|---|
| `event_time / valid_time` | رخداد یا اثر کسب‌وکار | زمان won یا تاریخ اثر اصلاح ارزش. |
| `delivered_drop / available_at_simulated` | نخستین delivery مجاز در replay | اصلاح drop 070، قابل استفاده از صبح ۷۱. |
| `ingested_at_utc / commit_seq` | دریافت و ثبت واقعی در اجرای نرم‌افزار | زمان اجرای امروز نباید جای روز شبیه‌سازی را بگیرد. |
| `config_effective_time / known_at` | زمان اثر و زمان اطلاع از تنظیم یا ساختار | تغییر warn در روز ۷۸ از گزارش ۷۹. |

`Requirement`: زمان‌های منبع به وقت تهران هستند (بریف، صفحه 14). متن خام Timestamp را بدون افزودن تاریخ رخداد جدید حفظ کنید. هر زمان استانداردشده باید تفسیر منبع و مقدار خام خود را حفظ کند. تبدیل SQL به PostgreSQL باید گروه‌بندی تاریخ و محاسبات مرجع را حفظ کند. تبدیل به UTC به‌تنهایی هم‌ارزی عددی را اثبات نمی‌کند.

شرط eligibility برای replay: `delivered_drop <= R-1` و `known_at_seq <= snapshot.commit_seq_max`. در اجرا، manifest و فایل مربوط باید committed باشند. سپس fact از همین ورودی ساخته می‌شود. فیلتر کردن تاریخ خروجی یک fact ساخته‌شده از کل ۹۰ روز، کافی نیست.

`business_date_max` تاریخ روز `R-1` است. تقویم می‌تواند ردیف‌های آینده داشته باشد، اما مقدار صفر تولیدشده برای آینده منتشر نمی‌شود. تاریخچهٔ اولیهٔ CRM قبل از روز ۱ معتبر است؛ `K_ENT_FC_SLA` در ممیزی ۴۰ تاریخ قبل از تقویم دارد. این خروجی‌ها نباید با شرط «همهٔ تاریخ‌ها باید در cal باشند» حذف شوند.

برای بازسازی دو پرسش متفاوت وجود دارد:

- `as_reported(R)`: مدیر در صبح R چه داده و گزارشی دریافت کرد؟ ورودی، policy و report version همان صبح استفاده می‌شود.
- `restated(business_date, knowledge_cutoff)`: با دانسته‌های بعدی، مقدار آن تاریخ چه می‌شود؟ cutoff جدید و mode مشخص لازم است.

بازسازی با فرمول یا policy جدید، `recomputed_under_new_policy` است؛ نباید به نام گزارش واقعی گذشته عرضه شود. مجوز مشاهدهٔ تاریخچه نیز با دسترسی فعلی کاربر و entitlement نسخهٔ تاریخی بررسی می‌شود؛ داشتن مجوز قدیمی برای کاربر لغوشده کافی نیست.

### 3.1. مشاهده: Fixture اصلاح تاریخی

شناسه Lead و مبالغ زیر مشاهده‌های منبع هستند. قرارداد، همان Cutoff عمومی و معنای جایگزینی است. این Lead، Drop یا تاریخ را هرگز به‌عنوان قاعده زمان اجرا در کد ثابت نکنید.

طبق S04 و S08، ارزش `L02045` در won روز ۰۶۴ برابر ۲۷٬۳۰۰٬۰۰۰ تومان است. مقدار اصلاح در drop 070 برابر ۱۵٬۰۰۰٬۰۰۰ تومان است. `value_corrected` مقدار جایگزین است؛ اختلاف، رویداد درآمد جدید محسوب نمی‌شود.

| cutoff | نمایش مجاز |
|---|---|
| صبح ۶۵ تا ۷۰ | فقط مقدار اولیهٔ شناخته‌شده؛ اصلاح هنوز نرسیده است. |
| صبح ۷۱ به بعد | مقدار اصلاح‌شده با انتساب به `date(won_at)=2026-09-24`. |
| بازکردن گزارش واقعی صبح ۷۰ در آینده | نسخهٔ قدیمی با همان مقدار و شواهد باقی می‌ماند. |

مقادیر MTD از تاریخ won تا پایان همان ماه و تا افق محاسبه متأثر می‌شوند. `ORDER BY drop_day DESC` در reference حفظ می‌شود. اگر چند اصلاح متعارض برای یک lead در یک drop برسد، SQL ترتیب ثانویهٔ مصوب ندارد. تعارض ثبت و مقدار مربوط نگه داشته می‌شود؛ ترتیب فایل، timestamp مساوی یا بزرگ‌ترین مبلغ قاعدهٔ انتخاب نیست.

<a id="data-4"></a>

## ۴. دریافت manifest-aware و نگاشت schema

برای هر drop سه مقایسه لازم است:

۱. `ExpectedDelivery` از SourceContract در برابر manifest؛ این کنترل منبع حذف‌شده از manifest را نیز پیدا می‌کند.

۲. manifest در برابر فایل‌های واقعی، header و row count؛ نبود فایل، فایل اضافه و اختلاف تعداد ثبت می‌شود.

۳. schema و محتوای فایل در برابر قرارداد معتبر؛ parse failure، datatype نامعتبر، key conflict و رابطهٔ حل‌نشده مستقل ثبت می‌شوند.

قرارداد پایه از خانواده‌های مستند S02 ساخته می‌شود. روز ۰۰۰ فقط CRM دارد. «فایل‌های روز اول» به‌تنهایی قرارداد همیشگی نیستند؛ source registry تاریخ شروع/پایان و الگوی دریافت دارد. نسخهٔ مخفی با ساختار یکسان از همان registry استفاده می‌کند، نه فهرست روزهای حادثه.

برای جریان دریافت، کیفیت و Snapshot از نماهای Structurizr با نام‌های `DataIntake` و `NightlyData` استفاده کنید. نگاشت ردیف منبع و جزئیات وضعیت رسید، نماهای مستقل موجود نیستند؛ آن‌ها را به‌صورت قرارداد حفظ و نبود نمودار را ثبت کنید.

تعهد اتمی در سطح فایل/منبع انجام می‌شود. یک فایل نیمه‌نوشته وارد snapshot نمی‌شود. receipt روز می‌تواند `partial` باشد و سایر منابع committed را گزارش کند. parser باید row count را با CSV parser بشمارد؛ شمار خط متن برای CSV دارای newline داخل quoted field درست نیست.

### ۴.۱. idempotency با duplicate detection فرق دارد

| حالت | اقدام |
|---|---|
| retry همان dataset/drop/source/file hash | receipt قبلی بازگردد؛ occurrence جدید و KPI جدید ساخته نشود. |
| همان مسیر و drop با hash متفاوت | delivery revision جدید و رابطه با نسخهٔ پیشین؛ فایل قدیمی حفظ شود. جایگزینی خودکار بدون قرارداد revision مجاز نیست. |
| payload یکسان در دو ردیف یا دو delivery مستقل | هر occurrence خام حفظ و duplicate candidate ثبت شود؛ سیاست ورودی تصمیم می‌گیرد. |
| business_id یکسان با payload متفاوت | conflict یا entity revision؛ با exact duplicate یکی نیست. |
| entity_id یکسان با چند event | تاریخچهٔ معتبر احتمالی؛ eventها با حذف تکرار entity حذف نمی‌شوند. |

`RAW` همهٔ occurrenceهای پذیرفته‌شدهٔ orders را به reference می‌دهد. `EXACT_PAYLOAD_DEDUP` فقط payloadهای دقیقاً برابر در ستون‌های اصلی CSV را پیش از تبدیل نوع، با یک نماینده به reference می‌دهد. metadata دریافت در equality payload نیست. تمام excluded occurrenceها به نماینده و دلیل متصل می‌شوند.

این دو policy با `input_policy_id` جدا اجرا می‌شوند. پیش‌فرض نهاییِ ارزیابی انتخاب نشده است. در حالت نامشخص، بستهٔ نهایی نباید خود را accepted بنامد. مقایسهٔ داخلی دو mode ممکن است؛ ترکیب مقدار RAW و DEDUP در یک گزارش ممنوع است. event dedup، سیاست مستقل و نیازمند هویت/قرارداد منبع است.

### ۴.۲. نسخهٔ schema

`SourceSchema` header اصلی، fingerprint، mapping، datatype و parser version دارد. دو نگاشت مشاهده‌شده:

| منبع | نام موجود در نسخهٔ دیگر | نام مورد انتظار reference |
|---|---|---|
| tickets | `create_time` | `created_at` |
| ticket_events | `event_time` | `at` |

انتخاب نگاشت با header شناخته‌شده انجام می‌شود. شرط `if day >= 82` وارد منطق نمی‌شود. اگر هر دو نام با مقدار متفاوت حاضر باشند، adapter تعارض می‌دهد. نام ناشناخته با شباهت زبانی یا LLM به ستون زمان نگاشت نمی‌شود. افزودن ستون ناشناخته می‌تواند حفظ شود؛ حذف/تغییر نوع ستون لازم، schema incident است.

برای reference، metadata داخلی به `o.*` و `t.*` تزریق نامحدود نمی‌شود. روابط سازگار فقط ستون‌های اصلی لازم و extension مستند `crm_lead_events.drop_day` را دارند. provenance در side table باقی می‌ماند.

### 4.3. مشاهده‌های منبع و قراردادهای نامعلوم

[بررسی‌های فقط‌خواندنی منبع](audit-2026-11-09/source-checks.json)، تعدادهای واقعی Manifest، امضاهای Header، ردیف‌های نمونه و نام‌های جایگزین Schema را ثبت می‌کنند. این بررسی‌ها یکتایی سراسری Raw، بسته‌شدن منبع یا کلیدهای خارجی جدید را اثبات نمی‌کنند. شناسه رخدادهای Event و فهرست مرجع والدهای مشتری و کمپین عرضه نشده‌اند. ارتباط‌های اختیاری خالی نباید والد فرضی ایجاد کنند.

توصیه بازبینی قبلی برای حذف همه تکرارهای دقیق سفارش، Requirement یا تصمیم Accepted نیست. فایل `review/types-and-missing/report.md` این مرحله عادی‌سازی را پیشنهاد می‌کند، اما RCA/KPI-VAL و S16 پرسش سیاست ورودی را باز نگه می‌دارند. حفظ RAW را از تصمیم RAW/DEDUP جدا نگه دارید. همچنین درخواست تأیید منطقه زمانی در آن گزارش، الزام صریح بریف درباره وقت تهران را دوباره باز نمی‌کند.

رشته خالی در CSV به‌طور خودکار SQL NULL، صفر یا ردیف نامعتبر نیست. تبدیل فقط در ورودی‌های مشتق‌شده و با قرارداد نسخه‌دار نوع و مقدار خالی انجام شود. فیلدهای اختیاری `order_id`، `staff_id`، `campaign_id`، `promised_by` و مبالغ اصلاح را حفظ کنید. رفتار دقیق Canonical برای NULL و نبود ردیف آزموده شود. خالی‌بودن تاریخ پایان، مجوز دسترسی ایجاد نمی‌کند و حذف کارمند را اثبات نمی‌کند.

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

در وضعیت عادی بدون incident، نتیجه می‌تواند طبق قرارداد «دادهٔ تحویل‌شده در آن صبح» منتشر شود و `not_asserted` باقی بماند. این کار ادعای کامل‌بودن واقعی جهان نیست. چگونگی انتشار پس از incident حل‌نشده موضوع [ADR-04](registry/decisions-registry.md#adr-04) است. نبود closure نباید بدون توضیح به‌معنای توقف دائمی کل سامانه باشد.

پیشنهاد اولیه برای incident شناخته‌شده، نگهداری unresolvedها و انتشار نتایج مستقل است. عدد صفر بازگشتی از `COUNT` یا `COALESCE` منبع غایب، گواه نبود رخداد نیست. backfill دریافت‌شده نیز incident را خودکار closed نمی‌کند.

در S10، هفت کلید پشتیبانی به علت نبود گروه denominator سفارش، مستقل و `no_reference_row` بودند. آن‌ها هفت عدد قابل بازگرداندن نیستند. ۱٬۷۳۳ مقدار تاریخی ثابت، از نظر کامل‌بودن همچنان نامعلوم بودند. معماری هیچ‌یک را صرفاً به دلیل ثابت‌ماندن عدد کامل اعلام نمی‌کند.

### 5.2. تفکیک معناهای اطمینان

`calculation_confidence` از اجرای موفق، parity و provenance به دست می‌آید؛ ترجیحاً با وضعیت و دلیل ثبت شود. `source_completeness` از شواهد منبع می‌آید. `cause_confidence` ارزیابی یک فرضیه است. هیچ‌کدام با یک امتیاز ساختگی جای دیگری را نمی‌گیرد.

`Requirement`: خطای داده به‌تنهایی نباید Signal کسب‌وکار ایجاد کند (بریف، صفحه 14، بخش خطاهای داده). `Open`: بخش‌های 4، 5 و 7 وضعیت‌های کیفیت و Invalidation را تعریف می‌کنند، اما رکورد ارزیابی ارتباط DQIncident، KpiObservation متأثر و مجوز ایجاد Signal را مشخص نمی‌کنند. قرارداد داده به نسخه‌های مرتبط مسئله و مشاهده، دلیل ارزیابی و نسخه قاعده و سیاست نیاز دارد. به [ADR-04](registry/decisions-registry.md#adr-04)، [ADR-07](registry/decisions-registry.md#adr-07)، [DL-03](registry/open-issues-registry.md#dl-03) و [DL-09](registry/open-issues-registry.md#dl-09) مراجعه کنید. بسته‌شدن این مورد به نگاشت مصوب وضعیت به مجوز ایجاد Signal و شواهد ورودی‌های غایب، دیررسیده و اصلاح‌شده نیاز دارد. این یادداشت سیاست انتشار یا قاعده‌ای برای داده نامعلوم انتخاب نمی‌کند.

<a id="data-6"></a>

## ۶. قرارداد اجرای مرجع و پوشش ۵۵ KPI

`Requirement`: معنا و نتیجه همه 55 تعریف Canonical KPI در S03-S04 حفظ شود. `Accepted`: موتور PostgreSQL تنها موتور اجرای محصول، شامل Queryهای سفارشی است. به [ADR-01](registry/decisions-registry.md#adr-01) مراجعه کنید. محاسبه‌گر تعبیه‌شده SQLite در محصول دیگر گزینه جاری نیست.

`Requirement`: SQL و Viewهای اصلی حفظ شوند. `Proposed`: تبدیل‌های PostgreSQL به‌صورت جداگانه همراه با Hash اصلی، نسخه تبدیل، نسخه موتور، پروفایل نوع ورودی، Snapshot و سیاست ورودی ثبت شوند. یک Test Oracle مستقل SQLite می‌تواند SQL اصلی را خارج از محصول اجرا کند. مصنوعات اکتشافی SQLite، پایگاه داده محصول نیستند.

آزمون پذیرش هم‌ارزی باید هر تعریف و کل رابطه خروجی آن را پوشش دهد:

- کلیدها، Dimensionها، گروه‌بندی و وجود ردیف.
- SQL NULL، نبود ردیف، صفر و مخرج صفر.
- نوع‌ها، تقسیم صحیح، ترتیب عملیات، مقادیر Boolean و تکثیر ردیف در Join.
- Median برای جمعیت‌های فرد، زوج، خالی و دارای NULL.
- محاسبات تاریخ، مرزهای زمانی، رویدادهای MIN/MAX و گردکردن مرجع.
- Windowهای متحرک، MTD، اصلاح‌ها، تکرارها، نام‌های جایگزین Schema و مجازبودن ورودی بر اساس Cutoff.

در دو طرف از ورودی‌های ثابت و سیاست‌های یکسان استفاده کنید. پذیرش نهایی همچنان به تصمیم RAW/DEDUP نیاز دارد. برابر بودن Snapshot نهایی، هم‌ارزی Replay را اثبات نمی‌کند. هر 30 گزارش صبحگاهی و Fixtureهای مرزی را مقایسه کنید. تلرانس پس از گردکردن مرجع صفر است. در Serializer دوباره گرد نکنید.

در S09 برای `items, order_value_toman, amount_toman, sessions, score, spend_toman, impressions, clicks, leads` از `INTEGER` استفاده شد. نوع `contract_value_toman` و `monthly_targets.target_million_toman` برابر `REAL` بود. فیلدهای عددی تقویم و `drop_day` از نوع `INTEGER` و شناسه‌ها و Timestampها از نوع `TEXT` بودند. این اطلاعات شواهد ممیزی هستند و جای Data Dictionary رسمی مفقود را نمی‌گیرند. پروفایل دقیق نوع‌ها ثبت و بازبینی شود. تبدیل همه مبالغ به REAL یا NUMERIC می‌تواند تقسیم صحیح را تغییر دهد. به‌طور مشخص `K_DIG_CPL_7D` را بررسی کنید.

رسیدهای آزمون Proposed، نسخه Oracle مربوط به SQLite، گزینه‌های Build، نسخه پیاده‌سازی Median، نسخه PostgreSQL، Hashهای SQL اصلی و View و تبدیل، نوع‌های ورودی و Hash نتایج را نیز نگه می‌دارند. نوع نامعتبر، Overflow یا ورودی اعشاری برای فیلد INTEGER به ثبت مسئله و سیاست صریح نیاز دارد. رشته‌های خام را حفظ کنید. آن‌ها را بی‌اعلام تبدیل نکنید.

عبارت‌های Median و تاریخ در PostgreSQL باید با رفتار SQLite مقایسه شوند. تابعی با هدف ریاضی یکسان، برابری نتایج گرد‌شده را اثبات نمی‌کند. S08 تفاوت‌های مرز زمانی را گزارش می‌کند. روش تبدیل همچنان Proposed است. در این کار هیچ تبدیل SQL یا آزمون هم‌ارزی تولید نشده است.

### 6.0. معنای Canonical مربوط به Viewها

این معناها از پنج View عرضه‌شده می‌آیند و برای هم‌ارزی محاسبات، Requirement هستند. این موارد مجوز افشای ردیف‌های منبع نیستند.

| View | رفتار دقیق انتخاب مقدار و مرز مهم |
|---|---|
| `order_fact` | عبارت `orders LEFT JOIN order_events USING(order_id)` با گروه‌بندی بر اساس شناسه سفارش. زمان منتخب برای paid، payment_failed، cancelled، picked، handed_over و delivered برابر MAX است. ستون‌های Metadata داخلی نباید به `o.*` افزوده شوند. Payloadهای متفاوت با یک شناسه کسب‌وکار به سیاست تعارض نیاز دارند؛ انتخاب ستون‌های غیرتجمیعی در گروه‌بندی، قاعده مستند «آخرین ردیف برنده است» نیست. |
| `ticket_fact` | عبارت `tickets LEFT JOIN ticket_events USING(ticket_id)`. برای first_response از MIN و برای inspected و resolved از MAX استفاده می‌شود؛ reopened یک پرچم MAX جداست. بازگشایی، فرمول‌های Canonical مربوط به resolved/backlog را با تفسیر چرخه جاری جایگزین نمی‌کند. |
| `lead_fact` | برای first_contact، qualified، proposal_sent، won و lost از MAX استفاده می‌شود. ارزش قرارداد، آخرین اصلاح بر اساس Drop تحویل‌شده و ترتیب `drop_day DESC` است؛ سپس COALESCE به مبلغ MAX مربوط به won برمی‌گردد. اصلاح، جایگزینی است و اختلاف آن درآمد جدید نیست. ترتیب ثانویه در یک Drop عرضه نشده است. اصلاح آخر با مقدار NULL به won برمی‌گردد و بی‌اعلام به دنبال اصلاح غیر NULL قبلی نمی‌گردد. |
| `task_fact` | Payload وظیفه به‌همراه MAX زمان done از LEFT JOIN. مقایسه‌های Canonical مربوط به overdue و مبنای زمانی created/due/done حفظ شوند. |
| `revenue_daily` | محور تقویم. مقدار B2C از مبلغ سفارش paid منهای مبلغ رویداد refund در تاریخ هر رخداد محاسبه می‌شود. Marketplace زیرمجموعه کانال است. مقدار B2B از ارزش قرارداد در تاریخ won استفاده می‌کند. مجموع‌های غایب در Join با COALESCE مرجع صفر می‌شوند؛ این کار کامل‌بودن منبع غایب را اثبات نمی‌کند. تعدد ردیف‌های Raw سفارش می‌تواند Joinهای درآمد را تغییر دهد. |

[قراردادهای معنایی 55-KPI](audit-2026-11-09/kpi-contracts.csv)، متن دقیق و Hash همه عبارت‌های SQL، تمام Metadata مرجع، مبنای زمانی و Window خروجی، معنای فرمول و جمعیت و آزمون‌های پذیرش مرتبط را حفظ می‌کنند. فهرست زیر همچنان خلاصه‌ای خوانا است. متن کامل SQL بر هر توضیح فشرده اولویت دارد. وابستگی اجرای Query با وابستگی مقدار منتخب، اثبات حداقل دامنه Invalidation یا مجوز مشاهده یکسان نیست.

### ۶.۱. کلیدهای خواندن جدول پوشش

در جدول زیر «منابع مقدار» از S03-S04 و dependency evidence در S10 آمده است. این ستون با همهٔ منابع لازم برای اجرای یک view یکسان نیست. برای نمونه، اجرای `revenue_daily` به CRM و سفارش نیاز دارد، ولی مقدار `b2b` به سفارش وابسته نیست.

اختصارها: `O=orders`، `OE=order_events`، `T=tickets`، `TE=ticket_events`، `C=csat`، `L=crm_leads`، `LE=crm_lead_events`، `A=tasks`، `AE=task_events`، `M=mkt_daily`، `S=web_sessions`، `CAL=cal` و `MT=monthly_targets`.

در ستون config، ترتیب عددها `target / warn / crit` است و `-` یعنی مقدار تعیین نشده. `esc` همان `escalate_after_days` است. این مقادیر از CSV نقل شده‌اند؛ پیشنهاد آستانهٔ تازه نیستند. precision نهایی همیشه از SQL می‌آید، نه از نمایش خلاصهٔ این جدول.

<!-- KPI_CATALOG_START -->

| KPI و خط CSV | entity / owner | واحد؛ dim | direction؛ rule؛ esc | target / warn / crit | ساعت یا پنجرهٔ کسب‌وکار | منابع مقدار |
|---|---|---|---|---|---|---|
| `K_ORG_NET_REV`؛ 2 | `ORG / M01` | میلیون تومان؛ `none` | `1; dow_baseline:35; esc=2` | `- / - / -` | روز paid/refunded و won؛ cal.d | `CAL, LE, L, OE, O` |
| `K_ORG_REV_MTD_ATTAIN`؛ 3 | `ORG / M01` | %؛ `none` | `1; threshold_from_day8; esc=3` | `100.0 / 95.0 / 90.0` | MTD ماه شمسی؛ cal.d | `CAL, LE, L, MT, OE, O` |
| `K_ORG_ONTIME`؛ 4 | `ORG / M01` | %؛ `none` | `1; threshold; esc=2` | `95.0 / 90.0 / 85.0` | delivered_at | `OE, O` |
| `K_ORG_CSAT`؛ 5 | `ORG / M01` | از ۵؛ `none` | `1; threshold; esc=2` | `4.3 / 3.9 / 3.7` | answered_at | `C` |
| `K_ORG_FRT_MED`؛ 6 | `ORG / M01` | ساعت؛ `none` | `-1; threshold; esc=2` | `2.0 / 3.0 / 5.0` | first_response_at؛ T_RSP | `TE, T` |
| `K_ORG_ORDERS`؛ 7 | `ORG / M01` | عدد؛ `none` | `1; dow_baseline:30; esc=2` | `- / - / -` | created_at؛ cal.d | `CAL, O` |
| `K_WF1_SLA`؛ 8 | `ORG / M01` | %؛ `none` | `1; threshold; esc=1` | `90.0 / 82.0 / 70.0` | delivered_at؛ چهار شرط SQL | `OE, O` |
| `K_WF2_SLA`؛ 9 | `ORG / M01` | %؛ `none` | `1; threshold; esc=1` | `90.0 / 80.0 / 70.0` | resolved_at؛ T_CMP | `TE, T` |
| `K_WF3_SLA_7D`؛ 10 | `ORG / M01` | %؛ `none` | `1; threshold; esc=3` | `65.0 / 50.0 / 40.0` | closed_at؛ پنجرهٔ ۷ روز شامل امروز | `CAL, LE, L` |
| `K_SAL_B2C_REV`؛ 11 | `U_SAL / M02` | میلیون تومان؛ `none` | `1; dow_baseline:35; esc=2` | `- / - / -` | روز paid/refunded؛ cal.d | `CAL, OE, O` |
| `K_SAL_CONV`؛ 12 | `U_SAL / M02` | %؛ `none` | `1; threshold; esc=2` | `2.4 / 2.0 / 1.7` | created_at و sessions.date | `O, S` |
| `K_SAL_PAYFAIL`؛ 13 | `U_SAL / M02` | %؛ `none` | `-1; threshold; esc=1` | `4.0 / 7.0 / 10.0` | created_at؛ failed_at موجود | `OE, O` |
| `K_SAL_PAYFAIL_BY_CH`؛ 14 | `U_SAL / M02` | %؛ `channel` | `-1; threshold; esc=1` | `4.0 / 9.0 / 12.0` | created_at؛ failed_at موجود | `OE, O` |
| `K_ENT_FC_SLA`؛ 15 | `T_ENT / M05` | %؛ `none` | `1; threshold; esc=2` | `85.0 / 70.0 / 60.0` | first_contact_at؛ شامل initial history | `LE, L` |
| `K_ENT_WINRATE_30D`؛ 16 | `T_ENT / M05` | %؛ `none` | `1; threshold; esc=3` | `35.0 / 28.0 / 22.0` | closed_at؛ پنجرهٔ ۳۰ روز | `CAL, LE, L` |
| `K_ENT_PIPELINE`؛ 17 | `T_ENT / M05` | عدد؛ `none` | `1; dow_baseline:40; esc=3` | `- / - / -` | proposal/close؛ وضعیت در cal.d | `CAL, LE, L` |
| `K_ENT_CONTRACT_MTD`؛ 18 | `T_ENT / M05` | میلیون تومان؛ `none` | `1; info; esc=3` | `- / - / -` | won_at؛ MTD ماه شمسی | `CAL, L, LE` |
| `K_TASK_OVERDUE_T_ENT`؛ 19 | `T_ENT / M05` | عدد؛ `none` | `-1; threshold; esc=2` | `2.0 / 4.0 / 8.0` | due/created/done؛ وضعیت در cal.d | `CAL, AE, A` |
| `K_DIG_LEADS`؛ 20 | `T_DIG / M06` | عدد؛ `none` | `1; dow_baseline:40; esc=2` | `- / - / -` | mkt_daily.date | `M` |
| `K_DIG_CPL_7D`؛ 21 | `T_DIG / M06` | هزار تومان؛ `none` | `-1; threshold; esc=3` | `1050.0 / 1250.0 / 1450.0` | mkt_daily.date؛ پنجرهٔ ۷ روز | `CAL, M` |
| `K_DIG_SPEND`؛ 22 | `T_DIG / M06` | میلیون تومان؛ `none` | `-1; info; esc=3` | `- / - / -` | mkt_daily.date | `M` |
| `K_TASK_OVERDUE_T_DIG`؛ 23 | `T_DIG / M06` | عدد؛ `none` | `-1; threshold; esc=2` | `2.0 / 4.0 / 8.0` | due/created/done؛ وضعیت در cal.d | `CAL, AE, A` |
| `K_MKT_ORDERS`؛ 24 | `T_MKT / M11` | عدد؛ `none` | `1; dow_baseline:40; esc=2` | `- / - / -` | created_at؛ marketplace | `O` |
| `K_MKT_REV`؛ 25 | `T_MKT / M11` | میلیون تومان؛ `none` | `1; info; esc=2` | `- / - / -` | paid/refunded؛ marketplace غیرصفر | `CAL, OE, O` |
| `K_TASK_OVERDUE_T_MKT`؛ 26 | `T_MKT / M11` | عدد؛ `none` | `-1; threshold; esc=2` | `2.0 / 4.0 / 8.0` | due/created/done؛ وضعیت در cal.d | `CAL, AE, A` |
| `K_OPS_ONTIME`؛ 27 | `U_OPS / M03` | %؛ `none` | `1; threshold; esc=2` | `95.0 / 90.0 / 85.0` | delivered_at | `OE, O` |
| `K_OPS_PICK_MED`؛ 28 | `U_OPS / M03` | ساعت؛ `none` | `-1; threshold; esc=1` | `4.0 / 5.0 / 8.0` | picked_at منهای paid_at | `OE, O` |
| `K_WH_PICK_MED`؛ 29 | `T_WH / M07` | ساعت؛ `none` | `-1; threshold; esc=1` | `4.0 / 5.0 / 8.0` | picked_at منهای paid_at | `OE, O` |
| `K_WH_PICK_12H_PCT`؛ 30 | `T_WH / M07` | %؛ `none` | `1; threshold; esc=1` | `95.0 / 85.0 / 70.0` | picked_at منهای paid_at | `OE, O` |
| `K_WH_BACKLOG`؛ 31 | `T_WH / M07` | عدد؛ `none` | `-1; threshold; esc=1` | `100.0 / 150.0 / 300.0` | paid/cancelled/picked؛ ساعت ۲۲ | `CAL, OE, O` |
| `K_WH_DAMAGE_RATE`؛ 32 | `T_WH / M07` | %؛ `none` | `-1; threshold; esc=2` | `0.8 / 2.2 / 3.0` | tickets.created_at / delivered_at | `CAL, OE, O, T` |
| `K_WH_DAMAGE_BY_CAT_7D`؛ 33 | `T_WH / M07` | %؛ `category` | `-1; threshold; esc=2` | `0.8 / 3.0 / 5.0` | tickets.created_at / delivered_at؛ ۷ روز | `CAL, OE, O, T` |
| `K_WH_INSPECT_MED`؛ 34 | `T_WH / M07` | ساعت؛ `none` | `-1; threshold; esc=2` | `18.0 / 26.0 / 36.0` | inspected_at منهای first_response_at | `TE, T` |
| `K_TASK_OVERDUE_T_WH`؛ 35 | `T_WH / M07` | عدد؛ `none` | `-1; threshold; esc=2` | `2.0 / 4.0 / 8.0` | due/created/done؛ وضعیت در cal.d | `CAL, AE, A` |
| `K_SHP_HANDOVER_MED`؛ 36 | `T_SHP / M08` | ساعت؛ `none` | `-1; threshold; esc=1` | `3.0 / 4.0 / 6.0` | handed_over_at منهای picked_at | `OE, O` |
| `K_SHP_ONTIME`؛ 37 | `T_SHP / M08` | %؛ `none` | `1; threshold; esc=2` | `95.0 / 90.0 / 85.0` | delivered_at | `OE, O` |
| `K_SHP_ONTIME_BY_CITY`؛ 38 | `T_SHP / M08` | %؛ `city` | `1; threshold; esc=1` | `95.0 / 85.0 / 75.0` | delivered_at | `OE, O` |
| `K_SHP_DELIV_DAYS_MED`؛ 39 | `T_SHP / M08` | روز؛ `none` | `-1; threshold; esc=2` | `1.8 / 2.3 / 3.0` | delivered_at منهای paid_at | `OE, O` |
| `K_TASK_OVERDUE_T_SHP`؛ 40 | `T_SHP / M08` | عدد؛ `none` | `-1; threshold; esc=2` | `2.0 / 4.0 / 8.0` | due/created/done؛ وضعیت در cal.d | `CAL, AE, A` |
| `K_SUP_FRT_MED`؛ 41 | `U_SUP / M04` | ساعت؛ `none` | `-1; threshold; esc=2` | `2.0 / 3.0 / 5.0` | first_response_at؛ T_RSP | `TE, T` |
| `K_SUP_CSAT`؛ 42 | `U_SUP / M04` | از ۵؛ `none` | `1; threshold; esc=2` | `4.3 / 3.9 / 3.7` | answered_at | `C` |
| `K_SUP_TICKETS`؛ 43 | `U_SUP / M04` | عدد؛ `none` | `-1; dow_baseline:35; esc=2` | `- / - / -` | created_at؛ cal.d | `CAL, T` |
| `K_SUP_BACKLOG`؛ 44 | `U_SUP / M04` | عدد؛ `none` | `-1; threshold; esc=2` | `60.0 / 80.0 / 150.0` | created/resolved؛ ساعت ۲۲ | `CAL, TE, T` |
| `K_RSP_FRT_MED`؛ 45 | `T_RSP / M09` | ساعت؛ `none` | `-1; threshold; esc=1` | `2.0 / 3.0 / 5.0` | first_response_at؛ T_RSP | `TE, T` |
| `K_RSP_FRT_2H_PCT`؛ 46 | `T_RSP / M09` | %؛ `none` | `1; threshold; esc=1` | `55.0 / 25.0 / 10.0` | first_response_at؛ T_RSP | `TE, T` |
| `K_RSP_TICKETS`؛ 47 | `T_RSP / M09` | عدد؛ `none` | `-1; dow_baseline:35; esc=1` | `- / - / -` | created_at؛ T_RSP؛ cal.d | `CAL, T` |
| `K_RSP_TICKETS_BY_CAT`؛ 48 | `T_RSP / M09` | عدد؛ `category` | `-1; dow_baseline:60; esc=1` | `- / - / -` | created_at؛ T_RSP | `T` |
| `K_RSP_BACKLOG`؛ 49 | `T_RSP / M09` | عدد؛ `none` | `-1; threshold; esc=1` | `15.0 / 25.0 / 50.0` | created/first_response؛ ساعت ۲۲ | `CAL, TE, T` |
| `K_RSP_CSAT`؛ 50 | `T_RSP / M09` | از ۵؛ `none` | `1; threshold; esc=2` | `4.3 / 3.9 / 3.7` | answered_at؛ join tickets/T_RSP | `C, T` |
| `K_TASK_OVERDUE_T_RSP`؛ 51 | `T_RSP / M09` | عدد؛ `none` | `-1; threshold; esc=2` | `2.0 / 4.0 / 8.0` | due/created/done؛ وضعیت در cal.d | `CAL, AE, A` |
| `K_CMP_RES_48H_PCT`؛ 52 | `T_CMP / M10` | %؛ `none` | `1; threshold; esc=1` | `90.0 / 80.0 / 70.0` | resolved_at؛ T_CMP | `TE, T` |
| `K_CMP_RES_MED`؛ 53 | `T_CMP / M10` | ساعت؛ `none` | `-1; threshold; esc=2` | `30.0 / 40.0 / 55.0` | resolved_at؛ T_CMP | `TE, T` |
| `K_CMP_TICKETS`؛ 54 | `T_CMP / M10` | عدد؛ `none` | `-1; dow_baseline:50; esc=2` | `- / - / -` | created_at؛ T_CMP؛ cal.d | `CAL, T` |
| `K_CMP_BACKLOG`؛ 55 | `T_CMP / M10` | عدد؛ `none` | `-1; threshold; esc=2` | `30.0 / 45.0 / 60.0` | created/resolved؛ T_CMP؛ ساعت ۲۲ | `CAL, TE, T` |
| `K_TASK_OVERDUE_T_CMP`؛ 56 | `T_CMP / M10` | عدد؛ `none` | `-1; threshold; esc=2` | `2.0 / 4.0 / 8.0` | due/created/done؛ وضعیت در cal.d | `CAL, AE, A` |

<!-- KPI_CATALOG_END -->

### ۶.۲. وابستگی عملیاتی هر تعریف

هر `DependencySpec` علاوه بر جدول بالا، فیلدهای زیر را دارد:

| فیلد | کاربرد |
|---|---|
| `execution_relations` | روابط Canonical الزامی و معادل‌های مصوب آن‌ها در PostgreSQL. در دسترس بودن رابطه جدا از وابستگی‌های مقدار بررسی شود. |
| `value_sources` | منابع واقعی مقدار منتخب، با projected fields و predicate. |
| `event_selectors` | مانند MIN first_response یا MAX delivered؛ فقط eventهای مؤثر. |
| `join_paths` | کلیدها و نوع اتصال؛ fan-out و نبود والد ممکن است مقدار را عوض کند. |
| `output_clock` | created، delivered، answered، resolved، won یا cal.d. |
| `window_operator` | نقطه‌ای، متحرک 7/30، MTD، وضعیت بازه در ساعت 22:00 یا overdue. |
| `structural_gates` | نبود denominator group یا predicateی که استقلال no-row را اثبات کند. |
| `dimension_dependencies` | مقدار category/channel/city و جابه‌جایی میان گروه‌های قدیم و جدید. |
| `population_lineage` | contributor IDs/hash، numerator و denominator population جدا. |
| `recompute_strategy` | بازسازی موجودیت، بازه تاریخ‌های متأثر یا اجرای کامل Query به‌عنوان Fallback. |

مشتق‌سازی اولیه از SQL parser و بررسی انسانی انجام می‌شود. regex تنها، برای CTE، subquery هم‌بسته و MIN/MAX کافی نیست. تا وقتی dependency دقیق تأیید نشده، recalculation گسترده‌تر انجام شود. بازسازی بیشتر از لازم قابل قبول است؛ حذف اثر واقعی قابل قبول نیست.

برای `K_ORG_CSAT/K_SUP_CSAT` فقط csat بر مقدار اثر دارد؛ برای `K_RSP_CSAT`، tickets نیز شرط join/team است. KPIهای overdue تیم پشتیبانی به tickets وابسته نیستند. ثبت وابستگی بر اساس نام تیم، اشتباه است.

<a id="data-7"></a>

## ۷. recalculation و invalidation

دو مسئله جدا هستند:

۱. **رکورد جدید معلوم:** entity، field، timestamp و join مربوط معلوم است. می‌توان خروجی‌های متأثر را محاسبه کرد.

۲. **منبع غایب با رکوردهای نامعلوم:** زمان و entity رکوردهای نرسیده معلوم نیست. بدون closure یا کران تأخیر، مجموعهٔ دقیق اثر قابل اثبات نیست. باید uncertainty را تا وابستگی‌های محتمل منتقل کرد.

### ۷.۱. الگوریتم پیشنهادی

۱. `InputDelta` را با source، occurrence، payload قبل/بعد، policy و دلیل بسازید.

۲. entityهای متصل را از join index پیدا کنید. factهای قدیم و جدید را در دو snapshot محاسبه کنید. تغییر فیلد و contributor set هر دو ثبت شوند.

۳. dependency graph را طی کنید. هر field تغییرکرده، گروه قدیم و جدید، بعد قدیم و جدید و بازهٔ مؤثر را مشخص کند.

۴. `DirtyKeySet` را با reason و dependency path ثبت کنید. نبود اثبات حداقل مجموعه، باعث fallback به کل بازهٔ تاریخی همان KPI شود.

5. تبدیل مصوب PostgreSQL را برای هر Canonical KPI متأثر، روی Snapshot جدید اجرا کنید. تعریف آن را حفظ کنید. در ابتدا، کل Query تبدیل‌شده را اجرا و کلیدهای خروجی را مقایسه کنید. Predicateهایی که معنای Query را تغییر می‌دهند اضافه نکنید.

۶. observation جدید و delta مقدار/row-state/contributor/quality ساخته شود. signal baseline، Insight Brief و cacheهای وابسته invalid شوند. گزارش منتشرشده پاک نشود.

۷. در آزمون، نتیجهٔ مسیر selective با full rebuild بر snapshot و policy یکسان مقایسه شود. فقط پس از برابری row set، مقدار، NULL و provenance، بهینه‌سازی پذیرفته شود.

### ۷.۲. قواعد بازهٔ اثر

| تغییر | دامنهٔ recalculation لازم |
|---|---|
| created_at یا dimension سفارش/تیکت | گروه قبلی و جدید و تمام joinهای وابسته؛ فقط روز دریافت نیست. |
| paid/refund | تاریخ هر رخداد برای revenue؛ اصلاح سفارش می‌تواند پرداخت و refundهای چند تاریخ را متأثر کند. |
| MIN first_response یا MAX delivered/resolved | entity projection قبل/بعد؛ خروجی ممکن است از یک روز به روز دیگر منتقل شود. |
| جزء rolling هفت‌روزه در روز t | خروجی‌های t تا t+6، محدود به افق محاسبهٔ فعلی؛ آینده به عنوان pending dependency باقی بماند. |
| close یک lead در روز t | win-rate روزهای t تا t+29 و SLA هفت‌روزه؛ pipeline پیش/پس از closure نیز بررسی شود. |
| ارزش قرارداد قدیمی | bucket تاریخ won و MTD از آن تاریخ تا پایان همان ماه؛ مالیات/ارز فرضی اضافه نشود. |
| backlog در ساعت ۲۲ | همهٔ روزهایی که عضویت entity در شرط open قبل/بعد عوض شده؛ بازه ممکن است طولانی باشد. |
| done_at یا due_date | روزهای overdue متأثر؛ تغییر timestamp می‌تواند ورود/خروج از بازه بسازد. |
| target ماه یا rule | مقدار attain مربوط به target ممکن است recalculation بخواهد؛ warn/crit فقط signal و report را invalid می‌کند. |
| org/access revision | scope و report eligibility، query/cache و evidence؛ مقدار reference موجود نباید بی‌دلیل تغییر کند. |

داده‌مدل هیچ سقف ثابتی مانند هفت یا سی روز برای پذیرش late record ندارد. window KPI محدود است، ولی تأخیر تحویل محدود فرض نمی‌شود. full historical recomputation fallback همیشه قابل دسترس باشد. closure نیز تضمین فنی حذف تاریخچه نیست.

### ۷.۳. آزمون‌های رگرسیون برخاسته از شواهد

| fixture | انتظار |
|---|---|
| صبح ۶۷ در برابر ۶۸ | ۳۲ تغییر تاریخی پشتیبانی از late support؛ دو تغییر پرداخت مستقل با آن مخلوط نشوند. |
| day 065، contributorها | در سه گروه درصدی، جمعیت تغییر می‌کند ولی ROUND یکسان است؛ evidence version باید عوض شود. |
| day 076 و mode سفارش | هشت KPI حساس و ۴۱ اختلاف snapshot نهایی در S09 قابل بازتولید باشند؛ policy مصوب جدا مشخص شود. |
| correction drop 070 | صبح ۷۰ دست‌نخورده؛ صبح ۷۱ مقدار تاریخ won و MTD را به‌روز می‌کند. |
| schema جدید | نگاشت بر header؛ تغییر روز حادثه در دادهٔ آزمون نباید منطق را بشکند. |

این اعداد، fixture دادهٔ توسعه‌اند. در runtime نقش قاعدهٔ کشف یا فهرست ثابت خروجی ندارند.

<a id="data-8"></a>

## ۸. lineage، query registry و نسخهٔ گزارش

[قرارداد خروجی در سند 001، بخش 9.1](001-system-blueprint.md#system-9)، فیلدهای `open_items`، `data_issues.source/type`، `decision_followups` و Validation ارتباط عدد با Query در `dataset/output_contract/brief_schema.json` را پوشش می‌دهد. نام‌های جایگزین خانواده منبع همچنان Proposed هستند. تعارض وضعیت در [ADR-09](registry/decisions-registry.md#adr-09) و [DL-11](registry/open-issues-registry.md#dl-11) و نگاشت اعداد افزوده در [DL-17](registry/open-issues-registry.md#dl-17) باز می‌ماند. این موارد، مسائل موجود هستند؛ یافته جدید یا نگاشت مصوب نیستند.

`Requirement`: علت‌های منتشرشده به حداقل دو شاهد مستقل نیاز دارند (بریف، صفحه 9، Insight Brief). کنترل و محدودیت‌های آن در [سند 001، بخش 8](001-system-blueprint.md#system-8) تعریف شده‌اند. `Open`: قراردادهای EvidenceRef و InsightVersion روش نگهداری گروه‌های شواهد هر علت، نتیجه بررسی استقلال، دلیل آن یا نسخه بررسی را مشخص نمی‌کنند. در نتیجه، بازسازی این Validation فقط از روی ارجاع‌ها ممکن نیست. طبق [ADR-09](registry/decisions-registry.md#adr-09) و [DL-11](registry/open-issues-registry.md#dl-11)، بسته‌شدن این مورد به نگاشت ذخیره‌سازی بازبینی‌شده و نمونه‌های Validation مرتبط با نسخه Insight و مخاطب مجاز نیاز دارد. در اینجا الگوریتم استقلال تصویب نمی‌شود.

`Requirement`: وضعیت خواندن، بستن و ارجاع مجاز و پیگیری بعدی تصمیم حفظ شوند (بریف، صفحات 3-4,11-12,15؛ S07 IN02/DE-01 و IN03/DE-02). [سند 001، بخش 9](001-system-blueprint.md#system-9) این عملیات را بیان کرده است. `Open`: قراردادهای ReportVersion، SignalEpisode و DecisionEvent/ActionDraft ارتباط عامل، زمان و موضوع را برای سابقه خواندن، بستن و ارجاع یا نگاشت تصمیم به Query مشاهده‌شده در `brief_schema.json#/properties/decision_followups` مشخص نمی‌کنند. قرارداد داده باید این رکوردها را از سابقه اعلان و شواهد اجرای اقدام جدا کند. بسته‌شدن این مورد به نگاشت‌های بازبینی‌شده تاریخچه و پیگیری، همراه با شواهد اثر گزارش‌شده و محدودیت‌های آن نیاز دارد. به [ADR-17](registry/decisions-registry.md#adr-17)، [DL-12](registry/open-issues-registry.md#dl-12) و [DL-18](registry/open-issues-registry.md#dl-18) مراجعه کنید. تصمیم، اجرای اقدام را اثبات نمی‌کند؛ داده ثابت Replay باید بدون تغییر بماند.

زنجیرهٔ ردیابی لازم چنین است:

برای مسیرهای کنترل‌شده Query، شواهد و گزارش از نماهای Structurizr با نام‌های `EvidenceAndAnalysis`، `ReportDelivery` و `InteractiveAssistant` استفاده کنید. نمای Data Lineage از عدد تا ردیف منبع هنوز وجود ندارد. قرارداد Data Lineage چنین است: عدد گزارش ← Query و نتیجه ثبت‌شده و زمینه آن ← مشارکت‌کنندگان و فیلدهای Fact ← رخدادهای منبع ← فایل اصلی و Manifest. این متن یک قرارداد است، نه لینک به نموداری ساختگی.

برای حجم فعلی، pointerهای row و contributor index در PostgreSQL کافی‌اند. ذخیرهٔ نسخهٔ کامل همهٔ facts برای هر روز الزامی نیست. می‌توان raw append-only، فهرست ورودی snapshot و checkpoint قابل بازسازی داشت. materialization وقتی پذیرفته است که برابر SELECT اصلی آزمون شود.

`QueryRun` تنها query string نیست. params، engine و aggregate version، input policy، scope، row count، result hash، error و زمان اجرا لازم‌اند. query بدون اجازهٔ کاربر می‌تواند در audit وجود داشته باشد، ولی مدیر خارج از scope حق خواندن SQL همراه پارامتر یا source pointers آن را ندارد.

هر `ReportVersion` مشخص می‌کند `as_reported`، `restated`، `recomputed_under_new_policy` یا `counterfactual` است. counterfactualهای S10 ابزار تشخیص بودند؛ هرگز به نام مقدار قابل‌دسترسی صبح ۶۷ منتشر نمی‌شوند. renderer باید این mode را قبل از هر نمایش بررسی کند.

پیشنهاد سیاست گزارش: نسخهٔ اولیه immutable؛ اصلاح بعدی با `supersedes`، دلیل، cutoff جدید و diff قابل مشاهده. URL ثابت گزارش به نسخهٔ واقعی نخست و فهرست نسخه‌ها اشاره کند. انتخاب «آخرین مقدار» در داشبورد نباید تاریخچهٔ گزارش را پنهان کند. دامنه و اعلان restatement در [ADR-05](registry/decisions-registry.md#adr-05) تصویب می‌شود.

<a id="data-9"></a>

## ۹. سازمان، دسترسی و config تاریخی

اصل دامنهٔ دسترسی از بریف ص۱۰ و ص۱۳ و `dataset/org/access_matrix.csv` می‌آید و تصمیم باز نیست. جدول مدیر به دامنه در [ADR-06](registry/decisions-registry.md#adr-06) ثبت شده است. طراحی AccessGrantVersion و نگاشت ردیف/ستون منابع مشترک، اجرای این الزام‌اند؛ مجوز جدید ایجاد نمی‌کنند. مدیر بالاتر فقط دادهٔ تجمیعی زیرمجموعه را می‌بیند؛ دادهٔ فردی فقط برای سرپرست مستقیم و مدیریت بار کار است. مرخصی در تحلیل فقط ظرفیت تجمیعی تیم باقی می‌ماند.

`OrgNode` نوع node را از داده می‌گیرد. `OrgEdgeVersion`، رابطهٔ parent-child با valid interval و known_at است. تغییر سطح یا افزودن تیم نباید به تغییر کد recursive traversal نیاز داشته باشد. cycle، parent غایب و چند parent متعارض کنترل شوند.

`AccessGrantVersion` entity scope، سطح فردی، purpose و زمان اثر را نگه می‌دارد. دسترسی تجمیعی ancestor، مجوز فردی descendant نیست. دادهٔ `staff_availability` برای تحلیل فقط در سطح ظرفیت مجاز خلاصه می‌شود. task ownership برای سرپرست مستقیم، از حضور و عملکرد کارکنان جداست.

static org فایل‌ها effective day دارند، ولی known_at دقیق ندارند. S07 نیز `org_change` روز ۷۵ دارد و S02 تغییر ورودی را از صبح بعد مؤثر می‌داند. پیشنهاد حل، ثبت هر دو زمان و تقدم policy مصوب است. دو حالت محاسبهٔ roster در تست‌ها حفظ شوند؛ هیچ‌کدام بدون تأیید، واقعیت قطعی قلمداد نشود.

calendar رخدادها نیز زمان اعلام ندارد. برای جلوگیری از نشت آینده، رخداد عملیاتی رخ‌نداده شاهد علت جاری نیست. اگر کمپین آینده به‌عنوان برنامهٔ اعلام‌شده لازم باشد، visibility contract و برچسب `planned` جدا می‌خواهد. monthly target و ساختار برنامه‌ریزی‌شده با «رویداد رخ‌داده» یکی نیستند.

`Requirement`: مدیران مجاز باید بتوانند اهداف، اولویت‌ها، Targetها، Thresholdها، قواعد تشدید، ساختار سازمان و تعریف‌های قابل گسترش KPI را بدون تغییر کد تنظیم کنند. 55 تعریف Canonical حفظ شوند. `Proposed`: از چرخه کنترل‌شده نامزدها در سند 001 و managerConfig در DSL استفاده شود. اولویت‌ها می‌توانند رتبه‌بندی و انتخاب، تمرکز شواهد مجاز و تأکید گزارش را شکل دهند. آن‌ها نمی‌توانند فرمول‌ها را تغییر دهند، مجوزها را گسترش دهند، مسئله داده را پنهان کنند یا علت را اثبات کنند.

برای ManagerConfigurationRevision و InteractiveEvidenceRevision به [سند 001، بخش 4](001-system-blueprint.md#system-4)، [سند 001، بخش 9](001-system-blueprint.md#system-9) و [نگاشت پرسش مدیر در بخش 7.2a، در ادامه بخش 7.2](registry/acceptance-register.md#manager-question-map) مراجعه کنید. این بخش‌ها S07 IN01/IN04-IN07، نوع تغییر، اختیار، زمان اثر، رسید Upload و آمادگی شواهد را پوشش می‌دهند. تعارض‌های زمان M11 و Q09/IN07 در [ADR-08](registry/decisions-registry.md#adr-08)، [ADR-16](registry/decisions-registry.md#adr-16) و [DL-10](registry/open-issues-registry.md#dl-10) باز می‌مانند. تأیید و فعال‌سازی تنظیمات نیز در [DL-19](registry/open-issues-registry.md#dl-19) باز می‌ماند. این قراردادهای موجود به ثبت یافته تکراری در اینجا نیاز ندارند.

<a id="data-10"></a>

## 10. مرز پایگاه داده با وضعیت Accepted

[ADR-01](registry/decisions-registry.md#adr-01)، PostgreSQL را تنها موتور پایگاه داده محصول ثبت می‌کند. S16 Q03 تصمیم تیم را بیان می‌کند. S17 از PostgreSQL برای ذخیره‌سازی، همه KPIها و همه Queryهای سفارشی استفاده می‌کند. محل حفاظت‌شده ذخیره فایل خام همچنان Archive است، نه پایگاه داده دوم.

| گزینه قبلی | وضعیت فعلی | اثر |
|---|---|---|
| SQLite برای کل محصول | گزینه Proposed که با Q03 کنار گذاشته شده است | این گزینه از مسیر میان‌بُر MVP وارد محصول نشود. |
| PostgreSQL به‌همراه محاسبه‌گر تعبیه‌شده SQLite در محصول | گزینه Proposed که با Q03 کنار گذاشته شده است | موتور دوم Query محصول حذف شود. مقایسه مرجع فقط در فرایند آزمون جدا انجام شود. |
| ذخیره‌سازی و محاسبه با PostgreSQL | مرز موتور Accepted؛ روش تبدیل Proposed | تبدیل‌ها نسخه‌دار شوند. درستی هر 55 تعریف اثبات شود. امنیت و کارایی همچنان به آزمون نیاز دارند. |

### 10.1. مسیر واحد اجرای محصول

محاسبه‌گر، SQL ثبت‌شده PostgreSQL را برای Snapshot ثابت می‌خواند. QueryGateway ابزارهای ازپیش‌تعریف‌شده و SQL سفارشی محدودشده را از طریق Projectionهای مصوب PostgreSQL ارائه می‌کند. SQL سفارشی فقط‌خواندنی و ثبت‌شده است و از Scope فراخوان پیروی می‌کند. پاسخ‌های مبتنی بر KPI موجود از تعریف و نسخه مصوب استفاده می‌کنند. تفکیک جدید به رکورد Query مستقل نیاز دارد.

سرویس Batch می‌تواند ورودی‌های بین‌تیمی را محاسبه کند. مجوز این سرویس هرگز به مجوز مدیر تبدیل نمی‌شود. کنترل‌های ردیف و ستون پیش از ورود شواهد به Agent اعمال شوند. مسیرهای نتیجه، Query، Cache، Log و Export مجوزسنجی شوند. پایگاه داده یا Parser به‌تنهایی نبود نشت را اثبات نمی‌کند.

تبدیل‌های دقیق، نقش‌ها، Viewها، Indexها و کنترل‌های Pool همچنان بخشی از طراحی باقی‌مانده هستند. [آزمون پذیرش Q03](registry/acceptance-register.md#at-02) تکمیل نشده است.

<a id="data-11"></a>

## ۱۱. عملیات، کارایی و بازیابی

ExecutionGrant حدود درخواست والد را تعیین می‌کند؛ BudgetLedger هزینه روزانه را ثبت می‌کند؛ DayRunOutcome پوشش الزامی گزارش‌ها را نگه می‌دارد. برای رکوردهای موجود Token، قیمت و Retry، تطبیق روزانه و زمان‌بندی سرتاسری مراحل مطابق بریف صفحات 14,16، از [سند 003، بخش ۳](003-roadmap.md#roadmap-measurement) استفاده کنید. حدود دقیق و انتخاب مدل در [ADR-10](registry/decisions-registry.md#adr-10)، [ADR-13](registry/decisions-registry.md#adr-13) و [DL-14](registry/open-issues-registry.md#dl-14) باز می‌مانند. سیاست Retry و شکست نیز در [ADR-14](registry/decisions-registry.md#adr-14) و [DL-13](registry/open-issues-registry.md#dl-13) باز می‌ماند. قرارداد اندازه‌گیری قبلاً ثبت شده و شکاف جدید نیست.

ایندکس‌های اولیهٔ پیشنهادی: source/drop/commit، entity/event/time، business_id، KPI/snapshot/date/dim، org edge interval و signal/recipient. ایندکس نهایی پس از query plan و benchmark انتخاب شود؛ ادعای سرعت در این سند وجود ندارد.

اجرای اولیه می‌تواند در هر صبح همهٔ ۵۵ query را بر facts cache‌شدهٔ همان snapshot اجرا کند. ابتدا correctness و سقف ۱۵ دقیقه سنجیده شود. selective recomputation زمانی ارزش دارد که benchmark، نیاز یا کاهش قابل‌توجه هزینه را نشان دهد.

`Proposed`: وضعیت‌های فنی Job، رسیدهای Validation، نتایج بسته و Export و پوشش روز جدا نگهداری شوند. شواهد Retry محدود، Lease، لغو، Timeout، شکست پیش از ساخت پیش‌نویس و شکست نهایی ثبت شوند. State Machine دقیق همچنان Open است. وضعیت‌های فنی نباید به مقادیر جدید Enum در Brief یا QA تبدیل شوند. Retry نباید انتشار تکراری ایجاد کند. شکست گزارش یک مدیر مانع انتشار بسته معتبر مدیر دیگر نمی‌شود. به [ADR-14](registry/decisions-registry.md#adr-14)، [AT-21](registry/acceptance-register.md#at-21) و [AT-28](registry/acceptance-register.md#at-28) مراجعه کنید.

backup باید metadata پایگاه داده و archive manifest را با یک checkpoint سازگار نگه دارد. restore زمانی معتبر است که hash فایل‌ها، snapshot rebuild و گزارش نمونه برابر باشند. retention و دورهٔ backup تصمیم عملیاتی باز هستند؛ برای نسخهٔ ارزیابی، تمام منابع و نسخه‌های لازم برای replay حفظ شوند.

دادهٔ قدیمی به دلیل دیررسیدن خودکار حذف نمی‌شود. اگر در آینده retention لازم شد، archive قابل بازیابی و قرارداد بازسازی تاریخی باید پیش از حذف دادهٔ آنلاین تصویب شوند.

مسیر ممیزی: [AUD-017 تا AUD-028](audit-2026-11-09/audit-report.md#aud-017-obsolete-and-misleading-data-visualization)، [بررسی‌های منبع](audit-2026-11-09/source-checks.json) و [قراردادهای معنایی KPI](audit-2026-11-09/kpi-contracts.csv). در این ممیزی هیچ Query مربوط به KPI اجرا نشد.
