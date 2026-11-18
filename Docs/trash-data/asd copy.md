# برنامه آشتی معماری DIDRAH

## 1. Current-state findings

### Git status

| مورد | وضعیت فعلی |
|---|---|
| شاخه | `main` همگام با `origin/main` |
| تغییر موجود کاربر | `architecture/structurizr/workspace.json` تغییر کرده است. تغییرها فقط metadata، layout و `lastSavedView` هستند. |
| فایل untracked | `D:\Projects\Arka\asd copy.md` |
| هشدار Git | خواندن ignore سراسری کاربر مجاز نبود. این هشدار روی repository اثر ندارد. |
| قاعده حفاظت | اجرای بعدی نباید دو مورد بالا را reset، overwrite یا حذف کند. |

### architecture status

- `workspace.dsl` وضعیت معماری را `Proposed` اعلام می‌کند.
- مدل شامل شش runtime container است: Web، Backend API، Background Worker، Scheduler/Replay، Agent Runtime و PostgreSQL.
- Protected File Archive یک data container است.
- repository هیچ application source، migration، DDL، Dockerfile یا Compose file ندارد.
- بنابراین، مدل فقط طراحی مفهومی است. مدل، پیاده‌سازی فیزیکی را اثبات نمی‌کند.
- `workspace.json` و Mermaidها generated artifact هستند. چند artifact با DSL فعال همگام نیست.

### MCP Structurizr validation result

- MCP روی DSL اصلی در خط `!docs docs` متوقف شد. قابلیت documentation در MCP فعال نیست.
- `!docs` و `!adrs` فقط از DSL درون حافظه حذف شدند. فایل اصلی تغییر نکرد.
- نتیجه MCP پس از حذف درون‌حافظه‌ای:
  - Parse: موفق.
  - Validate: `OK`.
  - Inspect: تعداد 143 finding.
  - Mermaid export: هر 10 view اجباری با موفقیت export شد.
- تفکیک 143 finding:
  - 131 relationship بدون technology.
  - 4 element خارج از همه viewها.
  - 6 deployment instance جداشده.
  - 1 missing documentation و 1 missing decisions. این دو finding فقط نتیجه حذف درون‌حافظه‌ای `!docs` و `!adrs` هستند.

### current active views

1. `L1_SystemContext`
2. `L2_Containers`
3. `L3_3_RevisedBackendApiComponents`
4. `L3_4_RevisedBackgroundWorkerComponents`
5. `L3_5_RevisedSchedulerReplayComponents`
6. `L3_6_AgentRuntimeComponents`
7. `D1_EvaluationCompose`
8. `S7_ReportGenerationScenario`
9. `S8_ManagerDecisionScenarios`
10. `S9_MeetingMinutesUploadScenario`

### current contradictions

- ADR-0012 یک image و `docker run` را الزام می‌کند. تصمیم قفل‌شده، شش service جدا با Docker Compose است.
- مسیر Submission Exporter به‌شکل `OUTPUT_DIR/submission/...` نوشته شده است. این متن می‌تواند `/submission/submission/...` بسازد.
- `Submission Output Directory` در L1 و L2 رابطه صریح ندارد. این node در هر دو view orphan است.
- `reportScenarioModel` و رابطه‌های 15 و 16 در model هستند، ولی در `S7` دیده نمی‌شوند.
- `S7` مسیر Submission Exporter و Submission Output را ندارد.
- سه component مربوط به Web در هیچ view نیستند.
- `L3_6` هم `backendApi` و هم componentهای فرزند Backend را include می‌کند. Structurizr فقط parent container را نشان می‌دهد.
- `D1_EvaluationCompose` دارای 13 element و صفر relationship است.
- Organization Configuration Service یک revision را queue می‌کند، ولی مسیر validation و بازگشت نتیجه به activation کامل نیست.
- Scheduler ورودی‌های `scripted_inputs.json` را می‌خواند، ولی componentی برای اعمال 23 ورودی ندارد.
- Agent Job دارای polling و lease است، ولی deadline reconciliation برای Runtime کاملا unavailable وجود ندارد.
- Model Gateway فقط budget را ثبت می‌کند. قرارداد کامل `ModelCallReceipt` وجود ندارد.
- Data Quality Service به‌اشتباه محل translation نیست، ولی component صحیح translation نیز وجود ندارد.
- brief schema فقط `effect_direction` را دارد. قرارداد کامل decision-effect وجود ندارد.

### generated Mermaid status

- artifact فعال ولی موجود‌نبود: `L3_4`, `L3_5`, `D1`.
- artifact موجود ولی view غیرفعال: `L3_2_BackgroundWorkerComponents` و `S1` تا `S6`.
- همه Mermaidهای فعال موجود از export فعلی کوتاه‌تر هستند. آن‌ها stale هستند.

### implementation evidence versus conceptual design

- تعداد KPIها در `kpi_dictionary.csv` برابر 55 است.
- SQLها فقط دو تفاوت ساده ندارند:
  - 9 KPI از `median()` استفاده می‌کنند.
  - 16 KPI از `julianday()` استفاده می‌کنند.
  - 4 KPI از date modifier استفاده می‌کنند.
  - 6 KPI boolean expression را در `AVG()` مصرف می‌کنند.
  - 11 KPI division دارند.
  - 36 KPI `ROUND()` دارند.
  - موارد `COALESCE`, `NULLIF`, window function و `USING` نیز وجود دارند.
- dataset شامل 16 question، دو decision، دو upload، یک priority، یک threshold change و یک org change است.
- هیچ migration یا DDL وجود ندارد. schemaها و roleها فقط طرح مفهومی هستند.

## 2. Locked decisions applied

| تصمیم قفل‌شده | اثر دقیق در برنامه |
|---|---|
| Docker Compose | ADR-0012 به شش service جدا تغییر می‌کند. فرمان مرجع `docker compose up --build --abort-on-container-exit` می‌ماند. ریسک عبارت قبلی مدرس درباره `docker run` ثبت می‌شود. |
| PostgreSQL only | SQLite فقط در Acceptance Test Harness اجرا می‌شود. هیچ SQLite runtime container مدل نمی‌شود. |
| Agent boundary | Agent Runtime فقط job را claim می‌کند، evidence مجاز می‌گیرد و candidate می‌سازد. KPI، workflow، signal، configuration، publication و file write بیرون Agent می‌مانند. |
| Decision effect | `no_change` حفظ می‌شود. `assessment_status` از `effect_direction` جدا می‌شود. |
| Recipient signal state | شش قرارداد Signal در schema `analytics` مستند می‌شوند. `SignalRecipientView` وضعیت گیرنده را نگه می‌دارد. |
| Translation placement | `kpiSqlTranslationAdapter` در Background Worker اضافه می‌شود. Data Quality Service و Snapshot این مسئولیت را نمی‌گیرند. |
| Submission path | ریشه خروجی `${OUTPUT_DIR}` است. مسیرها `${OUTPUT_DIR}/briefs/...` و `${OUTPUT_DIR}/qa/...` هستند. |
| Organization lifecycle | Configuration Validation Runner برای validation سازمان نیز استفاده می‌شود. activation فقط پس از validation و در D+1 انجام می‌شود. |
| Scripted replay | `scriptedManagerInputAdapter` در Scheduler/Replay اضافه می‌شود. این component فقط از Backend boundary استفاده می‌کند. |
| Agent failure | Run Coordinator deadline را reconcile می‌کند. Publisher گزارش را از Canonical JSON با fallback قطعی می‌سازد. QA و document analysis فقط failure صریح می‌گیرند. |
| Immutable evaluation evidence | `drops`, `history`, `calendar`, `uploads`, `scripted_inputs.json`, `reference_views.sql` و `kpi_dictionary.csv` تغییر نمی‌کنند. |

Defaultهای بسته‌شده برای failure policy:

- model-call timeout: 60 ثانیه.
- حداکثر دو attempt برای خطای transient.
- hard deadline هر Agent Job: 120 ثانیه پس از Ready.
- reconciliation cadence: هر 5 ثانیه و یک بار پیش از close شدن Run.
- report fallback فقط از Canonical Report JSON استفاده می‌کند.
- fallback علت، عدد، decision یا evidence جدید تولید نمی‌کند.

## 3. File-by-file change matrix

| absolute path | current issue | exact planned change | dependency | validation method | risk |
|---|---|---|---|---|---|
| `D:\Projects\Arka\architecture\structurizr\workspace.dsl` | relationship، component، view و path ناقص | اعمال همه componentها، relationshipها، properties، URLها و viewهای این برنامه | تصمیم‌های ADR و docs | MCP parse/validate/inspect و export | بالا |
| `...\workspace.json` | generated و دارای تغییر کاربر | فقط پس از DSL نهایی regenerate شود. layout موجود `L3_3` حفظ شود. hand-edit ممنوع است. | DSL نهایی | semantic diff و layout-key comparison | بالا |
| `...\README.md` | inventory و regeneration کامل نیست | source-of-truth، 14 view فعال، MCP limitation، link behavior و safe regeneration را ثبت کند | viewهای نهایی | link check و command review | متوسط |
| `...\adrs\0002-use-postgresql-and-verify-kpi-parity.md` | translation contract ناقص | Translator، hashها، semantics همه 55 KPI و جداسازی product/test را اضافه کند | KPI plan | ADR consistency search | متوسط |
| `...\adrs\0008-use-one-bounded-agent.md` | receipt و failure path ناقص | Agent deadline و `ModelCallReceipt` را ثبت کند | failure plan | traceability check | متوسط |
| `...\adrs\0009-publish-manager-reports-independently.md` | fallback باز است | policy قطعی report fallback و failure صریح QA/document را ثبت کند | failure plan | scenario review | متوسط |
| `...\adrs\0012-evaluation-deployment-profile.md` | با تصمیم Compose متعارض است | تصمیم را با شش service، mountها، health، shutdown و فرمان Compose جایگزین کند | locked deployment | contradiction grep | بالا |
| `...\adrs\0013-submission-exporter.md` | path root مبهم است | `${OUTPUT_DIR}/briefs` و `${OUTPUT_DIR}/qa` را ثبت کند | output contract | path test | بالا |
| `...\adrs\0014-organization-configuration-service.md` | validation connection ناقص است | lifecycle کامل revision، validation، D+1 activation و M11 را ثبت کند | org flow | scenario test | متوسط |
| `...\adrs\0015-decision-effect-evaluator.md` | status و direction مخلوط هستند | چهار assessment status و چهار direction را با قواعد شرطی ثبت کند | schema plan | JSON Schema tests | بالا |
| `...\adrs\0016-kpi-parity-validator.md` | translation در Replayer فرض شده است | Translator را به Worker منتقل کند. Parity Validator در Scheduler بماند. | KPI plan | architecture search | بالا |
| `...\adrs\0017-signal-episode-contract.md` | traceability جزئی است | recipient state و data-issue exclusion را به docs/tests پیوند دهد | signal docs | traceability check | پایین |
| `...\docs\01-purpose-and-scope.md` | deployment و output boundary کامل نیست | Compose، output root و architecture-only status را اضافه کند | ADR-0012/13 | term search | پایین |
| `...\docs\02-architecture-overview.md` | definition plane و replay adapter ندارد | سه plane، Scripted Adapter و failure reconciliation را اضافه کند | component model | flow review | متوسط |
| `...\docs\03-data-and-processing.md` | Normalizer و translation flow مخلوط نیستند، ولی صریح هم نیستند | daily data plane، KPI definition plane و restatement ownership را جدا کند | Worker model | flow comparison | متوسط |
| `...\docs\04-security-and-trust.md` | roleهای فعلی ناقص و `agent_query_reader` نامناسب است | 9 role نهایی، RLS و Agent restrictions را ثبت کند | DB plan | role grep | بالا |
| `...\docs\05-runtime-flows.md` | scripted replay، org validation و timeout ناقص است | سه flow و deadline state machine را اضافه کند | runtime model | scenario review | بالا |
| `...\docs\06-deployment-and-operations.md` | health/readiness/shutdown جزئی است | service، mount، volume، resource، network و timezone contract را کامل کند | ADR-0012 | deployment checklist | متوسط |
| `...\docs\07-quality-attributes.md` | fallback و receipt معیار ندارد | acceptance criteria برای deadline، cost receipt و parity را اضافه کند | failure/KPI plan | quality trace | پایین |
| `...\docs\08-risks-and-open-issues.md` | چند موضوع قفل‌شده هنوز Open است | ISSUE-V3-06 و بخش مرتبط KPI را resolved/partially resolved کند. ریسک‌های باقی‌مانده را نگه دارد. | ADR updates | issue consistency | متوسط |
| `...\docs\09-web-application-components.md` | وجود ندارد | سه component Web و anchorهای ثابت را مستند کند | DSL identifiers | anchor/link check | پایین |
| `...\docs\10-backend-api-components.md` | وجود ندارد | 20 component Backend و timeout/fallback/output ownership را مستند کند | Backend model | completeness script | متوسط |
| `...\docs\11-background-worker-components.md` | وجود ندارد | 15 component نهایی Worker را مستند کند | Worker model | completeness script | متوسط |
| `...\docs\12-scheduler-replay-components.md` | وجود ندارد | 7 component نهایی Scheduler را مستند کند | replay model | completeness script | متوسط |
| `...\docs\13-agent-runtime-components.md` | وجود ندارد | 5 component Agent و forbidden responsibilities را مستند کند | Agent model | completeness script | متوسط |
| `...\docs\14-data-stores-and-contracts.md` | وجود ندارد | PostgreSQL schemas، roles، Archive، DATA/OUTPUT و receipts را مستند کند | DB plan | schema/role check | بالا |
| `D:\Projects\Arka\Docs\architecture\001-system-blueprint.md` | output path و fallback هنوز قدیمی/باز است | output root و قطعی‌شدن failure policy را اصلاح کند | ADR updates | contradiction grep | متوسط |
| `...\002-data-architecture.md` | نام schemaها و roleها با DSL همسان نیست | 15 schema، 9 role، entity ownership و conceptual-only status را ثبت کند | DB plan | cross-file comparison | بالا |
| `...\003-roadmap.md` | Model receipt فیلدهای قدیمی دارد | فیلدها را به `ModelCallReceipt` نهایی و phase gateهای جدید وصل کند | receipt plan | field grep | متوسط |
| `...\004-reconciliation-review.md` | Q03، Q13 و Q16 هنوز Openهای حل‌شده دارند | وضعیت translation placement، M11 D+1 و fallback را reconcile کند | locked decisions | contradiction grep | متوسط |
| `D:\Projects\Arka\Docs\final review\architecture-control-register-v3.md` | ADR-0012، failure و KPI placement ناسازگار است | تصمیم‌های جدید را ثبت کند و source precedence را حفظ کند | همه ADRها | register consistency | بالا |
| `D:\Projects\Arka\DataSet\arka_dataset\output_contract\brief_schema.json` | decision effect ناقص است | fieldها و conditional validation را backward-compatible اضافه کند | ADR-0015 | Draft 2020-12 validation | بالا |
| `...\example_brief.json` | follow-up نمونه ندارد | یک `evaluated/no_change` نمونه کامل اضافه کند | schema نهایی | validate against schema | متوسط |
| `D:\Projects\Arka\architecture\structurizr\mermaid\` | missing و stale artifact دارد | پس از اثبات inventory، staleها با Git حذف و viewهای فعال regenerate شوند | DSL نهایی | key/hash comparison | متوسط |

## 4. Component change matrix

| container | existing/new component | action | responsibility | relationship change | documentation target | reason |
|---|---|---|---|---|---|---|
| Web | `chatUi`, `dashboardUi`, `workflowUi` | keep/extend docs | UIهای سه‌گانه | view جدید Web | docs 09 | componentها hidden هستند |
| Backend | `identityBoundary`, `authorizationService`, `managerInputService` | keep/extend | live و scripted request boundary | Scripted Adapter به Identity Boundary | docs 10 | replay باید همان boundary را مصرف کند |
| Backend | `configurationService` | extend | inactive config، activation پس از دو receipt | Semantic Registry و validator | docs 10 | activation ناقص است |
| Backend | `organizationConfigurationService` | extend | inactive org revision و D+1 activation | validation round-trip | docs 10 | lifecycle کامل دیده نمی‌شود |
| Backend | `runCoordinatorV2` | extend | job plan و deadline reconciliation | Output Validator و PostgreSQL | docs 10 | Ready job می‌تواند معطل بماند |
| Backend | `publisherV2` | extend | deterministic fallback renderer و publication | Exporter | docs 10 | component جدید لازم نیست |
| Backend | `submissionExporter` | extend | تنها writer در OUTPUT_DIR | explicit output relationships | docs 10 | path فعلی اشتباه است |
| Backend | `auditService` | extend | persistence owner برای ModelCallReceipt | Model Gateway → Audit Service | docs 10 | audit path ناقص است |
| Backend | سایر 13 component | keep/extend docs | مسئولیت فعلی | فقط technology/tag و docs | docs 10 | تغییر مرز لازم نیست |
| Worker | `sourceAdapters` | extend | parsing و source-contract selection | خروجی به Normalizer | docs 11 | versioning در این مرز می‌ماند |
| Worker | `normalizer` | add | canonical name/type/unit normalization | Source Adapters → Normalizer → DQ | docs 11 | lifecycle و failure آن از parser و DQ جدا است |
| Worker | `dataQualityService` | extend | duplicate/conflict، schema incident و DQ incident | ورودی از Normalizer | docs 11 | KPI translation ممنوع است |
| Worker | `ingestionCoordinator` | extend | late-arrival invalidation و restatement request | PostgreSQL/Run Coordinator state | docs 11 | component جدید لازم نیست |
| Worker | `configurationValidationRunnerV2` | rename display/extend | KPI structural validation و org validation | round-trip با دو Configuration Service | docs 11 | زیرساخت job موجود قابل استفاده است |
| Worker | `kpiSqlTranslationAdapter` | add | deterministic SQLite-to-PostgreSQL translation | Input Dataset، Semantic Registry | docs 11 | lifecycle و receipt مستقل دارد |
| Worker | `semanticRegistry` | extend | original/translated SQL، hashes، state و activation | Translator، Parity، Calculator | docs 11 | source of truth تعریف KPI است |
| Worker | `snapshotService` | extend | pin کردن `kpi_definition_version` | PostgreSQL | docs 11 | snapshot نباید formula را حمل کند |
| Worker | سایر 7 component | keep/extend docs | مسئولیت فعلی | traceability و failure docs | docs 11 | component جدید لازم نیست |
| Scheduler | `scriptedManagerInputAdapter` | add | اعمال 23 scripted input از مسیر Backend | Input Dataset، Replay، Identity Boundary | docs 12 | lifecycle و service identity مستقل دارد |
| Scheduler | `kpiParityValidator` | extend | exact row/dimension/null comparison و receipt | Dataset، Registry، PostgreSQL | docs 12 | parity باید executable باشد |
| Scheduler | سایر 5 component | keep/extend docs | clock، replay، profile و acceptance | technology/tag تکمیل شود | docs 12 | مرز فعلی مناسب است |
| Agent Runtime | `agentJobRunner` | extend | deadline-aware claim و terminal failure | PostgreSQL | docs 13 | source of truth همچنان DB است |
| Agent Runtime | `agentModelGateway` | extend | limits، budget و ModelCallReceipt | Audit Service | docs 13 | مسیر audit لازم است |
| Agent Runtime | سه component دیگر | keep/extend docs | orchestration، conversation، checkpoint | فقط docs/view | docs 13 | مرز فعلی مناسب است |
| Data stores | PostgreSQL و Archive | keep/extend properties | durable state و immutable bytes | deployment mounts/roles | docs 14 | هیچ database دوم اضافه نمی‌شود |

## 5. Relationship change list

| identifier/source | destination | description | technology | tag | action |
|---|---|---|---|---|---|
| `didrah` | `submissionOutput` | Writes only contract-approved brief and QA artifacts below OUTPUT_DIR | Filesystem contract | `ControlFlow` | add |
| `backendApi` | `submissionOutput` | Exports validated reports and QA results | Restricted filesystem I/O | `ControlFlow` | add |
| `submissionExporter` | `submissionOutput` | Writes `${OUTPUT_DIR}/briefs/...` and `${OUTPUT_DIR}/qa/...` atomically | Restricted filesystem I/O | `ControlFlow` | update |
| `publisherV2` | `submissionExporter` | Forwards each validated final report | In-process function call | `PrimaryFlow` | update |
| `outputValidator` | `submissionExporter` | Forwards each validated QA result | In-process function call | `PrimaryFlow` | update |
| `sourceAdapters` | `dataQualityService` | old direct parse-to-DQ path | In-process function call | `DataFlow` | remove |
| `sourceAdapters` | `normalizer` | Sends parsed rows with source-contract version | In-process function call | `DataFlow` | add |
| `normalizer` | `dataQualityService` | Sends canonical rows and normalization failures | In-process function call | `DataFlow` | add |
| `configurationValidationRunnerV2` | `kpiSqlTranslationAdapter` | Requests translation only for bootstrap or changed definitions | In-process function call | `ControlFlow` | add |
| `kpiSqlTranslationAdapter` | `inputDataset` | Reads immutable SQLite SQL and definition bytes | Read-only filesystem | `DataFlow` | add |
| `kpiSqlTranslationAdapter` | `semanticRegistry` | Stores inactive translation and Translation Receipt | In-process function call | `ControlFlow` | add |
| `kpiParityValidator` | `inputDataset` | Executes immutable reference SQL in isolated SQLite | Read-only filesystem and SQLite test engine | `DataFlow` | add |
| `kpiParityValidator` | `semanticRegistry` | Reads candidate PostgreSQL SQL and hashes | Internal read API | `DataFlow` | add |
| `kpiParityValidator` | `postgres` | Executes candidate and stores Parity Receipt | PostgreSQL protocol over TLS | `ControlFlow` | add |
| `kpiParityValidator` | `configurationService` | Supplies parity receipt for activation decision | Authenticated internal API | `Feedback` | add |
| `configurationValidationRunnerV2` | `configurationService` | Returns structural validation receipt | PostgreSQL-backed job result | `Feedback` | add |
| `configurationService` | `semanticRegistry` | Activates only a structurally valid and parity-valid version | In-process function call | `ControlFlow` | add |
| `kpiCalculator` | `semanticRegistry` | Reads only active approved PostgreSQL definitions | In-process function call | `DataFlow` | update |
| `snapshotService` | `postgres` | Pins data, config, org, policy and KPI-definition versions | PostgreSQL protocol over TLS | `ControlFlow` | update |
| `organizationConfigurationService` | `configurationValidationRunnerV2` | Queues deterministic org validation | PostgreSQL-backed job queue | `ControlFlow` | add |
| `configurationValidationRunnerV2` | `organizationConfigurationService` | Returns validated or rejected org revision | PostgreSQL-backed job result | `Feedback` | add |
| `replayCommandV2` | `scriptedManagerInputAdapter` | Applies inputs for the current simulated day | In-process function call | `ControlFlow` | add |
| `scriptedManagerInputAdapter` | `inputDataset` | Reads JSON and referenced upload bytes | Read-only filesystem | `DataFlow` | add |
| `scriptedManagerInputAdapter` | `identityBoundary` | Submits authenticated service requests through the live boundary | Authenticated HTTPS/JSON | `PrimaryFlow` | add |
| `managerInputService` | `decisionTracker` | Routes authorized scripted human decisions | In-process function call | `ControlFlow` | add |
| `runCoordinatorV2` | `outputValidator` | Submits expired report jobs for deterministic failure validation | In-process function call | `ControlFlow` | add |
| `runCoordinatorV2` | `postgres` | Reconciles deadlines, leases, attempts and terminal states | PostgreSQL protocol over TLS | `ControlFlow` | update |
| `agentJobRunner` | `postgres` | Claims only non-expired jobs and persists timeout/failure codes | PostgreSQL protocol over TLS | `DataFlow` | update |
| `agentModelGateway` | `auditService` | Records one ModelCallReceipt per attempt | Authenticated internal API | `ControlFlow` | add |

همه 131 relationship بدون technology نیز اصلاح می‌شوند. قاعده دقیق این است:

- person/UI: `Browser interaction over HTTPS`.
- UI/API و service/API: `Authenticated HTTPS/JSON`.
- component داخلی یک container: `In-process function call`.
- PostgreSQL: `PostgreSQL protocol over TLS`.
- Archive و DATA/OUTPUT: `Restricted filesystem I/O`.
- wake-up: `Internal authenticated API`.
- job queue/result: `PostgreSQL-backed job queue/result`.

رابطه‌های شماره‌دار `S7:01..23`، `S8:A01..A46` و `S9:B01..B42` technology و tag متناظر می‌گیرند. شماره، source، destination و description آن‌ها تغییر نمی‌کند.

## 6. View correction plan

| view key | current problem | correction | view type | expected visible elements |
|---|---|---|---|---|
| `L1_SystemContext` | Submission Output orphan | `didrah -> submissionOutput` را نشان دهد | System Context | 10 element، بدون orphan |
| `L2_Containers` | output orphan و scripted flow کلی ناقص | `backendApi -> submissionOutput` و Scheduler replay boundary را نشان دهد | Container | همه containerها و dependencyهای اصلی |
| `L3_2_WebApplicationComponents` | وجود ندارد | view جدید برای سه UI و Backend API | Component | `chatUi`, `dashboardUi`, `workflowUi`, `backendApi` |
| `L3_3_RevisedBackendApiComponents` | Agent relationships به container collapse می‌شوند | context container حفظ شود. جزئیات cross-container به `C1` منتقل شود | Component | همه 20 Backend component و external boundaryهای لازم |
| `L3_4_RevisedBackgroundWorkerComponents` | Normalizer و Translator ندارد | دو component جدید و دو plane را include کند | Component | 15 Worker component، Dataset، PostgreSQL، Archive |
| `L3_5_RevisedSchedulerReplayComponents` | scripted input application ناقص است | Scripted Adapter و KPI integration edges را include کند | Component | 7 Scheduler component و Backend boundary |
| `L3_6_AgentRuntimeComponents` | parent Backend childها را suppress می‌کند | `backendApi` را از include حذف کند. Backend componentهای خارجی را جدا include کند | Component | 5 Agent component، Gateway، Authorization، Evidence، Validator، Audit، PostgreSQL، LLM |
| `C1_BackendAgentIntegration` | Backend-Agent edgeها در L3ها collapse می‌شوند | view جدید static cross-container | Custom | producers، Runner، Orchestrator، Evidence، Validator، Audit، DB، LLM |
| `D1_EvaluationCompose` | صفر relationship و Archive/output mount غایب | instance identifier، explicit instance edges، Archive volume، DATA/OUTPUT mount و health properties اضافه شود | Deployment | شش service، PostgreSQL، Archive، دو mount، LLM egress |
| `S7_ReportGenerationScenario` | Model Gateway hidden و export path غایب | `reportScenarioModel`، timeout reconciliation، Exporter و Output را اضافه کند | Custom | مسیر کامل report تا فایل نهایی |
| `S8_ManagerDecisionScenarios` | technology ندارد | topology حفظ شود. technology/tag کامل شود | Custom | همان 18 element و 46 edge |
| `S9_MeetingMinutesUploadScenario` | technology ندارد | topology حفظ شود. technology/tag کامل شود | Custom | همان 17 element و 46 edge |
| `S10_KPITranslationAndParity` | lifecycle در هیچ view یکجا دیده نمی‌شود | view sequence جدید برای bootstrap/change/parity | Dynamic | Dataset، Translator، Registry، Validatorها، Config Service، Calculator |
| `S11_ScriptedManagerInputReplay` | routing انواع input دیده نمی‌شود | view sequence جدید برای adapter و Backend routing | Dynamic | Dataset، Adapter، Identity، Router و پنج handler |

## 7. Documentation plan

### ADR changes

- ADR-0012 تا ADR-0017 مطابق matrix بخش 3 اصلاح می‌شوند.
- ADR-0002، ADR-0008 و ADR-0009 فقط برای contractهای وابسته به تصمیم جدید اصلاح می‌شوند.
- status تصمیم‌های قفل‌شده دوباره باز نمی‌شود.

### docs 01–08

- deployment، سه processing plane، timeout، replay input، schema/role و traceability به متن افزوده می‌شوند.
- open issueهای حل‌شده از open list خارج می‌شوند.
- open issueهای خارج از این درخواست حفظ می‌شوند.

### new component docs 09–14

هر component یک anchor ثابت با الگوی زیر می‌گیرد:

`component-<dsl-identifier-in-kebab-case>`

هر section دقیقا این fieldها را دارد:

- purpose
- owning container
- owner/team
- inputs
- outputs
- source of truth
- responsibilities
- forbidden responsibilities
- dependencies
- allowed calls
- persisted data
- database schema
- database role
- idempotency
- timeout/retry
- failure
- fallback
- security boundary
- related ADRs
- brief requirements
- dataset scenarios
- acceptance tests
- open issues

### documentation links

- DSL همیشه property محلی `documentation.section` را نگه می‌دارد.
- ابتدا relative URL مانند `docs/11-background-worker-components.md#component-kpi-sql-translation-adapter` در Structurizr Local آزموده می‌شود.
- اگر relative URL کار نکند، URL از remote زیر ساخته می‌شود:
  `https://github.com/orgpilot-team/OrgPilot/blob/main/...`
- link test باید HTTP target یا local anchor را کنترل کند.

### traceability matrix design

فایل docs 09 تا 14 یک جدول تجمیعی با این ستون‌ها دارند:

`Component | Documentation section | ADR | Brief requirement | Dataset scenario | Acceptance test`

هر DSL identifier دقیقا یک row دارد. هر row حداقل یک acceptance test دارد.

## 8. KPI translation and parity plan

### initial 55-KPI bootstrap

`Immutable SQLite SQL → KPI SQL Translation Adapter → inactive PostgreSQL definition → structural validation → parity validation → explicit bootstrap activation → Semantic Registry`

- Translator فقط یک بار برای bootstrap اجرا می‌شود.
- هر KPI یک Translation Receipt و یک Parity Receipt دارد.
- activation گروهی فقط زمانی انجام می‌شود که هر 55 KPI موفق باشند.
- failure یک KPI کل bootstrap activation را fail-closed می‌کند.

### future KPI-change flow

`New/changed reference definition → inactive candidate → translation → structural receipt → parity receipt → explicit activation`

- old version فعال باقی می‌ماند تا candidate کامل شود.
- rollback فقط active pointer را به نسخه قبلی برمی‌گرداند.
- SQL مرجع overwrite نمی‌شود.

### daily calculation flow

`Pinned Snapshot + active KPI-definition version → KPI Calculator → KPI Observation`

- Translator و Parity Validator در daily run اجرا نمی‌شوند.
- Snapshot فقط versionها و data/config/org/policy را pin می‌کند.

### immutable reference handling

- `reference_views.sql` و `kpi_dictionary.csv` read-only می‌مانند.
- original SQL، source hash و file hash در Registry ثبت می‌شوند.
- PostgreSQL SQL در field و hash جدا ثبت می‌شود.

### receipts

Translation Receipt شامل:

`kpi_id, reference_hash, translator_version, translated_sql, translation_hash, rule_ids, created_at, status, failure_code`

Parity Receipt شامل:

`kpi_id, sqlite_engine_version, postgres_engine_version, snapshot_version, policy_version, reference_hash, translation_hash, row_count_pair, key_match, dimension_match, null_match, max_numeric_delta, tolerance, status`

مقایسه عددی:

- key، dimension، row count و NULL/no-row باید exact باشند.
- اگر reference صفر است، PostgreSQL نیز باید صفر باشد.
- در غیر این حالت، relative difference باید حداکثر 1% باشد.

## 9. Dataset scenario coverage

| scenario | expected architecture behavior | acceptance evidence |
|---|---|---|
| day 66 missing support data | نبود `tickets`, `ticket_events`, `csat` به DQ incident تبدیل شود. KPI وابسته `null` شود. report morning 67 مسئله را نشان دهد. | DataIssue، null observation، نبود business item |
| day 75 org change | IN05 به inactive org revision تبدیل شود. validation کامل شود. M11 در report morning 76 فعال شود. | revision، validation receipt، snapshot org_version |
| day 76 duplicates | exact duplicate فقط یک بار محاسبه شود. conflict merge نشود. data issue ثبت شود. | duplicate receipt، contributor count، report day 77 |
| day 80 upload | IN07 bytes و hash حفظ شوند. upload canonical KPI را تغییر ندهد. eligibility گزارش از D+1 است. | archive receipt، parse receipt، report morning 81 |
| day 82 schema change | `create_time/created_at` و `event_time/at` با contract version حل شوند. day hard-code ممنوع است. | schema receipt و mapping version |
| late/corrected data | snapshot قبلی تغییر نکند. full rebuild و restated report version ساخته شود. | invalidation event و `supersedes` |
| 16 QA questions | همه از Scripted Adapter به live Backend boundary بروند. | 16 QA files و scope receipts |
| two decisions | از Router به Decision and Follow-Up بروند. Agent آن‌ها را اجرا نکند. | two decision events |
| two uploads | bytes از DATA_DIR خوانده شوند و در Archive حفظ شوند. | two archive/parse receipts |
| priority change | Configuration Service، inactive revision و D+1 effect | config receipt |
| threshold change | Configuration Service، validation و D+1 effect | threshold version receipt |
| reports 62–91 | 30 صبح با cutoff D-1 و manager roster فعال تولید شوند. | coverage manifest و خروجی هر مدیر |

ترتیب فایل `scripted_inputs.json` حفظ می‌شود. Adapter ساعت را عقب نمی‌برد. ورودی‌های هم‌روز همان `input_id`, `day`, `manager_id`, `type` و attachment reference را حفظ می‌کنند.

## 10. Output-contract plan

### Submission paths

- `${OUTPUT_DIR}/briefs/day_XXX/<manager_id>.json`
- `${OUTPUT_DIR}/qa/<question_id>.json`
- اگر `OUTPUT_DIR=/submission` باشد:
  - `/submission/briefs/day_XXX/<manager_id>.json`
  - `/submission/qa/<question_id>.json`

### brief schema changes

در هر item از `decision_followups` این propertyهای optional اضافه می‌شوند:

- `assessment_status`: enum چهارحالته.
- `effect_direction`: enum فعلی حفظ می‌شود.
- `baseline_value`, `observed_value`, `effect_size`, `minimum_meaningful_change`: `number|null`.
- `comparison_window`: object شامل `baseline_start`, `baseline_end`, `observed_start`, `observed_end`.
- `method`: string.
- `assumptions`, `confounders`, `evidence_refs`: array of string.
- `confidence`: `number|null` با بازه 0 تا 1.
- `guardrail`: object شامل `kpi_id`, `threshold`, `operator`, `observed_value`, `status`.
- `insufficient_data_reason`: `string|null`.

Conditional rules فقط وقتی `assessment_status` وجود دارد اعمال می‌شوند:

- `evaluated` فقط `improved|worsened|no_change` را می‌پذیرد.
- `too_early` به `effect_direction=too_early` نیاز دارد.
- `insufficient_data` و `not_isolatable` وجود `effect_direction` را ممنوع می‌کنند.
- `not_isolatable` هرگز به `no_change` map نمی‌شود.

### backward compatibility

- fieldهای موجود حذف یا rename نمی‌شوند.
- legacy record بدون `assessment_status` همچنان valid است.
- enumهای `qa_answer_schema.json` تغییر نمی‌کنند.

### validation tests

- legacy example معتبر بماند.
- example جدید `evaluated/no_change` معتبر باشد.
- چهار assessment status تست مثبت داشته باشند.
- invalid mappingها تست منفی داشته باشند.
- مسیرهای خروجی و atomic rename آزموده شوند.

## 11. Database design reconciliation

### conceptual schemas

همه 15 namespace حفظ می‌شوند. آن‌ها service جدا نیستند.

| schema | owner data |
|---|---|
| `ingest` | source contracts، batches، files، parse و DQ receipts |
| `core` | canonical entities، events و snapshots |
| `org` | org nodes، edges، revisions و recipient eligibility |
| `security` | grants، policy versions و AuthContext records |
| `semantic` | KPI definitions، translations و activation state |
| `analytics` | KPI observations، signals و grouped items |
| `workflow` | workflow cases و stage observations |
| `reporting` | evidence packages، reports، QA و export receipts |
| `document` | upload metadata، fragments و parse receipts |
| `decision` | decisions، follow-ups و effect assessments |
| `orchestration` | runs، jobs، dependencies، leases و deadlines |
| `agent` | conversations، checkpoints و candidates |
| `evaluation` | parity و acceptance receipts |
| `operations` | budgets، health، run metrics و reconciliation state |
| `audit` | access، validation، publication و ModelCallReceipt |

### runtime roles

- `migration_owner`
- `ingestion_writer`
- `analytics_worker`
- `application_api`
- `agent_runtime_worker`
- `query_gateway_reader`
- `scheduler_replay`
- `submission_exporter`
- `audit_reader`

`agent_query_reader` حذف می‌شود. Agent Runtime general business-query permission نمی‌گیرد.

### RLS

- runtime roleها owner، SUPERUSER یا BYPASSRLS نیستند.
- manager-scoped reporting، QA، decision و conversation tableها `FORCE ROW LEVEL SECURITY` دارند.
- Query Gateway فقط approved views و scoped SELECT را می‌خواند.
- Agent Runtime فقط job، pinned reference، checkpoint و candidate مربوط به job خود را می‌خواند.
- Submission Exporter فقط validated projectionها و export receipt را می‌بیند.

### ModelCallReceipt

- producer: Model Gateway.
- persistence boundary: Audit Service.
- schema: `audit`.
- receipt شامل همه fieldهای اجباری prompt است.
- `manager_id` فقط در scope مجاز ذخیره می‌شود.
- `actual_cost` تا settlement می‌تواند null باشد.

### physical implementation status

- هیچ schema، table، role، policy، index یا migration فعلی اثبات نشده است.
- این task فقط architecture contract را reconcile می‌کند.
- اجرای بعدی نباید وجود DDL را ادعا کند.

## 12. Ordered execution phases

### Phase 0 — حفاظت از وضعیت موجود

- Files: Git working tree و generated artifacts.
- Edits: هیچ.
- Checks: `git status`, `git diff`, hash فایل‌های protected.
- Exit: layout diff و untracked file ثبت و محفوظ باشند.

### Phase 1 — قراردادها و تصمیم‌ها

- Files: ADRها، control register، docs 001 تا 004.
- Edits: Compose، output path، KPI placement، org lifecycle، failure و receipt.
- Dependency: تصمیم‌های قفل‌شده.
- Checks: contradictory-term search.
- Exit: هیچ سند authoritative تصمیم متعارض نداشته باشد.

### Phase 2 — model و relationship

- Files: `workspace.dsl`.
- Edits: componentها، relationshipها، properties، technology/tag و deployment.
- Dependency: Phase 1.
- Checks: MCP parse و validate.
- Exit: DSL معتبر باشد.

### Phase 3 — viewها

- Files: `workspace.dsl`.
- Edits: پنج correction، چهار view جدید و scenario completion.
- Dependency: Phase 2.
- Checks: MCP inspect و export.
- Exit: orphan، hidden element و deployment disconnect نماند.

### Phase 4 — component documentation

- Files: docs 01 تا 14 و README.
- Edits: component sections، anchors، properties و traceability matrix.
- Dependency: identifierهای نهایی.
- Checks: component-to-anchor completeness.
- Exit: هر 50 component یک anchor و traceability row داشته باشد.

### Phase 5 — output و database contracts

- Files: brief schema، example، docs 002/003/04/05/06.
- Edits: decision effect، schemas، roles، receipts و failure state.
- Dependency: component ownership.
- Checks: JSON Schema validation و cross-file role comparison.
- Exit: schema و example معتبر باشند.

### Phase 6 — generated artifacts

- Files: `workspace.json` و Mermaid directory.
- Edits: regenerate فقط از DSL نهایی.
- Dependency: همه phaseهای قبل.
- Checks: view-key inventory، semantic diff، layout preservation.
- Exit: generated artifacts دقیقا با active views برابر باشند.

### Phase 7 — final audit

- Files: همه فایل‌های تغییرکرده.
- Checks: MCP، local Structurizr، links، grep، `git diff --check`.
- Exit: فقط تغییرهای درون scope باقی بمانند.

## 13. Validation plan

- MCP parse روی DSL بدون تغییر فایل و با حذف درون‌حافظه‌ای فقط `!docs` و `!adrs`.
- MCP validate با انتظار `OK`.
- MCP inspect با انتظار صفر finding واقعی. دو finding docs/decisions در حالت stripped مجاز هستند.
- Mermaid export برای همه 14 view فعال.
- مقایسه declared element/relationship با Mermaid هر view.
- کنترل orphan، hidden element، excluded edge و parent/child conflict.
- local Structurizr validation با DSL کامل و `!docs`/`!adrs`.
- JSON Schema Draft 2020-12 validation برای legacy و example جدید.
- تست anchor و URL هر component.
- جست‌وجوی واژه‌های متعارض:
  - `single image`
  - `No Docker Compose`
  - `OUTPUT_DIR/submission`
  - `agent_query_reader`
  - translation در Data Quality یا Replayer
  - SQLite به‌عنوان product database
- `git diff --check`.
- مقایسه active view keys با Mermaid filenames.
- کنترل نبود تغییر در protected dataset files با hash.
- کنترل `workspace.json` برای حفظ vertexهای pre-existing کاربر.

## 14. Risks and rollback

| risk | control | rollback boundary |
|---|---|---|
| dirty worktree | baseline diff و عدم reset | فقط فایل‌های این plan revert شوند |
| generated artifact drift | generation در temp و compare پیش از replace | workspace.json و Mermaid از baseline بازیابی شوند |
| evaluator compatibility | schema additive و conditional | حذف fieldهای جدید بدون تغییر legacy |
| Compose versus teacher wording | acceptance risk در ADR-0012 ثبت شود | تصمیم Compose rollback نمی‌شود |
| schema compatibility | fieldهای قدیمی حفظ شوند | فقط conditionalهای جدید rollback شوند |
| SQL translation semantics | fail-closed و receipt برای هر KPI | active definition قبلی حفظ شود |
| documentation link failure | relative URL سپس GitHub fallback | property محلی همیشه حفظ شود |
| stale artifact deletion | فقط بعد از اثبات نبود view key و با Git | بازیابی از Git ممکن است |
| user layout loss | stable view key و semantic generation | generated file جایگزین نشود تا layout حفظ شود |

## 15. Definition of Done

- [ ] تغییرهای موجود کاربر حفظ شده‌اند.
- [ ] هیچ فایل protected dataset تغییر نکرده است.
- [ ] ADR-0012 با Docker Compose سازگار است.
- [ ] ریسک عبارت `docker run` ثبت شده است.
- [ ] PostgreSQL تنها product database است.
- [ ] SQLite فقط در parity harness است.
- [ ] KPI SQL Translation Adapter در Worker است.
- [ ] Data Quality Service translation انجام نمی‌دهد.
- [ ] هر 55 KPI Translation Receipt و Parity Receipt contract دارد.
- [ ] Organization validation و D+1 activation کامل است.
- [ ] Scripted Manager Input Adapter هر 23 input را پوشش می‌دهد.
- [ ] report timeout fallback قطعی دارد.
- [ ] QA و document failure صریح و persisted است.
- [ ] Submission path دوبار `submission` ندارد.
- [ ] L1 و L2 Submission Output orphan ندارند.
- [ ] Web L3 view وجود دارد.
- [ ] Agent Runtime view parent/child conflict ندارد.
- [ ] Backend-Agent Integration view وجود دارد.
- [ ] `S7` Model Gateway، Exporter و Output را نشان می‌دهد.
- [ ] deployment view relationship و volumeها را نشان می‌دهد.
- [ ] هر relationship technology دارد.
- [ ] هر component documentation anchor دارد.
- [ ] traceability matrix کامل است.
- [ ] ModelCallReceipt کامل و قابل audit است.
- [ ] schemaها و roleها در DSL و docs یکسان هستند.
- [ ] brief schema backward-compatible است.
- [ ] `qa_answer_schema.json` enumها تغییر نکرده‌اند.
- [ ] MCP parse، validate، inspect و export موفق هستند.
- [ ] local Structurizr validation موفق است.
- [ ] Mermaid inventory با active views برابر است.
- [ ] `git diff --check` موفق است.
- [ ] هیچ ادعای نادرست درباره implementation فیزیکی وجود ندارد.

## 16. Questions requiring user decision

هیچ پرسش مسدودکننده‌ای باقی نمانده است. این برنامه از تصمیم‌های قفل‌شده و defaultهای صریح بخش 2 استفاده می‌کند.
