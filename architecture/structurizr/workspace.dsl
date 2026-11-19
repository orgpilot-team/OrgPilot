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

        reportScenarioReplay -> reportScenarioRunStatus "01. Prepare reporting day" "In-process function call"
        reportScenarioRunStatus -> reportScenarioRunCoordinator "02. Start pinned run" "HTTPS/JSON"
        reportScenarioRunCoordinator -> reportScenarioPostgres "03. Plan run jobs" "PostgreSQL protocol over TLS"
        reportScenarioRunStage -> reportScenarioPostgres "04. Claim deterministic jobs" "PostgreSQL protocol over TLS"
        reportScenarioRunStage -> reportScenarioIngestion "05. Ingest and check quality" "In-process function call"
        reportScenarioRunStage -> reportScenarioSnapshot "06. Pin snapshot" "In-process function call"
        reportScenarioRunStage -> reportScenarioKpi "07. Calculate KPIs" "In-process function call"
        reportScenarioRunStage -> reportScenarioWorkflow "08. Rebuild workflows" "In-process function call"
        reportScenarioRunStage -> reportScenarioSignal "09. Detect and rank signals" "In-process function call"
        reportScenarioRunStage -> reportScenarioEvidenceBuilder "10. Build manager evidence" "In-process function call"
        reportScenarioEvidenceBuilder -> reportScenarioPostgres "11. Store package; unlock agent job" "PostgreSQL protocol over TLS"
        reportScenarioAgentRunner -> reportScenarioPostgres "12. Claim agent job" "PostgreSQL protocol over TLS"
        reportScenarioAgentRunner -> reportScenarioAuthorization "13. Recheck manager scope" "Authenticated HTTPS/JSON"
        reportScenarioAgentRunner -> reportScenarioAgent "14. Run report graph" "In-process function call"
        reportScenarioAgent -> reportScenarioModel "15. Generate bounded narrative" "In-process function call"
        reportScenarioModel -> reportScenarioAgent "16. Return completion or failure" "In-process function call"
        reportScenarioAgent -> reportScenarioAgentRunner "17. Return candidate or failure" "In-process function call"
        reportScenarioAgentRunner -> reportScenarioPostgres "18. Persist agent outcome" "PostgreSQL protocol over TLS"
        reportScenarioAgentRunner -> reportScenarioValidator "19. Validate persisted outcome" "Authenticated HTTPS/JSON"
        reportScenarioValidator -> reportScenarioPublisher "20. Release report or fallback" "In-process function call"
        reportScenarioPublisher -> reportScenarioPostgres "21. Publish; unlock next job" "PostgreSQL protocol over TLS"
        reportScenarioPostgres -> reportScenarioDelivery "22. Deliver manager report" "PostgreSQL protocol over TLS"
        reportScenarioRunCoordinator -> reportScenarioPostgres "23. Close terminal run" "PostgreSQL protocol over TLS"

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

        chatDecisionManager -> chatDecisionUi "A01. Enter decision request" "Human interaction"
        chatDecisionUi -> chatDecisionIdentity "A02. Submit authenticated request" "HTTPS/JSON"
        chatDecisionIdentity -> chatDecisionAuthorization "A03. Create trusted identity" "In-process function call"
        chatDecisionAuthorization -> chatDecisionRouter "A04. Pass authorized scope" "In-process function call"
        chatDecisionRouter -> chatDecisionGateway "A05. Route durable enqueue" "In-process function call"
        chatDecisionGateway -> chatDecisionPostgres "A06. Commit job; return job ID" "PostgreSQL protocol over TLS"
        chatDecisionGateway -> chatDecisionAgentRunner "A07. Send optional job-ID wake-up" "Authenticated HTTPS wake-up with job_id"
        chatDecisionGateway -> chatDecisionRouter "A08. Return committed job ID" "In-process function call"
        chatDecisionRouter -> chatDecisionUi "A09. Return accepted job ID" "HTTPS/JSON"
        chatDecisionUi -> chatDecisionManager "A10. Show pending job" "Human interaction"
        chatDecisionAgentRunner -> chatDecisionPostgres "A11. Claim job and pinned scope" "PostgreSQL protocol over TLS"
        chatDecisionAgentRunner -> chatDecisionAuthorization "A12. Recheck pinned scope" "Authenticated HTTPS/JSON"
        chatDecisionAgentRunner -> chatDecisionAgent "A13. Run decision-card graph" "In-process function call"
        chatDecisionAgent -> chatDecisionConversation "A14. Store turn; load history" "In-process function call"
        chatDecisionConversation -> chatDecisionPostgres "A15. Read and write conversation" "PostgreSQL protocol over TLS"
        chatDecisionAgent -> chatDecisionEvidence "A16. Request evidence bundle" "Authenticated HTTPS/JSON"
        chatDecisionEvidence -> chatDecisionQuery "A17. Run scoped evidence query" "In-process function call"
        chatDecisionQuery -> chatDecisionSqlGuard "A18. Validate one SELECT" "In-process function call"
        chatDecisionSqlGuard -> chatDecisionQuery "A19. Return approval or refusal" "In-process function call"
        chatDecisionQuery -> chatDecisionPostgres "A20. Run approved query" "PostgreSQL protocol over TLS"
        chatDecisionAgent -> chatDecisionModel "A21. Draft bounded decision card" "In-process function call"
        chatDecisionModel -> chatDecisionAgent "A22. Return completion or failure" "In-process function call"
        chatDecisionAgent -> chatDecisionAgentRunner "A23. Return candidate or failure" "In-process function call"
        chatDecisionAgentRunner -> chatDecisionPostgres "A24. Persist candidate or failure" "PostgreSQL protocol over TLS"
        chatDecisionAgentRunner -> chatDecisionValidator "A25. Validate persisted outcome" "Authenticated HTTPS/JSON"
        chatDecisionValidator -> chatDecisionConfirmation "A26. Release valid card" "In-process function call"
        chatDecisionConfirmation -> chatDecisionPostgres "A27. Store card and review state" "PostgreSQL protocol over TLS"
        chatDecisionUi -> chatDecisionIdentity "A28. Poll job status" "HTTPS/JSON"
        chatDecisionIdentity -> chatDecisionAuthorization "A29. Recheck status scope" "In-process function call"
        chatDecisionAuthorization -> chatDecisionRouter "A30. Pass status request" "In-process function call"
        chatDecisionRouter -> chatDecisionStatus "A31. Route status read" "In-process function call"
        chatDecisionStatus -> chatDecisionPostgres "A32. Read job status" "PostgreSQL protocol over TLS"
        chatDecisionStatus -> chatDecisionUi "A33. Return status or result" "HTTPS/JSON"
        chatDecisionUi -> chatDecisionManager "A34. Show state or card" "Human interaction"
        chatDecisionManager -> chatDecisionUi "A35. Choose review action" "Human interaction"
        chatDecisionUi -> chatDecisionIdentity "A36. Submit review command" "HTTPS/JSON"
        chatDecisionIdentity -> chatDecisionAuthorization "A37. Recreate trusted context" "In-process function call"
        chatDecisionAuthorization -> chatDecisionRouter "A38. Pass review command" "In-process function call"
        chatDecisionRouter -> chatDecisionConfirmation "A39. Route review command" "In-process function call"
        chatDecisionConfirmation -> chatDecisionGateway "A40. Request revision job" "In-process function call"
        chatDecisionGateway -> chatDecisionPostgres "A41. Commit revision job" "PostgreSQL protocol over TLS"
        chatDecisionGateway -> chatDecisionAgentRunner "A42. Send optional revision wake-up" "Authenticated HTTPS wake-up with job_id"
        chatDecisionConfirmation -> chatDecisionPostgres "A43. Store rejection" "PostgreSQL protocol over TLS"
        chatDecisionConfirmation -> chatDecisionTracker "A44. Forward confirmed card" "In-process function call"
        chatDecisionTracker -> chatDecisionAuthorization "A45. Recheck decision authority" "In-process function call"
        chatDecisionTracker -> chatDecisionPostgres "A46. Record decision and follow-up" "PostgreSQL protocol over TLS"

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

        minutesUploadManager -> minutesUploadUi "B01. Select supported document" "Human interaction"
        minutesUploadUi -> minutesUploadIdentity "B02. Submit authenticated upload" "HTTPS/JSON"
        minutesUploadIdentity -> minutesUploadAuthorization "B03. Create trusted identity" "In-process function call"
        minutesUploadAuthorization -> minutesUploadRouter "B04. Pass upload scope" "In-process function call"
        minutesUploadRouter -> minutesUploadProcessing "B05. Route document upload" "In-process function call"
        minutesUploadProcessing -> minutesUploadArchive "B06. Archive bytes and hash" "Controlled filesystem I/O"
        minutesUploadProcessing -> minutesUploadParser "B07. Request deterministic parse" "In-process function call"
        minutesUploadParser -> minutesUploadArchive "B08. Read approved upload bytes" "Controlled filesystem I/O"
        minutesUploadParser -> minutesUploadPostgres "B09. Store fragments and receipt" "PostgreSQL protocol over TLS"
        minutesUploadParser -> minutesUploadProcessing "B10. Return parse failure" "In-process function call"
        minutesUploadProcessing -> minutesUploadPostgres "B11. Commit document job" "PostgreSQL protocol over TLS"
        minutesUploadProcessing -> minutesUploadRouter "B12a. Return parse failure" "In-process function call"
        minutesUploadProcessing -> minutesUploadGateway "B12b. Request optional wake-up" "In-process function call"
        minutesUploadGateway -> minutesUploadAgentRunner "B13. Send job-ID wake-up" "Authenticated HTTPS wake-up with job_id"
        minutesUploadProcessing -> minutesUploadRouter "B14. Return committed job ID" "In-process function call"
        minutesUploadRouter -> minutesUploadUi "B15. Return accepted job ID" "HTTPS/JSON"
        minutesUploadAgentRunner -> minutesUploadPostgres "B16. Claim document job" "PostgreSQL protocol over TLS"
        minutesUploadAgentRunner -> minutesUploadAuthorization "B17. Recheck document scope" "Authenticated HTTPS/JSON"
        minutesUploadAgentRunner -> minutesUploadAgent "B18. Run document graph" "In-process function call"
        minutesUploadAgent -> minutesUploadModel "B19. Analyze approved evidence" "In-process function call"
        minutesUploadModel -> minutesUploadAgent "B20. Return completion or failure" "In-process function call"
        minutesUploadAgent -> minutesUploadAgentRunner "B21. Return candidate or failure" "In-process function call"
        minutesUploadAgentRunner -> minutesUploadPostgres "B22. Persist candidate or failure" "PostgreSQL protocol over TLS"
        minutesUploadAgentRunner -> minutesUploadValidator "B23. Validate persisted outcome" "Authenticated HTTPS/JSON"
        minutesUploadValidator -> minutesUploadConfirmation "B24. Release valid card" "In-process function call"
        minutesUploadConfirmation -> minutesUploadPostgres "B25. Store card and review state" "PostgreSQL protocol over TLS"
        minutesUploadUi -> minutesUploadIdentity "B26. Poll analysis status" "HTTPS/JSON"
        minutesUploadIdentity -> minutesUploadAuthorization "B27. Recheck status scope" "In-process function call"
        minutesUploadAuthorization -> minutesUploadRouter "B28. Pass status request" "In-process function call"
        minutesUploadRouter -> minutesUploadStatus "B29. Route status read" "In-process function call"
        minutesUploadStatus -> minutesUploadPostgres "B30. Read job status" "PostgreSQL protocol over TLS"
        minutesUploadStatus -> minutesUploadUi "B31. Return status or result" "HTTPS/JSON"
        minutesUploadUi -> minutesUploadManager "B32. Show validated card" "Human interaction"
        minutesUploadManager -> minutesUploadUi "B33. Choose review action" "Human interaction"
        minutesUploadUi -> minutesUploadIdentity "B34. Submit review command" "HTTPS/JSON"
        minutesUploadIdentity -> minutesUploadAuthorization "B35. Recreate trusted context" "In-process function call"
        minutesUploadAuthorization -> minutesUploadRouter "B36. Pass review command" "In-process function call"
        minutesUploadRouter -> minutesUploadConfirmation "B37. Route review command" "In-process function call"
        minutesUploadConfirmation -> minutesUploadProcessing "B38a. Request fragment-based revision" "In-process function call"
        minutesUploadProcessing -> minutesUploadPostgres "B38b. Commit revision job" "PostgreSQL protocol over TLS"
        minutesUploadProcessing -> minutesUploadGateway "B38c. Request optional wake-up" "In-process function call"
        minutesUploadGateway -> minutesUploadAgentRunner "B38d. Send revision job-ID wake-up" "Authenticated HTTPS wake-up with job_id"
        minutesUploadConfirmation -> minutesUploadPostgres "B39. Store rejection" "PostgreSQL protocol over TLS"
        minutesUploadConfirmation -> minutesUploadTracker "B40. Forward confirmed card" "In-process function call"
        minutesUploadTracker -> minutesUploadAuthorization "B41. Recheck decision authority" "In-process function call"
        minutesUploadTracker -> minutesUploadPostgres "B42. Record decision and follow-up" "PostgreSQL protocol over TLS"

        // Additional scenario-only mirrors complete the active 16-view set without adding product components.
        failureService = element "Product Services" "Failure and fallback" "Retains durable failure state." "ScenarioStep,ScenarioBackend"
        failureFallback = element "Deterministic Fallback" "Failure and fallback" "Publishes fallback or explicit failure." "ScenarioStep,ScenarioWorker"
        failureObservability = element "Optional Observability" "Failure and fallback" "Receives redacted failure telemetry." "ScenarioStep,ScenarioAgent"
        failureService -> failureFallback "Apply fallback or explicit failure" "In-process function call"
        failureFallback -> failureObservability "Export redacted failure telemetry" "OTLP"

        kpiTranslation = element "KPI Definition Preprocessor" "KPI translation and parity" "Translates approved KPI SQL." "ScenarioStep,ScenarioWorker"
        kpiValidation = element "Configuration Validation Runner" "KPI translation and parity" "Validates KPI SQL and fixtures." "ScenarioStep,ScenarioWorker"
        kpiParity = element "KPI Parity Validator" "KPI translation and parity" "Checks SQLite and PostgreSQL parity." "ScenarioStep,ScenarioScheduler"
        kpiTranslation -> kpiValidation "Validate SQL and fixtures" "In-process function call"
        kpiValidation -> kpiParity "Run acceptance parity" "Acceptance test interface"

        orgCandidate = element "Inactive Organization Revision Intake" "Organization configuration D+1" "Accepts an authorized inactive revision." "ScenarioStep,ScenarioBackend"
        orgValidation = element "Organization Revision Validator" "Organization configuration D+1" "Validates the inactive revision." "ScenarioStep,ScenarioWorker"
        orgActivation = element "D+1 Organization Activator" "Organization configuration D+1" "Activates an approved revision at D+1." "ScenarioStep,ScenarioBackend"
        orgCandidate -> orgValidation "Queue deterministic validation" "PostgreSQL-backed job queue"
        orgValidation -> orgActivation "Return D+1 validation receipt" "PostgreSQL protocol over TLS"

        scriptedInput = element "Scripted Manager Input Adapter" "Scripted manager input replay" "Reads versioned replay input." "ScenarioStep,ScenarioScheduler"
        scriptedApi = element "Backend API" "Scripted manager input replay" "Applies the product request boundary." "ScenarioStep,ScenarioBackend"
        scriptedResult = element "Replay Acceptance" "Scripted manager input replay" "Checks result and contract evidence." "ScenarioStep,ScenarioScheduler"
        scriptedInput -> scriptedApi "Submit the pinned scripted input" "HTTPS, REST/JSON"
        scriptedApi -> scriptedResult "Return validated result references" "HTTPS, REST/JSON"

        restatementIntake = element "Normalized Intake" "Late or corrected data restatement" "Normalizes corrected source data." "ScenarioStep,ScenarioWorker"
        restatementCompute = element "Deterministic Recalculation" "Late or corrected data restatement" "Recomputes affected deterministic results." "ScenarioStep,ScenarioWorker"
        restatementPublish = element "Validated Republishing" "Late or corrected data restatement" "Publishes validated restated artifacts." "ScenarioStep,ScenarioBackend"
        restatementIntake -> restatementCompute "Recompute corrected snapshot" "In-process function call"
        restatementCompute -> restatementPublish "Validate and republish artifacts" "PostgreSQL-backed job queue"

        // System-level relationships
        seniorManager -> didrah "Executive access" "HTTPS"
        unitManager -> didrah "Unit management access" "HTTPS"
        teamSupervisor -> didrah "Team supervision access" "HTTPS"
        evaluator -> didrah "Replay and acceptance" "CLI and HTTPS/JSON"
        operator -> didrah "Operational monitoring" "HTTPS"
        inputDataset -> didrah "Versioned source and replay input" "Read-only filesystem: CSV, JSON, and Markdown"
        didrah -> identityProvider "Identity validation" "OIDC or internal authentication over HTTPS"
        didrah -> llmProvider "Bounded model calls" "HTTPS/JSON"
        didrah -> langfuse "Optional redacted telemetry" "OTLP export"

        // Container-level relationships
        seniorManager -> webApp "Executive access" "HTTPS"
        unitManager -> webApp "Unit management access" "HTTPS"
        teamSupervisor -> webApp "Team supervision access" "HTTPS"
        evaluator -> schedulerReplay "Run replay" "CLI and HTTPS/JSON"
        evaluator -> backendApi "Read acceptance evidence" "HTTPS/JSON"
        operator -> backendApi "Read operational status" "HTTPS"
        inputDataset -> worker "Nightly source drops" "Read-only filesystem"
        inputDataset -> schedulerReplay "Replay inputs" "Read-only filesystem: JSON, CSV, and Markdown"
        backendApi -> identityProvider "Validate identity" "OIDC over HTTPS or internal authentication"
        webApp -> backendApi "Product API" "HTTPS, REST/JSON, W3C traceparent"
        schedulerReplay -> backendApi "Run control" "HTTPS, REST/JSON"
        schedulerReplay -> postgres "Replay state" "PostgreSQL protocol over TLS"
        backendApi -> agentRuntime "Optional job-ID wake-up" "Authenticated HTTPS wake-up with job_id"
        backendApi -> postgres "Product state" "PostgreSQL protocol over TLS, EF Core/Npgsql"
        worker -> postgres "Deterministic jobs and results" "PostgreSQL protocol over TLS, EF Core/Npgsql"
        worker -> fileArchive "Source archive" "Controlled filesystem I/O"
        backendApi -> fileArchive "Upload archive" "Controlled filesystem API"
        backendApi -> submissionOutput "Validated export" "Controlled filesystem I/O"
        agentRuntime -> postgres "Restricted agent job state" "Restricted PostgreSQL role"
        agentRuntime -> llmProvider "Bounded model calls" "HTTPS/JSON"
        agentRuntime -> backendApi "Evidence, query, and validation" "HTTPS Evidence/Query/Validation API"
        webApp -> otelCollector "Optional browser telemetry" "OTLP/HTTP"
        backendApi -> otelCollector "Optional API telemetry" "OTLP"
        worker -> otelCollector "Optional worker telemetry" "OTLP"
        schedulerReplay -> otelCollector "Optional replay telemetry" "OTLP"
        agentRuntime -> otelCollector "Optional agent telemetry" "OTLP"
        otelCollector -> langfuse "Redacted telemetry export" "OTLP export"

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
        webApp -> identityBoundary "Submit authenticated request" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }
        identityBoundary -> identityProvider "Validate identity" "OIDC over HTTPS or internal authentication" {
            tags "ExternalFlow"
        }
        identityBoundary -> authorizationService "Create trusted context" "In-process function call" {
            tags "PrimaryFlow"
        }
        authorizationService -> postgres "Read grants and policy" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        authorizationService -> managerInputService "Pass trusted scope" "In-process function call" {
            tags "PrimaryFlow"
        }

        // Request routing and manager commands.
        managerInputService -> reportApi "Route report reads" "In-process function call" {
            tags "ControlFlow"
        }
        managerInputService -> configurationService "Route configuration candidate" "In-process function call" {
            tags "ControlFlow"
        }
        managerInputService -> organizationConfigurationService "Route organization change" "In-process function call" {
            tags "ControlFlow"
        }
        managerInputService -> agentGateway "Route durable agent job" "In-process function call" {
            tags "PrimaryFlow"
        }
        agentGateway -> postgres "Commit interactive job" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        agentGateway -> managerInputService "Return committed job ID" "In-process function call" {
            tags "Feedback"
        }
        managerInputService -> webApp "Return accepted job ID" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }
        agentGateway -> agentJobRunner "Send optional job-ID wake-up" "Internal authenticated API" {
            tags "PrimaryFlow"
        }
        managerInputService -> agentJobStatusService "Route job-status read" "In-process function call" {
            tags "ControlFlow"
        }
        managerInputService -> documentProcessingRunner "Route document upload" "In-process function call" {
            tags "PrimaryFlow"
        }
        managerInputService -> decisionConfirmationService "Route review command" "In-process function call" {
            tags "ControlFlow"
        }
        documentProcessingRunner -> fileArchive "Archive upload bytes and hash" "Restricted file system I/O" {
            tags "ControlFlow"
        }
        documentProcessingRunner -> documentParser "Request deterministic parse" "In-process function call" {
            tags "PrimaryFlow"
        }
        documentParser -> fileArchive "Read approved upload bytes" "Restricted file system I/O" {
            tags "DataFlow"
        }
        documentParser -> postgres "Store fragments and parse receipt" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        documentProcessingRunner -> postgres "Commit document-analysis job" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        documentProcessingRunner -> managerInputService "Return document job ID" "In-process function call" {
            tags "Feedback"
        }
        documentProcessingRunner -> agentGateway "Request optional Runtime wake-up" "In-process function call" {
            tags "ControlFlow"
        }
        configurationService -> authorizationService "Check configuration authority" "In-process function call" {
            tags "PolicyCheck"
        }
        configurationService -> postgres "Store candidate; queue validation" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        organizationConfigurationService -> authorizationService "Check organization authority" "In-process function call" {
            tags "PolicyCheck"
        }
        organizationConfigurationService -> postgres "Store revision; activate at D+1" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        decisionTracker -> authorizationService "Check decision authority" "In-process function call" {
            tags "PolicyCheck"
        }
        decisionTracker -> postgres "Record decision and follow-up" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        decisionTracker -> agentGateway "Request draft only" "In-process function call" {
            tags "ControlFlow"
        }

        // Bounded analysis. Tool and model responses are implicit unless a failure path needs a separate edge.
        agentOrchestrator -> evidenceService "Request authorized evidence" "Internal authenticated API" {
            tags "DataFlow"
        }
        agentOrchestrator -> conversationService "Store turn; load history" "Internal authenticated API" {
            tags "DataFlow"
        }
        conversationService -> postgres "Read and write conversation" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        evidenceService -> authorizationService "Check evidence scope" "In-process function call" {
            tags "PolicyCheck"
        }
        evidenceService -> queryGateway "Run registered evidence query" "In-process function call" {
            tags "DataFlow"
        }
        evidenceService -> fileArchive "Read approved evidence bytes" "Restricted file system I/O" {
            tags "DataFlow"
        }
        queryGateway -> authorizationService "Get scope and allowlists" "In-process function call" {
            tags "PolicyCheck"
        }
        queryGateway -> sqlGuard "Validate one SELECT" "In-process function call" {
            tags "DataFlow"
        }
        sqlGuard -> queryGateway "Return approval or refusal" "In-process function call" {
            tags "Feedback"
        }
        queryGateway -> postgres "Run scoped read-only query" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        queryGateway -> auditService "Record query evidence" "In-process function call" {
            tags "ControlFlow"
        }
        agentJobRunner -> postgres "Claim job; persist outcome" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        agentJobRunner -> agentOrchestrator "Run bounded job graph" "In-process function call" {
            tags "PrimaryFlow"
        }
        agentJobRunner -> outputValidator "Validate persisted outcome" "Internal authenticated API" {
            tags "PrimaryFlow"
        }
        agentOrchestrator -> agentModelGateway "Request bounded model work" "In-process function call" {
            tags "ModelFlow"
        }
        agentModelGateway -> postgres "Reserve model-cost budget" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        agentModelGateway -> llmProvider "Send evidence; receive completion" "HTTPS/JSON" {
            tags "ExternalFlow"
        }
        agentModelGateway -> agentOrchestrator "Return completion or failure" "In-process function call" {
            tags "Feedback"
        }
        checkpointStore -> postgres "Read and write checkpoints" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        agentJobStatusService -> authorizationService "Check job-result access" "In-process function call" {
            tags "PolicyCheck"
        }
        agentJobStatusService -> postgres "Read authorized job status" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        agentJobStatusService -> webApp "Return authorized job result" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }

        // Validation, delivery, and accountability.
        outputValidator -> postgres "Store validation result" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        outputValidator -> queryGateway "Recheck reported numbers" "In-process function call" {
            tags "Feedback"
        }
        outputValidator -> authorizationService "Recheck recipient scope" "In-process function call" {
            tags "PolicyCheck"
        }
        outputValidator -> evidenceService "Check provenance and alternatives" "In-process function call" {
            tags "Feedback"
        }
        outputValidator -> auditService "Record validation evidence" "In-process function call" {
            tags "ControlFlow"
        }
        outputValidator -> conversationService "Store validated answer or failure" "Internal authenticated API" {
            tags "ControlFlow"
        }
        outputValidator -> decisionConfirmationService "Release valid decision card" "In-process function call" {
            tags "PrimaryFlow"
        }
        decisionConfirmationService -> postgres "Store card and review state" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        decisionConfirmationService -> webApp "Return card or review status" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }
        decisionConfirmationService -> agentGateway "Request interactive revision" "In-process function call" {
            tags "Feedback"
        }
        decisionConfirmationService -> documentProcessingRunner "Request document revision" "In-process function call" {
            tags "Feedback"
        }
        decisionConfirmationService -> decisionTracker "Forward confirmed decision card" "In-process function call" {
            tags "ControlFlow"
        }
        outputValidator -> reportApi "Release valid result or failure" "In-process function call" {
            tags "PrimaryFlow"
        }
        reportApi -> authorizationService "Recheck audience and purpose" "In-process function call" {
            tags "PolicyCheck"
        }
        reportApi -> queryGateway "Run dashboard or workflow query" "In-process function call" {
            tags "DataFlow"
        }
        reportApi -> postgres "Read reports and failure states" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        reportApi -> webApp "Return response or failure" "HTTPS/JSON" {
            tags "PrimaryFlow"
        }
        auditService -> postgres "Store restricted audit evidence" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        publisherV2 -> postgres "Publish report; unlock next job" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        publisherV2 -> auditService "Record publication evidence" "In-process function call" {
            tags "ControlFlow"
        }
        publisherV2 -> submissionExporter "Forward validated report" "In-process function call" {
            tags "PrimaryFlow"
        }
        outputValidator -> submissionExporter "Forward validated QA result" "In-process function call" {
            tags "PrimaryFlow"
        }
        submissionExporter -> postgres "Read results; store export receipt" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        submissionExporter -> submissionOutput "Write validated contract files" "Controlled filesystem I/O" {
            tags "ControlFlow"
        }

        // Worker component relationships
        ingestionCoordinator -> inputDataset "Read nightly source contracts" "Read-only filesystem: CSV and JSON"
        ingestionCoordinator -> sourceAdapters "Parse source contracts" "In-process function call"
        sourceAdapters -> fileArchive "Archive source bytes and hashes" "Controlled filesystem I/O"
        sourceAdapters -> normalizer "Submit fields for normalization" "In-process function call"
        normalizer -> dataQualityService "Check normalized rows" "In-process function call"
        dataQualityService -> postgres "Store records and data issues" "PostgreSQL protocol over TLS"
        snapshotService -> postgres "Pin run snapshot" "PostgreSQL protocol over TLS"
        snapshotService -> projectionService "Build reproducible projections" "In-process function call"
        projectionService -> postgres "Read events; store projections" "PostgreSQL protocol over TLS"
        kpiCalculator -> semanticRegistry "Read approved KPI definitions" "In-process function call"
        configurationValidationRunnerV2 -> kpiDefinitionPreprocessor "Translate KPI candidate" "In-process function call"
        kpiDefinitionPreprocessor -> semanticRegistry "Register validated KPI definition" "In-process function call"
        semanticRegistry -> postgres "Read KPI definitions" "PostgreSQL protocol over TLS"
        kpiCalculator -> postgres "Calculate KPIs and lineage" "PostgreSQL protocol over TLS"
        workflowEngine -> postgres "Rebuild workflow observations" "PostgreSQL protocol over TLS"
        signalEngine -> postgres "Detect and store signals" "PostgreSQL protocol over TLS"
        decisionEffectEvaluator -> postgres "Store decision-effect assessment" "PostgreSQL protocol over TLS"
        runStageCoordinatorV2 -> decisionEffectEvaluator "Evaluate due decision effects" "In-process function call"
        decisionEffectEvaluator -> reportEvidenceBuilderV2 "Add follow-up assessment" "In-process function call"

        // Current run-control, report-evidence, agent, publication, and evaluation flow.
        evaluator -> replayCommandV2 "Start replay range" "Command-line interface"
        inputDataset -> scriptedManagerInputAdapter "Supply scripted manager inputs" "Read-only filesystem"
        replayCommandV2 -> scriptedManagerInputAdapter "Replay pinned manager inputs" "In-process function call"
        scriptedManagerInputAdapter -> backendApi "Submit scripted product input" "HTTPS, REST/JSON"
        inputDataset -> replayCommandV2 "Supply replay range" "Read-only JSON"
        replayCommandV2 -> simulationClockV2 "Pin business date and cutoff" "In-process function call"
        replayCommandV2 -> evaluationProfileLoaderV2 "Load evaluation profile" "In-process function call"
        replayCommandV2 -> runStatusClientV2 "Start or resume simulated day" "In-process function call"
        replayCommandV2 -> acceptanceTestHarnessV2 "Start terminal acceptance checks" "In-process function call"
        runStatusClientV2 -> runCoordinatorV2 "Start and monitor runs" "Authenticated HTTPS/JSON"
        runCoordinatorV2 -> authorizationService "Validate run-control identity" "In-process function call"
        evaluator -> acceptanceTestHarnessV2 "Start acceptance checks" "Command-line interface"
        acceptanceTestHarnessV2 -> evaluationProfileLoaderV2 "Load acceptance limits" "In-process function call"
        acceptanceTestHarnessV2 -> runStatusClientV2 "Read terminal run status" "In-process function call"
        acceptanceTestHarnessV2 -> postgres "Store acceptance results" "PostgreSQL protocol over TLS"
        acceptanceTestHarnessV2 -> kpiParityValidator "Run KPI parity suite" "In-process function call"

        runCoordinatorV2 -> postgres "Plan and close pinned run" "PostgreSQL protocol over TLS"
        configurationService -> configurationValidationRunnerV2 "Queue configuration validation" "PostgreSQL-backed job queue"
        configurationValidationRunnerV2 -> semanticRegistry "Check KPI dependencies" "In-process function call"
        configurationValidationRunnerV2 -> postgres "Store configuration validation receipt" "PostgreSQL protocol over TLS"
        runStageCoordinatorV2 -> postgres "Claim and record run-stage jobs" "PostgreSQL protocol over TLS"
        runStageCoordinatorV2 -> ingestionCoordinator "Run pinned intake" "In-process function call"
        runStageCoordinatorV2 -> snapshotService "Create snapshot" "In-process function call"
        runStageCoordinatorV2 -> kpiCalculator "Calculate approved KPIs" "In-process function call"
        runStageCoordinatorV2 -> workflowEngine "Rebuild workflows" "In-process function call"
        runStageCoordinatorV2 -> signalEngine "Detect and rank signals" "In-process function call"
        runStageCoordinatorV2 -> reportEvidenceBuilderV2 "Build manager evidence" "In-process function call"
        reportEvidenceBuilderV2 -> postgres "Store package; unlock agent job" "PostgreSQL protocol over TLS"

        outputValidator -> publisherV2 "Release package or fallback" "In-process function call"

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
            autoLayout lr 180 140
        }

        // C4 core view: deployable applications and data stores inside the DIDRAH boundary.
        container didrah L2_Containers "C4 container view of the DIDRAH applications, data stores, users, and external dependencies." {
            title "02 - C4 Level 2 - Containers for DIDRAH"
            include inputDataset submissionOutput identityProvider llmProvider langfuse webApp backendApi worker schedulerReplay postgres fileArchive agentRuntime otelCollector
            exclude "webApp -> otelCollector"
            exclude "backendApi -> otelCollector"
            exclude "worker -> otelCollector"
            exclude "schedulerReplay -> otelCollector"
            exclude "agentRuntime -> otelCollector"
            autoLayout lr 160 100
        }

        // Revised C4 Level 3 views.
        component webApp L3_2_WebApplicationComponents "Web Application view for the Persian management interfaces and their authenticated Backend API and optional telemetry boundaries." {
            title "03.2 - C4 Level 3 - Web Application Components"
            include seniorManager unitManager teamSupervisor backendApi chatUi dashboardUi workflowUi
            exclude "seniorManager -> webApp"
            exclude "unitManager -> webApp"
            exclude "teamSupervisor -> webApp"
            exclude "webApp -> backendApi"
            autoLayout lr 180 120
        }

        component backendApi L3_3_RevisedBackendApiComponents "Backend API view with durable agent-job producers, a job-ID-only Runtime wake-up, unified Runtime claiming, status reads, in-process document intake and parsing, manager-confirmed decision cards, scheduler-only run control, validation, publication, delivery, and submission export." {
            title "03.3 - C4 Level 3 - Backend API Components"
            include webApp postgres agentJobRunner agentOrchestrator identityBoundary authorizationService managerInputService configurationService organizationConfigurationService decisionTracker runCoordinatorV2 documentProcessingRunner documentParser agentGateway evidenceService queryGateway sqlGuard outputValidator agentJobStatusService decisionConfirmationService publisherV2 submissionExporter reportApi auditService
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
            exclude "agentGateway -> managerInputService"
            exclude "documentProcessingRunner -> managerInputService"
            exclude "decisionTracker -> agentGateway"
            exclude "queryGateway -> auditService"
            exclude "outputValidator -> auditService"
            exclude "decisionConfirmationService -> agentGateway"
            exclude "decisionConfirmationService -> documentProcessingRunner"
            exclude "managerInputService -> webApp"
            exclude "agentJobStatusService -> authorizationService"
            exclude "reportApi -> queryGateway"
            exclude "authorizationService -> postgres"
            exclude "documentProcessingRunner -> postgres"
            exclude "configurationService -> postgres"
            exclude "organizationConfigurationService -> postgres"
            exclude "decisionTracker -> postgres"
            exclude "queryGateway -> postgres"
            exclude "agentJobRunner -> postgres"
            exclude "agentJobStatusService -> postgres"
            exclude "decisionConfirmationService -> postgres"
            exclude "reportApi -> postgres"
            exclude "auditService -> postgres"
            exclude "submissionExporter -> postgres"
            exclude "runCoordinatorV2 -> authorizationService"
            exclude "outputValidator -> submissionExporter"
            exclude "webApp -> backendApi"
            exclude "backendApi -> agentRuntime"
            exclude "backendApi -> postgres"
            exclude "agentRuntime -> backendApi"
            exclude "agentRuntime -> postgres"
            autoLayout lr 20 20
        }

        component worker L3_4_RevisedBackgroundWorkerComponents "Background Worker view with PostgreSQL-backed run-stage execution, independent configuration validation, deterministic analytics, decision effect evaluation, and one-manager-at-a-time report evidence assembly. Manager document processing remains inside the Backend API." {
            title "03.4 - C4 Level 3 - Background Worker Components"
            include inputDataset postgres fileArchive configurationService runCoordinatorV2 runStageCoordinatorV2 configurationValidationRunnerV2 ingestionCoordinator sourceAdapters normalizer dataQualityService snapshotService projectionService semanticRegistry kpiDefinitionPreprocessor kpiCalculator workflowEngine signalEngine reportEvidenceBuilderV2 decisionEffectEvaluator
            exclude "inputDataset -> worker"
            exclude "worker -> postgres"
            exclude "worker -> fileArchive"
            autoLayout tb 20 20
        }

        component schedulerReplay L3_5_RevisedSchedulerReplayComponents "Revised Scheduler and Replay Runner view that controls simulated time and replay through the Backend Run Coordinator and runs acceptance checks outside the daily publication path." {
            title "03.5 - C4 Level 3 - Revised Scheduler and Replay Runner Components"
            include evaluator inputDataset backendApi postgres runCoordinatorV2 replayCommandV2 simulationClockV2 evaluationProfileLoaderV2 runStatusClientV2 acceptanceTestHarnessV2 kpiParityValidator scriptedManagerInputAdapter
            exclude "evaluator -> schedulerReplay"
            exclude "inputDataset -> schedulerReplay"
            exclude "schedulerReplay -> backendApi"
            exclude "schedulerReplay -> postgres"
            autoLayout lr 160 120
        }

        component agentRuntime L3_6_AgentRuntimeComponents "Agent Runtime view with one PostgreSQL-backed Runner for every report, interactive, and document Agent Job; authenticated wake-ups are hints only, and evidence and validation use Backend services." {
            title "03.6 - C4 Level 3 - Agent Runtime Components"
            include postgres llmProvider agentGateway evidenceService outputValidator agentOrchestrator agentJobRunner conversationService agentModelGateway checkpointStore
            exclude "backendApi -> agentRuntime"
            exclude "agentRuntime -> postgres"
            exclude "agentRuntime -> llmProvider"
            exclude "agentRuntime -> backendApi"
            autoLayout lr 140 100
        }

        deployment didrah "Evaluation" D1_EvaluationCompose "Evaluation deployment using separate Docker Compose services started with one command." {
            include *
            autoLayout tb 100 80
        }

        // Numbered end-to-end scenario for the revised L3 architecture.
        custom S7_ReportGenerationScenario "04.7 - Scenario - Report Generation" "Primary report-generation path across Scheduler, Backend API, Background Worker, and PostgreSQL." {
            include reportScenarioReplay reportScenarioRunStatus reportScenarioRunCoordinator reportScenarioPostgres reportScenarioRunStage reportScenarioIngestion reportScenarioSnapshot reportScenarioKpi reportScenarioWorkflow reportScenarioSignal reportScenarioEvidenceBuilder reportScenarioAgentRunner reportScenarioAuthorization reportScenarioAgent reportScenarioModel reportScenarioValidator reportScenarioPublisher reportScenarioDelivery
            autoLayout tb 50 40
        }

        custom S8_ManagerDecisionScenarios "04.8 - Scenario - Manager Chat Decision" "Human-in-the-loop manager chat decision flow using a durable PostgreSQL Agent Job, a job-ID-only Runtime wake-up, authenticated status polling, deterministic validation, and explicit manager confirmation." {
            include chatDecisionManager chatDecisionUi chatDecisionIdentity chatDecisionAuthorization chatDecisionRouter chatDecisionGateway chatDecisionAgentRunner chatDecisionStatus chatDecisionConversation chatDecisionEvidence chatDecisionQuery chatDecisionSqlGuard chatDecisionAgent chatDecisionModel chatDecisionValidator chatDecisionConfirmation chatDecisionTracker chatDecisionPostgres
            autoLayout tb 40 30
        }

        custom S9_MeetingMinutesUploadScenario "04.9 - Scenario - Meeting-Minutes Upload" "Human-in-the-loop document decision flow: deterministic archive and parsing, durable PostgreSQL Agent Job creation only after successful parsing, job-ID-only Runtime wake-up, authenticated status polling, validation, and manager review." {
            include minutesUploadManager minutesUploadUi minutesUploadIdentity minutesUploadAuthorization minutesUploadRouter minutesUploadProcessing minutesUploadParser minutesUploadGateway minutesUploadAgentRunner minutesUploadStatus minutesUploadAgent minutesUploadModel minutesUploadValidator minutesUploadConfirmation minutesUploadTracker minutesUploadArchive minutesUploadPostgres
            autoLayout tb 40 30
        }

        custom S10_FailureAndFallback "04.10 - Scenario - Failure and Fallback" "Fail-closed validation and deterministic publication fallback, with optional fail-open observability." {
            include failureService failureFallback failureObservability
            autoLayout lr 140 100
        }

        custom S11_KpiTranslationAndParity "04.11 - Scenario - KPI Translation and Parity" "Versioned PostgreSQL KPI translation, deterministic validation, and SQLite/PostgreSQL acceptance parity outside the product runtime." {
            include kpiTranslation kpiValidation kpiParity
            autoLayout lr 140 100
        }

        custom S12_OrganizationConfigurationD1 "04.12 - Scenario - Organization Configuration D+1" "Authorized inactive organization revision, deterministic validation, and D+1 activation through the product control boundary." {
            include orgCandidate orgValidation orgActivation
            autoLayout lr 140 100
        }

        custom S13_ScriptedManagerInputReplay "04.13 - Scenario - Scripted Manager Input Replay" "Versioned evaluation inputs enter through the same authenticated Backend API boundary as interactive manager inputs." {
            include scriptedInput scriptedApi scriptedResult
            autoLayout lr 140 100
        }

        custom S14_LateCorrectedDataRestatement "04.14 - Scenario - Late or Corrected Data Restatement" "Corrected source data is re-ingested, normalized, validated, pinned, recomputed, and republished with traceable receipts." {
            include restatementIntake restatementCompute restatementPublish
            autoLayout lr 140 100
        }

        styles {
            element "Element" {
                shape RoundedBox
                color #ffffff
                background #334155
                fontSize 18
                width 280
                height 150
            }
            element "ScenarioStep" {
                shape RoundedBox
                color #ffffff
                fontSize 18
                width 250
                height 140
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
                jump true
                fontSize 20
                width 160
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
