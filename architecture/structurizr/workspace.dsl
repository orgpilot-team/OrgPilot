workspace "DIDRAH Proposed Architecture" "Proposed C4 model for the DIDRAH management assistant. Open decisions are not approved facts." {
    !identifiers flat
    !impliedRelationships false

    // Architecture sources: this DSL, docs/01-purpose-and-scope.md through docs/16-domain-model.md, and adrs/.
    // Authoritative implementation contract: docs/15-implementation-contract.md (ADR-0025); TA clarifications win over older brief values.
    // DDD model for Backend API, Background Worker, and Agent Runtime: docs/16-domain-model.md (ADR-0024).
    // Evaluation references: DataSet/arka_dataset/README_FA.md and output_contract/*.json are read-only.
    // PostgreSQL is the selected product database; any engine with identical results is permitted (ADR-0002).
    // SQLite is an external test oracle for reference SQL only. It is not a runtime container.
    // Status: Accepted for implementation under the evaluation profile; open decisions remain in docs/08-risks-and-open-issues.md.

    model {
        // People
        seniorManager = person "Senior Manager" "Reads organization health, workflows, escalations, and pending decisions." "Person,Executive"
        unitManager = person "Unit Manager" "Reads authorized aggregates and records decisions and follow-up actions." "Person,Manager"
        teamSupervisor = person "Team Supervisor" "Reads team data and authorized workload details." "Person,Manager"
        evaluator = person "Evaluator" "Runs Docker, replay, hidden-data checks, and acceptance tests." "Person,Evaluator"
        operator = person "Operator" "Monitors runs, failures, cost, backup, and restore evidence." "Person,Operator"

        // External systems
        inputDataset = softwareSystem "DIDRAH Input Dataset" "Provides versioned source, replay, upload, configuration, and history data." "External,Source,Evaluation" {
            url "{workspace}/documentation/DIDRAH#input-dataset-contract"
        }
        submissionOutput = softwareSystem "Submission Output Directory" "Writable OUTPUT_DIR mount for approved brief and QA files only." "External,Storage,Evaluation" {
            url "{workspace}/documentation/DIDRAH#submission-output-contract"
        }
        identityProvider = softwareSystem "Identity Provider" "Authenticates users and supplies a trusted identity. The product or internal method is open." "External,Identity,OpenDecision"
        llmProvider = softwareSystem "Language Model Provider" "Returns bounded language-model completions. Evaluation profile: deepseek/deepseek-v4.1-flash-1017 via OpenAI-compatible API; only external endpoint reachable in the graded run." "External,AI" {
            url "{workspace}/documentation/DIDRAH#llm-provider-and-configuration"
        }
        langfuse = softwareSystem "Langfuse" "Receives optional redacted telemetry in the development profile only. Disabled in the graded Evaluation profile because outbound network is closed (ADR-0027)." "External,Observability"

        didrah = softwareSystem "DIDRAH" "A bounded agentic management assistant. It computes deterministic metrics and supports human decisions." "Target" {
            !docs docs
            !adrs adrs adrtools

            properties {
                "architecture.status" "Accepted for implementation (evaluation profile)"
                "architecture.style" "Modular Monolith with DDD bounded contexts (ADR-0024)"
                "implementation.contract" "docs/15-implementation-contract.md (ADR-0025)"
                "domain.model" "docs/16-domain-model.md (ADR-0024)"
                "database.decision" "PostgreSQL 18 selected; any engine with identical results permitted"
                "agent.boundary" "One bounded AI agent; deterministic core outside the agent"
                "budget.minutes_per_day" "5"
                "budget.usd_total_30_days" "5"
                "budget.cost_formula" "logged input+output tokens x provider official rate on evaluation day"
                "determinism.two_runs" "identical numbers and discovered signals (ADR-0026)"
                "network.egress.evaluation" "LLM API only (ADR-0027)"
                "kpi.parity.tolerance" "±1% (dev and evaluation); zero only for text-to-JSON number matching"
            }

            webApp = container "Web Application" "Persian RTL web application. It provides the three required management interfaces." "React 19, TypeScript, Vite" "Web" {
                chatUi = component "Conversational Assistant UI" "Shows reports and answers. It accepts scoped questions, uploads, and manager operations." "Web UI" "Web" {
                    url "{workspace}/documentation/DIDRAH#conversational-assistant-ui"
                }
                dashboardUi = component "Role-Based Dashboard UI" "Shows authorized KPIs, targets, trends, drill-downs, decisions, and open actions." "Web UI" "Web" {
                    url "{workspace}/documentation/DIDRAH#role-based-dashboard-ui"
                }
                workflowUi = component "Workflow Control Room UI" "Shows WF1-WF3, stage SLA, bottlenecks, escalations, and pending decisions. Senior Manager only." "Web UI" "Web,ExecutiveOnly" {
                    url "{workspace}/documentation/DIDRAH#workflow-control-room-ui"
                }
            }

            backendApi = container "Backend API" "Authorizes requests, creates durable jobs, validates outcomes, and delivers results. DDD contexts: Identity & Access, Manager Interaction, Analysis Coordination, Decision Governance, Publication & Delivery, Audit (docs/16-domain-model.md)." "ASP.NET Core, .NET 10 LTS, REST/JSON, OpenAPI" "API" {
                properties {
                    "ddd.contexts" "Identity & Access, Manager Interaction, Analysis Coordination, Decision Governance, Publication & Delivery, Audit"
                    "ddd.aggregates" "Grant, AccessPolicy, ManagerRequest, ConversationSession, AgentJob, DecisionCard, Decision, ReportVersion, ExportBatch, AuditEntry"
                    "ddd.use_cases" "SubmitManagerQuestion, SubmitUpload, ConfirmDecision, RecordFollowUp, PublishReport, ExportSubmission, ActivateConfiguration, ActivateOrganizationRevision, StartRun, CloseRun, ReadJobStatus, ReadScopedReport"
                    "ddd.ports" "IAgentJobRepository, IDecisionRepository, IReportVersionRepository, IAccessPolicyRepository, IAuditLog, IEvidencePort, IScopedQueryPort, IClockPort"
                    "ddd.anti_corruption" "Source/upload text is data; LLM output is a candidate only; provider API translated at Model Gateway"
                }
                group "01 Access" {
                    identityBoundary = component "Identity Boundary" "Validates the session and creates a trusted identity context." "Deterministic module" "Security" {
                        url "{workspace}/documentation/DIDRAH#identity-boundary"
                    }
                    authorizationService = component "Authorization Service" "Builds the permitted row, column, role, purpose, and policy scope." "Deterministic module" "Security" {
                        url "{workspace}/documentation/DIDRAH#authorization-service"
                    }
                }

                group "02 Request Routing" {
                    managerInputService = component "Manager Request Router" "Routes each authorized request to one fixed handler. It does not execute work." "Deterministic request dispatcher" "API" {
                        url "{workspace}/documentation/DIDRAH#manager-request-router"
                    }
                    configurationService = component "Configuration Service" "Stores inactive candidates and activates only a valid approved version." "Deterministic configuration control" "Governance" {
                        url "{workspace}/documentation/DIDRAH#configuration-service"
                    }
                    organizationConfigurationService = component "Organization Configuration Service" "Validates versioned organization changes and activates them at D+1." "Deterministic organization control" "Governance" {
                        url "{workspace}/documentation/DIDRAH#organization-configuration-service"
                    }
                    decisionTracker = component "Decision and Follow-Up" "Records authorized human decisions and their follow-up contracts. It does not execute them." "Deterministic decision control" "Decision" {
                        url "{workspace}/documentation/DIDRAH#decision-and-follow-up"
                    }
                    runCoordinatorV2 = component "Run Coordinator" "Creates pinned run plans, monitors terminal jobs, and closes each run." "Deterministic run control" "Governance" {
                        url "{workspace}/documentation/DIDRAH#run-coordinator"
                    }
                }

                group "03 Bounded Analysis" {
                    agentGateway = component "Agent Runtime Gateway" "Enqueues interactive jobs and sends best-effort job-ID wake-ups. PostgreSQL stays authoritative." "Deterministic job gateway" "AI" {
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
                    outputValidator = component "Output Validator" "Checks schema, evidence, scope, and response rules, then records the validation state." "Deterministic validator" "Governance" {
                        url "{workspace}/documentation/DIDRAH#output-validator"
                    }
                    agentJobStatusService = component "Agent Job Status API" "Returns authorized persisted job status and result references. It never executes jobs." "Deterministic delivery API" "API" {
                        url "{workspace}/documentation/DIDRAH#agent-job-status-api"
                    }
                    publisherV2 = component "Publisher" "Atomically publishes validated canonical JSON or deterministic fallback text." "Deterministic publication module" "Processing" {
                        url "{workspace}/documentation/DIDRAH#publisher"
                    }
                    submissionExporter = component "Submission Exporter" "Validates and atomically exports approved brief and QA artifacts under OUTPUT_DIR." "Deterministic export module" "Processing" {
                        url "{workspace}/documentation/DIDRAH#submission-exporter"
                    }
                    reportApi = component "Report and Dashboard API" "Reads published reports and dashboard data, and returns validated interactive answers or explicit failures." "Deterministic delivery API" "API" {
                        url "{workspace}/documentation/DIDRAH#report-and-dashboard-api"
                    }
                    auditService = component "Audit Service" "Records query, model, validation, cost, and failure evidence." "Deterministic module" "Governance" {
                        url "{workspace}/documentation/DIDRAH#audit-service"
                    }
                }

                group "05 Document Decision Flow" {
                    documentProcessingRunner = component "Document Processing Runner" "Archives and parses uploads, then creates durable analysis or revision jobs." "Deterministic document intake and job producer" "Processing" {
                        url "{workspace}/documentation/DIDRAH#document-processing-runner"
                    }
                    documentParser = component "Document Parser" "Validates uploads and stores immutable fragments and a parse receipt." "Deterministic document parser" "Processing" {
                        url "{workspace}/documentation/DIDRAH#document-parser"
                    }
                    decisionConfirmationService = component "Decision Confirmation Service" "Stores validated cards and handles authenticated confirm, edit, or reject commands." "Deterministic decision review control" "Decision" {
                        url "{workspace}/documentation/DIDRAH#decision-confirmation-service"
                    }
                }
            }

            worker = container "Background Worker" "Executes deterministic processing and validation jobs and stores results in PostgreSQL. DDD contexts: Intake & Data Quality, Snapshot & Projection, Semantic & KPI, Workflow & Signal, Decision Effect, Run Orchestration (docs/16-domain-model.md)." ".NET 10 Worker Service" "Worker" {
                properties {
                    "ddd.contexts" "Intake & Data Quality, Snapshot & Projection, Semantic & KPI, Workflow & Signal, Decision Effect, Run Orchestration"
                    "ddd.aggregates" "IngestionBatch, DataIssue, Snapshot, Projection, KpiDefinition, KpiResult, WorkflowObservation, SignalEpisode, EffectAssessment, RunStage"
                    "ddd.value_objects" "SourceKey, EventKey=(entity_id,event_type,event_time), DedupKey, PinnedVersions, QueryRun, Lineage, SuccessCriterion"
                    "ddd.domain_services" "DeduplicationService, DataIssueClassifier, KpiParityService, RollupService, WorkflowReconstructionService, SignalDetectionService, EscalationPolicyService, DecisionEffectService, ReportEvidenceAssembler"
                    "dedup.keys" "order_id,ticket_id,lead_id,task_id; events=(entity_id,event_type,event_time)"
                    "lead.abandoned_after_days" "14"
                    "lead.kpi_populations" "K_WF3_SLA_7D and K_ENT_WINRATE_30D: closed leads only; K_ENT_PIPELINE: proposals sent only"
                }
                runStageCoordinatorV2 = component "Run Stage Coordinator" "Claims Ready jobs and runs their deterministic stages from stored dependencies." "PostgreSQL-backed deterministic job runner" "Processing" {
                    url "{workspace}/documentation/DIDRAH#run-stage-coordinator"
                }
                configurationValidationRunnerV2 = component "Configuration Validation Runner" "Validates configuration jobs and stores receipts. It does not activate configuration." "PostgreSQL-backed validation runner" "Governance" {
                    url "{workspace}/documentation/DIDRAH#configuration-validation-runner"
                }
                ingestionCoordinator = component "Ingestion Coordinator" "Checks manifests, hashes, idempotency keys, source status, and atomic batch commits." "Deterministic module" "Processing" {
                    url "{workspace}/documentation/DIDRAH#ingestion-coordinator"
                }
                sourceAdapters = component "Source Adapters" "Parse versioned source schemas and preserve the source bytes and headers." "Deterministic adapters" "Processing" {
                    url "{workspace}/documentation/DIDRAH#source-adapters"
                }
                normalizer = component "Normalizer" "Converts parsed fields to canonical types, units, identifiers, and time semantics." "Deterministic normalization module" "Processing" {
                    url "{workspace}/documentation/DIDRAH#normalizer"
                }
                dataQualityService = component "Data Quality Service" "Records data_issues with exact types: 'missing' every morning until arrival (dependent KPIs null, never zero), one 'late_arrival' the next morning with same-morning recomputation and signal publication, and 'duplicate' with source 'orders' after dedup. A data issue is never a business signal; only a signal created by recomputation is published." "Deterministic module" "DataQuality" {
                    url "{workspace}/documentation/DIDRAH#data-quality-service"
                }
                snapshotService = component "Snapshot Service" "Pins committed data, organization, access policy, and configuration versions for a run." "Deterministic module" "Processing" {
                    url "{workspace}/documentation/DIDRAH#snapshot-service"
                }
                projectionService = component "Projection Service" "Builds reproducible facts and process projections from committed source events." "Deterministic module" "Processing" {
                    url "{workspace}/documentation/DIDRAH#projection-service"
                }
                semanticRegistry = component "Semantic Registry" "Versions KPI definitions, PostgreSQL SQL, units, precision, targets, ownership, direction (1=more better, -1=less better), escalate_after_days, and dependencies. Includes corrected config/monthly_targets.csv with scope=U_SAL for Q03." "Deterministic registry" "Analytics" {
                    url "{workspace}/documentation/DIDRAH#semantic-registry"
                }
                kpiDefinitionPreprocessor = component "KPI Definition Preprocessor" "Translates approved KPI definitions into versioned PostgreSQL SQL before validation and registration." "Deterministic PostgreSQL SQL preprocessor" "Analytics" {
                    url "{workspace}/documentation/DIDRAH#kpi-definition-preprocessor"
                }
                kpiCalculator = component "KPI Calculator" "Executes the 55 approved PostgreSQL KPI queries and records QueryRun and lineage." "PostgreSQL SQL" "Analytics" {
                    url "{workspace}/documentation/DIDRAH#kpi-calculator"
                }
                workflowEngine = component "Workflow Engine" "Reconstructs three workflows and calculates stage timing, SLA, backlog, and bottlenecks. Stage owner = measuring KPI owner; whole-workflow owner = Senior Manager. Leads with no progress after 14 days are abandoned, not bottlenecks." "Deterministic process analysis" "Analytics" {
                    url "{workspace}/documentation/DIDRAH#workflow-engine"
                }
                signalEngine = component "Signal Engine" "Maintains deterministic signal lifecycles (new/ongoing/escalated), escalation by crit or warn dwell time, suppression of unchanged repeats, unfavorable-direction-only R5, and executive co-cause grouping. Guardrail breaches arrive as signals." "Deterministic rules" "Analytics" {
                    url "{workspace}/documentation/DIDRAH#signal-engine"
                }
                reportEvidenceBuilderV2 = component "Report Evidence Builder" "Builds one pinned evidence package and model-independent canonical report per job." "Deterministic report evidence assembly" "Reporting" {
                    url "{workspace}/documentation/DIDRAH#report-evidence-builder"
                }
                decisionEffectEvaluator = component "Decision Effect Evaluator" "Evaluates KPI change and guardrails with workload normalization or comparable-case baseline; exports improved/worsened/too_early; 'not isolatable' is never 'no effect'; guardrail breach emits a signal. No LLM." "Deterministic evaluation module" "Decision" {
                    url "{workspace}/documentation/DIDRAH#decision-effect-evaluator"
                }
            }

            schedulerReplay = container "Scheduler and Replay Runner" "Owns the simulated clock, run lease, replay range, evaluation profile, and resumable job dispatch." ".NET 10 Console or Worker Process" "Scheduler" {
                replayCommandV2 = component "Replay Command" "Accepts a replay range, sequences simulated days, and resumes from the last terminal day." "Application command" "Scheduler,Candidate" {
                    url "{workspace}/documentation/DIDRAH#replay-command"
                }
                simulationClockV2 = component "Simulation Clock" "Derives the pinned business date and source cutoff without using the host clock as product time." "Deterministic clock" "Scheduler,Candidate" {
                    url "{workspace}/documentation/DIDRAH#simulation-clock"
                }
                evaluationProfileLoaderV2 = component "Evaluation Profile Loader" "Loads the selected evaluation limits, acceptance thresholds, and run options." "Deterministic configuration reader" "Evaluation,Candidate" {
                    url "{workspace}/documentation/DIDRAH#evaluation-profile-loader"
                }
                runStatusClientV2 = component "Run Status Client" "Starts and monitors runs only through the Backend Run Coordinator." "Internal API client" "Scheduler,Candidate" {
                    url "{workspace}/documentation/DIDRAH#run-status-client"
                }
                acceptanceTestHarnessV2 = component "Acceptance Test Harness" "Runs replay, regression, leakage, performance, contract, and KPI parity checks." "Deterministic test harness" "Evaluation,Candidate" {
                    url "{workspace}/documentation/DIDRAH#acceptance-test-harness"
                }
                kpiParityValidator = component "KPI Parity Validator" "Compares SQLite reference results with equivalent PostgreSQL results within ±1% and records receipts. Asserts median()→percentile_cont(0.5) not percentile_disc, julianday→EXTRACT(EPOCH)/86400 with unit conversion, 100.0* percentages, timezone and rounding." "Deterministic parity module" "Evaluation" {
                    url "{workspace}/documentation/DIDRAH#kpi-parity-validator"
                }
                scriptedManagerInputAdapter = component "Scripted Manager Input Adapter" "Submits versioned replay inputs through the same Backend API as interactive inputs." "Deterministic evaluation input adapter" "Evaluation" {
                    url "{workspace}/documentation/DIDRAH#scripted-manager-input-adapter"
                }
            }

            postgres = container "PostgreSQL" "The only product database. It stores product state, analytical results, access policy, checkpoints, and audit records." "PostgreSQL 18" "Database" {
                url "{workspace}/documentation/DIDRAH#postgresql-product-database"
                properties {
                    "schemas.proposed" "ingest, core, org, semantic, analytics, workflow, reporting, document, decision, agent, audit"
                    "security" "RLS, FORCE ROW LEVEL SECURITY, non-owner runtime roles, no BYPASSRLS"
                    "runtime.roles.proposed" "Separate least-privilege roles for ingestion, analytics, application API, restricted agent job data, and audit reads; final role names are open"
                    "migration.owner" "migration_owner; never used at runtime"
                }
            }

            fileArchive = container "Protected File Archive" "Stores original source and upload bytes with hashes and manifests. It is not a query database." "Protected mounted filesystem or compatible object storage" "Storage" {
                url "{workspace}/documentation/DIDRAH#protected-file-archive"
            }

            agentRuntime = container "Agent Runtime" "Claims durable Agent Jobs from PostgreSQL and runs bounded graphs. Wake-ups are hints only. DDD contexts: Job Execution, Bounded Reasoning, Model Access, Conversation (docs/16-domain-model.md)." "Python 3.12, LangGraph, Pydantic" "AI" {
                properties {
                    "ddd.contexts" "Job Execution, Bounded Reasoning, Model Access, Conversation"
                    "ddd.aggregates" "AgentJobExecution, Checkpoint, ReasoningSession, Candidate, ModelReservation, ModelCallReceipt, ConversationTurn"
                    "ddd.domain_services" "JobClaimingService, GraphSelectionService, BudgetSettlementService, RetryPolicyService, CandidateValidationService"
                    "ddd.ports" "IAgentJobRepository, ICheckpointStore, IModelPort, IEvidencePort, IBudgetLedger, IClockPort"
                    "model.timeout_seconds" "30"
                    "model.max_retries" "2 (bounded exponential backoff)"
                    "model.temperature" "0"
                    "model.fallback" "Report with correct numbers and no LLM narrative on provider failure"
                }
                agentOrchestrator = component "Bounded Agent Orchestrator" "Coordinates one bounded report, interactive, or document decision-card graph. Produces structured candidates only." "LangGraph runtime" "AI" {
                    url "{workspace}/documentation/DIDRAH#bounded-agent-orchestrator"
                }
                agentJobRunner = component "Agent Job Runner" "Claims leased jobs, runs the bounded graph, and persists a candidate or terminal failure." "PostgreSQL-backed unified agent job runner" "AI" {
                    url "{workspace}/documentation/DIDRAH#agent-job-runner"
                }
                conversationService = component "Conversation Service" "Stores manager-scoped conversation sessions and validated turns, returns bounded history window." "Deterministic conversation module" "AI" {
                    url "{workspace}/documentation/DIDRAH#conversation-service"
                }
                agentModelGateway = component "Model Gateway" "Applies token, time (30s), retry (max 2), and cost limits to every model call. Reserves and settles the single $5/30-day budget using provider official rates; temperature 0; on failure returns no-narrative deterministic report. Only external endpoint in the graded run." "Provider-neutral model client" "AI" {
                    url "{workspace}/documentation/DIDRAH#model-gateway"
                }
                checkpointStore = component "PostgreSQL Checkpoint Store" "Stores LangGraph checkpoints in PostgreSQL for resumability and idempotency." "PostgreSQL-backed checkpoint" "AI" {
                    url "{workspace}/documentation/DIDRAH#postgresql-checkpoint-store"
                }
            }

            otelCollector = container "OpenTelemetry Collector" "Exports optional redacted OTLP data to Langfuse. Product workflows remain fail-open." "OpenTelemetry Collector, optional Compose service" "Observability"
        }

        // Scenario-only elements. These mirrors keep numbered cross-container flows
        // explicit without changing the reusable C4 component relationships.
        reportScenarioReplay = element "Replay Command" "Scheduler and Replay Runner" "Resolves clock and profile, then starts one reporting day." "ScenarioStep,ScenarioScheduler"
        reportScenarioRunStatus = element "Run Status Client" "Scheduler and Replay Runner" "Starts and monitors the run through the Backend Run Coordinator." "ScenarioStep,ScenarioScheduler"
        reportScenarioRunCoordinator = element "Run Coordinator" "Backend API" "Creates the pinned plan, monitors terminal jobs, and closes the run." "ScenarioStep,ScenarioBackend"
        reportScenarioPostgres = element "PostgreSQL" "Job and report store" "Stores jobs, pinned inputs, reports, run status, and receipts." "ScenarioStep,ScenarioDatabase"
        reportScenarioRunStage = element "Run Stage Coordinator" "Background Worker" "Claims Ready jobs and invokes stages from stored dependencies." "ScenarioStep,ScenarioWorker"
        reportScenarioIngestion = element "Ingestion Coordinator" "Background Worker" "Runs source parsing and data-quality checks through Source Adapters and Data Quality Service." "ScenarioStep,ScenarioWorker"
        reportScenarioSnapshot = element "Snapshot Service" "Background Worker" "Creates the pinned Snapshot and requests reproducible projections from Projection Service." "ScenarioStep,ScenarioWorker"
        reportScenarioKpi = element "KPI Calculator" "Background Worker" "Calculates approved KPIs using definitions from Semantic Registry." "ScenarioStep,ScenarioWorker"
        reportScenarioWorkflow = element "Workflow Engine" "Background Worker" "Reconstructs WF1-WF3 and calculates stage, SLA, backlog, and bottleneck observations." "ScenarioStep,ScenarioWorker"
        reportScenarioSignal = element "Signal Engine" "Background Worker" "Detects, groups, ranks, suppresses, and escalates deterministic signals." "ScenarioStep,ScenarioWorker"
        reportScenarioEvidenceBuilder = element "Report Evidence Builder" "Background Worker" "Stores a pinned evidence package and canonical report without a model call." "ScenarioStep,ScenarioWorker"
        reportScenarioAgentRunner = element "Agent Job Runner" "Agent Runtime" "Claims leased jobs and persists a candidate or failure before validation." "ScenarioStep,ScenarioAgent"
        reportScenarioAuthorization = element "Authorization Service" "Backend API" "Revalidates the pinned manager scope for the agent job." "ScenarioStep,ScenarioBackend"
        reportScenarioAgent = element "Bounded Agent Orchestrator" "Agent Runtime" "Runs the bounded report narrative graph and returns a candidate only." "ScenarioStep,ScenarioAgent"
        reportScenarioModel = element "Model Gateway" "Agent Runtime" "Applies shared budget and model limits and returns a completion or explicit failure." "ScenarioStep,ScenarioAgent"
        reportScenarioValidator = element "Output Validator" "Backend API" "Validates the report, evidence, scope, schema, and response rules." "ScenarioStep,ScenarioBackend"
        reportScenarioPublisher = element "Publisher" "Backend API" "Publishes a validated report or authorized fallback and records a receipt." "ScenarioStep,ScenarioBackend"
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
        chatDecisionManager = element "A - Manager" "Scenario A - decision in manager chat" "Submits a request and confirms, edits, or rejects the validated card." "ScenarioStep,ScenarioActor"
        chatDecisionUi = element "A - Conversational Assistant UI" "Web Application" "Submits requests, shows the job ID, and polls for a validated card." "ScenarioStep,ScenarioWeb"
        chatDecisionIdentity = element "A - Identity Boundary" "Backend API" "Validates the manager session and creates trusted identity context." "ScenarioStep,ScenarioChat"
        chatDecisionAuthorization = element "A - Authorization Service" "Backend API" "Builds and rechecks the permitted data and policy scope." "ScenarioStep,ScenarioChat"
        chatDecisionRouter = element "A - Manager Request Router" "Backend API" "Routes authorized chat, status, and review requests to fixed handlers." "ScenarioStep,ScenarioChat"
        chatDecisionGateway = element "A - Agent Runtime Gateway" "Backend API" "Creates an interactive job and sends a best-effort job-ID wake-up." "ScenarioStep,ScenarioChat"
        chatDecisionAgentRunner = element "A - Agent Job Runner" "Agent Runtime" "Claims leased jobs, runs the graph, and persists a candidate or failure." "ScenarioStep,ScenarioAgent"
        chatDecisionStatus = element "A - Agent Job Status API" "Backend API" "Returns authorized job status and persisted result references." "ScenarioStep,ScenarioChat"
        chatDecisionConversation = element "A - Conversation Service" "Agent Runtime" "Stores manager-scoped turns and supplies bounded history; conversation text is not business evidence." "ScenarioStep,ScenarioAgent"
        chatDecisionEvidence = element "A - Evidence Service" "Backend API" "Builds a traceable Evidence Bundle inside the trusted scope." "ScenarioStep,ScenarioChat"
        chatDecisionQuery = element "A - Query Gateway" "Backend API" "Runs registered tools and scoped read-only SQL with limits and audit." "ScenarioStep,ScenarioChat"
        chatDecisionSqlGuard = element "A - SQL AST Guard" "Backend API" "Allows one approved SELECT statement and rejects unsafe SQL." "ScenarioStep,ScenarioChat"
        chatDecisionAgent = element "A - Bounded Agent Orchestrator" "Agent Runtime" "Produces a structured interactive decision-card candidate; it cannot confirm or execute it." "ScenarioStep,ScenarioAgent"
        chatDecisionModel = element "A - Model Gateway" "Agent Runtime" "Applies token, time, retry, and cost limits to bounded analysis and drafting." "ScenarioStep,ScenarioAgent"
        chatDecisionValidator = element "A - Output Validator" "Backend API" "Checks decision-card contract, cited values, evidence, scope, and response rules." "ScenarioStep,ScenarioChat"
        chatDecisionConfirmation = element "A - Decision Confirmation Service" "Backend API" "Stores the validated card and accepts only an authenticated manager review command." "ScenarioStep,ScenarioChat"
        chatDecisionTracker = element "A - Decision and Follow-Up" "Backend API" "Records a confirmed human decision and follow-up contract without executing the decision." "ScenarioStep,ScenarioChat"
        chatDecisionPostgres = element "A - PostgreSQL" "Scenario A state" "Stores jobs, pinned scope, conversations, outcomes, reviews, and decisions." "ScenarioStep,ScenarioDatabase"

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

        minutesUploadManager = element "B - Manager" "Scenario B - meeting-minutes upload" "Uploads meeting minutes and reviews the validated decision card." "ScenarioStep,ScenarioActor"
        minutesUploadUi = element "B - Conversational Assistant UI" "Web Application" "Submits the upload, polls job status, and presents the validated card." "ScenarioStep,ScenarioWeb"
        minutesUploadIdentity = element "B - Identity Boundary" "Backend API" "Validates the manager session and creates trusted identity context." "ScenarioStep,ScenarioDocument"
        minutesUploadAuthorization = element "B - Authorization Service" "Backend API" "Builds and rechecks the permitted data and policy scope." "ScenarioStep,ScenarioDocument"
        minutesUploadRouter = element "B - Manager Request Router" "Backend API" "Routes authorized upload, status, and review commands to fixed handlers." "ScenarioStep,ScenarioDocument"
        minutesUploadProcessing = element "B - Document Processing Runner" "Backend API" "Archives and parses the upload, then creates a durable analysis job." "ScenarioStep,ScenarioDocument"
        minutesUploadParser = element "B - Document Parser" "Backend API" "Validates the contract and treats document content only as data." "ScenarioStep,ScenarioDocument"
        minutesUploadGateway = element "B - Agent Runtime Gateway" "Backend API" "Sends a best-effort job-ID wake-up after the durable job commit." "ScenarioStep,ScenarioDocument"
        minutesUploadAgentRunner = element "B - Agent Job Runner" "Agent Runtime" "Claims analysis jobs, runs the graph, and persists a candidate or failure." "ScenarioStep,ScenarioAgent"
        minutesUploadStatus = element "B - Agent Job Status API" "Backend API" "Returns authorized job status and persisted document results." "ScenarioStep,ScenarioDocument"
        minutesUploadAgent = element "B - Bounded Agent Orchestrator" "Agent Runtime" "Produces a structured document decision-card candidate without confirming or executing it." "ScenarioStep,ScenarioAgent"
        minutesUploadModel = element "B - Model Gateway" "Agent Runtime" "Applies token, time, retry, and cost limits to bounded document analysis and drafting." "ScenarioStep,ScenarioAgent"
        minutesUploadValidator = element "B - Output Validator" "Backend API" "Checks the decision-card contract, document evidence references, scope, and response rules." "ScenarioStep,ScenarioDocument"
        minutesUploadConfirmation = element "B - Decision Confirmation Service" "Backend API" "Stores the validated card and accepts only an authenticated manager review command." "ScenarioStep,ScenarioDocument"
        minutesUploadTracker = element "B - Decision and Follow-Up" "Backend API" "Records a confirmed human decision and its follow-up contract without executing the decision." "ScenarioStep,ScenarioDocument"
        minutesUploadArchive = element "B - Protected File Archive" "Protected storage" "Stores original upload bytes with their hash and manifest." "ScenarioStep,ScenarioStorage"
        minutesUploadPostgres = element "B - PostgreSQL" "Scenario B state" "Stores fragments, receipts, jobs, pinned scope, outcomes, reviews, and decisions." "ScenarioStep,ScenarioDatabase"

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
        dataQualityService -> signalEngine "Publish signals created by late-arrival recomputation (same morning)" "In-process domain event"
        dataQualityService -> projectionService "Trigger corrected snapshot rebuild on late arrival" "In-process domain event"
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
        decisionEffectEvaluator -> signalEngine "Emit guardrail-breach signal" "In-process domain event"

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
            // Single-image evaluation profile per ADR-0021. One docker build and one docker run.
            // Logical C4 containers are unchanged; they run as separate processes inside one image.
            // The Web Application is served by the Compose development profile, not the graded run.
            deploymentNode "Evaluation Host" "Reference host: four CPU cores, sixteen GB RAM, no GPU, read-only /data and writable /submission. Network egress: LLM API only (ADR-0027). Max 5 minutes per processing day; container runs twice with identical numbers and signals (ADR-0026)." "Linux host" {
                deploymentNode "team_x Evaluation Image" "One image built with docker build and started with one docker run. The batch entrypoint orchestrates all product processes; no Compose or second container is required." "Docker image" {
                    deploymentNode "Backend API" "API and deterministic validation process" "Process" {
                        containerInstance backendApi
                    }
                    deploymentNode "Background Worker" "Deterministic processing process" "Process" {
                        containerInstance worker
                    }
                    deploymentNode "Scheduler" "Replay and acceptance process" "Process" {
                        containerInstance schedulerReplay
                    }
                    deploymentNode "Agent Runtime" "Bounded agent graph process" "Process" {
                        containerInstance agentRuntime
                    }
                    deploymentNode "PostgreSQL" "Local product database process; data directory created fresh at run time" "Process" {
                        containerInstance postgres
                    }
                    deploymentNode "OpenTelemetry Collector" "Loopback-only, fail-open telemetry relay. Langfuse export disabled in Evaluation (ADR-0027)." "Process" {
                        containerInstance otelCollector
                    }
                }
                deploymentNode "Mounted Filesystems" "Read-only input, protected archive, and writable evaluator output mounts" "Docker volumes or compatible mounted storage" {
                    softwareSystemInstance inputDataset
                    containerInstance fileArchive
                    softwareSystemInstance submissionOutput
                }
            }
            deploymentNode "External Observability Egress" "Disabled in the graded Evaluation profile (closed network); development-only Langfuse endpoint" "External service" {
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

        deployment didrah "Evaluation" D1_EvaluationCompose "Evaluation deployment: one team_x image started with one docker run; logical product containers run as separate processes inside the image. Per ADR-0021." {
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
                width 320
                height 190
            }
            element "ScenarioStep" {
                shape RoundedBox
                color #ffffff
                fontSize 18
                width 300
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
