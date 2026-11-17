workspace "DIDRAH Proposed Architecture" "Proposed C4 model for the DIDRAH management assistant. Open decisions are not approved facts." {
    !identifiers flat
    !impliedRelationships false

    // Architecture source: Docs/final review/proposed-architecture.md
    // Requirement source: the Persian DIDRAH agentic management assistant brief in Docs.
    // Evaluation source: DataSet/arka_dataset/README_FA.md and output_contract/*.json
    // Team decision: PostgreSQL is the only product database.
    // SQLite is an external test oracle for reference SQL only. It is not a runtime container.
    // Status: Proposed for team review. This workspace does not claim implementation.
    // Open decisions include KPI SQL parity, exact RLS projections, report schema,
    // signal boundary rules, workflow stage ownership, retry limits, provider/model,
    // retention, RPO/RTO, and the suppressed/ongoing output mapping.

    model {
        // People
        seniorManager = person "Senior Manager" "Reads organization health, cross-unit workflows, escalations, and pending decisions." "Person,Executive"
        unitManager = person "Unit Manager" "Reads authorized unit and team aggregates. Records decisions and follow-up actions." "Person,Manager"
        teamSupervisor = person "Team Supervisor" "Reads team data and authorized direct-member work details for workload management." "Person,Manager"
        evaluator = person "Evaluator" "Runs Docker, replay, hidden-data checks, and acceptance tests." "Person,Evaluator"
        operator = person "Operator" "Monitors runs, failures, cost, backup, and restore evidence." "Person,Operator"

        // External systems
        inputDataset = softwareSystem "DIDRAH Input Dataset" "Provides nightly drops, manifests, manager inputs, uploads, configuration, and history through one versioned data contract. Development and hidden evaluation datasets use the same structure." "External,Source,Evaluation"
        identityProvider = softwareSystem "Identity Provider" "Authenticates users and supplies a trusted identity. The product or internal method is open." "External,Identity,OpenDecision"
        llmProvider = softwareSystem "Language Model Provider" "Returns bounded language-model completions. The provider and model are open decisions." "External,AI,OpenDecision"

        didrah = softwareSystem "DIDRAH" "A bounded agentic management assistant. It computes deterministic metrics and supports human decisions." "Target" {
            !docs docs
            !adrs adrs adrtools

            properties {
                "architecture.status" "Proposed"
                "architecture.style" "Modular Monolith"
                "database.decision" "PostgreSQL only"
                "agent.boundary" "One bounded AI agent; deterministic core outside the agent"
            }

            webApp = container "Web Application" "Persian RTL web application. It provides the three required management interfaces." "Web application; framework open" "Web" {
                chatUi = component "Conversational Assistant UI" "Shows reports and answers. It accepts scoped questions, uploads, and manager operations." "Web UI" "Web"
                dashboardUi = component "Role-Based Dashboard UI" "Shows authorized KPIs, targets, trends, drill-downs, decisions, and open actions." "Web UI" "Web"
                workflowUi = component "Workflow Control Room UI" "Shows WF1-WF3, stage SLA, bottlenecks, escalations, and pending decisions. Senior Manager only." "Web UI" "Web,ExecutiveOnly"
            }

            backendApi = container "Backend API" "Authenticates requests and routes each request through bounded analysis, validation, and delivery." "Application runtime; framework open" "API" {
                group "01 Access" {
                    identityBoundary = component "Identity Boundary" "Validates the session and creates a trusted identity context." "Deterministic module" "Security"
                    authorizationService = component "Authorization Service" "Builds the permitted row, column, role, purpose, and policy scope." "Deterministic module" "Security"
                }

                group "02 Request Routing" {
                    managerInputService = component "Manager Request Router" "Classifies each authorized request by its explicit request type and sends it to one fixed handler. It does not authorize requests, execute work, or create jobs." "Deterministic request dispatcher" "API"
                    configurationService = component "Configuration Service" "Accepts authorized configuration candidates, stores inactive versions, queues deterministic validation, and activates only an approved valid version. It does not calculate KPIs." "Deterministic configuration control" "Governance"
                    decisionTracker = component "Decision and Follow-Up" "Records an authorized human decision, its owner, deadline, success criteria, and later follow-up results. It does not execute the decision." "Deterministic decision control" "Decision"
                    runCoordinatorV2 = component "Run Coordinator" "Accepts run commands only from the Scheduler and Replay Runner. It creates each pinned run and its complete job plan, stores dependencies and manager order, monitors terminal jobs, and closes the run. It does not execute jobs." "Deterministic run control" "Governance"
                }

                group "03 Bounded Analysis" {
                    agentOrchestrator = component "Bounded Agent Orchestrator" "Coordinates one bounded report, interactive, configuration-candidate, or document decision-card graph. It can produce structured candidates but cannot confirm, activate, or execute them." "LangGraph runtime" "AI"
                    agentJobRunnerV2 = component "Agent Job Runner" "Claims queued Agent Jobs with its restricted database role, loads the pinned manager-scoped report package, invokes the bounded report graph, and forwards either a narrative result or a terminal model failure for validation. It cannot widen the pinned scope." "PostgreSQL-backed job runner" "AI"
                    conversationService = component "Conversation Service" "Stores manager-scoped conversation sessions and validated turns, and returns a bounded history window for interactive analysis. Conversation text is not business evidence." "Deterministic conversation module" "AI"
                    evidenceService = component "Evidence Service" "Builds a traceable Evidence Bundle inside the authorized scope supplied with the request." "Deterministic module" "Evidence"
                    queryGateway = component "Query Gateway" "Runs registered tools and scoped read-only SQL with limits and audit." "Deterministic query execution" "Query"
                    sqlGuard = component "SQL AST Guard" "Allows one approved SELECT statement and rejects unsafe SQL." "SQL parser and policy" "Security"
                    modelGateway = component "Model Gateway" "Applies token, time, retry, and cost limits to every model call." "Provider-neutral model client" "AI"
                }

                group "04 Validate and Deliver" {
                    outputValidator = component "Output Validator" "Checks the output schema, cited values, evidence references, allowed scope, response rules, and decision-card contract. It does not repeat KPI calculation, document parsing, or report-evidence assembly." "Deterministic validator" "Governance"
                    publisherV2 = component "Publisher" "Atomically publishes model-independent canonical JSON with validated Persian narrative when available, or deterministic fallback text when the model API is unavailable. It records publication receipts and artifact failures." "Deterministic publication module" "Processing"
                    reportApi = component "Report and Dashboard API" "Reads published reports and dashboard data, and returns validated interactive answers or explicit failures." "Deterministic delivery API" "API"
                    auditService = component "Audit Service" "Records query, model, validation, cost, and failure evidence." "Deterministic module" "Governance"
                }

                // Keep this feature group after the existing components so their generated
                // element IDs and the manual layout in workspace.json remain stable.
                group "05 Document Decision Flow" {
                    documentProcessingRunner = component "Document Processing Runner" "Accepts an authorized upload from the Manager Request Router, preserves the original bytes, invokes deterministic parsing, and creates a Document Analysis Job only after a successful parse. It does not call a model or create a decision." "Deterministic document intake controller" "Processing"
                    documentParser = component "Document Parser" "Reads approved upload bytes, validates a supported document contract, and stores immutable fragments and a parse receipt. It treats document content as data, not instructions." "Deterministic document parser" "Processing"
                    documentAnalysisJobRunner = component "Document Analysis Job Runner" "Claims only Document Analysis Jobs, reloads their pinned actor, scope, policy, and document fragments, invokes the bounded document decision-card graph, and submits its outcome for validation. It never claims report Agent Jobs or records decisions." "PostgreSQL-backed document job runner" "AI"
                    decisionConfirmationService = component "Decision Confirmation Service" "Stores a validated decision card, returns it for manager review, and accepts an authenticated confirm, edit, or reject command. It forwards only a confirmed card to Decision and Follow-Up and does not execute the decision." "Deterministic decision review control" "Decision"
                }
            }

            worker = container "Background Worker" "Executes deterministic ingestion, snapshot, KPI, workflow, signal, report-evidence, and configuration-validation jobs. It stores results in PostgreSQL and does not run agent graphs or publish reports." "Application runtime; shared modular codebase" "Worker" {
                runStageCoordinatorV2 = component "Run Stage Coordinator" "Claims Ready deterministic jobs from PostgreSQL and invokes ingestion, snapshot, KPI, workflow, signal, and report-evidence components according to stored dependencies. It does not create jobs." "PostgreSQL-backed deterministic job runner" "Processing"
                configurationValidationRunnerV2 = component "Configuration Validation Runner" "Claims configuration-validation jobs, checks KPI SQL, type, unit, scope, rollup, dependencies, and parity fixtures, and stores a validation receipt. It does not activate configuration." "PostgreSQL-backed validation runner" "Governance"
                ingestionCoordinator = component "Ingestion Coordinator" "Checks manifests, hashes, idempotency keys, source status, and atomic batch commits." "Deterministic module" "Processing"
                sourceAdapters = component "Source Adapters" "Parse versioned source schemas and preserve the source bytes and headers." "Deterministic adapters" "Processing"
                dataQualityService = component "Data Quality Service" "Records missing sources, late arrivals, duplicates, corrections, schema changes, and quarantine results." "Deterministic module" "DataQuality"
                snapshotService = component "Snapshot Service" "Pins committed data, organization, access policy, and configuration versions for a run." "Deterministic module" "Processing"
                projectionService = component "Projection Service" "Builds reproducible facts and process projections from committed source events." "Deterministic module" "Processing"
                semanticRegistry = component "Semantic Registry" "Versions KPI definitions, PostgreSQL SQL, units, precision, targets, ownership, and dependencies." "Deterministic registry" "Analytics"
                kpiCalculator = component "KPI Calculator" "Executes the 55 approved PostgreSQL KPI queries and records QueryRun and lineage." "PostgreSQL SQL" "Analytics"
                workflowEngine = component "Workflow Engine" "Reconstructs three workflows and calculates stage timing, SLA, backlog, and bottlenecks." "Deterministic process analysis" "Analytics"
                signalEngine = component "Signal Engine" "Applies R1-R8, ownership, grouping, ranking, suppression, and escalation without LLM." "Deterministic rules" "Analytics"
                reportEvidenceBuilderV2 = component "Report Evidence Builder" "Executes one claimed Report Evidence Job. It builds and stores one pinned, manager-scoped Evidence Package and model-independent Canonical Report JSON. It does not create jobs, call a model, validate model output, or publish reports." "Deterministic report evidence assembly" "Reporting"
            }

            schedulerReplay = container "Scheduler and Replay Runner" "Owns the simulated clock, run lease, replay range, evaluation profile, and resumable job dispatch." "Application command/process" "Scheduler" {
                replayCommandV2 = component "Replay Command" "Accepts a replay range, sequences simulated days, and resumes from the last terminal day." "Application command" "Scheduler,Candidate"
                simulationClockV2 = component "Simulation Clock" "Derives the pinned business date and source cutoff without using the host clock as product time." "Deterministic clock" "Scheduler,Candidate"
                evaluationProfileLoaderV2 = component "Evaluation Profile Loader" "Loads the selected evaluation limits, acceptance thresholds, and run options." "Deterministic configuration reader" "Evaluation,Candidate"
                runStatusClientV2 = component "Run Status Client" "Starts and monitors runs only through the Backend Run Coordinator." "Internal API client" "Scheduler,Candidate"
                acceptanceTestHarnessV2 = component "Acceptance Test Harness" "Runs replay, hidden-data, regression, leakage, performance, cost, and output-contract checks outside the daily report-publication path." "Deterministic test harness" "Evaluation,Candidate"
            }

            postgres = container "PostgreSQL" "The only product database. It stores product state, analytical results, access policy, checkpoints, and audit records." "PostgreSQL" "Database" {
                properties {
                    "schemas.proposed" "ingest, core, org, semantic, analytics, workflow, reporting, document, decision, agent, audit"
                    "security" "RLS, FORCE ROW LEVEL SECURITY, non-owner runtime roles, no BYPASSRLS"
                    "runtime.roles.proposed" "ingestion_writer, analytics_worker, application_api, agent_query_reader, audit_reader"
                    "migration.owner" "migration_owner; never used at runtime"
                }
            }

            fileArchive = container "Protected File Archive" "Stores original source and upload bytes with hashes and manifests. It is not a query database." "Protected volume or object storage" "Storage"
        }

        // Scenario-only elements. Structurizr dynamic views cannot show components
        // from multiple containers, so this custom model mirrors the revised L3
        // component names only for the numbered report-generation scenario.
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
        reportScenarioAgentRunner = element "Agent Job Runner" "Backend API" "Claims one Ready Agent Job, loads its report package, and controls bounded report-graph execution." "ScenarioStep,ScenarioBackend"
        reportScenarioAuthorization = element "Authorization Service" "Backend API" "Revalidates the pinned manager scope before report-graph execution." "ScenarioStep,ScenarioBackend"
        reportScenarioAgent = element "Bounded Agent Orchestrator" "Backend API" "Uses Evidence Service, Query Gateway, SQL AST Guard, and Model Gateway to produce an optional narrative candidate." "ScenarioStep,ScenarioBackend"
        reportScenarioValidator = element "Output Validator" "Backend API" "Validates Canonical Report JSON, narrative or model failure, evidence, scope, schema, and report rules." "ScenarioStep,ScenarioBackend"
        reportScenarioPublisher = element "Publisher" "Backend API" "Publishes each validated manager report or authorized deterministic fallback and records its publication receipt." "ScenarioStep,ScenarioBackend"
        reportScenarioDelivery = element "Report and Dashboard API / Web Application" "Report delivery" "Reads and delivers each published manager report." "ScenarioStep,ScenarioWeb"

        reportScenarioReplay -> reportScenarioRunStatus "01. Prepare one reporting day"
        reportScenarioRunStatus -> reportScenarioRunCoordinator "02. Request a pinned run"
        reportScenarioRunCoordinator -> reportScenarioPostgres "03. Create the Run, all Jobs, dependencies, and manager order"
        reportScenarioRunStage -> reportScenarioPostgres "04. Claim Ready deterministic Jobs"
        reportScenarioRunStage -> reportScenarioIngestion "05. Run ingestion and data-quality checks"
        reportScenarioRunStage -> reportScenarioSnapshot "06. Create the pinned Snapshot"
        reportScenarioRunStage -> reportScenarioKpi "07. Calculate approved KPIs"
        reportScenarioRunStage -> reportScenarioWorkflow "08. Reconstruct workflows"
        reportScenarioRunStage -> reportScenarioSignal "09. Detect and rank signals"
        reportScenarioRunStage -> reportScenarioEvidenceBuilder "10. For each manager in order, execute the Ready Report Evidence Job"
        reportScenarioEvidenceBuilder -> reportScenarioPostgres "11. Store the package, complete the Job, and unlock its Agent Job"
        reportScenarioAgentRunner -> reportScenarioPostgres "12. Claim the Ready Agent Job and load its package"
        reportScenarioAgentRunner -> reportScenarioAuthorization "13. Revalidate manager scope"
        reportScenarioAgentRunner -> reportScenarioAgent "14. Run the bounded report graph"
        reportScenarioAgentRunner -> reportScenarioValidator "15. Submit narrative candidate or model failure"
        reportScenarioValidator -> reportScenarioPublisher "16. Release a valid report or authorized fallback"
        reportScenarioPublisher -> reportScenarioPostgres "17. Publish the report, complete the Job, and unlock the next manager"
        reportScenarioPostgres -> reportScenarioDelivery "18. Deliver the published manager report"
        reportScenarioRunCoordinator -> reportScenarioPostgres "19. After all required Jobs are terminal, persist final status and close the Run"

        // System-level relationships
        seniorManager -> didrah "Reads organization health, workflows, escalations, and pending decisions" "HTTPS"
        unitManager -> didrah "Reads authorized unit and team results and records decisions" "HTTPS"
        teamSupervisor -> didrah "Reads authorized team results and direct-member workload" "HTTPS"
        evaluator -> didrah "Runs replay, hidden-data checks, and acceptance tests" "CLI and HTTPS/JSON"
        operator -> didrah "Monitors runs, failures, cost, backup, and restore evidence" "HTTPS"
        inputDataset -> didrah "Supplies versioned source data and scripted manager activity" "Read-only filesystem: CSV, JSON, and Markdown"
        didrah -> identityProvider "Validates trusted user identities" "OIDC or internal authentication over HTTPS"
        didrah -> llmProvider "Requests bounded model completions" "HTTPS/JSON"

        // Container-level relationships
        seniorManager -> webApp "Reads organization health, cross-unit workflows, escalations, and decisions" "HTTPS"
        unitManager -> webApp "Reads authorized unit and team results and records decisions" "HTTPS"
        teamSupervisor -> webApp "Reads authorized team results and direct-member workload" "HTTPS"
        evaluator -> schedulerReplay "Starts replay and acceptance checks" "CLI and HTTPS/JSON"
        evaluator -> backendApi "Reads acceptance evidence and exported outputs" "HTTPS/JSON"
        operator -> backendApi "Reads authorized operational status" "HTTPS"
        inputDataset -> worker "Supplies eligible nightly drops, manifests, and source contracts" "Read-only filesystem: CSV and JSON"
        inputDataset -> schedulerReplay "Supplies scripted manager inputs, upload attachments, and replay scenarios" "Read-only filesystem: JSON, CSV, and Markdown"
        backendApi -> identityProvider "Validates sessions and trusted identities" "OIDC over HTTPS or internal authentication"
        webApp -> backendApi "Requests reports, scoped queries, uploads, configuration changes, and decisions" "HTTPS/JSON"
        schedulerReplay -> backendApi "Starts and monitors pinned runs through the Run Coordinator" "Authenticated HTTPS/JSON"
        schedulerReplay -> postgres "Reads replay evidence and records acceptance results" "PostgreSQL protocol over TLS"
        worker -> agentOrchestrator "Supplies a canonical Insight Brief for an optional bounded Persian narrative" "Internal authenticated call" {
            tags "PrimaryFlow"
        }
        backendApi -> postgres "Reads and writes scoped application state and durable jobs" "PostgreSQL protocol over TLS"
        worker -> postgres "Claims durable jobs and reads or writes deterministic results" "PostgreSQL protocol over TLS"
        worker -> fileArchive "Archives and reads approved source bytes" "Restricted file system I/O"
        backendApi -> fileArchive "Archives uploads and reads approved fragments" "Restricted file system I/O"
        backendApi -> llmProvider "Calls only through Model Gateway" "HTTPS/JSON"

        // Web component relationships
        seniorManager -> chatUi "Reads executive brief and asks aggregate questions"
        seniorManager -> dashboardUi "Reads organization health"
        seniorManager -> workflowUi "Reads WF1-WF3 and escalations"
        unitManager -> chatUi "Reads unit brief and records decisions"
        unitManager -> dashboardUi "Reads unit and team aggregates"
        teamSupervisor -> chatUi "Reads team brief and asks scoped questions"
        teamSupervisor -> dashboardUi "Reads team KPIs and direct-workload details"
        chatUi -> backendApi "Submits questions and manager operations; retrieves reports and answers" "HTTPS/JSON"
        dashboardUi -> backendApi "Retrieves authorized metrics, trends, and drill-down results" "HTTPS/JSON"
        workflowUi -> backendApi "Retrieves executive workflow, bottleneck, and escalation results" "HTTPS/JSON"

        // API component relationships.
        // Primary request path: Web -> Identity -> Authorization -> Router -> Agent -> Validator -> Delivery -> Web.
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
        managerInputService -> agentOrchestrator "Starts an interactive question or chat decision-card graph" "In-process function call" {
            tags "PrimaryFlow"
        }
        agentOrchestrator -> configurationService "Submits a structured configuration candidate for explicit approval" "In-process function call" {
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
        documentProcessingRunner -> postgres "Creates a Document Analysis Job only after a successful parse" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        documentAnalysisJobRunner -> postgres "Claims a Document Analysis Job and loads its pinned actor, scope, policy, and fragments" "PostgreSQL protocol over TLS" {
            tags "DataFlow"
        }
        documentAnalysisJobRunner -> agentOrchestrator "Invokes the bounded document decision-card graph" "In-process function call" {
            tags "PrimaryFlow"
        }
        documentAnalysisJobRunner -> outputValidator "Submits a decision-card candidate or explicit terminal failure" "In-process function call" {
            tags "PrimaryFlow"
        }
        configurationService -> authorizationService "Checks actor authority and affected scope" "In-process function call" {
            tags "PolicyCheck"
        }
        configurationService -> postgres "Stores an inactive configuration version and enqueues a deterministic validation job" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        decisionTracker -> authorizationService "Checks decision authority" "In-process function call" {
            tags "PolicyCheck"
        }
        decisionTracker -> postgres "Appends decision and follow-up events" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        decisionTracker -> agentOrchestrator "Requests a draft only" "In-process function call" {
            tags "ControlFlow"
        }

        // Bounded analysis. Tool and model responses are implicit unless a failure path needs a separate edge.
        agentOrchestrator -> evidenceService "Requests an authorized evidence bundle" "In-process function call" {
            tags "DataFlow"
        }
        agentOrchestrator -> conversationService "Stores the manager message and loads bounded conversation history" "In-process function call" {
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
        agentOrchestrator -> modelGateway "Requests bounded analysis or drafting" "In-process function call" {
            tags "ModelFlow"
        }
        modelGateway -> postgres "Reserves and settles the cost budget" "PostgreSQL protocol over TLS" {
            tags "ControlFlow"
        }
        modelGateway -> llmProvider "Sends authorized evidence and receives a completion" "HTTPS/JSON" {
            tags "ExternalFlow"
        }
        modelGateway -> auditService "Records model and cost evidence" "In-process function call" {
            tags "ControlFlow"
        }
        modelGateway -> agentOrchestrator "Returns a completion or terminal failure" "In-process function call" {
            tags "Feedback"
        }
        agentOrchestrator -> outputValidator "Submits a draft and evidence references" "In-process function call" {
            tags "PrimaryFlow"
        }

        // Validation, delivery, and accountability.
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
        outputValidator -> conversationService "Stores the validated answer or explicit terminal failure" "In-process function call" {
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
        decisionConfirmationService -> agentOrchestrator "Requests a revised decision card after a manager edit" "In-process function call" {
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

        // Worker component relationships
        ingestionCoordinator -> inputDataset "Reads expected nightly drops, manifests, and source contracts" "Read-only filesystem: CSV and JSON"
        ingestionCoordinator -> sourceAdapters "Parses each source contract" "In-process function call"
        sourceAdapters -> fileArchive "Preserves original bytes, headers, and hashes" "Restricted file system I/O"
        sourceAdapters -> dataQualityService "Submits parsed and rejected rows" "In-process function call"
        dataQualityService -> postgres "Writes accepted records, quarantine, and DataIssues" "PostgreSQL protocol over TLS"
        snapshotService -> postgres "Pins committed batches, organization, policy, and configuration versions" "PostgreSQL protocol over TLS"
        snapshotService -> projectionService "Requests reproducible facts and process projections" "In-process function call"
        projectionService -> postgres "Reads events and writes facts and projections" "PostgreSQL protocol over TLS"
        kpiCalculator -> semanticRegistry "Reads approved PostgreSQL SQL and metadata" "In-process function call"
        semanticRegistry -> postgres "Reads versioned KPI definitions and dependencies" "PostgreSQL protocol over TLS"
        kpiCalculator -> postgres "Executes KPI SQL and writes observations, QueryRun, and lineage" "PostgreSQL protocol over TLS"
        workflowEngine -> postgres "Reads events and writes case, stage, SLA, and bottleneck observations" "PostgreSQL protocol over TLS"
        signalEngine -> postgres "Reads KPI and history; writes episodes, ownership, suppression, and escalation" "PostgreSQL protocol over TLS"

        // Current run-control, report-evidence, agent, publication, and evaluation flow.
        evaluator -> replayCommandV2 "Starts a replay range and requests acceptance results"
        inputDataset -> replayCommandV2 "Supplies scripted replay range and manager-input scenarios" "Read-only JSON"
        replayCommandV2 -> simulationClockV2 "Requests one pinned business date and source cutoff per day"
        replayCommandV2 -> evaluationProfileLoaderV2 "Loads the selected evaluation profile"
        replayCommandV2 -> runStatusClientV2 "Starts or resumes each simulated day with the pinned date, cutoff, profile, and run options"
        replayCommandV2 -> acceptanceTestHarnessV2 "Starts acceptance checks after the replay range reaches a terminal state"
        runStatusClientV2 -> runCoordinatorV2 "Starts and monitors runs through the internal Backend API" "Authenticated HTTPS/JSON"
        runCoordinatorV2 -> authorizationService "Validates the Scheduler or Replay service identity and run-control permission" "In-process function call"
        evaluator -> acceptanceTestHarnessV2 "Starts replay acceptance, hidden-data, and regression checks"
        acceptanceTestHarnessV2 -> evaluationProfileLoaderV2 "Loads acceptance thresholds and limits"
        acceptanceTestHarnessV2 -> runStatusClientV2 "Reads terminal replay run status and artifact references"
        acceptanceTestHarnessV2 -> postgres "Reads replay evidence and writes acceptance results"

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

        agentJobRunnerV2 -> postgres "Claims Ready Agent Jobs and loads Canonical Report JSON, evidence, Snapshot, scope, and checkpoint state" "PostgreSQL protocol over TLS"
        agentJobRunnerV2 -> agentOrchestrator "Invokes the bounded report graph and receives its outcome" "In-process function call"
        agentJobRunnerV2 -> outputValidator "Submits canonical JSON with a narrative candidate or explicit model failure" "In-process function call"
        outputValidator -> publisherV2 "Releases a validated package or authorizes deterministic fallback publication" "In-process function call"
        publisherV2 -> postgres "Atomically commits Canonical Report JSON, validated narrative or fallback text, and publication receipt; completes the Agent Job and unlocks the next manager Job" "PostgreSQL protocol over TLS"
        publisherV2 -> auditService "Records publication mode and artifact failures" "In-process function call"

    }

    views {
        properties {
            "structurizr.sort" "key"
        }

        // C4 core view: one software system and its directly connected people and software systems.
        systemContext didrah L1_SystemContext "Business-facing C4 system context for DIDRAH." {
            title "01 - C4 Level 1 - System Context for DIDRAH"
            include seniorManager unitManager teamSupervisor evaluator operator didrah inputDataset identityProvider llmProvider
            default
        }

        // C4 core view: deployable applications and data stores inside the DIDRAH boundary.
        container didrah L2_Containers "C4 container view of the DIDRAH applications, data stores, users, and external dependencies." {
            title "02 - C4 Level 2 - Containers for DIDRAH"
            include seniorManager unitManager teamSupervisor evaluator operator inputDataset identityProvider llmProvider webApp backendApi worker schedulerReplay postgres fileArchive
        }

        // Revised C4 Level 3 views.
        component backendApi L3_3_RevisedBackendApiComponents "Backend API view with authorized request routing, in-process document intake and parsing, separate report and document job runners, manager-confirmed decision cards, scheduler-only run control, validation, publication, and delivery." {
            title "03.3 - C4 Level 3 - Backend API Components"
            include webApp fileArchive identityProvider llmProvider postgres runStatusClientV2 identityBoundary authorizationService managerInputService configurationService decisionTracker runCoordinatorV2 documentProcessingRunner documentParser documentAnalysisJobRunner agentJobRunnerV2 agentOrchestrator conversationService evidenceService queryGateway sqlGuard modelGateway outputValidator decisionConfirmationService publisherV2 reportApi auditService
            exclude "configurationService -> authorizationService"
            exclude "decisionTracker -> authorizationService"
            exclude "evidenceService -> authorizationService"
            exclude "queryGateway -> authorizationService"
            exclude "sqlGuard -> queryGateway"
            exclude "modelGateway -> agentOrchestrator"
            exclude "outputValidator -> queryGateway"
            exclude "outputValidator -> authorizationService"
            exclude "outputValidator -> evidenceService"
            exclude "reportApi -> authorizationService"
        }

        component worker L3_4_RevisedBackgroundWorkerComponents "Background Worker view with PostgreSQL-backed run-stage execution, independent configuration validation, deterministic analytics, and one-manager-at-a-time report evidence assembly. Manager document processing remains inside the Backend API." {
            title "03.4 - C4 Level 3 - Background Worker Components"
            include inputDataset postgres fileArchive configurationService runCoordinatorV2 agentJobRunnerV2 runStageCoordinatorV2 configurationValidationRunnerV2 ingestionCoordinator sourceAdapters dataQualityService snapshotService projectionService semanticRegistry kpiCalculator workflowEngine signalEngine reportEvidenceBuilderV2
        }

        component schedulerReplay L3_5_RevisedSchedulerReplayComponents "Revised Scheduler and Replay Runner view that controls simulated time and replay through the Backend Run Coordinator and runs acceptance checks outside the daily publication path." {
            title "03.5 - C4 Level 3 - Revised Scheduler and Replay Runner Components"
            include evaluator inputDataset postgres runCoordinatorV2 replayCommandV2 simulationClockV2 evaluationProfileLoaderV2 runStatusClientV2 acceptanceTestHarnessV2
        }

        // Numbered end-to-end scenario for the revised L3 architecture.
        custom S7_ReportGenerationScenario "04.7 - Scenario - Report Generation" "Primary report-generation path across Scheduler, Backend API, Background Worker, and PostgreSQL." {
            include reportScenarioReplay reportScenarioRunStatus reportScenarioRunCoordinator reportScenarioPostgres reportScenarioRunStage reportScenarioIngestion reportScenarioSnapshot reportScenarioKpi reportScenarioWorkflow reportScenarioSignal reportScenarioEvidenceBuilder reportScenarioAgentRunner reportScenarioAuthorization reportScenarioAgent reportScenarioValidator reportScenarioPublisher reportScenarioDelivery
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
