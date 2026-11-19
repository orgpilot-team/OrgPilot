فاز ۱ تکمیل شد. طبق دستور، اجرای کار در همین نقطه متوقف شد. هیچ فایلی تغییر نکرد.

## تقسیم کار به فازهای قابل Resume

### فاز ۱ — ثبت Baseline و بررسی مدل

- هدف: ثبت وضعیت Git، منابع فعال، فایل‌های محافظت‌شده و وضعیت فعلی MCP.
- ورودی‌ها: `workspace.dsl`، پوشه‌های `docs` و `adrs` و فایل‌های Reference.
- فایل‌های قابل تغییر: هیچ‌کدام.
- فایل‌های ممنوع: همه فایل‌های پروژه.
- اقدامات: بررسی Git، ثبت SHA-256، اسکن ارجاع‌های منسوخ و اجرای MCP.
- اعتبارسنجی: تطبیق `HEAD` با `origin/main`، Working Tree تمیز و تطبیق Hashها.
- Exit Criteria: Baseline کامل و قابل تکرار باشد.
- Resume: شروع فاز ۲ از ADR-0001.

### فاز ۲ — اصلاح ADRها

- هدف: همگام‌سازی تصمیم‌های معماری قبل از تغییر مستندات و DSL.
- ورودی‌ها: ADRهای موجود، تصمیم‌های Locked و Open Decisionهای Plan.
- فایل‌های قابل تغییر: ADR-0001 تا ADR-0013، ADR-0015، ADR-0016 و ADRهای جدید 0018 تا 0020. ADR-0014 و ADR-0017 فقط در صورت تعارض واقعی.
- فایل‌های ممنوع: `workspace.dsl`، مستندات، فایل‌های Reference و پوشه‌های غیرفعال.
- اقدامات: حذف Sourceهای منسوخ، اصلاح deployment، durable jobs، export، SQLite و observability.
- اعتبارسنجی: Link scan، بررسی Status و تطبیق تصمیم‌ها با Plan.
- Exit Criteria: ADRها مستقل باشند و Open Decisionها مقدار اختراعی نداشته باشند.
- توقف و Resume: در نخستین ADR نامعتبر توقف شود. ادامه از همان ADR انجام شود.

### فاز ۳ — مستندات پایه و README

- هدف: همگام‌سازی راهنمای Structurizr و مستندات 01 تا 08 با ADRها.
- ورودی‌ها: خروجی فاز ۲ و منابع اصلی معماری.
- فایل‌های قابل تغییر: `README.md` و `docs/01` تا `docs/08`.
- فایل‌های ممنوع: Component documentation، DSL و Referenceها.
- اقدامات: ثبت Scope، Technology Matrix، امنیت، runtime flow، deployment و risks.
- اعتبارسنجی: Link scan و تطبیق با ADRها.
- Exit Criteria: هیچ ارجاع فعال به `final review` یا `trash-data` باقی نماند.
- توقف و Resume: ادامه از نخستین سندی که Validation آن پاس نشده است.

### فاز ۴ — اصلاح مدل Structurizr

- هدف: تکمیل C4، Technologyها، deployment، relationships و 16 View.
- ورودی‌ها: ADRها و مستندات تأییدشده.
- فایل قابل تغییر: [workspace.dsl](D:/Projects/Arka/architecture/structurizr/workspace.dsl).
- فایل‌های ممنوع: [workspace.json](D:/Projects/Arka/architecture/structurizr/workspace.json)، Referenceها و مستندات غیرفعال.
- اقدامات: افزودن سه Component، OTel Collector، Langfuse، Web L3 و روابط صریح.
- اعتبارسنجی: MCP parse، validate و inspect.
- Exit Criteria: 50 Product Component، 16 View، صفر finding عملیاتی و حفظ `!impliedRelationships false`.
- توقف و Resume: ادامه از بخش DSL مرتبط با نخستین خطای MCP.

### فاز ۵ — Component documentation و URLها

- هدف: مستندسازی 50 Component و چهار Store/Contract.
- ورودی‌ها: مدل تأییدشده فاز ۴.
- فایل‌های قابل تغییر: `docs/09` تا `docs/14`. فقط URLهای لازم در `workspace.dsl` نیز مجاز هستند.
- فایل‌های ممنوع: فایل‌های Reference و مستندات غیرفعال.
- اقدامات: ایجاد 54 Anchor و تطبیق 54 URL.
- اعتبارسنجی: شمارش Anchorها، Link test و MCP validation.
- Exit Criteria: همه Anchorها و URLها معتبر باشند.
- توقف و Resume: ادامه از نخستین سند یا Anchor نامعتبر.

### فاز ۶ — تولید Mermaid

- هدف: تولید 16 Artifact از DSL تأییدشده.
- ورودی‌ها: مدل و URLهای نهایی.
- فایل‌های قابل تغییر: فقط 16 فایل `.mmd` مشخص‌شده در Plan.
- فایل‌های ممنوع: DSL، `workspace.json` و Artifactهای قدیمی فاقد View فعال.
- اقدامات: MCP export و ذخیره فقط فیلد `definition`.
- اعتبارسنجی: تعداد 16 فایل و نبود JSON خام.
- Exit Criteria: تمام Viewها با View key صحیح Export شوند.
- توقف و Resume: ادامه از نخستین View صادرنشده.

### فاز ۷ — اعتبارسنجی نهایی

- هدف: اجرای همه Acceptance Criteria.
- ورودی‌ها: خروجی فازهای ۲ تا ۶.
- فایل‌های قابل تغییر: هیچ‌کدام. هر نقص باید به فاز مالک برگردد.
- فایل‌های ممنوع: تمام فایل‌های محافظت‌شده و خارج از Scope.
- اقدامات: Structurizr Local روی کپی موقت، بررسی 54 لینک، Schema validation، Hash و Git diff.
- اعتبارسنجی: همه 24 مرحله Validation Plan.
- Exit Criteria: همه Acceptance Criteria پاس شوند.
- توقف و Resume: در صورت خطا، بازگشت به فاز مالک خطا.

## نتیجه فاز ۱

Git:

- شاخه: `main`
- Commit: `58fa603490ab6f5e8491fd909f086e313229544f`
- `origin/main`: همان Commit
- Working Tree: تمیز
- Commit summary: `cleaning docs folder`

مدل فعلی MCP:

- Parse: پاس
- Validate: پاس
- Product Component: 47
- Web: 3
- Backend API: 20
- Background Worker: 13
- Scheduler/Replay: 6
- Agent Runtime: 5
- Inspector findings: 143
- Missing Technology: 131
- Disconnected deployment instance: 6
- خارج از View: 4
- Synthetic documentation finding: 1
- Synthetic decision finding: 1

MCP برای `!docs` و `!adrs` قابلیت لازم را فعال نکرده است. بررسی با کپی درون‌حافظه‌ای و بدون این دو Directive انجام شد. فایل اصلی تغییر نکرد.

Baseline فایل‌های محافظت‌شده:

| فایل | SHA-256 |
|---|---|
| `workspace.json` | `cfd7522b93ecf8cca00dcbbb3ada8911f951dc27467dbfb6d44da64e11a7020b` |
| `reference_views.sql` | `8f9e299a3451eba280f3b70688ac796f41c9be27d28ade5c0c13386eafda01b4` |
| `kpi_dictionary.csv` | `35406feb924c7239ba017a37417f2074a89a6d9bfe09fcf8733fb5c4b133d2d3` |
| `brief_schema.json` | `a8545f2073421db9dd90748087ada0f43e9971516775a5f711a64d8695bafe35` |
| `qa_answer_schema.json` | `ea9656df1071b9734f75fbdfb9bf3ef9a0186202689499d2a1d7f5e8f04af426` |
| `example_brief.json` | `f277585d9d6a2af98e098a982d7911222b8d43781efe569268b21293ed782ab8` |
| `scripted_inputs.json` | `4a33727212f82bd5a30fbd29c1f1eec63fc46264bcf4ee2be92faf795d080d54` |

## گزارش پایان فاز

- فایل‌های تغییرکرده: هیچ‌کدام.
- Validation: پاس.
- تصمیم باز جدید: هیچ‌کدام.
- Blocker: ندارد.
- Commit یا Push: انجام نشد.
- نقطه دقیق Resume: **فاز ۲، قبل از نخستین تغییر، از بررسی و اصلاح ADR-0001 شروع شود.**

## نتیجه فاز ۲ — اصلاح ADRها

وضعیت: تکمیل‌شده در 2026-11-19.

### نتیجه

- Sourceهای منسوخ از ADR-0001 تا ADR-0011 حذف شدند و با Related Requirementهای مستقل جایگزین شدند.
- ADR-0002 مرز PostgreSQL 18 و SQLite داخل Acceptance Test Harness را ثبت می‌کند.
- ADR-0005 مرز Query Gateway و دسترسی محدود Agent Runtime را ثبت می‌کند.
- ADR-0008 پروتکل Durable Job، Commit قبل از بازگشت `job_id`، Wake-up اختیاری و Claim از PostgreSQL را ثبت می‌کند.
- ADR-0012 دارای Status برابر `Superseded` و لینک معتبر به ADR-0018 است.
- ADR-0013 direct join، containment، atomic rename، hash، receipt و جلوگیری از `/submission/submission` را ثبت می‌کند.
- ADR-0015 Decision Effect را Internal-only نگه می‌دارد و تغییر Output Contract را ممنوع می‌کند.
- ADR-0016 SQLite را فقط داخل Acceptance Test Harness نگه می‌دارد.
- ADR-0018، ADR-0019 و ADR-0020 با تمام بخش‌های الزامی ایجاد شدند.
- ADR-0014 و ADR-0017 تغییر نکردند، زیرا تعارض واقعی نداشتند.

### فایل‌های تغییرکرده

- `architecture/structurizr/adrs/0001-unified-data-intake-and-preparation.md`
- `architecture/structurizr/adrs/0002-use-postgresql-and-verify-kpi-parity.md`
- `architecture/structurizr/adrs/0003-preserve-published-report-versions.md`
- `architecture/structurizr/adrs/0004-continue-publication-with-incomplete-sources.md`
- `architecture/structurizr/adrs/0005-enforce-scoped-read-only-queries.md`
- `architecture/structurizr/adrs/0006-use-deterministic-signal-lifecycle.md`
- `architecture/structurizr/adrs/0007-assign-workflow-and-stage-owners.md`
- `architecture/structurizr/adrs/0008-use-one-bounded-agent.md`
- `architecture/structurizr/adrs/0009-publish-manager-reports-independently.md`
- `architecture/structurizr/adrs/0010-require-human-decision-control.md`
- `architecture/structurizr/adrs/0011-retain-replay-and-audit-evidence.md`
- `architecture/structurizr/adrs/0012-evaluation-deployment-profile.md`
- `architecture/structurizr/adrs/0013-submission-exporter.md`
- `architecture/structurizr/adrs/0015-decision-effect-evaluator.md`
- `architecture/structurizr/adrs/0016-kpi-parity-validator.md`
- `architecture/structurizr/adrs/0018-adopt-modular-monolith-and-compose-runtime.md` — جدید
- `architecture/structurizr/adrs/0019-use-postgresql-durable-agent-jobs-and-limited-runtime-access.md` — جدید
- `architecture/structurizr/adrs/0020-use-opentelemetry-and-langfuse.md` — جدید
- `plan-stage.md` — ثبت وضعیت فاز

`plan.md` تغییر نکرد.

### Validation

- Scope scan: پاس؛ هیچ فایل خارج از ADRها و فایل کنترلی `plan-stage.md` تغییر نکرد.
- Legacy link scan: پاس؛ هیچ ارجاعی به `final review`، `trash-data`، `ADR-V3-*` یا Control Register قدیمی در ADRها باقی نماند.
- ADR link validation: پاس؛ همه لینک‌های Markdown محلی معتبر هستند.
- Status validation: پاس؛ ADR-0011 همچنان `Proposed` است و ADR-0012 برابر `Superseded` است.
- Supersession chain: پاس؛ ADR-0012 و ADR-0018 به یکدیگر ارجاع معتبر دارند.
- New ADR structure: پاس؛ هر سه ADR جدید تمام بخش‌های الزامی Plan را دارند.
- Open Decision validation: پاس؛ هیچ مقدار باز به‌عنوان الزام نهایی ثبت نشد.
- Output Contract protection: پاس؛ Hash همه فایل‌های Reference با Baseline برابر است.
- `workspace.json` protection: پاس؛ Hash با Baseline برابر است.
- Whitespace و `git diff --check`: پاس.
- MCP Structurizr: فاز ۲ نقطه MCP ندارد. نقطه بعدی MCP پس از تغییر `workspace.dsl` در فاز ۴ است.

### تصمیم‌های باز

- Scheduler به‌صورت .NET Console یا Worker Service.
- نام نهایی DB Role محدود Agent Runtime.
- Migration از `agent_query_reader` یا حفظ آن.
- Langfuse managed یا self-hosted.
- OTLP/gRPC یا OTLP/HTTP برای Serviceهای Backend.

این تصمیم‌ها بخش‌های مستقل را متوقف نمی‌کنند و مقدار جدیدی برای آن‌ها ثبت نشد.

### Blockerها

Blocker وجود ندارد.

### Resume

نقطه دقیق Resume: **فاز ۳، قبل از نخستین تغییر، از `architecture/structurizr/README.md` و سپس `architecture/structurizr/docs/01-purpose-and-scope.md` شروع شود.**

## نتیجه فاز ۳ — مستندات پایه و README

وضعیت: تکمیل‌شده در 2026-11-19.

### نتیجه

- README روش استفاده از منابع، MCP، Structurizr Local روی کپی موقت، Mermaid export و URL validation را ثبت می‌کند.
- docs/01 Source policy، Scope و Agent Runtime boundary را ثبت می‌کند.
- docs/02 Technology Matrix، Modular Monolith، Containerها و shared-library boundary را ثبت می‌کند.
- docs/03 Daily Data Plane، Normalization و KPI Acceptance Plane را ثبت می‌کند.
- docs/04 Query Gateway و مرز محدود PostgreSQL برای Agent Runtime را ثبت می‌کند.
- docs/05 Durable Job، wake-up اختیاری، claim، validation، export و trace correlation را ثبت می‌کند.
- docs/06 Docker Compose، process و containerهای جدا، volumeها و observability profile اختیاری را ثبت می‌کند.
- docs/07 Acceptance coverage، parity، leakage، performance، cost و observability را ثبت می‌کند.
- docs/08 ریسک‌ها و 16 تصمیم باز را بدون مقدار اختراعی ثبت می‌کند.

### فایل‌های تغییرکرده

- `architecture/structurizr/README.md`
- `architecture/structurizr/docs/01-purpose-and-scope.md`
- `architecture/structurizr/docs/02-architecture-overview.md`
- `architecture/structurizr/docs/03-data-and-processing.md`
- `architecture/structurizr/docs/04-security-and-trust.md`
- `architecture/structurizr/docs/05-runtime-flows.md`
- `architecture/structurizr/docs/06-deployment-and-operations.md`
- `architecture/structurizr/docs/07-quality-attributes.md`
- `architecture/structurizr/docs/08-risks-and-open-issues.md`
- `plan-stage.md` — فقط ثبت وضعیت کنترلی؛ خارج از Commit فاز

### Validation

- Link scan: پاس.
- Source و legacy-reference scan: پاس؛ هیچ ارجاع فعال به منابع منسوخ باقی نماند.
- Technology Matrix: پاس و با ADR-0018 هماهنگ است.
- Security boundary: پاس و با ADR-0005 و ADR-0019 هماهنگ است.
- Runtime Flow: پاس و wake-up فقط Hint است.
- Output validation و export flow: پاس.
- Deployment: پاس و Docker Compose با process و containerهای جدا ثبت شده است.
- Observability: پاس و فقط OpenTelemetry و Langfuse در Scope هستند.
- Open Decision count: پاس؛ 16 تصمیم باز ثبت شده است.
- ADR Status consistency: پاس.
- `git diff --check`: پاس.
- Protected files و فایل‌های ممنوع: بدون تغییر.
- `plan.md`: Read-only و Hash آن بدون تغییر است.
- MCP Structurizr: فاز ۳ نقطه MCP ندارد. MCP در فاز ۴ و پس از تغییر `workspace.dsl` اجرا می‌شود.

### تصمیم‌های باز

16 تصمیم باز مصوب در docs/08 ثبت شده‌اند. این تصمیم‌ها بخش‌های مستقل را متوقف نمی‌کنند و مقدار جدیدی برای آن‌ها ثبت نشد.

### Blockerها

Blocker وجود ندارد.

### Resume

نقطه دقیق Resume: **فاز ۴، قبل از نخستین تغییر، از `architecture/structurizr/workspace.dsl` و بخش Source comments و Technology/Container definitions شروع شود. سپس MCP parse، validate و inspect اجرا شود.**

### Commit و Push فاز ۳

- Commit: `429f7fb9` (`docs: align Structurizr phase 3 documentation`)
- Commit scope: فقط ۹ فایل فاز ۳
- Push: موفق به `origin/main`
- تغییرات فاز ۲ و فایل‌های کنترلی وارد این Commit نشدند.

## نتیجه فاز ۴ — اصلاح مدل Structurizr

وضعیت: تکمیل‌شده در 2026-11-19.

### نتیجه

- Source commentها فقط منابع فعال معماری و Referenceهای Read-only را مشخص می‌کنند.
- Technology همه Containerها طبق Plan ثبت شد.
- `Normalizer`، `KPI Definition Preprocessor` و `Scripted Manager Input Adapter` اضافه شدند.
- OpenTelemetry Collector به‌عنوان تنها Container جدید و بدون Product Component اضافه شد.
- Langfuse به‌عنوان External Software System و وابستگی اختیاری و fail-open اضافه شد.
- همه رابطه‌های Product، Component، Scenario و Deployment دارای Technology صریح هستند.
- `!impliedRelationships false` حفظ شد.
- L3 Web Application، Deployment کامل و مجموعه ۱۶ View فعال شدند.
- Model Gateway در Report Scenario قرار گرفت و تعارض parent/child در L3 Agent رفع شد.
- State و Record به Product Component تبدیل نشدند.

### فایل‌های تغییرکرده

- `architecture/structurizr/workspace.dsl`
- `plan-stage.md` — فقط ثبت وضعیت و Resume

### Validation

- MCP parse: پاس.
- MCP validate: پاس.
- MCP inspect: صفر Finding عملیاتی.
- دو Finding مستندات و تصمیم‌ها مصنوعی هستند. علت، حذف موقت و درون‌حافظه‌ای `!docs` و `!adrs` برای MCP است. فایل اصلی این دو Directive را حفظ می‌کند.
- Product Component: دقیقاً ۵۰؛ Web برابر ۳، Backend برابر ۲۰، Worker برابر ۱۵، Scheduler برابر ۷ و Agent Runtime برابر ۵.
- View: دقیقاً ۱۶.
- Relationship بدون Technology: صفر.
- Deployment instance جداشده: صفر.
- Element خارج از View: صفر.
- `!impliedRelationships false`: حفظ شد.
- ارجاع فعال به `Docs/final review`، `Docs/trash-data` یا مسیر `submission/submission`: صفر.
- State/Record Component: صفر.
- `workspace.json` و فایل‌های Reference و Output Contract: بدون تغییر.
- `git diff --check`: پاس.

### تصمیم‌های باز

تصمیم‌های باز مصوب تغییر نکردند. مقدار یا الزام جدیدی برای آن‌ها ثبت نشد.

### Blockerها

Blocker وجود ندارد.

### Resume

نقطه دقیق Resume: **فاز ۵، قبل از نخستین تغییر، از `architecture/structurizr/docs/09-web-application-components.md` و سپس تطبیق ۵۴ Anchor و URL طبق `plan.md` شروع شود.**

## نتیجه فاز اصلاحی ۴.۱ — تثبیت Visual Layout

وضعیت: تکمیل‌شده در 2026-11-19.

### نتیجه

- هر ۱۶ View در Structurizr Local و روی یک کپی موقت از Workspace بازبینی شد.
- برای هر View، `autoLayout`، جهت، فاصله عناصر، includeها و endpoint رابطه‌ها بررسی شد.
- متن رابطه‌های بلند کوتاه شد. Technology، endpoint، Tag و معنی معماری ثابت ماند.
- C2 فقط Containerها، Storeها و سیستم‌های خارجی را نشان می‌دهد. Personها و رابطه‌های جزئی Telemetry در C2 نمایش داده نمی‌شوند.
- جزئیات OpenTelemetry Collector و Langfuse در Deployment و Viewهای مناسب باقی ماند.
- L3 Backend همه ۲۰ Product Component را نگه می‌دارد و ۳۲ رابطه اصلی را نشان می‌دهد. مسیرهای Detail و بازگشت در مدل و سناریوهای S8 و S9 باقی مانده‌اند.
- هیچ Component، Relationship یا تصمیم معماری حذف نشد.
- `workspace.json` و فایل‌های ممنوع تغییر داده نشدند.

### نتیجه بازبینی هر View

| View | نتیجه | یادداشت |
|---|---|---|
| `L1_SystemContext` | پاس | عناصر در قاب هستند و ارتباط‌های سطح سیستم خوانا هستند. |
| `L2_Containers` | پاس | فقط اطلاعات سطح Container نمایش داده می‌شود؛ جزئیات Observability حذف شده است. |
| `L3_2_WebApplicationComponents` | پاس | سه UI و Backend endpoint بدون هم‌پوشانی جدی نمایش داده می‌شوند. |
| `L3_3_RevisedBackendApiComponents` | پاس | ۲۰ Component و endpointهای Web، PostgreSQL و Agent Runtime با مسیرهای اصلی نمایش داده می‌شوند. |
| `L3_4_RevisedBackgroundWorkerComponents` | پاس | زنجیره Intake، Analytics و Report Evidence در قاب و خوانا است. |
| `L3_5_RevisedSchedulerReplayComponents` | پاس | Replay، Clock، Run Status و Acceptance path جدا و خوانا هستند. |
| `L3_6_AgentRuntimeComponents` | پاس | مرز Backend، Runtime، PostgreSQL و Model Provider روشن است. |
| `D1_EvaluationCompose` | پاس | همه Deployment instanceها در قاب هستند؛ Collector و Langfuse در مرز Observability قرار دارند. |
| `S7_ReportGenerationScenario` | پاس | ۲۳ گام شماره‌دار بدون فلش معلق نمایش داده می‌شوند. |
| `S8_ManagerDecisionScenarios` | پاس | ۴۶ گام شماره‌دار و endpointهای review، validation و durable job حفظ شدند. |
| `S9_MeetingMinutesUploadScenario` | پاس | ۴۶ رابطه سناریو، archive، parse، review و revision را کامل نشان می‌دهند. |
| `S10_FailureAndFallback` | پاس | مسیر failure، fallback و observability خوانا است. |
| `S11_KpiTranslationAndParity` | پاس | Translation، validation و parity بدون هم‌پوشانی نمایش داده می‌شوند. |
| `S12_OrganizationConfigurationD1` | پاس | Intake، validation و D+1 activation خوانا هستند. |
| `S13_ScriptedManagerInputReplay` | پاس | Adapter، Backend API و acceptance endpoint در یک مسیر روشن هستند. |
| `S14_LateCorrectedDataRestatement` | پاس | Intake، recalculation و republishing در یک مسیر روشن هستند. |

### فایل‌های تغییرکرده

- `architecture/structurizr/workspace.dsl`
- `plan-stage.md` — فقط ثبت نتیجه و Resume

### Validation

- MCP parse: پاس.
- MCP validate: پاس.
- MCP inspect: صفر Finding عملیاتی.
- دو Finding مستندات و تصمیم‌ها مصنوعی هستند. علت، حذف موقت و درون‌حافظه‌ای `!docs` و `!adrs` برای MCP است. فایل اصلی هر دو Directive را حفظ می‌کند.
- Product Component: دقیقاً ۵۰.
- View: دقیقاً ۱۶.
- Relationship: تعداد ۲۹۵؛ Relationship بدون Technology برابر صفر.
- `!impliedRelationships false`: حفظ شد.
- بازبینی بصری Structurizr Local: ۱۶ از ۱۶ View پاس.
- عنصر خارج از قاب، فلش معلق، هم‌پوشانی جدی یا متن بریده: مشاهده نشد.
- `workspace.json`: خارج از Commit و بدون ویرایش دستی در این فاز.
- `git diff --check`: پاس.

### تصمیم‌های باز

تصمیم‌های باز مصوب تغییر نکردند. مقدار یا الزام جدیدی برای آن‌ها ثبت نشد.

### Blockerها

Blocker وجود ندارد.

### Resume

نقطه دقیق Resume: **فاز ۵، قبل از نخستین تغییر، از `architecture/structurizr/docs/09-web-application-components.md` و سپس تطبیق ۵۴ Anchor و URL طبق `plan.md` شروع شود.**
