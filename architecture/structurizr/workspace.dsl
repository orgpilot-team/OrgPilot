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
        nightlySources = softwareSystem "Simulated Nightly Sources" "Supplies CSV and JSON drops, manifests, organization data, configuration, and history." "External,Source"
        managerInputFeed = softwareSystem "Manager Input Feed" "Supplies scripted questions, priorities, threshold changes, uploads, decisions, and organization changes." "External,Source"
        identityProvider = softwareSystem "Identity Provider" "Authenticates users and supplies a trusted identity. The product or internal method is open." "External,Identity,OpenDecision"
        llmProvider = softwareSystem "Language Model Provider" "Returns bounded language-model completions. The provider and model are open decisions." "External,AI,OpenDecision"
        hiddenDataset = softwareSystem "Hidden Evaluation Dataset" "Uses the same data contract with different events and dates." "External,Evaluation"

        didrah = softwareSystem "DIDRAH" "A bounded agentic management assistant. It computes deterministic metrics and supports human decisions." "Target" {
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

            backendApi = container "Backend API" "Authenticates requests and serves reports, queries, manager inputs, and decisions." "Application runtime; framework open" "API" {
                identityBoundary = component "Identity Boundary" "Validates the session and builds a trusted AuthContext. It does not trust manager_id from the client or model." "Deterministic module" "Security"
                authorizationService = component "Authorization Service" "Builds row, column, role, purpose, and policy scope from trusted identity and versioned grants." "Deterministic module" "Security"
                managerInputService = component "Manager Input Service" "Receives questions, priorities, configuration changes, uploads, decisions, and organization changes." "Deterministic module" "API"
                configurationService = component "Configuration Service" "Versions goals, targets, thresholds, escalation rules, KPI candidates, organization, and access grants." "Deterministic module" "Governance"
                queryGateway = component "Query Gateway" "Executes registered tools and constrained read-only SQL with RLS, timeout, row limits, and audit." "Deterministic query execution" "Security,Query"
                sqlGuard = component "SQL AST Guard" "Allows one SELECT statement over approved relations, columns, joins, and functions. It rejects DDL, DML, SET, COPY, and unsafe calls." "SQL parser and policy" "Security,Query"
                reportApi = component "Report and Dashboard API" "Reads published reports, dashboard data, workflow observations, and explicit failure states with a fresh access check." "Deterministic module" "API"
                decisionTracker = component "Decision and Follow-Up" "Records human decisions, delegation, closure, deadlines, action drafts, and later observations. It executes no action." "Deterministic module" "Decision"
                agentOrchestrator = component "Bounded Agent Orchestrator" "Runs one bounded agent through the report graph and interactive graph. It cannot create numbers, grants, signals, or actions." "LangGraph runtime" "AI"
                evidenceService = component "Evidence Service" "Builds authorized and traceable evidence bundles before any model call." "Deterministic module" "Security,Analysis"
                modelGateway = component "Model Gateway" "Applies token, time, retry, and daily cost limits. It is the only path to the LLM Provider." "Provider-neutral model client" "AI"
                outputValidator = component "Output Validator" "Checks numbers, query references, evidence, access, JSON schema, tone, recurrence, and report content." "Deterministic validator" "Governance"
                auditService = component "Audit Service" "Records query, model, access, validation, publication, cost, and failure evidence with restricted visibility." "Deterministic module" "Governance"
            }

            worker = container "Background Worker" "Runs deterministic ingestion, snapshots, KPI calculation, workflow projection, signals, report jobs, and evaluation." "Application runtime; shared modular codebase" "Worker" {
                ingestionCoordinator = component "Ingestion Coordinator" "Checks manifests, hashes, idempotency keys, source status, and atomic batch commits." "Deterministic module" "Processing"
                sourceAdapters = component "Source Adapters" "Parse versioned source schemas and preserve the source bytes and headers." "Deterministic adapters" "Processing"
                dataQualityService = component "Data Quality Service" "Records missing sources, late arrivals, duplicates, corrections, schema changes, and quarantine results." "Deterministic module" "DataQuality"
                snapshotService = component "Snapshot Service" "Pins committed data, organization, access policy, and configuration versions for a run." "Deterministic module" "Processing"
                projectionService = component "Projection Service" "Builds reproducible facts and process projections from committed source events." "Deterministic module" "Processing"
                semanticRegistry = component "Semantic Registry" "Versions KPI definitions, PostgreSQL SQL, units, precision, targets, ownership, and dependencies." "Deterministic registry" "Analytics"
                kpiCalculator = component "KPI Calculator" "Executes the 55 approved PostgreSQL KPI queries and records QueryRun and lineage." "PostgreSQL SQL" "Analytics"
                workflowEngine = component "Workflow Engine" "Reconstructs three workflows and calculates stage timing, SLA, backlog, and bottlenecks." "Deterministic process analysis" "Analytics"
                signalEngine = component "Signal Engine" "Applies R1-R8, ownership, grouping, ranking, suppression, and escalation without LLM." "Deterministic rules" "Analytics"
                reportJobCoordinator = component "Report Job Coordinator" "Creates one job per active manager and requests a bounded report graph with pinned context." "Deterministic orchestration" "Processing"
                publisher = component "Publisher" "Atomically publishes valid text and JSON per manager. It records independent failures and daily coverage." "Deterministic module" "Processing"
                evaluationService = component "Evaluation Service" "Checks coverage, KPI parity, detection, leakage, time, cost, replay, and output contracts." "Deterministic test harness" "Evaluation"
            }

            schedulerReplay = container "Scheduler and Replay Runner" "Owns the simulated clock, run lease, replay range, evaluation profile, and resumable job dispatch." "Application command/process" "Scheduler"

            postgres = container "PostgreSQL" "The only product database. It stores product state, analytical results, access policy, checkpoints, and audit records." "PostgreSQL" "Database" {
                properties {
                    "schemas.proposed" "ingest, core, org, semantic, analytics, workflow, reporting, decision, agent, audit"
                    "security" "RLS, FORCE ROW LEVEL SECURITY, non-owner runtime roles, no BYPASSRLS"
                    "runtime.roles.proposed" "ingestion_writer, analytics_worker, application_api, agent_query_reader, audit_reader"
                    "migration.owner" "migration_owner; never used at runtime"
                }
            }

            fileArchive = container "Protected File Archive" "Stores original source and upload bytes with hashes and manifests. It is not a query database." "Protected volume or object storage" "Storage"
        }

        // System-level relationships
        seniorManager -> didrah "Reads executive reports and records human decisions"
        unitManager -> didrah "Reads unit reports and records human decisions"
        teamSupervisor -> didrah "Reads team reports and records human decisions"
        evaluator -> didrah "Runs replay and acceptance checks"
        operator -> didrah "Monitors operations and recovery evidence"
        nightlySources -> didrah "Supplies read-only nightly deliveries"
        managerInputFeed -> didrah "Submits scripted manager inputs"
        didrah -> identityProvider "Validates user identities with"
        didrah -> llmProvider "Requests bounded model completions"
        hiddenDataset -> didrah "Supplies hidden evaluation data"

        // Container-level relationships
        seniorManager -> webApp "Reads organization health, cross-unit workflows, escalations, and decisions" "HTTPS"
        unitManager -> webApp "Reads authorized unit and team results and records decisions" "HTTPS"
        teamSupervisor -> webApp "Reads authorized team results and direct-member workload" "HTTPS"
        evaluator -> schedulerReplay "Starts replay and checks outputs" "CLI or API"
        evaluator -> backendApi "Reads acceptance evidence and exported outputs" "HTTPS/JSON"
        operator -> backendApi "Reads authorized operational status" "HTTPS"
        nightlySources -> worker "Supplies eligible CSV and JSON drops" "File delivery"
        hiddenDataset -> worker "Supplies hidden drops with the same contract" "File delivery"
        managerInputFeed -> backendApi "Submits scripted inputs" "HTTPS or input adapter"
        backendApi -> identityProvider "Validates sessions and trusted identities" "OIDC or internal method; open"
        webApp -> backendApi "Requests reports, scoped queries, uploads, configuration changes, and decisions" "HTTPS/JSON"
        schedulerReplay -> worker "Dispatches deterministic run stages with a pinned clock" "PostgreSQL-backed jobs"
        schedulerReplay -> backendApi "Requests manager report and QA jobs" "Internal authenticated API"
        schedulerReplay -> postgres "Claims run leases and records run state" "TLS/PostgreSQL"
        worker -> backendApi "Requests bounded report graphs and records job outcomes" "Internal authenticated API"
        worker -> agentOrchestrator "Starts one bounded report graph for each manager job" "Internal authenticated call"
        backendApi -> worker "Queues approved structured uploads and configuration validation" "PostgreSQL-backed jobs"
        backendApi -> postgres "Reads and writes scoped application state" "TLS/PostgreSQL"
        worker -> postgres "Reads snapshots and writes deterministic results" "TLS/PostgreSQL"
        worker -> fileArchive "Archives and reads approved source bytes" "Restricted file API"
        backendApi -> fileArchive "Archives uploads and reads approved fragments" "Restricted file API"
        backendApi -> llmProvider "Calls only through Model Gateway" "Model API"

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

        // API component relationships
        webApp -> identityBoundary "Submits session credentials"
        managerInputFeed -> identityBoundary "Submits an evaluator-authenticated identity"
        identityBoundary -> identityProvider "Validates identity when an external provider is selected"
        identityBoundary -> authorizationService "Creates trusted AuthContext"
        authorizationService -> postgres "Reads versioned hierarchy, grants, purpose, and policy"
        webApp -> managerInputService "Submits questions, uploads, settings, and decisions"
        managerInputService -> configurationService "Submits authorized configuration candidates"
        managerInputService -> decisionTracker "Submits explicit human decisions and status changes"
        managerInputService -> agentOrchestrator "Starts an authorized interactive graph"
        managerInputService -> fileArchive "Preserves original upload bytes"
        managerInputService -> worker "Queues approved structured uploads"
        configurationService -> authorizationService "Checks actor authority and affected scope"
        configurationService -> postgres "Versions candidates, approvals, activation, and rollback"
        configurationService -> worker "Requests deterministic validation before activation"
        reportApi -> authorizationService "Rechecks current audience and purpose"
        reportApi -> queryGateway "Requests registered dashboard and workflow queries"
        reportApi -> postgres "Reads immutable report versions and failure states"
        reportApi -> webApp "Returns authorized reports, answers, and explicit failure states"
        decisionTracker -> authorizationService "Checks human decision authority"
        decisionTracker -> postgres "Appends decision, draft, deadline, status, and follow-up events"
        decisionTracker -> agentOrchestrator "Requests a task or message draft after a recorded decision"
        agentOrchestrator -> evidenceService "Requests an authorized EvidenceBundle"
        agentOrchestrator -> queryGateway "Requests tools or proposes constrained custom SQL"
        agentOrchestrator -> modelGateway "Requests bounded analysis or Persian drafting"
        agentOrchestrator -> outputValidator "Submits report or interactive answer drafts"
        evidenceService -> authorizationService "Checks rows, columns, purpose, and evidence audience"
        evidenceService -> queryGateway "Runs registered evidence queries"
        evidenceService -> postgres "Reads authorized KPI, workflow, calendar, and decision references"
        evidenceService -> fileArchive "Reads only approved document fragments"
        queryGateway -> authorizationService "Gets trusted scope and allowlists"
        queryGateway -> sqlGuard "Validates candidate SQL AST"
        sqlGuard -> queryGateway "Returns an approved statement or refusal"
        queryGateway -> postgres "Runs a read-only transaction with RLS, timeout, and limits"
        queryGateway -> auditService "Records SQL, parameters, scope, snapshot, rows, hash, and refusal"
        modelGateway -> postgres "Reserves and settles the shared daily cost budget"
        modelGateway -> llmProvider "Sends only authorized evidence and receives completion" "Model API"
        modelGateway -> auditService "Records model, prompt, tokens, latency, retry, and cost"
        modelGateway -> agentOrchestrator "Returns a completion or an explicit terminal failure"
        outputValidator -> queryGateway "Rechecks every reported number and query reference"
        outputValidator -> authorizationService "Rechecks recipient scope and individual-data limits"
        outputValidator -> evidenceService "Checks evidence groups, alternatives, and provenance"
        outputValidator -> postgres "Stores validation receipts and exact failure reasons"
        outputValidator -> publisher "Submits only a validated manager package"
        auditService -> postgres "Stores restricted audit, cost, and operational evidence"

        // Worker component relationships
        schedulerReplay -> ingestionCoordinator "Starts idempotent intake for the selected cutoff"
        ingestionCoordinator -> nightlySources "Reads expected files and manifests"
        ingestionCoordinator -> hiddenDataset "Reads hidden files through the same adapters"
        ingestionCoordinator -> sourceAdapters "Parses each source contract"
        sourceAdapters -> fileArchive "Preserves original bytes, headers, and hashes"
        sourceAdapters -> dataQualityService "Submits parsed and rejected rows"
        dataQualityService -> postgres "Writes accepted records, quarantine, and DataIssues"
        schedulerReplay -> snapshotService "Requests a pinned snapshot"
        snapshotService -> postgres "Pins committed batches, org, policy, and configuration versions"
        snapshotService -> projectionService "Requests reproducible facts and process projections"
        projectionService -> postgres "Reads events and writes facts and projections"
        schedulerReplay -> kpiCalculator "Requests all approved KPI definitions"
        kpiCalculator -> semanticRegistry "Reads approved PostgreSQL SQL and metadata"
        semanticRegistry -> postgres "Reads versioned KPI definitions and dependencies"
        kpiCalculator -> postgres "Executes KPI SQL and writes observations, QueryRun, and lineage"
        schedulerReplay -> workflowEngine "Requests WF1-WF3 projection for the snapshot"
        workflowEngine -> postgres "Reads events and writes case, stage, SLA, and bottleneck observations"
        schedulerReplay -> signalEngine "Requests signal detection and ranking"
        signalEngine -> postgres "Reads KPI and history; writes episodes, ownership, suppression, and escalation"
        schedulerReplay -> reportJobCoordinator "Creates one job per active manager"
        reportJobCoordinator -> backendApi "Requests one bounded report graph per manager"
        reportJobCoordinator -> postgres "Writes job lease, attempt, outcome, and daily coverage"
        publisher -> postgres "Atomically commits text, JSON, publication receipt, or explicit failure"
        publisher -> evaluationService "Reports package and export outcome"
        evaluationService -> postgres "Reads run evidence and writes acceptance results"
        evaluationService -> schedulerReplay "Returns complete or partial run status"

        // Deployment model for the one-command evaluation target.
        deploymentEnvironment "Evaluation" {
            deploymentNode "Reference Host" "Evaluator-provided Docker host." "Docker Compose" "DeploymentNode" {
                webNode = deploymentNode "Web Container" "Serves the Persian RTL web application." "Container" "DeploymentNode,WebNode" {
                    containerInstance webApp
                }
                apiNode = deploymentNode "API Container" "Runs Backend API and the bounded interactive/report agent runtime." "Container" "DeploymentNode,ApiNode" {
                    containerInstance backendApi
                }
                workerNode = deploymentNode "Worker Container" "Runs deterministic background processing." "Container" "DeploymentNode,WorkerNode" {
                    containerInstance worker
                }
                schedulerNode = deploymentNode "Scheduler Container or Command" "Runs the simulated clock and replay command." "Container" "DeploymentNode,SchedulerNode" {
                    containerInstance schedulerReplay
                }
                dataNode = deploymentNode "PostgreSQL Container" "Runs the only product database with persistent storage." "Container" "DeploymentNode,DataNode" {
                    containerInstance postgres
                }
                archiveNode = deploymentNode "Archive Volume" "Stores protected original files and manifests." "Persistent volume" "DeploymentNode,StorageNode" {
                    containerInstance fileArchive
                }
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
            include seniorManager unitManager teamSupervisor didrah nightlySources identityProvider llmProvider
            autoLayout tb
            default
        }

        // C4 core view: deployable applications and data stores inside the DIDRAH boundary.
        container didrah L2_Containers "C4 container view of the DIDRAH applications, data stores, users, and external dependencies." {
            title "02 - C4 Level 2 - Containers for DIDRAH"
            include seniorManager unitManager teamSupervisor nightlySources identityProvider llmProvider webApp backendApi worker schedulerReplay postgres fileArchive
            autoLayout tb
        }

        // C4 Level 3: each view opens one container and shows all of its components.
        component backendApi L3_1_BackendApiComponents "Complete C4 component view of Backend API access control, manager operations, secure queries, agent orchestration, validation, reports, decisions, and audit." {
            title "03.1 - C4 Level 3 - Backend API Components"
            include webApp worker managerInputFeed identityProvider llmProvider postgres fileArchive identityBoundary authorizationService managerInputService configurationService queryGateway sqlGuard reportApi decisionTracker agentOrchestrator evidenceService modelGateway outputValidator auditService
            
        }

        component worker L3_2_BackgroundWorkerComponents "Complete C4 component view of Background Worker intake, data quality, snapshots, deterministic analytics, report jobs, publication, and evaluation." {
            title "03.2 - C4 Level 3 - Background Worker Components"
            include nightlySources hiddenDataset schedulerReplay backendApi postgres fileArchive ingestionCoordinator sourceAdapters dataQualityService snapshotService projectionService semanticRegistry kpiCalculator workflowEngine signalEngine reportJobCoordinator publisher evaluationService
            
        }

        // C4 supporting views: numbered runtime interactions for complex or recurring behavior.
        dynamic didrah S1_NightlyReporting "Previous-day intake through independent validated manager packages." {
            title "04.1 - Supporting Dynamic - Nightly Reporting"
            schedulerReplay -> postgres "Claim run lease and pin the evaluation profile"
            schedulerReplay -> worker "Start previous-day intake and deterministic analytics"
            nightlySources -> worker "Supply eligible deliveries"
            worker -> fileArchive "Preserve original bytes and manifests"
            worker -> postgres "Commit data and freeze Snapshot"
            worker -> postgres "Compute 55 key performance indicators, three workflows, and signal episodes"
            schedulerReplay -> backendApi "Request bounded report jobs for active managers"
            backendApi -> llmProvider "Analyze authorized evidence and draft Persian content"
            backendApi -> postgres "Store validation receipts and report outcomes"
            worker -> postgres "Atomically publish valid packages and record failures"
            schedulerReplay -> postgres "Record coverage, time, cost, and final run state"
            autoLayout tb
        }

        dynamic backendApi S2_InteractiveQuery "A manager question becomes a constrained SQL query, a row-filtered result, and a checked answer." {
            title "04.2 - Supporting Dynamic - Interactive Query"
            teamSupervisor -> webApp "Ask a scoped question"
            webApp -> identityBoundary "Submit session and question"
            identityBoundary -> identityProvider "Validate identity"
            identityBoundary -> authorizationService "Build trusted AuthContext"
            managerInputService -> agentOrchestrator "Start interactive graph with pinned Snapshot"
            agentOrchestrator -> evidenceService "Read permitted context"
            agentOrchestrator -> queryGateway "Propose candidate SQL and QuerySpec"
            queryGateway -> sqlGuard "Parse and validate one SELECT statement"
            queryGateway -> postgres "Execute read-only SQL with forced row-level security and limits"
            queryGateway -> auditService "Record actual SQL, scope, Snapshot, and result hash"
            agentOrchestrator -> modelGateway "Draft answer from executed results only"
            modelGateway -> llmProvider "Request bounded completion"
            agentOrchestrator -> outputValidator "Check numbers, evidence, scope, and answer-quality schema"
            outputValidator -> queryGateway "Recheck referenced numbers"
            reportApi -> webApp "Return checked Persian answer, query identifier, and permitted SQL"
            autoLayout tb
        }

        dynamic backendApi S3_HumanDecision "The system proposes. A human decides and authorizes any external action." {
            title "04.3 - Supporting Dynamic - Human Decision"
            unitManager -> webApp "Read decision card and evidence"
            webApp -> identityBoundary "Submit explicit decision"
            identityBoundary -> authorizationService "Build trusted actor and decision scope"
            managerInputService -> decisionTracker "Record select, delegate, close, or escalate"
            decisionTracker -> postgres "Append decision, owner, deadline, and success criteria"
            decisionTracker -> agentOrchestrator "Request task or message draft only"
            agentOrchestrator -> modelGateway "Draft without sending"
            modelGateway -> llmProvider "Request bounded draft"
            decisionTracker -> postgres "Store draft linked to the human decision"
            unitManager -> webApp "Review and send outside DIDRAH"
            schedulerReplay -> worker "On later days, measure observations against success criteria"
            worker -> postgres "Append supported follow-up result and limitations"
            autoLayout tb
        }

        dynamic didrah S4_ReplayRecovery "Replay uses the production path and resumes from durable stage outcomes." {
            title "04.4 - Supporting Dynamic - Replay and Recovery"
            evaluator -> schedulerReplay "Start mornings 62-91 with an EvaluationProfile"
            schedulerReplay -> postgres "Claim replay namespace, run lease, and pinned versions"
            hiddenDataset -> worker "Supply hidden drops through normal adapters"
            schedulerReplay -> worker "Run the same intake, KPI, workflow, and signal stages"
            worker -> postgres "Record stage outcomes and checkpoints"
            schedulerReplay -> backendApi "Run reports and scripted questions"
            backendApi -> postgres "Record packages, answer quality, query, model, and validation evidence"
            schedulerReplay -> postgres "Resume failed stages with the same idempotency keys"
            evaluator -> backendApi "Read acceptance report and explicit partial failures"
            autoLayout tb
        }

        dynamic backendApi S5_IndependentPublication "One manager can fail while another valid package is published. Daily coverage remains incomplete." {
            title "04.5 - Supporting Dynamic - Independent Publication"
            worker -> agentOrchestrator "Start manager A and manager B report graphs"
            agentOrchestrator -> modelGateway "Request manager A language draft"
            modelGateway -> llmProvider "Call provider within retry and cost limits"
            modelGateway -> agentOrchestrator "Return final failure for manager A"
            auditService -> postgres "Record A failure without a fabricated draft"
            worker -> postgres "Keep daily run incomplete and continue manager B"
            agentOrchestrator -> outputValidator "Submit manager B draft"
            outputValidator -> queryGateway "Verify every number and query reference"
            outputValidator -> authorizationService "Verify B recipient scope"
            worker -> postgres "Atomically publish B text and JSON if valid"
            reportApi -> webApp "Return A failure state or B valid package by scope"
            autoLayout tb
        }

        // C4 supporting view: container instances mapped to one deployment environment.
        deployment * "Evaluation" S6_EvaluationDeployment "C4 deployment view for one-command Docker Compose execution on the evaluator reference host." {
            title "04.6 - Supporting Deployment - Evaluation Environment"
            include *
            autoLayout lr
        }

        styles {
            element "Element" {
                shape RoundedBox
                color #ffffff
                background #334155
                fontSize 20
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
            element "DeploymentNode" {
                background #475569
            }
            element "DataNode" {
                shape Cylinder
                background #5b21b6
            }
            element "StorageNode" {
                shape Folder
                background #6d28d9
            }
            relationship "Relationship" {
                color #64748b
                routing Orthogonal
                fontSize 16
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
