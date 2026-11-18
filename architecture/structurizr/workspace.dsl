workspace "DIDRAH Proposed Architecture" "Proposed C4 model for the DIDRAH management assistant. Open decisions are not approved facts." {
    !identifiers flat
    !impliedRelationships false

    // Architecture sources: this DSL, docs/01-purpose-and-scope.md through docs/08-risks-and-open-issues.md, and adrs/.
    // Evaluation references: DataSet/arka_dataset/README_FA.md and output_contract/*.json are read-only.
    // Team decision: PostgreSQL is the only product database.
    // SQLite is an external test oracle for reference SQL only. It is not a runtime container.
    // Status: Proposed. This workspace does not claim implementation.
    // Open decisions remain in docs/08-risks-and-open-issues.md and the accepted ADR set.

    model {
        // People
        seniorManager = person "Senior Manager" "Reads organization health, cross-unit workflows, escalations, and pending decisions." "Person,Executive"
        unitManager = person "Unit Manager" "Reads authorized unit and team aggregates. Records decisions and follow-up actions." "Person,Manager"
        teamSupervisor = person "Team Supervisor" "Reads team data and authorized direct-member work details for workload management." "Person,Manager"
        evaluator = person "Evaluator" "Runs Docker, replay, hidden-data checks, and acceptance tests." "Person,Evaluator"
        operator = person "Operator" "Monitors runs, failures, cost, backup, and restore evidence." "Person,Operator"

        // External systems
        inputDataset = softwareSystem "DIDRAH Input Dataset" "Provides nightly drops, manifests, manager inputs, uploads, configuration, and history through one versioned data contract. Development and hidden evaluation datasets use the same structure." "External,Source,Evaluation"
        submissionOutput = softwareSystem "Submission Output Directory" "Evaluator-provided writable OUTPUT_DIR mount. DIDRAH writes only contract-approved brief and QA files under /submission." "External,Storage,Evaluation"
        identityProvider = softwareSystem "Identity Provider" "Authenticates users and supplies a trusted identity. The product or internal method is open." "External,Identity,OpenDecision"
        llmProvider = softwareSystem "Language Model Provider" "Returns bounded language-model completions. The provider and model are open decisions." "External,AI,OpenDecision"
        langfuse = softwareSystem "Langfuse" "Receives optional, redacted OpenTelemetry data for agent traces, model calls, token use, cost, and evaluation. DIDRAH core workflows remain fail-open when it is unavailable." "External,Observability"

        didrah = softwareSystem "DIDRAH" "A bounded agentic management assistant. It computes deterministic metrics and supports human decisions." "Target" {
            !docs docs
            !adrs adrs adrtools

            properties {
                "architecture.status" "Proposed"
                "architecture.style" "Modular Monolith"
                "database.decision" "PostgreSQL only"
                "agent.boundary" "One bounded AI agent; deterministic core outside the agent"
            }

            webApp = container "Web Application" "Persian RTL web application. It provides the three required management interfaces." "React 19, TypeScript, Vite" "Web" {
                chatUi = component "Conversational Assistant UI" "Shows reports and answers. It accepts scoped questions, uploads, and manager operations." "Web UI" "Web"
                dashboardUi = component "Role-Based Dashboard UI" "Shows authorized KPIs, targets, trends, drill-downs, decisions, and open actions." "Web UI" "Web"
                workflowUi = component "Workflow Control Room UI" "Shows WF1-WF3, stage SLA, bottlenecks, escalations, and pending decisions. Senior Manager only." "Web UI" "Web,ExecutiveOnly"
            }

            backendApi = container "Backend API" "Authenticates and authorizes requests, creates durable agent jobs in PostgreSQL, coordinates optional Runtime wake-ups, validates outcomes, and delivers results." "ASP.NET Core, .NET 10 LTS, REST/JSON, OpenAPI" "API" {
                group "01 Access" {
                    identityBoundary = component "Identity Boundary" "Validates the session and creates a trusted identity context." "Deterministic module" "Security"
                    authorizationService = component "Authorization Service" "Builds the permitted row, column, role, purpose, and policy scope." "Deterministic module" "Security"
                }

                group "02 Request Routing" {
                    managerInputService = component "Manager Request Router" "Classifies each authorized request by its explicit request type and sends it to one fixed handler. It does not authorize requests, execute work, or create jobs." "Deterministic request dispatcher" "API"
                    configurationService = component "Configuration Service" "Accepts authorized configuration candidates, stores inactive versions, queues deterministic validation, and activates only an approved valid version. It does not calculate KPIs." "Deterministic configuration control" "Governance"
                    organizationConfigurationService = component "Organization Configuration Service" "Applies versioned organization changes: manager, scope, RLS, mandatory reports, activation time, cache, conversation, query visibility, recipient list. Activates at D+1 after deterministic validation." "Deterministic organization control" "Governance"
                    decisionTracker = component "Decision and Follow-Up" "Records an authorized human decision, its owner, deadline, success criteria, guardrail, and later follow-up results. It does not execute the decision." "Deterministic decision control" "Decision"
                    runCoordinatorV2 = component "Run Coordinator" "Accepts run commands only from the Scheduler and Replay Runner. It creates each pinned run and its complete job plan, stores dependencies and manager order, monitors terminal jobs, and closes the run. It does not execute jobs." "Deterministic run control" "Governance"
                }

                group "03 Bounded Analysis" {
                    agentGateway = component "Agent Runtime Gateway" "Validates and durably enqueues idempotent interactive Agent Jobs in PostgreSQL. For already-created jobs such as document analysis, it sends only a best-effort authenticated job-ID wake-up. It does not execute graphs or make the wake-up the source of truth." "Deterministic job gateway" "AI" {
                        url "{workspace}/documentation/DIDRAH#agent-runtime-gateway"
                    }
                    evidenceService = component "Evidence Service" "Builds a traceable Evidence Bundle inside the authorized scope supplied with the request." "Deterministic module" "Evidence" {
                        url "{workspace}/documentation/DIDRAH#evidence-service"
                    }
                    queryGateway = component "Query Gateway" "Runs registered tools and scoped read-only SQL with limits and audit." "Deterministic query execution" "Query" {
                        url "{workspace}/documentation/DIDRAH#query-gateway"
                    }
                    sqlGuard = component "SQL AST Guard" "Allows one approved SELECT statement and rejects unsafe SQL." "SQL parser and policy" "Security" {
                        url "{workspace}/documentation/DIDRAH#sql-ast-guard"
                    }
                }

                group "04 Validate and Deliver" {
                    outputValidator = component "Output Validator" "Checks the output schema, cited values, evidence references, allowed scope, response rules, and decision-card contract. Persists a validation receipt and validated/rejected job state; it does not repeat KPI calculation, document parsing, or report-evidence assembly." "Deterministic validator" "Governance"
                    agentJobStatusService = component "Agent Job Status API" "Returns an authorized agent-job ID and its queued, running, awaiting-validation, validated, published, or failed status; reads persisted outcomes from PostgreSQL and never executes jobs." "Deterministic delivery API" "API"
                    publisherV2 = component "Publisher" "Atomically publishes model-independent canonical JSON with validated Persian narrative when available, or deterministic fallback text when the model API is unavailable. It records publication receipts and artifact failures." "Deterministic publication module" "Processing"
                    submissionExporter = component "Submission Exporter" "Reads validated reports and QA results, validates against JSON Schema, resolves a contained direct join under OUTPUT_DIR, and writes atomically to briefs/ and qa/ with hash, relative artifact path, trace ID, and export receipt. No internal logs or database files are exported." "Deterministic export module" "Processing"
                    reportApi = component "Report and Dashboard API" "Reads published reports and dashboard data, and returns validated interactive answers or explicit failures." "Deterministic delivery API" "API"
                    auditService = component "Audit Service" "Records query, model, validation, cost, and failure evidence." "Deterministic module" "Governance"
                }

                group "05 Document Decision Flow" {
                    documentProcessingRunner = component "Document Processing Runner" "Accepts authorized uploads, preserves original bytes, parses deterministically, and creates a durable document-analysis Agent Job only after successful parsing. On manager edit, it can create an idempotent revision job from already-approved pinned fragments. It may request a best-effort Runtime wake-up; it never claims or executes jobs." "Deterministic document intake and job producer" "Processing"
                    documentParser = component "Document Parser" "Reads approved upload bytes, validates a supported document contract, and stores immutable fragments and a parse receipt. It treats document content as data, not instructions." "Deterministic document parser" "Processing"
                    decisionConfirmationService = component "Decision Confirmation Service" "Stores a validated decision card and accepts authenticated confirm, edit, or reject commands. On edit, it routes a new durable revision job to the producer for that workload type. It forwards only a confirmed card to Decision and Follow-Up and does not execute the decision." "Deterministic decision review control" "Decision"
                }
            }

            worker = container "Background Worker" "Executes deterministic ingestion, snapshot, KPI, workflow, signal, report-evidence, configuration-validation, and decision-effect-evaluation jobs. It stores results in PostgreSQL and does not run agent graphs or publish reports." ".NET 10 Worker Service" "Worker" {
                runStageCoordinatorV2 = component "Run Stage Coordinator" "Claims Ready deterministic jobs from PostgreSQL and invokes ingestion, snapshot, KPI, workflow, signal, report-evidence, and decision-effect-evaluation components according to stored dependencies. It does not create jobs." "PostgreSQL-backed deterministic job runner" "Processing"
                configurationValidationRunnerV2 = component "Configuration Validation Runner" "Claims configuration-validation jobs, checks KPI SQL, type, unit, scope, rollup, dependencies, and parity fixtures, and stores a validation receipt. It does not activate configuration." "PostgreSQL-backed validation runner" "Governance"
                ingestionCoordinator = component "Ingestion Coordinator" "Checks manifests, hashes, idempotency keys, source status, and atomic batch commits." "Deterministic module" "Processing"
                sourceAdapters = component "Source Adapters" "Parse versioned source schemas and preserve the source bytes and headers." "Deterministic adapters" "Processing"
                normalizer = component "Normalizer" "Converts parsed source fields to canonical types, units, identifiers, and time semantics before data-quality validation. It does not parse source formats or decide data quality." "Deterministic normalization module" "Processing"
                dataQualityService = component "Data Quality Service" "Records missing sources, late arrivals, duplicates, corrections, schema changes, and quarantine results." "Deterministic module" "DataQuality"
                snapshotService = component "Snapshot Service" "Pins committed data, organization, access policy, and configuration versions for a run." "Deterministic module" "Processing"
                projectionService = component "Projection Service" "Builds reproducible facts and process projections from committed source events." "Deterministic module" "Processing"
                semanticRegistry = component "Semantic Registry" "Versions KPI definitions, PostgreSQL SQL, units, precision, targets, ownership, and dependencies." "Deterministic registry" "Analytics"
                kpiDefinitionPreprocessor = component "KPI Definition Preprocessor" "Translates and versions approved KPI definitions as PostgreSQL SQL artifacts before deterministic validation and registration." "Deterministic PostgreSQL SQL preprocessor" "Analytics"
                kpiCalculator = component "KPI Calculator" "Executes the 55 approved PostgreSQL KPI queries and records QueryRun and lineage." "PostgreSQL SQL" "Analytics"
                workflowEngine = component "Workflow Engine" "Reconstructs three workflows and calculates stage timing, SLA, backlog, and bottlenecks." "Deterministic process analysis" "Analytics"
                signalEngine = component "Signal Engine" "Maintains SignalEpisode and SignalOccurrence lifecycles, per-recipient status, escalation history, suppression decisions, and grouped executive items under R1-R8. Data issues are excluded from business items; no LLM." "Deterministic rules" "Analytics"
                reportEvidenceBuilderV2 = component "Report Evidence Builder" "Executes one claimed Report Evidence Job. It builds and stores one pinned, manager-scoped Evidence Package and model-independent Canonical Report JSON. It does not create jobs, call a model, validate model output, or publish reports." "Deterministic report evidence assembly" "Reporting"
                decisionEffectEvaluator = component "Decision Effect Evaluator" "Evaluates target KPI against the comparison period and minimum meaningful change, applies guardrail, and records method, assumptions, confidence, confounders, insufficient-data reason, and structured effect evidence. Outputs improved/worsened/too_early/no_change or an explicit not-isolatable assessment. No LLM." "Deterministic evaluation module" "Decision"
            }

            schedulerReplay = container "Scheduler and Replay Runner" "Owns the simulated clock, run lease, replay range, evaluation profile, and resumable job dispatch." ".NET 10 Console or Worker Process" "Scheduler" {
                replayCommandV2 = component "Replay Command" "Accepts a replay range, sequences simulated days, and resumes from the last terminal day." "Application command" "Scheduler,Candidate"
                simulationClockV2 = component "Simulation Clock" "Derives the pinned business date and source cutoff without using the host clock as product time." "Deterministic clock" "Scheduler,Candidate"
                evaluationProfileLoaderV2 = component "Evaluation Profile Loader" "Loads the selected evaluation limits, acceptance thresholds, and run options." "Deterministic configuration reader" "Evaluation,Candidate"
                runStatusClientV2 = component "Run Status Client" "Starts and monitors runs only through the Backend Run Coordinator." "Internal API client" "Scheduler,Candidate"
                acceptanceTestHarnessV2 = component "Acceptance Test Harness" "Runs replay, hidden-data, regression, leakage, performance, cost, output-contract, and SQLite/PostgreSQL KPI parity checks outside the daily report-publication path." "Deterministic test harness" "Evaluation,Candidate"
                kpiParityValidator = component "KPI Parity Validator" "Executes 55 reference SQL on SQLite and translated PostgreSQL SQL on equivalent snapshot, compares row sets, nulls, values within ±1%, median vs percentile_cont, timezone, date boundaries. Produces Parity Receipt per KPI. No Agent role." "Deterministic parity module" "Evaluation"
                scriptedManagerInputAdapter = component "Scripted Manager Input Adapter" "Reads versioned scripted manager inputs and approved attachment references for deterministic replay, then submits them through the same Backend API boundary as interactive inputs." "Deterministic evaluation input adapter" "Evaluation"
            }

            postgres = container "PostgreSQL" "The only product database. It stores product state, analytical results, access policy, checkpoints, and audit records." "PostgreSQL 18" "Database" {
                properties {
                    "schemas.proposed" "ingest, core, org, semantic, analytics, workflow, reporting, document, decision, agent, audit"
                    "security" "RLS, FORCE ROW LEVEL SECURITY, non-owner runtime roles, no BYPASSRLS"
                    "runtime.roles.proposed" "Separate least-privilege roles for ingestion, analytics, application API, restricted agent job data, and audit reads; final role names are open"
                    "migration.owner" "migration_owner; never used at runtime"
                }
            }

            fileArchive = container "Protected File Archive" "Stores original source and upload bytes with hashes and manifests. It is not a query database." "Protected mounted filesystem or compatible object storage" "Storage"

            agentRuntime = container "Agent Runtime" "Claims and executes all durable report, interactive, and document-analysis Agent Jobs from PostgreSQL. The database is authoritative; authenticated Backend wake-ups are best-effort hints only. No KPI calculation, signal detection, workflow, configuration, or publication." "Python 3.12, LangGraph, Pydantic" "AI" {
                agentOrchestrator = component "Bounded Agent Orchestrator" "Coordinates one bounded report, interactive, or document decision-card graph. Produces structured candidates only." "LangGraph runtime" "AI"
                agentJobRunner = component "Agent Job Runner" "Claims every Ready report, interactive, and document-analysis Agent Job from PostgreSQL with a lease; loads pinned inputs, scope, and checkpoint state; invokes the bounded graph; persists the candidate with awaiting-validation state, or an explicit terminal execution failure, before validation. Polling recovers missed wake-ups." "PostgreSQL-backed unified agent job runner" "AI"
                conversationService = component "Conversation Service" "Stores manager-scoped conversation sessions and validated turns, returns bounded history window." "Deterministic conversation module" "AI"
                agentModelGateway = component "Model Gateway" "Applies token, time, retry, and cost limits to every model call. Reserves and settles budget." "Provider-neutral model client" "AI"
                checkpointStore = component "PostgreSQL Checkpoint Store" "Stores LangGraph checkpoints in PostgreSQL for resumability and idempotency." "PostgreSQL-backed checkpoint" "AI"
            }

            otelCollector = container "OpenTelemetry Collector" "Optionally receives redacted OTLP telemetry from DIDRAH services and exports allowed observability data to Langfuse. Its availability never controls product workflow success." "OpenTelemetry Collector, optional Compose service" "Observability"
        }

        // Scenario-only elements. These mirrors keep numbered cross-container flows
        // explicit without changing the reusable C4 component relationships.
        reportScenarioReplay = element "Replay Command" "Scheduler and Replay Runner" "Resolves the Simulation Clock and Evaluation Profile, then starts one reporting day." "ScenarioStep,ScenarioScheduler"
        reportScenarioRunStatus = element "Run Status Client" "Scheduler and Replay Runner" "Starts and monitors the run only through the Backend Run Coordinator." "ScenarioStep,ScenarioScheduler"
        reportScenarioRunCoordinator = element "Run Coordinator" "Backend API" "Creates the pinned run and complete job plan, stores dependencies and manager order, monitors terminal jobs, and closes the run." "ScenarioStep,ScenarioBackend"
        reportScenarioPostgres = element "PostgreSQL" "Job and report store" "Stores durable jobs, pinned inputs, report packages, final run status, published reports, and publication receipts." "ScenarioStep,ScenarioDatabase"
        reportScenarioRunStage = element "Run Stage Coordinator" "Background Worker" "Claims Ready deterministic jobs and invokes their components according to dependencies stored in PostgreSQL." "ScenarioStep,ScenarioWorker"
        reportScenarioIngestion = element "Ingestion Coordinator" "Background Worker" "Runs source parsing and data-quality checks through Source Adapters and Data Quality Service." "ScenarioStep,ScenarioWorker"
        reportScenarioSnapshot = element "Snapshot Service" "Background Worker" "Creates the pinned Snapshot and requests reproducible projections from Projection Service." "ScenarioStep,ScenarioWorker"
        reportScenarioKpi = element "KPI Calculator" "Background Worker" "Calculates approved KPIs using definitions from Semantic Registry." "ScenarioStep,ScenarioWorker"
        reportScenarioWorkflow = element "Workflow Engine" "Background Worker" "Reconstructs WF1-WF3 and calculates stage, SLA, backlog, and bottleneck observations." "ScenarioStep,ScenarioWorker"
        reportScenarioSignal = element "Signal Engine" "Background Worker" "Detects, groups, ranks, suppresses, and escalates deterministic signals." "ScenarioStep,ScenarioWorker"
        reportScenarioEvidenceBuilder = element "Report Evidence Builder" "Background Worker" "Executes one Report Evidence Job and stores the pinned Evidence Package and Canonical Report JSON without a model call." "ScenarioStep,ScenarioWorker"
        reportScenarioAgentRunner = element "Agent Job Runner" "Agent Runtime" "Claims and leases every Ready Agent Job type, loads pinned inputs, and persists candidate or execution failure before validation." "ScenarioStep,ScenarioAgent"
        reportScenarioAuthorization = element "Authorization Service" "Backend API" "Revalidates the pinned manager scope for the agent job." "ScenarioStep,ScenarioBackend"
        reportScenarioAgent = element "Bounded Agent Orchestrator" "Agent Runtime" "Runs the bounded report narrative graph and returns a candidate only." "ScenarioStep,ScenarioAgent"
        reportScenarioModel = element "Model Gateway" "Agent Runtime" "Applies shared budget and model limits and returns a completion or explicit failure." "ScenarioStep,ScenarioAgent"
        reportScenarioValidator = element "Output Validator" "Backend API" "Validates Canonical Report JSON, narrative or model failure, evidence, scope, schema, and report rules." "ScenarioStep,ScenarioBackend"
        reportScenarioPublisher = element "Publisher" "Backend API" "Publishes each validated manager report or authorized deterministic fallback and records its publication receipt." "ScenarioStep,ScenarioBackend"
        reportScenarioDelivery = element "Report and Dashboard API / Web Application" "Report delivery" "Reads and delivers each published manager report." "ScenarioStep,ScenarioWeb"

        reportScenarioReplay -> reportScenarioRunStatus "01. Prepare one reporting day" "In-process function call"
        reportScenarioRunStatus -> reportScenarioRunCoordinator "02. Request a pinned run" "HTTPS/JSON"
        reportScenarioRunCoordinator -> reportScenarioPostgres "03. Create the Run, all Jobs, dependencies, and manager order" "PostgreSQL protocol over TLS"
        reportScenarioRunStage -> reportScenarioPostgres "04. Claim Ready deterministic Jobs" "PostgreSQL protocol over TLS"
        reportScenarioRunStage -> reportScenarioIngestion "05. Run ingestion and data-quality checks" "In-process function call"
        reportScenarioRunStage -> reportScenarioSnapshot "06. Create the pinned Snapshot" "In-process function call"
        reportScenarioRunStage -> reportScenarioKpi "07. Calculate approved KPIs" "In-process function call"
        reportScenarioRunStage -> reportScenarioWorkflow "08. Reconstruct workflows" "In-process function call"
        reportScenarioRunStage -> reportScenarioSignal "09. Detect and rank signals" "In-process function call"
        reportScenarioRunStage -> reportScenarioEvidenceBuilder "10. For each manager in order, execute the Ready Report Evidence Job" "In-process function call"
        reportScenarioEvidenceBuilder -> reportScenarioPostgres "11. Store package, complete evidence Job, and unlock the preplanned Agent Job" "PostgreSQL protocol over TLS"
        reportScenarioAgentRunner -> reportScenarioPostgres "12. Claim and lease Ready Agent Job; load pinned report package, scope, and checkpoint" "PostgreSQL protocol over TLS"
        reportScenarioAgentRunner -> reportScenarioAuthorization "13. Revalidate pinned manager scope over the Backend API boundary" "Authenticated HTTPS/JSON"
        reportScenarioAgentRunner -> reportScenarioAgent "14. Run the bounded report graph" "In-process function call"
        reportScenarioAgent -> reportScenarioModel "15. Request bounded narrative generation" "In-process function call"
        reportScenarioModel -> reportScenarioAgent "16. Return completion or explicit model failure" "In-process function call"
        reportScenarioAgent -> reportScenarioAgentRunner "17. Return narrative candidate or model failure to job owner" "In-process function call"
        reportScenarioAgentRunner -> reportScenarioPostgres "18. Persist candidate as awaiting-validation or explicit terminal execution failure" "PostgreSQL protocol over TLS"
        reportScenarioAgentRunner -> reportScenarioValidator "19. Submit persisted outcome for deterministic validation" "Authenticated HTTPS/JSON"
        reportScenarioValidator -> reportScenarioPublisher "20. Release valid report or authorized fallback" "In-process function call"
        reportScenarioPublisher -> reportScenarioPostgres "21. Publish report, complete Job, and unlock the next manager" "PostgreSQL protocol over TLS"
        reportScenarioPostgres -> reportScenarioDelivery "22. Deliver the published manager report" "PostgreSQL protocol over TLS"
        reportScenarioRunCoordinator -> reportScenarioPostgres "23. After all required Jobs are terminal, persist final status and close the Run" "PostgreSQL protocol over TLS"

        // Scenario-only mirrors: durable jobs are committed before any Runtime wake-up.
        chatDecisionManager = element "A - Manager" "Scenario A - decision in manager chat" "Submits a decision request and is the only actor allowed to confirm, edit, or reject a validated card." "ScenarioStep,ScenarioActor"
        chatDecisionUi = element "A - Conversational Assistant UI" "Web Application" "Submits chat/review requests, displays the queued job ID, and polls authorized job status until a validated card is ready." "ScenarioStep,ScenarioWeb"
        chatDecisionIdentity = element "A - Identity Boundary" "Backend API" "Validates the manager session and creates trusted identity context." "ScenarioStep,ScenarioChat"
        chatDecisionAuthorization = element "A - Authorization Service" "Backend API" "Builds and rechecks permitted role, row, column, purpose, and policy scope." "ScenarioStep,ScenarioChat"
        chatDecisionRouter = element "A - Manager Request Router" "Backend API" "Routes authorized chat, status, and review requests to fixed handlers." "ScenarioStep,ScenarioChat"
        chatDecisionGateway = element "A - Agent Runtime Gateway" "Backend API" "Creates an idempotent interactive Agent Job in PostgreSQL and sends only a best-effort authenticated job-ID wake-up." "ScenarioStep,ScenarioChat"
        chatDecisionAgentRunner = element "A - Agent Job Runner" "Agent Runtime" "Claims and leases canonical jobs from PostgreSQL, loads pinned inputs, runs the graph, and persists its candidate or failure." "ScenarioStep,ScenarioAgent"
        chatDecisionStatus = element "A - Agent Job Status API" "Backend API" "Returns authorized queued, running, awaiting-validation, validated, or failed status and persisted result references." "ScenarioStep,ScenarioChat"
        chatDecisionConversation = element "A - Conversation Service" "Agent Runtime" "Stores manager-scoped turns and supplies bounded history; conversation text is not business evidence." "ScenarioStep,ScenarioAgent"
        chatDecisionEvidence = element "A - Evidence Service" "Backend API" "Builds a traceable Evidence Bundle inside the trusted scope." "ScenarioStep,ScenarioChat"
        chatDecisionQuery = element "A - Query Gateway" "Backend API" "Runs registered tools and scoped read-only SQL with limits and audit." "ScenarioStep,ScenarioChat"
        chatDecisionSqlGuard = element "A - SQL AST Guard" "Backend API" "Allows one approved SELECT statement and rejects unsafe SQL." "ScenarioStep,ScenarioChat"
        chatDecisionAgent = element "A - Bounded Agent Orchestrator" "Agent Runtime" "Produces a structured interactive decision-card candidate; it cannot confirm or execute it." "ScenarioStep,ScenarioAgent"
        chatDecisionModel = element "A - Model Gateway" "Agent Runtime" "Applies token, time, retry, and cost limits to bounded analysis and drafting." "ScenarioStep,ScenarioAgent"
        chatDecisionValidator = element "A - Output Validator" "Backend API" "Checks decision-card contract, cited values, evidence, scope, and response rules." "ScenarioStep,ScenarioChat"
        chatDecisionConfirmation = element "A - Decision Confirmation Service" "Backend API" "Stores the validated card and accepts only an authenticated manager review command." "ScenarioStep,ScenarioChat"
        chatDecisionTracker = element "A - Decision and Follow-Up" "Backend API" "Records a confirmed human decision and follow-up contract without executing the decision." "ScenarioStep,ScenarioChat"
        chatDecisionPostgres = element "A - PostgreSQL" "Scenario A state" "Stores durable Agent Jobs, pinned request/scope, conversation, outcomes, validation/review state, decisions, and follow-up events." "ScenarioStep,ScenarioDatabase"

        chatDecisionManager -> chatDecisionUi "A01. Enter a decision request in manager chat" "Human interaction"
        chatDecisionUi -> chatDecisionIdentity "A02. Submit session and request over HTTPS/JSON" "HTTPS/JSON"
        chatDecisionIdentity -> chatDecisionAuthorization "A03. Validate session and create trusted AuthContext" "In-process function call"
        chatDecisionAuthorization -> chatDecisionRouter "A04. Pass trusted scope and request context" "In-process function call"
        chatDecisionRouter -> chatDecisionGateway "A05. Route decision-card request for durable enqueue" "In-process function call"
        chatDecisionGateway -> chatDecisionPostgres "A06. Commit idempotent Agent Job with actor, scope, policy, request, and conversation references; return job ID" "PostgreSQL protocol over TLS"
        chatDecisionGateway -> chatDecisionAgentRunner "A07. Best-effort authenticated wake-up carrying only job ID" "Authenticated HTTPS wake-up with job_id"
        chatDecisionGateway -> chatDecisionRouter "A08. Return committed job ID to request handler" "In-process function call"
        chatDecisionRouter -> chatDecisionUi "A09. Return accepted job ID; request may finish before execution" "HTTPS/JSON"
        chatDecisionUi -> chatDecisionManager "A10. Display pending job ID" "Human interaction"
        chatDecisionAgentRunner -> chatDecisionPostgres "A11. Claim and lease Ready job; load canonical pinned inputs and scope" "PostgreSQL protocol over TLS"
        chatDecisionAgentRunner -> chatDecisionAuthorization "A12. Revalidate pinned scope through Backend policy boundary" "Authenticated HTTPS/JSON"
        chatDecisionAgentRunner -> chatDecisionAgent "A13. Invoke bounded interactive decision-card graph" "In-process function call"
        chatDecisionAgent -> chatDecisionConversation "A14. Store manager turn and load bounded history" "In-process function call"
        chatDecisionConversation -> chatDecisionPostgres "A15. Read/write manager-scoped conversation" "PostgreSQL protocol over TLS"
        chatDecisionAgent -> chatDecisionEvidence "A16. Request authorized Evidence Bundle from Backend" "Authenticated HTTPS/JSON"
        chatDecisionEvidence -> chatDecisionQuery "A17. Run registered evidence queries within trusted scope" "In-process function call"
        chatDecisionQuery -> chatDecisionSqlGuard "A18. Validate one approved SELECT" "In-process function call"
        chatDecisionSqlGuard -> chatDecisionQuery "A19. Return approval or refusal" "In-process function call"
        chatDecisionQuery -> chatDecisionPostgres "A20. Execute approved read-only query and retain lineage" "PostgreSQL protocol over TLS"
        chatDecisionAgent -> chatDecisionModel "A21. Request bounded analysis and decision-card draft" "In-process function call"
        chatDecisionModel -> chatDecisionAgent "A22. Return completion or explicit terminal failure" "In-process function call"
        chatDecisionAgent -> chatDecisionAgentRunner "A23. Return structured candidate or failure to job owner" "In-process function call"
        chatDecisionAgentRunner -> chatDecisionPostgres "A24. Persist candidate with awaiting-validation state, or explicit terminal execution failure" "PostgreSQL protocol over TLS"
        chatDecisionAgentRunner -> chatDecisionValidator "A25. Submit persisted candidate/failure for deterministic validation" "Authenticated HTTPS/JSON"
        chatDecisionValidator -> chatDecisionConfirmation "A26. Release only valid card for manager review" "In-process function call"
        chatDecisionConfirmation -> chatDecisionPostgres "A27. Store validated card, evidence references, and review state" "PostgreSQL protocol over TLS"
        chatDecisionUi -> chatDecisionIdentity "A28. Poll job status with authenticated session" "HTTPS/JSON"
        chatDecisionIdentity -> chatDecisionAuthorization "A29. Revalidate identity and scope for status read" "In-process function call"
        chatDecisionAuthorization -> chatDecisionRouter "A30. Pass authorized status request" "In-process function call"
        chatDecisionRouter -> chatDecisionStatus "A31. Route status request to fixed handler" "In-process function call"
        chatDecisionStatus -> chatDecisionPostgres "A32. Read authorized job status and persisted result" "PostgreSQL protocol over TLS"
        chatDecisionStatus -> chatDecisionUi "A33. Return queued/running/awaiting-validation state, validated card reference, or explicit failure" "HTTPS/JSON"
        chatDecisionUi -> chatDecisionManager "A34. Display pending state or validated card; system does not confirm or execute it" "Human interaction"
        chatDecisionManager -> chatDecisionUi "A35. Choose confirm, edit, or reject" "Human interaction"
        chatDecisionUi -> chatDecisionIdentity "A36. Submit authenticated review command" "HTTPS/JSON"
        chatDecisionIdentity -> chatDecisionAuthorization "A37. Revalidate identity and recreate trusted AuthContext" "In-process function call"
        chatDecisionAuthorization -> chatDecisionRouter "A38. Pass authorized review command" "In-process function call"
        chatDecisionRouter -> chatDecisionConfirmation "A39. Route review command to fixed handler" "In-process function call"
        chatDecisionConfirmation -> chatDecisionGateway "A40. On edit, request a new durable revision job" "In-process function call"
        chatDecisionGateway -> chatDecisionPostgres "A41. Commit idempotent revision Agent Job with updated request and pinned scope" "PostgreSQL protocol over TLS"
        chatDecisionGateway -> chatDecisionAgentRunner "A42. Best-effort wake-up for revision job ID" "Authenticated HTTPS wake-up with job_id"
        chatDecisionConfirmation -> chatDecisionPostgres "A43. On reject, store terminal review status" "PostgreSQL protocol over TLS"
        chatDecisionConfirmation -> chatDecisionTracker "A44. On confirm only, forward manager-confirmed card" "In-process function call"
        chatDecisionTracker -> chatDecisionAuthorization "A45. Recheck decision authority and affected scope" "In-process function call"
        chatDecisionTracker -> chatDecisionPostgres "A46. Append decision, owner, deadline, success criteria, guardrail, and follow-up; do not execute" "PostgreSQL protocol over TLS"

        minutesUploadManager = element "B - Manager" "Scenario B - meeting-minutes upload" "Uploads meeting minutes, then reviews the validated decision card extracted from approved document evidence." "ScenarioStep,ScenarioActor"
        minutesUploadUi = element "B - Conversational Assistant UI" "Web Application" "Submits the authenticated upload, displays a pending analysis job, polls its status, and presents the validated card for manager review." "ScenarioStep,ScenarioWeb"
        minutesUploadIdentity = element "B - Identity Boundary" "Backend API" "Validates the manager session and creates trusted identity context." "ScenarioStep,ScenarioDocument"
        minutesUploadAuthorization = element "B - Authorization Service" "Backend API" "Builds and rechecks the permitted row, column, role, purpose, and policy scope." "ScenarioStep,ScenarioDocument"
        minutesUploadRouter = element "B - Manager Request Router" "Backend API" "Routes authorized upload, status, and review commands to fixed handlers." "ScenarioStep,ScenarioDocument"
        minutesUploadProcessing = element "B - Document Processing Runner" "Backend API" "Archives and deterministically parses the upload; creates a durable Agent Job only after successful parsing." "ScenarioStep,ScenarioDocument"
        minutesUploadParser = element "B - Document Parser" "Backend API" "Validates the supported contract and treats meeting-minutes content as data, not instructions." "ScenarioStep,ScenarioDocument"
        minutesUploadGateway = element "B - Agent Runtime Gateway" "Backend API" "Sends only a best-effort authenticated job-ID wake-up after the durable document Agent Job is committed." "ScenarioStep,ScenarioDocument"
        minutesUploadAgentRunner = element "B - Agent Job Runner" "Agent Runtime" "Claims and leases document-analysis Agent Jobs from PostgreSQL, reloads pinned fragments and scope, executes the graph, and persists its candidate or failure." "ScenarioStep,ScenarioAgent"
        minutesUploadStatus = element "B - Agent Job Status API" "Backend API" "Returns authorized queued, running, awaiting-validation, validated, or failed status and persisted document result references." "ScenarioStep,ScenarioDocument"
        minutesUploadAgent = element "B - Bounded Agent Orchestrator" "Agent Runtime" "Produces a structured document decision-card candidate without confirming or executing it." "ScenarioStep,ScenarioAgent"
        minutesUploadModel = element "B - Model Gateway" "Agent Runtime" "Applies token, time, retry, and cost limits to bounded document analysis and drafting." "ScenarioStep,ScenarioAgent"
        minutesUploadValidator = element "B - Output Validator" "Backend API" "Checks the decision-card contract, document evidence references, scope, and response rules." "ScenarioStep,ScenarioDocument"
        minutesUploadConfirmation = element "B - Decision Confirmation Service" "Backend API" "Stores the validated card and accepts only an authenticated manager review command." "ScenarioStep,ScenarioDocument"
        minutesUploadTracker = element "B - Decision and Follow-Up" "Backend API" "Records a confirmed human decision and its follow-up contract without executing the decision." "ScenarioStep,ScenarioDocument"
        minutesUploadArchive = element "B - Protected File Archive" "Protected storage" "Stores original upload bytes with their hash and manifest." "ScenarioStep,ScenarioStorage"
        minutesUploadPostgres = element "B - PostgreSQL" "Scenario B state" "Stores immutable fragments, parse receipts, durable document Agent Jobs, pinned scope, outcomes, review state, decisions, and follow-up events." "ScenarioStep,ScenarioDatabase"

        minutesUploadManager -> minutesUploadUi "B01. Select meeting minutes and explicit supported document type" "Human interaction"
        minutesUploadUi -> minutesUploadIdentity "B02. Submit session and upload over HTTPS" "HTTPS/JSON"
        minutesUploadIdentity -> minutesUploadAuthorization "B03. Validate session and create trusted AuthContext" "In-process function call"
        minutesUploadAuthorization -> minutesUploadRouter "B04. Pass trusted scope and upload context" "In-process function call"
        minutesUploadRouter -> minutesUploadProcessing "B05. Route authorized document upload" "In-process function call"
        minutesUploadProcessing -> minutesUploadArchive "B06. Preserve original bytes, hash, and manifest" "Controlled filesystem I/O"
        minutesUploadProcessing -> minutesUploadParser "B07. Request deterministic parsing of archived upload" "In-process function call"
        minutesUploadParser -> minutesUploadArchive "B08. Read only approved original upload bytes" "Controlled filesystem I/O"
        minutesUploadParser -> minutesUploadPostgres "B09. On successful parse, store immutable fragments and parse receipt" "PostgreSQL protocol over TLS"
        minutesUploadParser -> minutesUploadProcessing "B10. On unsupported/invalid document, return parse failure; create no Agent Job" "In-process function call"
        minutesUploadProcessing -> minutesUploadPostgres "B11. After parse success, commit one durable document Agent Job with actor, scope, policy, and fragment references" "PostgreSQL protocol over TLS"
        minutesUploadProcessing -> minutesUploadRouter "B12a. On parse failure, return failure without a job ID" "In-process function call"
        minutesUploadProcessing -> minutesUploadGateway "B12b. After job commit, request best-effort Runtime wake-up" "In-process function call"
        minutesUploadGateway -> minutesUploadAgentRunner "B13. Send authenticated wake-up containing job ID only" "Authenticated HTTPS wake-up with job_id"
        minutesUploadProcessing -> minutesUploadRouter "B14. Return committed job ID after successful parse and enqueue" "In-process function call"
        minutesUploadRouter -> minutesUploadUi "B15. Return accepted job ID; analysis may continue asynchronously" "HTTPS/JSON"
        minutesUploadAgentRunner -> minutesUploadPostgres "B16. Claim and lease Ready document job; load pinned fragments and scope" "PostgreSQL protocol over TLS"
        minutesUploadAgentRunner -> minutesUploadAuthorization "B17. Revalidate pinned actor and document scope" "Authenticated HTTPS/JSON"
        minutesUploadAgentRunner -> minutesUploadAgent "B18. Invoke bounded document decision-card graph" "In-process function call"
        minutesUploadAgent -> minutesUploadModel "B19. Request bounded analysis of approved document evidence" "In-process function call"
        minutesUploadModel -> minutesUploadAgent "B20. Return completion or explicit terminal failure" "In-process function call"
        minutesUploadAgent -> minutesUploadAgentRunner "B21. Return structured decision-card candidate or failure" "In-process function call"
        minutesUploadAgentRunner -> minutesUploadPostgres "B22. Persist candidate with awaiting-validation state, or explicit terminal execution failure" "PostgreSQL protocol over TLS"
        minutesUploadAgentRunner -> minutesUploadValidator "B23. Submit persisted candidate/failure for deterministic validation" "Authenticated HTTPS/JSON"
        minutesUploadValidator -> minutesUploadConfirmation "B24. Release only a valid card for manager review" "In-process function call"
        minutesUploadConfirmation -> minutesUploadPostgres "B25. Store validated card, evidence references, and review status" "PostgreSQL protocol over TLS"
        minutesUploadUi -> minutesUploadIdentity "B26. Poll analysis status using authenticated session" "HTTPS/JSON"
        minutesUploadIdentity -> minutesUploadAuthorization "B27. Revalidate identity and scope for status read" "In-process function call"
        minutesUploadAuthorization -> minutesUploadRouter "B28. Pass authorized status request" "In-process function call"
        minutesUploadRouter -> minutesUploadStatus "B29. Route status request to fixed handler" "In-process function call"
        minutesUploadStatus -> minutesUploadPostgres "B30. Read authorized job state and persisted result" "PostgreSQL protocol over TLS"
        minutesUploadStatus -> minutesUploadUi "B31. Return queued/running/awaiting-validation state, validated card reference, or explicit failure" "HTTPS/JSON"
        minutesUploadUi -> minutesUploadManager "B32. Display validated card; system does not send or execute it" "Human interaction"
        minutesUploadManager -> minutesUploadUi "B33. Choose confirm, edit, or reject" "Human interaction"
        minutesUploadUi -> minutesUploadIdentity "B34. Submit authenticated review command" "HTTPS/JSON"
        minutesUploadIdentity -> minutesUploadAuthorization "B35. Revalidate identity and recreate trusted AuthContext" "In-process function call"
        minutesUploadAuthorization -> minutesUploadRouter "B36. Pass authorized review command" "In-process function call"
        minutesUploadRouter -> minutesUploadConfirmation "B37. Route review command to fixed handler" "In-process function call"
        minutesUploadConfirmation -> minutesUploadProcessing "B38a. On edit, request a document-analysis revision using the existing approved fragments" "In-process function call"
        minutesUploadProcessing -> minutesUploadPostgres "B38b. Commit idempotent revision job with updated request and pinned references" "PostgreSQL protocol over TLS"
        minutesUploadProcessing -> minutesUploadGateway "B38c. Request best-effort wake-up after revision job commit" "In-process function call"
        minutesUploadGateway -> minutesUploadAgentRunner "B38d. Send job-ID-only wake-up for revision" "Authenticated HTTPS wake-up with job_id"
        minutesUploadConfirmation -> minutesUploadPostgres "B39. On reject, store terminal review status" "PostgreSQL protocol over TLS"
        minutesUploadConfirmation -> minutesUploadTracker "B40. On confirm only, forward manager-confirmed card" "In-process function call"
        minutesUploadTracker -> minutesUploadAuthorization "B41. Recheck decision authority and affected scope" "In-process function call"
        minutesUploadTracker -> minutesUploadPostgres "B42. Append decision, owner, deadline, success criteria, guardrail, and follow-up; do not execute" "PostgreSQL protocol over TLS"

        // Additional scenario-only mirrors complete the active 16-view set without adding product components.
        failureService = element "Product Services" "Failure and fallback" "Detect a workflow or model failure and retain durable product state." "ScenarioStep,ScenarioBackend"
        failureFallback = element "Deterministic Fallback" "Failure and fallback" "Publishes only an authorized deterministic fallback or an explicit failure." "ScenarioStep,ScenarioWorker"
        failureObservability = element "Optional Observability" "Failure and fallback" "Receives redacted telemetry without controlling product success." "ScenarioStep,ScenarioAgent"
        failureService -> failureFallback "Use validated fallback rules or return an explicit failure" "In-process function call"
        failureFallback -> failureObservability "Export redacted failure telemetry when available" "OTLP"

        kpiTranslation = element "KPI Definition Preprocessor" "KPI translation and parity" "Translates an approved KPI candidate to versioned PostgreSQL SQL." "ScenarioStep,ScenarioWorker"
        kpiValidation = element "Configuration Validation Runner" "KPI translation and parity" "Validates SQL, type, unit, scope, rollup, dependencies, and fixtures." "ScenarioStep,ScenarioWorker"
        kpiParity = element "KPI Parity Validator" "KPI translation and parity" "Compares equivalent SQLite reference and PostgreSQL results in the acceptance path." "ScenarioStep,ScenarioScheduler"
        kpiTranslation -> kpiValidation "Validate the translated definition and fixtures" "In-process function call"
        kpiValidation -> kpiParity "Run acceptance parity after deterministic validation" "Acceptance test interface"

        orgCandidate = element "Inactive Organization Revision Intake" "Organization configuration D+1" "Accepts an authorized organization revision as inactive." "ScenarioStep,ScenarioBackend"
        orgValidation = element "Organization Revision Validator" "Organization configuration D+1" "Validates the inactive revision before activation." "ScenarioStep,ScenarioWorker"
        orgActivation = element "D+1 Organization Activator" "Organization configuration D+1" "Activates only an approved valid revision at the D+1 boundary." "ScenarioStep,ScenarioBackend"
        orgCandidate -> orgValidation "Queue deterministic validation" "PostgreSQL-backed job queue"
        orgValidation -> orgActivation "Return a durable validation receipt for D+1 activation" "PostgreSQL protocol over TLS"

        scriptedInput = element "Scripted Manager Input Adapter" "Scripted manager input replay" "Reads a versioned evaluation input and approved attachment references." "ScenarioStep,ScenarioScheduler"
        scriptedApi = element "Backend API" "Scripted manager input replay" "Applies the same identity, authorization, and request boundary used by interactive inputs." "ScenarioStep,ScenarioBackend"
        scriptedResult = element "Replay Acceptance" "Scripted manager input replay" "Checks durable result and contract evidence." "ScenarioStep,ScenarioScheduler"
        scriptedInput -> scriptedApi "Submit the pinned scripted input" "HTTPS, REST/JSON"
        scriptedApi -> scriptedResult "Return job status and validated result references" "HTTPS, REST/JSON"

        restatementIntake = element "Normalized Intake" "Late or corrected data restatement" "Re-ingests and normalizes a late or corrected source batch." "ScenarioStep,ScenarioWorker"
        restatementCompute = element "Deterministic Recalculation" "Late or corrected data restatement" "Pins corrected inputs and recomputes affected projections, KPIs, workflows, and signals." "ScenarioStep,ScenarioWorker"
        restatementPublish = element "Validated Republishing" "Late or corrected data restatement" "Publishes only validated restated artifacts and traceable receipts." "ScenarioStep,ScenarioBackend"
        restatementIntake -> restatementCompute "Recompute affected deterministic results from the corrected snapshot" "In-process function call"
        restatementCompute -> restatementPublish "Validate and republish affected manager artifacts" "PostgreSQL-backed job queue"

        // System-level relationships
        seniorManager -> didrah "Reads organization health, workflows, escalations, and pending decisions" "HTTPS"
        unitManager -> didrah "Reads authorized unit and team results and records decisions" "HTTPS"
        teamSupervisor -> didrah "Reads authorized team results and direct-member workload" "HTTPS"
        evaluator -> didrah "Runs replay, hidden-data checks, and acceptance tests" "CLI and HTTPS/JSON"
        operator -> didrah "Monitors runs, failures, cost, backup, and restore evidence" "HTTPS"
        inputDataset -> didrah "Supplies versioned source data and scripted manager activity" "Read-only filesystem: CSV, JSON, and Markdown"
        didrah -> identityProvider "Validates trusted user identities" "OIDC or internal authentication over HTTPS"
        didrah -> llmProvider "Requests bounded model completions" "HTTPS/JSON"
        didrah -> langfuse "Exports optional redacted agent and model telemetry through the OpenTelemetry Collector" "OTLP export"

        // Container-level relationships
        seniorManager -> webApp "Reads organization health, cross-unit workflows, escalations, and decisions" "HTTPS"
        unitManager -> webApp "Reads authorized unit and team results and records decisions" "HTTPS"
        teamSupervisor -> webApp "Reads authorized team results and direct-member workload" "HTTPS"
        evaluator -> schedulerReplay "Starts replay and acceptance checks" "CLI and HTTPS/JSON"
        evaluator -> backendApi "Reads acceptance evidence and exported outputs" "HTTPS/JSON"
        operator -> backendApi "Reads authorized operational status" "HTTPS"
        inputDataset -> worker "Supplies eligible nightly drops, manifests, and source contracts" "Read-only filesystem"
        inputDataset -> schedulerReplay "Supplies scripted manager inputs, upload attachments, and replay scenarios" "Read-only filesystem: JSON, CSV, and Markdown"
        backendApi -> identityProvider "Validates sessions and trusted identities" "OIDC over HTTPS or internal authentication"
        webApp -> backendApi "Requests reports, scoped queries, uploads, configuration changes, and decisions" "HTTPS, REST/JSON, W3C traceparent"
        schedulerReplay -> backendApi "Starts and monitors pinned runs through the Run Coordinator" "HTTPS, REST/JSON"
        schedulerReplay -> postgres "Reads replay state and evidence and records acceptance results" "PostgreSQL protocol over TLS"
        backendApi -> agentRuntime "Sends a best-effort authenticated Agent Runtime wake-up with job_id only; PostgreSQL remains the durable queue and source of job data" "Authenticated HTTPS wake-up with job_id"
        backendApi -> postgres "Reads and writes scoped state; Run Coordinator plans report Agent Jobs, while Gateway and Document Processing Runner create durable interactive and document Agent Jobs" "PostgreSQL protocol over TLS, EF Core/Npgsql"
        worker -> postgres "Claims durable jobs and reads or writes deterministic results" "PostgreSQL protocol over TLS, EF Core/Npgsql"
        worker -> fileArchive "Archives and reads approved source bytes" "Controlled filesystem I/O"
        backendApi -> fileArchive "Archives uploads and reads approved fragments" "Controlled filesystem API"
        backendApi -> submissionOutput "Exports validated brief and QA files by a contained direct join under OUTPUT_DIR" "Controlled filesystem I/O"
        agentRuntime -> postgres "Claims and leases all Ready Agent Jobs through a restricted role, reads pinned job data, and persists outcomes, terminal status, and checkpoints" "Restricted PostgreSQL role"
        agentRuntime -> llmProvider "Calls only through Model Gateway" "HTTPS/JSON"
        agentRuntime -> backendApi "Requests authorized business evidence, scoped queries, and deterministic validation" "HTTPS Evidence/Query/Validation API"
        webApp -> otelCollector "Exports browser telemetry when enabled; product flow is fail-open" "OTLP/HTTP"
        backendApi -> otelCollector "Exports redacted API traces and metrics; product flow is fail-open" "OTLP"
        worker -> otelCollector "Exports redacted worker traces and metrics; product flow is fail-open" "OTLP"
        schedulerReplay -> otelCollector "Exports redacted replay traces and metrics; product flow is fail-open" "OTLP"
        agentRuntime -> otelCollector "Exports allowed agent, model, token, cost, and evaluation telemetry; product flow is fail-open" "OTLP"
        otelCollector -> langfuse "Exports allowed redacted observability data" "OTLP export"

        // Web component relationships
        seniorManager -> chatUi "Reads executive brief and asks aggregate questions" "Human interaction"
        seniorManager -> dashboardUi "Reads organization health" "Human interaction"
        seniorManager -> workflowUi "Reads WF1-WF3 and escalations" "Human interaction"
        unitManager -> chatUi "Reads unit brief and records decisions" "Human interaction"
        unitManager -> dashboardUi "Reads unit and team aggregates" "Human interaction"
        teamSupervisor -> chatUi "Reads team brief and asks scoped questions" "Human interaction"
        teamSupervisor -> dashboardUi "Reads team KPIs and direct-workload details" "Human interaction"
        chatUi -> backendApi "Submits questions and manager operations; retrieves reports and answers" "HTTPS/JSON"
        dashboardUi -> backendApi "Retrieves authorized metrics, trends, and drill-down results" "HTTPS/JSON"
        workflowUi -> backendApi "Retrieves executive workflow, bottleneck, and escalation results" "HTTPS/JSON"

        // API component relationships.
        // Request path: Web -> Identity -> Authorization -> Router -> durable Agent Job -> Runtime Runner -> persisted outcome -> validation/status/delivery.
        webApp -> identityBoundary "Submits session and request" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }
        identityBoundary -> identityProvider "Validates identity" "OIDC over HTTPS or internal authentication" {
            tags "ExternalFlow"
        }
        identityBoundary -> authorizationService "Creates trusted AuthContext" "In-process function call" {
            tags "PrimaryFlow"
        }
        authorizationService -> postgres "Reads hierarchy, grants, and policy" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        authorizationService -> managerInputService "Passes trusted scope and request context" "In-process function call" {
            tags "PrimaryFlow"
        }

        // Request routing and manager commands.
        managerInputService -> reportApi "Routes published report and dashboard reads" "In-process function call" {
            tags "ControlFlow"
        }
        managerInputService -> configurationService "Routes a configuration candidate" "In-process function call" {
            tags "ControlFlow"
        }
        managerInputService -> organizationConfigurationService "Routes an organization change candidate" "In-process function call" {
            tags "ControlFlow"
        }
        managerInputService -> agentGateway "Routes an authorized interactive question or chat decision-card request for durable enqueue" "In-process function call" {
            tags "PrimaryFlow"
        }
        agentGateway -> postgres "Creates an idempotent interactive Agent Job with pinned actor, scope, policy, request, and conversation references" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        agentGateway -> managerInputService "Returns the committed interactive job ID to the request handler" "In-process function call" {
            tags "Feedback"
        }
        managerInputService -> webApp "Returns accepted job ID after durable enqueue" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }
        agentGateway -> agentJobRunner "Sends best-effort authenticated wake-up containing job ID only; Runner claims canonical job data from PostgreSQL" "Internal authenticated API" {
            tags "PrimaryFlow"
        }
        managerInputService -> agentJobStatusService "Routes an authorized agent-job status read" "In-process function call" {
            tags "ControlFlow"
        }
        managerInputService -> documentProcessingRunner "Routes an authorized document upload" "In-process function call" {
            tags "PrimaryFlow"
        }
        managerInputService -> decisionConfirmationService "Routes an authenticated confirm, edit, or reject command" "In-process function call" {
            tags "ControlFlow"
        }
        documentProcessingRunner -> fileArchive "Preserves original upload bytes, hash, and manifest" "Restricted file system I/O" {
            tags "ControlFlow"
        }
        documentProcessingRunner -> documentParser "Requests deterministic parsing of the archived upload" "In-process function call" {
            tags "PrimaryFlow"
        }
        documentParser -> fileArchive "Reads approved original upload bytes" "Restricted file system I/O" {
            tags "DataFlow"
        }
        documentParser -> postgres "Stores immutable document fragments and a parse receipt" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        documentProcessingRunner -> postgres "After successful parsing, creates the durable document-analysis Agent Job with pinned actor, scope, policy, and fragment references" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        documentProcessingRunner -> managerInputService "Returns the committed document job ID to the request handler" "In-process function call" {
            tags "Feedback"
        }
        documentProcessingRunner -> agentGateway "Requests a best-effort Runtime wake-up after the durable document Agent Job is committed" "In-process function call" {
            tags "ControlFlow"
        }
        configurationService -> authorizationService "Checks actor authority and affected scope" "In-process function call" {
            tags "PolicyCheck"
        }
        configurationService -> postgres "Stores an inactive configuration version and enqueues a deterministic validation job" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        organizationConfigurationService -> authorizationService "Checks actor authority and affected scope" "In-process function call" {
            tags "PolicyCheck"
        }
        organizationConfigurationService -> postgres "Stores inactive org revision, queues deterministic validation, activates at D+1" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        decisionTracker -> authorizationService "Checks decision authority" "In-process function call" {
            tags "PolicyCheck"
        }
        decisionTracker -> postgres "Appends decision, follow-up events, success criteria, guardrail" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        decisionTracker -> agentGateway "Requests a draft only" "In-process function call" {
            tags "ControlFlow"
        }

        // Bounded analysis. Tool and model responses are implicit unless a failure path needs a separate edge.
        agentOrchestrator -> evidenceService "Requests an authorized evidence bundle" "Internal authenticated API" {
            tags "DataFlow"
        }
        agentOrchestrator -> conversationService "Stores the manager message and loads bounded conversation history" "Internal authenticated API" {
            tags "DataFlow"
        }
        conversationService -> postgres "Reads and writes manager-scoped sessions and conversation turns" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        evidenceService -> authorizationService "Checks evidence scope" "In-process function call" {
            tags "PolicyCheck"
        }
        evidenceService -> queryGateway "Runs a registered evidence query" "In-process function call" {
            tags "DataFlow"
        }
        evidenceService -> fileArchive "Reads approved original evidence bytes by archive reference" "Restricted file system I/O" {
            tags "DataFlow"
        }
        queryGateway -> authorizationService "Gets scope and allowlists" "In-process function call" {
            tags "PolicyCheck"
        }
        queryGateway -> sqlGuard "Validates one SELECT statement" "In-process function call" {
            tags "DataFlow"
        }
        sqlGuard -> queryGateway "Returns approval or refusal" "In-process function call" {
            tags "Feedback"
        }
        queryGateway -> postgres "Runs a scoped read-only query" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        queryGateway -> auditService "Records query evidence" "In-process function call" {
            tags "ControlFlow"
        }
        agentJobRunner -> postgres "Claims and leases Ready report, interactive, and document Agent Jobs; loads pinned inputs; persists candidate with awaiting-validation state or explicit terminal execution failure" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        agentJobRunner -> agentOrchestrator "Invokes the bounded graph for the claimed job and receives a structured candidate" "In-process function call" {
            tags "PrimaryFlow"
        }
        agentJobRunner -> outputValidator "After persisting the job outcome, submits the candidate or explicit failure for deterministic validation" "Internal authenticated API" {
            tags "PrimaryFlow"
        }
        agentOrchestrator -> agentModelGateway "Requests bounded model analysis or drafting" "In-process function call" {
            tags "ModelFlow"
        }
        agentModelGateway -> postgres "Reserves and settles the shared model-cost budget" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        agentModelGateway -> llmProvider "Sends authorized evidence and receives a completion" "HTTPS/JSON" {
            tags "ExternalFlow"
        }
        agentModelGateway -> agentOrchestrator "Returns a completion or explicit terminal failure" "In-process function call" {
            tags "Feedback"
        }
        checkpointStore -> postgres "Stores and reads LangGraph checkpoints" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        agentJobStatusService -> authorizationService "Checks actor access to the owning job and its result" "In-process function call" {
            tags "PolicyCheck"
        }
        agentJobStatusService -> postgres "Reads authorized Agent Job state, validation receipt, and persisted outcome" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        agentJobStatusService -> webApp "Returns only the owning manager's authorized job status and validated result reference" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }

        // Validation, delivery, and accountability.
        outputValidator -> postgres "Persists validation receipt and moves an awaiting-validation Agent Job to validated or rejected" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        outputValidator -> queryGateway "Rechecks reported numbers" "In-process function call" {
            tags "Feedback"
        }
        outputValidator -> authorizationService "Rechecks recipient scope" "In-process function call" {
            tags "PolicyCheck"
        }
        outputValidator -> evidenceService "Checks provenance and alternatives" "In-process function call" {
            tags "Feedback"
        }
        outputValidator -> auditService "Records validation evidence" "In-process function call" {
            tags "ControlFlow"
        }
        outputValidator -> conversationService "Returns the validated answer or explicit terminal failure for scoped conversation storage" "Internal authenticated API" {
            tags "ControlFlow"
        }
        outputValidator -> decisionConfirmationService "Releases a valid decision card for manager review" "In-process function call" {
            tags "PrimaryFlow"
        }
        decisionConfirmationService -> postgres "Stores the decision candidate, validated card, source references, and review status" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        decisionConfirmationService -> webApp "Returns the decision card or review status" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }
        decisionConfirmationService -> agentGateway "On interactive edit, requests an idempotent revision Agent Job; Gateway commits it to PostgreSQL before a job-ID-only wake-up" "In-process function call" {
            tags "Feedback"
        }
        decisionConfirmationService -> documentProcessingRunner "On document edit, requests an idempotent revision Agent Job from the document producer; approved fragments remain pinned" "In-process function call" {
            tags "Feedback"
        }
        decisionConfirmationService -> decisionTracker "Forwards only a manager-confirmed decision card" "In-process function call" {
            tags "ControlFlow"
        }
        outputValidator -> reportApi "Releases a valid result or explicit failure" "In-process function call" {
            tags "PrimaryFlow"
        }
        reportApi -> authorizationService "Rechecks audience and purpose" "In-process function call" {
            tags "PolicyCheck"
        }
        reportApi -> queryGateway "Runs a dashboard or workflow query" "In-process function call" {
            tags "DataFlow"
        }
        reportApi -> postgres "Reads published reports and failure states" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        reportApi -> webApp "Returns a valid response or explicit failure" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }
        auditService -> postgres "Stores restricted audit evidence" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        publisherV2 -> postgres "Atomically commits Canonical Report JSON, validated narrative or fallback text, and publication receipt; completes the Agent Job and unlocks the next manager Job" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        publisherV2 -> auditService "Records publication mode and artifact failures" "In-process function call" {
            tags "ControlFlow"
        }
        publisherV2 -> submissionExporter "Forwards each validated final report for contract export" "In-process function call" {
            tags "PrimaryFlow"
        }
        outputValidator -> submissionExporter "Forwards each validated QA result for contract export" "In-process function call" {
            tags "PrimaryFlow"
        }
        submissionExporter -> postgres "Reads validated final reports and QA results; records export receipts" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        submissionExporter -> submissionOutput "Writes atomic files to OUTPUT_DIR/briefs/day_XXX/<manager_id>.json and OUTPUT_DIR/qa/<question_id>.json after path-containment validation" "Controlled filesystem I/O" {
            tags "ControlFlow"
        }

        // Worker component relationships
        ingestionCoordinator -> inputDataset "Reads expected nightly drops, manifests, and source contracts" "Read-only filesystem: CSV and JSON"
        ingestionCoordinator -> sourceAdapters "Parses each source contract" "In-process function call"
        sourceAdapters -> fileArchive "Preserves original bytes, headers, and hashes" "Controlled filesystem I/O"
        sourceAdapters -> normalizer "Submits parsed source fields for canonical normalization" "In-process function call"
        normalizer -> dataQualityService "Submits normalized rows and normalization failures for data-quality checks" "In-process function call"
        dataQualityService -> postgres "Writes accepted records, quarantine, and DataIssues" "PostgreSQL protocol over TLS"
        snapshotService -> postgres "Pins committed batches, organization, policy, and configuration versions" "PostgreSQL protocol over TLS"
        snapshotService -> projectionService "Requests reproducible facts and process projections" "In-process function call"
        projectionService -> postgres "Reads events and writes facts and projections" "PostgreSQL protocol over TLS"
        kpiCalculator -> semanticRegistry "Reads approved PostgreSQL SQL and metadata" "In-process function call"
        configurationValidationRunnerV2 -> kpiDefinitionPreprocessor "Translates an approved KPI candidate to versioned PostgreSQL SQL before validation" "In-process function call"
        kpiDefinitionPreprocessor -> semanticRegistry "Registers validated PostgreSQL KPI SQL and metadata as a versioned definition" "In-process function call"
        semanticRegistry -> postgres "Reads versioned KPI definitions and dependencies" "PostgreSQL protocol over TLS"
        kpiCalculator -> postgres "Executes KPI SQL and writes observations, QueryRun, and lineage" "PostgreSQL protocol over TLS"
        workflowEngine -> postgres "Reads events and writes case, stage, SLA, and bottleneck observations" "PostgreSQL protocol over TLS"
        signalEngine -> postgres "Reads KPI and history; writes episodes, occurrences, per-recipient status, suppression, grouping, and escalation events" "PostgreSQL protocol over TLS"
        decisionEffectEvaluator -> postgres "Reads KPI observations, decision records, context; writes structured effect assessment" "PostgreSQL protocol over TLS"
        runStageCoordinatorV2 -> decisionEffectEvaluator "Invokes decision effect evaluation for due follow-ups" "In-process function call"
        decisionEffectEvaluator -> reportEvidenceBuilderV2 "Provides the deterministic follow-up assessment for manager reporting" "In-process function call"

        // Current run-control, report-evidence, agent, publication, and evaluation flow.
        evaluator -> replayCommandV2 "Starts a replay range and requests acceptance results" "Command-line interface"
        inputDataset -> scriptedManagerInputAdapter "Supplies versioned scripted manager inputs and approved attachment references" "Read-only filesystem"
        replayCommandV2 -> scriptedManagerInputAdapter "Requests deterministic manager-input replay for the pinned business date" "In-process function call"
        scriptedManagerInputAdapter -> backendApi "Submits scripted manager inputs through the product API boundary" "HTTPS, REST/JSON"
        inputDataset -> replayCommandV2 "Supplies scripted replay range" "Read-only JSON"
        replayCommandV2 -> simulationClockV2 "Requests one pinned business date and source cutoff per day" "In-process function call"
        replayCommandV2 -> evaluationProfileLoaderV2 "Loads the selected evaluation profile" "In-process function call"
        replayCommandV2 -> runStatusClientV2 "Starts or resumes each simulated day with the pinned date, cutoff, profile, and run options" "In-process function call"
        replayCommandV2 -> acceptanceTestHarnessV2 "Starts acceptance checks after the replay range reaches a terminal state" "In-process function call"
        runStatusClientV2 -> runCoordinatorV2 "Starts and monitors runs through the internal Backend API" "Authenticated HTTPS/JSON"
        runCoordinatorV2 -> authorizationService "Validates the Scheduler or Replay service identity and run-control permission" "In-process function call"
        evaluator -> acceptanceTestHarnessV2 "Starts replay acceptance, hidden-data, and regression checks" "Command-line interface"
        acceptanceTestHarnessV2 -> evaluationProfileLoaderV2 "Loads acceptance thresholds and limits" "In-process function call"
        acceptanceTestHarnessV2 -> runStatusClientV2 "Reads terminal replay run status and artifact references" "In-process function call"
        acceptanceTestHarnessV2 -> postgres "Reads replay evidence and writes acceptance results" "PostgreSQL protocol over TLS"
        acceptanceTestHarnessV2 -> kpiParityValidator "Runs the SQLite/PostgreSQL parity suite" "In-process function call"

        runCoordinatorV2 -> postgres "Creates each pinned Run, all Jobs, dependency edges, and manager execution order; monitors terminal states and records final Run status" "PostgreSQL protocol over TLS"
        configurationService -> configurationValidationRunnerV2 "Queues an inactive configuration candidate for deterministic validation" "PostgreSQL-backed job queue"
        configurationValidationRunnerV2 -> semanticRegistry "Checks the candidate against current KPI definitions and dependencies" "In-process function call"
        configurationValidationRunnerV2 -> postgres "Claims the validation Job and stores SQL, scope, rollup, parity, and validation receipts" "PostgreSQL protocol over TLS"
        runStageCoordinatorV2 -> postgres "Claims run-stage jobs and records stage attempts and outcomes" "PostgreSQL protocol over TLS"
        runStageCoordinatorV2 -> ingestionCoordinator "Invokes idempotent intake for the pinned cutoff" "In-process function call"
        runStageCoordinatorV2 -> snapshotService "Invokes snapshot creation after intake" "In-process function call"
        runStageCoordinatorV2 -> kpiCalculator "Invokes all approved KPI calculations for the snapshot" "In-process function call"
        runStageCoordinatorV2 -> workflowEngine "Invokes WF1-WF3 reconstruction for the snapshot" "In-process function call"
        runStageCoordinatorV2 -> signalEngine "Invokes deterministic signal detection and ranking" "In-process function call"
        runStageCoordinatorV2 -> reportEvidenceBuilderV2 "Invokes the builder for each claimed Report Evidence Job in stored manager order" "In-process function call"
        reportEvidenceBuilderV2 -> postgres "Stores the Evidence Package and Canonical Report JSON, completes the Report Evidence Job, and unlocks its existing Agent Job" "PostgreSQL protocol over TLS"

        outputValidator -> publisherV2 "Releases a validated package or authorizes deterministic fallback publication" "In-process function call"

        // Defined after the static relationships so Structurizr can replicate them between instances.
        deploymentEnvironment "Evaluation" {
            deploymentNode "Evaluation Host and Docker Compose" "Separate service containers started together with one docker compose command." "Docker Compose" {
                deploymentNode "Web" "User interface" "Docker container" {
                    containerInstance webApp
                }
                deploymentNode "Backend API" "API and deterministic validation" "Docker container" {
                    containerInstance backendApi
                }
                deploymentNode "Background Worker" "Deterministic processing" "Docker container" {
                    containerInstance worker
                }
                deploymentNode "Scheduler" "Replay and acceptance" "Docker container" {
                    containerInstance schedulerReplay
                }
                deploymentNode "Agent Runtime" "Bounded agent graphs" "Docker container" {
                    containerInstance agentRuntime
                }
                deploymentNode "PostgreSQL" "Product database" "Docker container" {
                    containerInstance postgres
                }
                deploymentNode "OpenTelemetry Collector" "Optional, fail-open telemetry relay" "Docker container" {
                    containerInstance otelCollector
                }
                deploymentNode "Mounted Filesystems" "Read-only input, protected archive, and writable evaluator output mounts" "Docker volumes or compatible mounted storage" {
                    softwareSystemInstance inputDataset
                    containerInstance fileArchive
                    softwareSystemInstance submissionOutput
                }
            }
            deploymentNode "External Observability Egress" "Optional managed or separately hosted observability endpoint" "External service" {
                softwareSystemInstance langfuse
            }
        }

    }

    views {
        properties {
            "structurizr.sort" "key"
        }

        // C4 core view: one software system and its directly connected people and software systems.
        systemContext didrah L1_SystemContext "Business-facing C4 system context for DIDRAH." {
            title "01 - C4 Level 1 - System Context for DIDRAH"
            include seniorManager unitManager teamSupervisor evaluator operator didrah inputDataset submissionOutput identityProvider llmProvider langfuse
            default
        }

        // C4 core view: deployable applications and data stores inside the DIDRAH boundary.
        container didrah L2_Containers "C4 container view of the DIDRAH applications, data stores, users, and external dependencies." {
            title "02 - C4 Level 2 - Containers for DIDRAH"
            include seniorManager unitManager teamSupervisor evaluator operator inputDataset submissionOutput identityProvider llmProvider langfuse webApp backendApi worker schedulerReplay postgres fileArchive agentRuntime otelCollector
        }

        // Revised C4 Level 3 views.
        component webApp L3_2_WebApplicationComponents "Web Application view for the Persian management interfaces and their authenticated Backend API and optional telemetry boundaries." {
            title "03.2 - C4 Level 3 - Web Application Components"
            include seniorManager unitManager teamSupervisor backendApi otelCollector chatUi dashboardUi workflowUi
        }

        component backendApi L3_3_RevisedBackendApiComponents "Backend API view with durable agent-job producers, a job-ID-only Runtime wake-up, unified Runtime claiming, status reads, in-process document intake and parsing, manager-confirmed decision cards, scheduler-only run control, validation, publication, delivery, and submission export." {
            title "03.3 - C4 Level 3 - Backend API Components"
            include webApp fileArchive submissionOutput identityProvider llmProvider postgres agentRuntime runStatusClientV2 identityBoundary authorizationService managerInputService configurationService organizationConfigurationService decisionTracker runCoordinatorV2 documentProcessingRunner documentParser agentGateway evidenceService queryGateway sqlGuard outputValidator agentJobStatusService decisionConfirmationService publisherV2 submissionExporter reportApi auditService
            exclude "configurationService -> authorizationService"
            exclude "organizationConfigurationService -> authorizationService"
            exclude "decisionTracker -> authorizationService"
            exclude "evidenceService -> authorizationService"
            exclude "queryGateway -> authorizationService"
            exclude "sqlGuard -> queryGateway"
            exclude "outputValidator -> queryGateway"
            exclude "outputValidator -> authorizationService"
            exclude "outputValidator -> evidenceService"
            exclude "reportApi -> authorizationService"
        }

        component worker L3_4_RevisedBackgroundWorkerComponents "Background Worker view with PostgreSQL-backed run-stage execution, independent configuration validation, deterministic analytics, decision effect evaluation, and one-manager-at-a-time report evidence assembly. Manager document processing remains inside the Backend API." {
            title "03.4 - C4 Level 3 - Background Worker Components"
            include inputDataset postgres fileArchive configurationService runCoordinatorV2 runStageCoordinatorV2 configurationValidationRunnerV2 ingestionCoordinator sourceAdapters normalizer dataQualityService snapshotService projectionService semanticRegistry kpiDefinitionPreprocessor kpiCalculator workflowEngine signalEngine reportEvidenceBuilderV2 decisionEffectEvaluator
        }

        component schedulerReplay L3_5_RevisedSchedulerReplayComponents "Revised Scheduler and Replay Runner view that controls simulated time and replay through the Backend Run Coordinator and runs acceptance checks outside the daily publication path." {
            title "03.5 - C4 Level 3 - Revised Scheduler and Replay Runner Components"
            include evaluator inputDataset backendApi postgres runCoordinatorV2 replayCommandV2 simulationClockV2 evaluationProfileLoaderV2 runStatusClientV2 acceptanceTestHarnessV2 kpiParityValidator scriptedManagerInputAdapter
        }

        component agentRuntime L3_6_AgentRuntimeComponents "Agent Runtime view with one PostgreSQL-backed Runner for every report, interactive, and document Agent Job; authenticated wake-ups are hints only, and evidence and validation use Backend services." {
            title "03.6 - C4 Level 3 - Agent Runtime Components"
            include postgres llmProvider agentGateway agentOrchestrator agentJobRunner conversationService agentModelGateway checkpointStore evidenceService queryGateway sqlGuard outputValidator agentJobStatusService auditService
        }

        deployment didrah "Evaluation" D1_EvaluationCompose "Evaluation deployment using separate Docker Compose services started with one command." {
            include *
            autoLayout lr
        }

        // Numbered end-to-end scenario for the revised L3 architecture.
        custom S7_ReportGenerationScenario "04.7 - Scenario - Report Generation" "Primary report-generation path across Scheduler, Backend API, Background Worker, and PostgreSQL." {
            include reportScenarioReplay reportScenarioRunStatus reportScenarioRunCoordinator reportScenarioPostgres reportScenarioRunStage reportScenarioIngestion reportScenarioSnapshot reportScenarioKpi reportScenarioWorkflow reportScenarioSignal reportScenarioEvidenceBuilder reportScenarioAgentRunner reportScenarioAuthorization reportScenarioAgent reportScenarioModel reportScenarioValidator reportScenarioPublisher reportScenarioDelivery
        }

        custom S8_ManagerDecisionScenarios "04.8 - Scenario - Manager Chat Decision" "Human-in-the-loop manager chat decision flow using a durable PostgreSQL Agent Job, a job-ID-only Runtime wake-up, authenticated status polling, deterministic validation, and explicit manager confirmation." {
            include chatDecisionManager chatDecisionUi chatDecisionIdentity chatDecisionAuthorization chatDecisionRouter chatDecisionGateway chatDecisionAgentRunner chatDecisionStatus chatDecisionConversation chatDecisionEvidence chatDecisionQuery chatDecisionSqlGuard chatDecisionAgent chatDecisionModel chatDecisionValidator chatDecisionConfirmation chatDecisionTracker chatDecisionPostgres
            autoLayout lr 240 160
        }

        custom S9_MeetingMinutesUploadScenario "04.9 - Scenario - Meeting-Minutes Upload" "Human-in-the-loop document decision flow: deterministic archive and parsing, durable PostgreSQL Agent Job creation only after successful parsing, job-ID-only Runtime wake-up, authenticated status polling, validation, and manager review." {
            include minutesUploadManager minutesUploadUi minutesUploadIdentity minutesUploadAuthorization minutesUploadRouter minutesUploadProcessing minutesUploadParser minutesUploadGateway minutesUploadAgentRunner minutesUploadStatus minutesUploadAgent minutesUploadModel minutesUploadValidator minutesUploadConfirmation minutesUploadTracker minutesUploadArchive minutesUploadPostgres
            autoLayout lr 240 160
        }

        custom S10_FailureAndFallback "04.10 - Scenario - Failure and Fallback" "Fail-closed validation and deterministic publication fallback, with optional fail-open observability." {
            include failureService failureFallback failureObservability
            autoLayout lr 240 160
        }

        custom S11_KpiTranslationAndParity "04.11 - Scenario - KPI Translation and Parity" "Versioned PostgreSQL KPI translation, deterministic validation, and SQLite/PostgreSQL acceptance parity outside the product runtime." {
            include kpiTranslation kpiValidation kpiParity
            autoLayout lr 240 160
        }

        custom S12_OrganizationConfigurationD1 "04.12 - Scenario - Organization Configuration D+1" "Authorized inactive organization revision, deterministic validation, and D+1 activation through the product control boundary." {
            include orgCandidate orgValidation orgActivation
            autoLayout lr 240 160
        }

        custom S13_ScriptedManagerInputReplay "04.13 - Scenario - Scripted Manager Input Replay" "Versioned evaluation inputs enter through the same authenticated Backend API boundary as interactive manager inputs." {
            include scriptedInput scriptedApi scriptedResult
            autoLayout lr 240 160
        }

        custom S14_LateCorrectedDataRestatement "04.14 - Scenario - Late or Corrected Data Restatement" "Corrected source data is re-ingested, normalized, validated, pinned, recomputed, and republished with traceable receipts." {
            include restatementIntake restatementCompute restatementPublish
            autoLayout lr 240 160
        }

        styles {
            element "Element" {
                shape RoundedBox
                color #ffffff
                background #334155
                fontSize 20
            }
            element "ScenarioStep" {
                shape RoundedBox
                color #ffffff
                fontSize 18
                width 360
                height 180
            }
            element "ScenarioChat" {
                background #1d4ed8
            }
            element "ScenarioAgent" {
                background #a21caf
            }
            element "ScenarioDocument" {
                background #0f766e
            }
            element "ScenarioActor" {
                shape Person
                background #7c2d12
            }
            element "ScenarioStorage" {
                shape Folder
                background #6d28d9
            }
            element "ScenarioScheduler" {
                background #0e7490
            }
            element "ScenarioBackend" {
                background #1d4ed8
            }
            element "ScenarioWorker" {
                background #0f766e
            }
            element "ScenarioDatabase" {
                shape Cylinder
                background #6d28d9
            }
            element "ScenarioWeb" {
                background #0369a1
            }
            element "Person" {
                shape Person
                background #7c2d12
            }
            element "Target" {
                background #1e3a8a
            }
            element "External" {
                background #64748b
            }
            element "Source" {
                background #475569
            }
            element "Web" {
                background #0369a1
            }
            element "API" {
                background #1d4ed8
            }
            element "Worker" {
                background #0f766e
            }
            element "Scheduler" {
                background #0e7490
            }
            element "Database" {
                shape Cylinder
                background #5b21b6
            }
            element "Storage" {
                shape Folder
                background #6d28d9
            }
            element "Security" {
                background #92400e
            }
            element "Evidence" {
                background #0f766e
            }
            element "Query" {
                background #0f766e
            }
            element "Analytics" {
                background #166534
            }
            element "AI" {
                background #a21caf
            }
            element "Decision" {
                background #9a3412
            }
            element "Evaluation" {
                background #475569
            }
            element "OpenDecision" {
                stroke #f59e0b
                strokeWidth 4
            }
            element "Group" {
                color #94a3b8
                stroke #334155
                strokeWidth 2
            }
            element "AgentRuntime" {
                background #a21caf
            }
            element "Group:01 Access" {
                color #f2b84b
                stroke #7c5b20
            }
            element "Group:02 Request Routing" {
                color #60a5fa
                stroke #1d4ed8
            }
            element "Group:03 Bounded Analysis" {
                color #5eead4
                stroke #0f766e
            }
            element "Group:04 Validate and Deliver" {
                color #67e8f9
                stroke #0e7490
            }
            relationship "Relationship" {
                color #64748b
                routing Orthogonal
                fontSize 14
                thickness 1
                dashed true
            }
            relationship "PrimaryFlow" {
                color #22d3ee
                thickness 3
                dashed false
            }
            relationship "DataFlow" {
                color #2dd4bf
                thickness 2
                dashed false
            }
            relationship "ModelFlow" {
                color #c084fc
                thickness 2
                dashed false
            }
            relationship "ControlFlow" {
                color #64748b
                thickness 1
                dashed false
            }
            relationship "PolicyCheck" {
                color #f59e0b
                thickness 1
                dashed true
            }
            relationship "ExternalFlow" {
                color #f59e0b
                thickness 2
                dashed true
            }
            relationship "Feedback" {
                color #94a3b8
                thickness 1
                dashed true
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
