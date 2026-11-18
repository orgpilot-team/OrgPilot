<proposed_plan>
# Plan نهایی تکمیل معماری DIDRAH در Structurizr

این Plan فقط فایل‌های معماری Structurizr را تغییر می‌دهد. فایل‌های پروژه در این مرحله تغییر نمی‌کنند. در اجرای بعدی نیز تغییرات فعلی کاربر باید حفظ شوند.

## 1. Current-state findings

### وضعیت Working Tree

- `architecture/structurizr/workspace.dsl` تغییر کاربر دارد.
- `architecture/structurizr/workspace.json` تغییر کاربر دارد.
- `architecture/structurizr/docs/10-backend-api-components.md` یک Proof of Concept جدید است.
- Mermaidهای قبلی در Working Tree حذف شده‌اند.
- `Docs/trash-data/` یک پوشه جدید و خارج از Scope این Task است.
- تعداد زیادی حذف دیگر در `Docs/` وجود دارد. این تغییرات متعلق به کاربر هستند. اجرای Plan نباید آن‌ها را Restore یا Reset کند.

قبل از هر تغییر آینده باید این Baseline ثبت شود:

```powershell
git status --short
git diff -- architecture/structurizr/workspace.dsl
git diff -- architecture/structurizr/workspace.json
```

Hash فایل‌های No-change نیز باید ثبت شود.

### وضعیت مدل فعلی

مدل فعلی 47 Component دارد:

- Web Application: 3
- Backend API: 20
- Background Worker: 13
- Scheduler/Replay: 6
- Agent Runtime: 5

سه Component لازم هنوز در مدل نیستند:

- Normalizer
- KPI Definition Preprocessor
- Scripted Manager Input Adapter

تعداد نهایی Product Componentها 50 خواهد بود.

چهار Store/Contract نیز جدا از Componentها هستند:

- PostgreSQL Product Database
- Protected File Archive
- Input Dataset Contract
- Submission Output Contract

### نتیجه فعلی MCP Structurizr

نسخه درون‌حافظه‌ای DSL، پس از حذف موقت `!docs` و `!adrs`، با موفقیت Parse و Validate شد.

Inspect فعلی 143 Finding دارد:

- 131 Relationship بدون Technology
- 6 Deployment Instance قطع‌شده
- 4 Element خارج از View
- 1 Missing Documentation مصنوعی
- 1 Missing Decisions مصنوعی

چهار Element خارج از View:

- Conversational Assistant UI
- Role-Based Dashboard UI
- Workflow Control Room UI
- Model Gateway در Report Scenario

دو Finding مربوط به Documentation و Decisions فقط نتیجه حذف موقت Directiveها هستند.

### تعارض‌های فعلی

- `workspace.dsl` هنوز به `Docs/final review/proposed-architecture.md` ارجاع دارد.
- `docs/01` و `docs/08` به `Docs/final review` ارجاع زنده دارند.
- ADR-0001 تا ADR-0011 به Control Register قدیمی ارجاع دارند.
- ADR-0012 هنوز Single Image و `docker run` را Accepted می‌داند.
- `Submission Exporter` هنوز مسیر اشتباه `OUTPUT_DIR/submission/...` را توصیف می‌کند.
- ADR-0015 تغییر `brief_schema.json` را پیشنهاد می‌کند. این پیشنهاد باید حذف شود.
- Technology کانتینرها هنوز با عبارت‌هایی مانند `framework open` ثبت شده است.
- L3 Web Application وجود ندارد.
- Observability boundary در مدل وجود ندارد.
- Acceptance Test Harness و KPI Parity Validator موجود هستند، اما مرز SQLite و Product Runtime باید دقیق‌تر شود.

## 2. Locked architectural decisions

### منابع معتبر

منبع اصلی معماری فقط این موارد است:

- `architecture/structurizr/workspace.dsl`
- `architecture/structurizr/docs/`
- `architecture/structurizr/adrs/`

این منابع باید با موارد زیر تطبیق داده شوند:

- بریف رسمی پروژه
- پیام‌های تکمیلی TA
- دیتاست و قراردادهای ماشین‌خوان ارزیابی

قواعد منبع:

- `Docs/final review/` Source of Truth نیست.
- `Docs/trash-data/` Source of Truth نیست.
- هیچ‌کدام از این دو پوشه تغییر یا حذف نمی‌شوند.
- هیچ لینک زنده از Structurizr به این دو پوشه باقی نمی‌ماند.
- اطلاعات قدیمی فقط پس از تطبیق با بریف، TA یا قرارداد رسمی وارد معماری می‌شود.
- اطلاعات مبهم به Open Decision تبدیل می‌شود.

### Technology و Deployment

- Web: React، TypeScript و Vite
- Backend API: ASP.NET Core روی .NET 10 LTS
- Worker: .NET 10 Worker Service
- Scheduler: .NET 10 Console یا Worker Process
- Agent Runtime: Python 3.12، LangGraph و Pydantic
- Product Database: PostgreSQL 18
- .NET data access: EF Core و Npgsql
- Job claim و Approved SQL execution: Npgsql مستقیم
- API: REST/JSON و OpenAPI
- Deployment: Docker Compose
- معماری .NET: Modular Monolith با Libraryهای مشترک
- API، Worker و Scheduler Process و Container جدا دارند.
- PostgreSQL منبع حقیقت Job، Lease، Attempt، Dependency و Replay State است.
- `!impliedRelationships false` حفظ می‌شود.

موارد زیر وارد Scope نمی‌شوند:

- Hangfire
- Redis
- RabbitMQ
- Kafka
- Kubernetes
- Service Mesh
- Microservice جدید
- Grafana
- Tempo
- Jaeger
- Prometheus
- Loki
- Datadog

### Agent Runtime boundary

- Backend Job را به‌صورت Durable در PostgreSQL ثبت می‌کند.
- Backend پس از Commit، `job_id` را برمی‌گرداند.
- Backend می‌تواند یک Wake-up احرازشده و اختیاری ارسال کند.
- Wake-up فقط Hint است.
- Agent Runtime Job را از PostgreSQL Claim می‌کند.
- Agent Runtime Scope، Context و Evidence reference را دوباره بارگذاری می‌کند.
- Agent Runtime Candidate یا Failure را ثبت می‌کند.
- Agent Runtime SQL دلخواه روی داده تجاری اجرا نمی‌کند.
- Agent Runtime از Evidence Service و Query Gateway برای داده تجاری استفاده می‌کند.
- Agent Runtime هیچ Migration یا Policy change انجام نمی‌دهد.

### SQLite و Acceptance

- SQLite Product Database یا Runtime Container نیست.
- SQLite فقط داخل Acceptance Test Harness اجرا می‌شود.
- Reference SQL و KPI Dictionary تغییر نمی‌کنند.
- KPI Parity Validator در محدوده Scheduler/Replay و Acceptance قرار دارد.

### Output Contract

- سه فایل Output Contract مرجع و Read-only هستند.
- Decision Effect یک رکورد داخلی و Versioned در PostgreSQL است.
- Decision Effect ساختار Output Contract را تغییر نمی‌دهد.
- Exporter فقط فیلدهای مجاز Schema مرجع را صادر می‌کند.
- مسیر خروجی مستقیماً از `OUTPUT_DIR` ساخته می‌شود.

### Observability

- فقط OpenTelemetry و Langfuse در Scope هستند.
- `otel-collector` یک Infrastructure Container اختیاری است.
- Langfuse یک External Observability System است، مگر Self-hosting بعداً تصویب شود.
- نبود Langfuse Core Workflow را متوقف نمی‌کند.
- Full telemetry در PostgreSQL محصول ذخیره نمی‌شود.

## 3. Open decisions

| تصمیم | وضعیت و محل ثبت |
|---|---|
| Scheduler به‌صورت .NET Console یا Worker Service | Open در ADR-0018 |
| نام نهایی DB Role محدود Agent Runtime | Open در ADR-0019 |
| Migration از `agent_query_reader` یا حفظ آن | Open در ADR-0019 |
| Python PostgreSQL driver | Open در docs/08 |
| Langfuse managed یا self-hosted | Open در ADR-0020 |
| OTLP/gRPC یا OTLP/HTTP برای Serviceهای Backend | Configuration decision در docs/06 |
| Model/provider | Open در docs/08 |
| Model call timeout | Open در docs/08 |
| Agent Job deadline | Open در docs/08 |
| Retry count | Open در docs/08 |
| Dead-letter policy | Open در docs/08 |
| Reconciliation cadence | Open در docs/08 |
| Fallback content | Open در docs/08 |
| LangGraph node boundaries | Open در docs/08 |
| Retention و backup frequency | Open در docs/08 |
| RPO و RTO | Open در docs/08 |

هیچ مقدار پیشنهادی در این موارد نباید با Status برابر `Accepted` ثبت شود.

## 4. File-by-file change list

### مدل و راهنمای Structurizr

| فایل | دلیل تغییر | بخش‌های تغییر | موارد ممنوع | Validation |
|---|---|---|---|---|
| `architecture/structurizr/workspace.dsl` | همگام‌سازی C4 با تصمیم‌های جدید | Source comments، Technology، سه Component، OTel Collector، Langfuse، relationships، URLs، views، deployment | تغییر `!impliedRelationships false`، ساخت State به‌عنوان Component، تغییر Scope قراردادها | MCP parse/validate/inspect/export و Structurizr Local |
| `architecture/structurizr/README.md` | مستقل‌کردن روش استفاده از Structurizr | Source policy، MCP workflow، Local validation، Mermaid generation، URL validation | تبدیل README به Source of Truth معماری | link scan و اجرای دستورهای مستند |
| `architecture/structurizr/workspace.json` | تغییر ندارد | هیچ بخش | hand-edit، reset، overwrite یا regeneration روی نسخه کاربر | Hash قبل و بعد باید یکسان باشد |

### Documentation

| فایل | دلیل تغییر | بخش‌های تغییر | موارد ممنوع | Validation |
|---|---|---|---|---|
| `docs/01-purpose-and-scope.md` | حذف منابع قدیمی و تثبیت Scope | Source policy، in-scope، out-of-scope، Agent boundary | لینک به `final review` یا `trash-data` | link scan و review با بریف |
| `docs/02-architecture-overview.md` | ثبت Technology Matrix و Modular Monolith | Containers، processes، shared libraries، API contract | معرفی Microservice یا Broker | تطبیق با L2 و ADR-0018 |
| `docs/03-data-and-processing.md` | تکمیل Daily Data Plane و KPI Acceptance Plane | Normalization، PostgreSQL 18، Reference SQLite، KPI parity | نمایش SQLite به‌عنوان Product DB | تطبیق با ADR-0002 و ADR-0016 |
| `docs/04-security-and-trust.md` | تکمیل Agent DB boundary | Role contract، table/view access، forbidden access، Query Gateway path | Role جدید بدون ADR، دسترسی Agent به جدول‌های تجاری | review با ADR-0005 و ADR-0019 |
| `docs/05-runtime-flows.md` | ثبت Flowهای Durable Job و Output | job commit، optional wake-up، claim، validation، export | Wake-up به‌عنوان queue یا Source of Truth | scenario review و DSL relationships |
| `docs/06-deployment-and-operations.md` | جایگزینی Single Image با Compose | Services، volumes، PostgreSQL 18، optional observability profile | Kubernetes، Service Mesh، ابزار اضافی | تطبیق با D1 و ADR-0018 |
| `docs/07-quality-attributes.md` | ثبت Acceptance و Observability | replay، parity، leakage، performance، trace correlation | افزودن backend مشاهده‌پذیری دیگر | تطبیق با ADR-0016 و ADR-0020 |
| `docs/08-risks-and-open-issues.md` | حذف Control Register قدیمی و تمرکز Open Decisionها | جدول Open Decision، risk owner، decision location | ارجاع به پوشه‌های منسوخ | link scan و تطبیق با ADR statusها |
| `docs/09-web-application-components.md` | مستندسازی سه Component وب | Container scope، trust boundary، Component Map، سه Anchor | Component جدید یا business logic در UI | Anchor و URL test |
| `docs/10-backend-api-components.md` | تکمیل Proof of Concept برای 20 Component | Container contract و 20 بخش Component | حذف چهار URL فعلی کاربر بدون جایگزین | شمارش 20 Anchor و Structurizr Local |
| `docs/11-background-worker-components.md` | مستندسازی 15 Component Worker | Daily processing، KPI preprocessing و Component sections | Agent graph یا publication در Worker | شمارش 15 Anchor |
| `docs/12-scheduler-replay-components.md` | مستندسازی هفت Component Scheduler | Replay، Harness، Parity Validator، Scripted Adapter | SQLite به‌عنوان Container | شمارش هفت Anchor |
| `docs/13-agent-runtime-components.md` | مستندسازی پنج Component Agent | claim، graph، checkpoint، conversation، model gateway | SQL تجاری مستقیم، KPI calculation، publication | شمارش پنج Anchor |
| `docs/14-stores-and-contracts.md` | مستندسازی چهار Store/Contract | ownership، mutability، access، retention status، authority | ایجاد Store جدید یا Schema claim | شمارش چهار Anchor |

### ADRهای موجود

| فایل | دلیل تغییر | بخش‌های تغییر | موارد ممنوع | Validation |
|---|---|---|---|---|
| `adrs/0001-unified-data-intake-and-preparation.md` | حذف Source قدیمی | Source و traceability | تغییر Decision بدون Requirement | link scan |
| `adrs/0002-use-postgresql-and-verify-kpi-parity.md` | ثبت PostgreSQL 18 و SQLite داخل Harness | Context، Decision، Consequences | Product SQLite | تطبیق با docs/03 |
| `adrs/0003-preserve-published-report-versions.md` | حذف Source قدیمی | Source | تغییر version policy | link scan |
| `adrs/0004-continue-publication-with-incomplete-sources.md` | حذف Source قدیمی | Source | تغییر publication behavior | link scan |
| `adrs/0005-enforce-scoped-read-only-queries.md` | تکمیل Query Gateway و Agent restriction | Decision، permissions، consequences، Source | SQL دلخواه Agent | تطبیق با docs/04 |
| `adrs/0006-use-deterministic-signal-lifecycle.md` | حذف Source قدیمی | Source | تغییر Signal lifecycle | link scan |
| `adrs/0007-assign-workflow-and-stage-owners.md` | حذف Source قدیمی | Source | تغییر ownership | link scan |
| `adrs/0008-use-one-bounded-agent.md` | تکمیل Durable Job protocol | Backend commit، optional wake-up، Runtime claim | Wake-up به‌عنوان Source of Truth | تطبیق با Agent L3 |
| `adrs/0009-publish-manager-reports-independently.md` | حذف Source قدیمی | Source | تغییر independence policy | link scan |
| `adrs/0010-require-human-decision-control.md` | حذف Source قدیمی | Source | خودکارسازی تصمیم انسانی | link scan |
| `adrs/0011-retain-replay-and-audit-evidence.md` | حذف Source قدیمی | Source | تغییر retention بدون تصمیم | link scan |
| `adrs/0012-evaluation-deployment-profile.md` | Decision فعلی منسوخ است | Status برابر Superseded و لینک به ADR-0018 | بازنویسی تاریخچه ADR | ADR link validation |
| `adrs/0013-submission-exporter.md` | اصلاح مسیر و امنیت Export | direct join، containment، atomic rename، receipt | تغییر Output Schema | path acceptance tests |
| `adrs/0015-decision-effect-evaluator.md` | حذف الزام تغییر Schema مرجع | internal record، export mapping، versioning | تغییر `brief_schema.json` | تطبیق با Schema read-only |
| `adrs/0016-kpi-parity-validator.md` | انتقال کامل SQLite به Harness | execution flow، comparisons، receipts | SQLite Runtime Container | تطبیق با Scheduler L3 |

ADR-0014 و ADR-0017 فقط در صورت وجود تعارض واقعی تغییر می‌کنند. تغییر صرفاً برای هماهنگی نگارشی مجاز نیست.

### ADRهای جدید

| فایل | دلیل تغییر | بخش‌های اصلی | موارد ممنوع | Validation |
|---|---|---|---|---|
| `adrs/0018-adopt-modular-monolith-and-compose-runtime.md` | ثبت Technology Stack و Deployment جدید | .NET 10، React، Python، PostgreSQL 18، shared libraries، Compose | Microservice یا Broker جدید | تطبیق با L2 و D1 |
| `adrs/0019-use-postgresql-durable-agent-jobs-and-limited-runtime-access.md` | ثبت Job protocol و Agent DB boundary | jobs، leases، attempts، wake-up، allowed/forbidden access | دسترسی Agent به همه داده تجاری | security review |
| `adrs/0020-use-opentelemetry-and-langfuse.md` | ثبت observability محدود | SDKs، collector، Langfuse، traceparent، fail-open | backend مشاهده‌پذیری دیگر | تطبیق با docs/06 و docs/07 |

### Mermaid Artifactها

پس از تثبیت DSL فقط Artifactهای این Viewها تولید می‌شوند:

- `structurizr-L1_SystemContext.mmd`
- `structurizr-L2_Containers.mmd`
- `structurizr-L3_2_WebApplicationComponents.mmd`
- `structurizr-L3_3_RevisedBackendApiComponents.mmd`
- `structurizr-L3_4_RevisedBackgroundWorkerComponents.mmd`
- `structurizr-L3_5_RevisedSchedulerReplayComponents.mmd`
- `structurizr-L3_6_AgentRuntimeComponents.mmd`
- `structurizr-D1_EvaluationCompose.mmd`
- `structurizr-S7_ReportGenerationScenario.mmd`
- `structurizr-S8_ManagerDecisionScenarios.mmd`
- `structurizr-S9_MeetingMinutesUploadScenario.mmd`
- `structurizr-S10_FailureAndFallback.mmd`
- `structurizr-S11_KpiTranslationAndParity.mmd`
- `structurizr-S12_OrganizationConfigurationD1.mmd`
- `structurizr-S13_ScriptedManagerInputReplay.mmd`
- `structurizr-S14_LateCorrectedDataRestatement.mmd`

فایل‌های قدیمی `S1` تا `S6` و `L3_2_BackgroundWorkerComponents` Restore نمی‌شوند، مگر View key فعال متناظر وجود داشته باشد.

## 5. Structurizr model changes

### Containerها

Technology رشته‌های فعلی با مقادیر زیر جایگزین می‌شوند:

- Web Application: `React 19, TypeScript, Vite`
- Backend API: `ASP.NET Core, .NET 10 LTS, REST/JSON, OpenAPI`
- Background Worker: `.NET 10 Worker Service`
- Scheduler and Replay Runner: `.NET 10 Console or Worker Process`
- Agent Runtime: `Python 3.12, LangGraph, Pydantic`
- PostgreSQL: `PostgreSQL 18`
- Protected File Archive: `Protected mounted filesystem or compatible object storage`
- OpenTelemetry Collector: `OpenTelemetry Collector, optional Compose service`

Langfuse به‌عنوان External Software System مدل می‌شود.

`otel-collector` تنها Container جدید است. Requirement مستقیم Observability این Container را توجیه می‌کند. این Container Product Component ندارد و در شمارش 50 Component وارد نمی‌شود.

### Componentهای جدید

فقط این سه Component اضافه می‌شوند:

1. `Normalizer`
   - Requirement: جداسازی parsing، normalization و Data Quality
   - Owner: Background Worker
2. `KPI Definition Preprocessor`
   - Requirement: ترجمه و Versioning تعریف PostgreSQL KPI
   - Owner: Background Worker
3. `Scripted Manager Input Adapter`
   - Requirement: Replay ورودی‌های رسمی ارزیابی
   - Owner: Scheduler/Replay

### مواردی که Component نمی‌شوند

- Agent Job
- Lease
- Attempt
- Dependency
- Replay State
- Decision Effect
- Inactive Organization Revision
- Activation Boundary
- KPI Candidate
- Parity Receipt
- Export Receipt
- Trace Context
- Versioned KPI SQL Artifact

این موارد Record یا State هستند.

### Viewها

16 View قبلی حفظ و تکمیل می‌شوند. View جدید Observability ساخته نمی‌شود. OTel Collector و Langfuse در L2 و Deployment View دیده می‌شوند.

- L3 Web اضافه می‌شود.
- L3 Agent Parent/child conflict رفع می‌شود.
- Report Scenario شامل Model Gateway می‌شود.
- Deployment View شامل Service instances، PostgreSQL، mounts، Collector و Langfuse egress می‌شود.
- SQLite در Deployment View دیده نمی‌شود.

## 6. Documentation structure

هر فایل Container این ساختار ثابت را دارد:

1. Purpose and Scope
2. Runtime Technology
3. Trust Boundary
4. Allowed Responsibilities
5. Forbidden Responsibilities
6. Component Map
7. Internal Relationships
8. External Relationships
9. Component Sections
10. Container-level Open Issues

هر Component این بخش‌ها را دارد:

- DSL identifier
- Display name
- Purpose
- Responsibilities
- Inputs
- Outputs
- Owned state
- Dependencies
- Security boundary
- Forbidden responsibilities
- Failure behavior
- Idempotency
- Observability
- Related ADRs
- Open issues

### Anchor inventory

- Web: 3 Anchor
- Backend: 20 Anchor
- Worker: 15 Anchor
- Scheduler: 7 Anchor
- Agent: 5 Anchor
- Stores/Contracts: 4 Anchor

مجموع: 54 Anchor

Anchorها همان فهرست تأییدشده قبلی هستند. سه Anchor جدید Component:

- `normalizer`
- `kpi-definition-preprocessor`
- `scripted-manager-input-adapter`

چهار Store/Contract Anchor:

- `postgresql-product-database`
- `protected-file-archive`
- `input-dataset-contract`
- `submission-output-contract`

URL تمام Elementهای مستندشده:

```dsl
url "{workspace}/documentation/DIDRAH#<anchor>"
```

Viewها فایل Documentation مستقل ندارند. View فقط مدل را نمایش می‌دهد.

## 7. ADR additions and revisions

ترتیب اجرا:

1. Source referenceهای ADR-0001 تا ADR-0011 پاک یا با Requirement رسمی جایگزین شوند.
2. ADR-0012 به Superseded تغییر کند.
3. ADR-0018 Technology و Compose را ثبت کند.
4. ADR-0008 و ADR-0019 Job boundary را بدون تعارض ثبت کنند.
5. ADR-0013 Output path و atomic export را ثبت کند.
6. ADR-0015 Decision Effect را Internal-only ثبت کند.
7. ADR-0016 SQLite Harness و Parity را ثبت کند.
8. ADR-0020 Observability را ثبت کند.
9. Status، link و supersession chain همه ADRها Validate شود.

هر ADR جدید باید این بخش‌ها را داشته باشد:

- Status
- Context
- Decision
- Alternatives rejected
- Consequences
- Security impact
- Operational impact
- Related requirements
- Related model elements
- Open decisions

## 8. Technology Matrix

| Element | Technology | محدودیت |
|---|---|---|
| Web Application | React + TypeScript + Vite | بدون business calculation |
| Backend API | ASP.NET Core روی .NET 10 LTS | Modular Monolith process |
| Background Worker | .NET 10 Worker Service | deterministic processing |
| Scheduler/Replay | .NET 10 Console یا Worker | بدون DB mutation خارج از job/replay contract |
| Agent Runtime | Python 3.12 + LangGraph + Pydantic | Candidate generation only |
| Product Database | PostgreSQL 18 | تنها Product DB |
| SQLite | Embedded در Acceptance Test Harness | فقط Reference Oracle |
| .NET ORM | EF Core + Npgsql | CRUD و transactionهای عادی |
| Direct .NET SQL | Npgsql | Job claim و Approved KPI SQL |
| API | REST/JSON + OpenAPI | traceparent propagation |
| Deployment | Docker Compose | Processهای جدا |
| Tracing | OpenTelemetry | SDK و OTLP |
| Agent observability | Langfuse | Optional و fail-open |

Shared .NET libraries می‌توانند این موارد را نگه‌داری کنند:

- Domain contracts
- Application contracts
- PostgreSQL persistence primitives
- OpenAPI DTOs
- Authorization primitives
- Job state model
- Output validation interfaces
- Observability conventions

Shared library به معنی shared database ownership یا in-process deployment نیست.

## 9. Container and Component ownership

| Container | Owner responsibilities | Component count |
|---|---|---:|
| Web | RTL UI، accessibility، authorized presentation | 3 |
| Backend API | identity، authorization، routing، durable job creation، validation، publication، export | 20 |
| Worker | ingestion، normalization، DQ، snapshot، KPI، workflow، signal، evidence | 15 |
| Scheduler/Replay | time، replay، acceptance، parity، scripted inputs | 7 |
| Agent Runtime | claim، graph execution، candidate/failure، checkpoint | 5 |
| OTel Collector | OTLP receive/export | 0 Product Component |

### Backend ownership

Backend مالک این عملیات است:

- Durable job creation
- Authorization
- Evidence and Query boundary
- Candidate validation
- Job status delivery
- Publication
- Submission export

Backend Agent graph اجرا نمی‌کند.

### Agent ownership

Agent Runtime فقط مالک این Stateها است:

- Job claim metadata
- Lease و Attempt update
- LangGraph checkpoint
- Conversation state
- Candidate/Outcome
- Failure record
- Job-scoped Evidence reference

Agent Runtime مالک داده تجاری، KPI Definition، Organization Policy یا Output publication نیست.

### Acceptance ownership

Acceptance Test Harness مالک این عملیات ارزیابی است:

- 30-day replay
- KPI parity
- hidden-data tests
- regression tests
- leakage tests
- output-contract validation
- performance checks
- cost checks

## 10. Relationship change list

روابط Container-level صریح:

| From | To | Technology |
|---|---|---|
| Web | Backend | HTTPS, REST/JSON, W3C traceparent |
| Backend | PostgreSQL | PostgreSQL protocol over TLS, EF Core/Npgsql |
| Backend | Protected Archive | Controlled filesystem API |
| Backend | Submission Output | Controlled filesystem I/O |
| Backend | Agent Runtime | Authenticated HTTPS wake-up with job_id |
| Worker | PostgreSQL | PostgreSQL protocol over TLS, EF Core/Npgsql |
| Worker | Input Dataset | Read-only filesystem |
| Worker | Protected Archive | Controlled filesystem I/O |
| Scheduler | Backend | HTTPS, REST/JSON |
| Scheduler | PostgreSQL | PostgreSQL protocol over TLS برای replay state مجاز |
| Agent Runtime | PostgreSQL | Restricted PostgreSQL role |
| Agent Runtime | Backend | HTTPS Evidence/Query/Validation API |
| Agent Runtime | LLM Provider | HTTPS/JSON |
| Web | OTel Collector | OTLP/HTTP، در صورت فعال بودن |
| Backend | OTel Collector | OTLP |
| Worker | OTel Collector | OTLP |
| Scheduler | OTel Collector | OTLP |
| Agent Runtime | OTel Collector | OTLP |
| OTel Collector | Langfuse | OTLP export |

قواعد Agent/PostgreSQL relationship:

- دسترسی فقط به Agent Job، Lease، Attempt، Checkpoint، Conversation، Candidate و job-scoped Evidence view مجاز است.
- دسترسی مستقیم به Orders، Customers، Organization و KPI facts مجاز نیست.
- داده تجاری فقط از Backend Evidence Service یا Query Gateway دریافت می‌شود.

Relationshipهای Component و Scenario نیز باید Technology داشته باشند. Inspect نباید Relationship بدون Technology گزارش کند.

## 11. Output path and validation rules

مسیرهای صحیح:

```text
OUTPUT_DIR/briefs/day_XXX/<manager_id>.json
OUTPUT_DIR/qa/<question_id>.json
```

برای `OUTPUT_DIR=/submission`:

```text
/submission/briefs/day_XXX/<manager_id>.json
/submission/qa/<question_id>.json
```

مسیر ممنوع:

```text
OUTPUT_DIR/submission/briefs/...
```

### Submission Exporter

Exporter باید:

1. Output path را با direct join بسازد.
2. مسیر نهایی را Resolve کند.
3. Path containment را کنترل کند.
4. Absolute path injection و `..` را رد کند.
5. فقط Output معتبر را قبول کند.
6. ابتدا فایل موقت را در همان filesystem بنویسد.
7. Flush و close را کامل کند.
8. Atomic rename انجام دهد.
9. Content hash ثبت کند.
10. Export Receipt را در PostgreSQL ثبت کند.
11. در Receipt، `trace_id` و artifact path نسبی را ثبت کند.

### Output Validator

Validator باید:

- فایل را با Schema مرجع Validate کند.
- Scope و Evidence reference را Validate کند.
- Path containment را قبل از Export بررسی کند.
- Validation Receipt ثبت کند.
- Schema مرجع را تغییر ندهد.

### Decision Effect mapping

Decision Effect کامل فقط در PostgreSQL ذخیره می‌شود.

Export mapping:

- `evaluated + improved|worsened|no_change` → مقدار مجاز `effect_direction`
- `too_early` → مقدار مجاز `too_early`
- `insufficient_data` یا `not_isolatable` → `effect_direction` صادر نمی‌شود؛ محدودیت فقط در `detail_fa` مجاز ثبت می‌شود.
- هیچ فیلد داخلی جدید به JSON خروجی اضافه نمی‌شود.

## 12. Observability design

### Instrumentation

- Web از OpenTelemetry JavaScript SDK استفاده می‌کند.
- API، Worker و Scheduler از OpenTelemetry .NET SDK استفاده می‌کنند.
- Agent Runtime از OpenTelemetry Python instrumentation استفاده می‌کند.
- W3C `traceparent` در REST callها منتقل می‌شود.
- `trace_id` در Run، Job، Validation Receipt، Publication Receipt، Parity Receipt و Export Receipt ثبت می‌شود.
- Jobهای asynchronous از Span Link یا persisted trace context استفاده می‌کنند.

### Collector

- `otel-collector` یک Compose service اختیاری است.
- Collector OTLP دریافت می‌کند.
- Collector telemetry را به Langfuse صادر می‌کند.
- Product serviceها نباید به availability آن وابسته باشند.
- Queue یا retry داخلی Collector نباید جای Product job durability را بگیرد.

### Langfuse

Langfuse فقط برای این موارد است:

- Agent trace
- LLM call
- Token usage
- Cost
- Agent evaluation
- Prompt/model metadata مجاز

Langfuse نباید raw restricted business data، secret، full document یا unauthorized manager context دریافت کند.

### PostgreSQL

PostgreSQL فقط correlation metadata و receiptهای معماری را نگه‌داری می‌کند:

- `trace_id`
- `run_id`
- `job_id`
- receipt ID
- status
- timestamps

Span، log و full telemetry در PostgreSQL محصول ذخیره نمی‌شوند.

## 13. Validation sequence

1. Git baseline و Hash فایل‌های محافظت‌شده ثبت شود.
2. تمام ارجاع‌های `final review` و `trash-data` در Structurizr جست‌وجو شود.
3. ADRها ابتدا اصلاح شوند.
4. docs/01 تا docs/08 با ADRها هماهنگ شوند.
5. `workspace.dsl` بر اساس ADRها اصلاح شود.
6. Component inventory دوباره استخراج شود.
7. شمارش باید دقیقاً 50 Component باشد.
8. شش فایل Component Documentation کامل شوند.
9. شمارش Anchorها باید 54 باشد.
10. URLهای DSL با Anchorها مقایسه شوند.
11. MCP `parse` اجرا شود.
12. MCP `validate` اجرا شود.
13. MCP `inspect` اجرا شود.
14. اگر MCP روی `!docs` یا `!adrs` متوقف شد، فقط نسخه درون‌حافظه‌ای بدون این دو Directive بررسی شود.
15. دو Finding مصنوعی Documentation/Decision جدا ثبت شوند.
16. همه 16 View با MCP Export شوند.
17. از پاسخ JSON فقط فیلد `definition` در `.mmd` نوشته شود.
18. JSON خام MCP ذخیره نشود.
19. Structurizr Local با یک کپی موقت اجرا شود.
20. Local نباید `workspace.json` مخزن را تغییر دهد.
21. 54 لینک داخلی در Local باز و بررسی شوند.
22. `example_brief.json` به‌صورت Read-only با `brief_schema.json` Validate شود.
23. Hash همه No-change files با Baseline مقایسه شود.
24. Git diff نهایی فقط فایل‌های مجاز را نشان دهد.

## 14. Acceptance criteria

Plan اجراشده فقط در این شرایط کامل است:

- هیچ فایل `Docs/final review/` تغییر نکرده باشد.
- هیچ فایل `Docs/trash-data/` تغییر یا حذف نشده باشد.
- هیچ ارجاع زنده به این دو پوشه در Structurizr باقی نمانده باشد.
- `workspace.json` نسبت به Baseline تغییر نکرده باشد.
- `workspace.dsl` تنها منبع مدل C4 باشد.
- 50 Product Component وجود داشته باشد.
- چهار Store/Contract مستند شده باشد.
- 54 Anchor و 54 URL داخلی معتبر وجود داشته باشد.
- سه Component جدید فقط با Requirement مشخص اضافه شده باشند.
- OTel Collector تنها Infrastructure Container جدید باشد.
- State یا Record به Component تبدیل نشده باشد.
- Technology Matrix در DSL، docs و ADRها یکسان باشد.
- هیچ Technology ممنوع وارد مدل نشده باشد.
- Agent wake-up فقط Hint باشد.
- Agent Runtime Job را از PostgreSQL Claim کند.
- Agent DB access محدود و مستند باشد.
- SQLite فقط در Acceptance Test Harness باشد.
- Output Contractهای مرجع بدون تغییر باشند.
- مسیر `submission/submission` تولید نشود.
- Exporter atomic write، containment، hash و receipt داشته باشد.
- Decision Effect فقط Internal Record باشد.
- OpenTelemetry و Langfuse تنها ابزارهای Observability باشند.
- Observability fail-open و optional باشد.
- MCP Parse و Validate موفق باشند.
- Inspect هیچ Finding عملیاتی نداشته باشد.
- شش disconnected Deployment Instance رفع شده باشند.
- 131 Missing Technology رفع شده باشند.
- چهار out-of-view Finding رفع شده باشند.
- تمام 16 View Export شوند.
- Structurizr Local همه docs، ADRها، URLها و Viewها را نمایش دهد.

## 15. Explicit no-change files

این فایل‌ها و پوشه‌ها در اجرای Plan تغییر نمی‌کنند:

- `DataSet/arka_dataset/config/reference_views.sql`
- `DataSet/arka_dataset/config/kpi_dictionary.csv`
- `DataSet/arka_dataset/output_contract/brief_schema.json`
- `DataSet/arka_dataset/output_contract/qa_answer_schema.json`
- `DataSet/arka_dataset/output_contract/example_brief.json`
- `DataSet/arka_dataset/manager_inputs/scripted_inputs.json`
- `Docs/final review/**`
- `Docs/trash-data/**`
- `architecture/structurizr/workspace.json`
- بریف رسمی پروژه
- تمام فایل‌های دیتاست ارزیابی
- QA enum بدون تصمیم رسمی

تغییرات و حذف‌های فعلی کاربر در خارج از Change Scope نباید Restore، Reset یا Commit شوند.

## 16. Risks and rollback strategy

| ریسک | کنترل | Rollback boundary |
|---|---|---|
| overwrite تغییرات کاربر | ثبت Baseline و patchهای محدود | هر فایل مستقل |
| انتقال اطلاعات نامعتبر از اسناد قدیمی | تطبیق با بریف، TA یا Contract | حذف بخش منتقل‌شده |
| تغییر ناخواسته Output Contract | Hash و Git diff | Output files باید بدون تغییر بمانند |
| گسترده‌شدن DB Role Agent | ADR-0019 و permission matrix | rollback بخش security model |
| تبدیل State به Component | inventory review | rollback element addition |
| وابستگی Core Workflow به Langfuse | fail-open requirement | حذف observability relationship/config |
| افزایش Scope ابزارها | Technology allow-list | حذف ابزار خارج از allow-list |
| stale Mermaid | generation پس از تثبیت DSL | rollback کل Artifact batch |
| ذخیره JSON خام MCP | استخراج اجباری `definition` | حذف Artifact نامعتبر و Export دوباره |
| تغییر `workspace.json` توسط Local | اجرای Local روی کپی موقت | Restore کپی؛ فایل مخزن دست‌نخورده |
| ناسازگاری ADR و DSL | ADR-first execution | rollback DSL phase |
| از دست‌رفتن Requirement هنگام حذف لینک قدیمی | ثبت Requirement provenance رسمی | بازگرداندن فقط متن تأییدشده |

ترتیب Rollback:

1. Mermaid Artifactها
2. View و Relationshipهای DSL
3. Component Documentation
4. docs/01 تا docs/08
5. ADRهای جدید
6. Revisionهای ADR موجود

هیچ Rollback نباید از `git reset --hard`، `git checkout --` یا تغییر `workspace.json` استفاده کند.
</proposed_plan>