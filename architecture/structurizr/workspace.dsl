workspace "ARKA Canonical Architecture" "Proposed target system. This model does not claim that the application is implemented." {
    !identifiers flat
    !impliedRelationships false

    // SOURCE AUTHORITY (paths are relative to the repository root).
    // 1. Project-owner decisions in the architecture task, 2026-11-09.
    // 2. Project_berif/ DIDRAH official PDF: all 19 pages, text and visual review.
    // 3. dataset/README_FA.md; config/kpi_dictionary.csv; config/reference_views.sql;
    //    config/workflow_definitions.csv; config/escalation_rules.csv; config/monthly_targets.csv;
    //    org/{units,teams,managers,staff,access_matrix}.csv; calendar/*.csv;
    //    drops/day_000..day_090/; history/*; manager_inputs/scripted_inputs.json;
    //    uploads/*; output_contract/{brief_schema,qa_answer_schema,example_brief}.json.
    // 4. docs/architecture/001-system-blueprint.md, 002-data-architecture.md,
    //    003-decisions-and-roadmap.md and visualizations/open-questions.md are proposals.
    // 5. Engineering recommendations in this model are target design choices.
    //
    // VERIFIED REPOSITORY STATE: dataset and review Python files perform exploration.
    // Documentation builders and validators check documents. Notebooks and review reports
    // are analytical artifacts. No complete application, API, worker or deployment was found.
    // Existing arka_explore.sqlite is a review artifact; it is excluded from the target system.
    // review/{rca-001,kpi-val-001,dq-001}-report.md and audit_stage6.txt describe tests.
    // They do not prove PostgreSQL parity or production acceptance. Do not ingest developer
    // documents, notebooks, audit outputs or hidden evaluation labels as operational evidence.
    // A complete official raw-column data dictionary was not found. The observed column
    // catalog is derived documentation, not an approved source contract.
    //
    // PRECEDENCE CONFLICTS:
    // The earlier SQLite calculator and dual-engine query proposals are superseded.
    // PostgreSQL is the only database engine, including KPI and custom-query execution.
    // Q identifiers below belong to THIS TASK. Other documents reuse these identifiers.
    // A separate original 17-question record was not found in the inspected repository.
    // The supplied task and existing open-decision blocks remain authoritative here.
    //
    // OPEN DECISIONS -- do not infer approval from element names or relationships.
    // Q03: Prove mathematical and numerical equivalence for all 55 PostgreSQL KPI ports.
    //      Cover types, integer division, median, date arithmetic, booleans, grouping,
    //      reference rounding, dimensions, NULL and absent SQL rows. No parity claim here.
    // Q05: Organizer approval of RAW versus exact-payload DEDUP calculation policy.
    //      Preserve every original occurrence. File retry idempotency is a separate concern.
    // Q08: Conflicting payload and same-drop correction precedence. No last-row-wins rule.
    // Q11: Exact workflow stage-to-team ownership mapping. End-to-end owner M01 is supplied.
    // Q12: Threshold equality, incomplete baseline, zero baseline, holiday handling,
    //      unknown warning days and episode reset details require explicit policy.
    // Q13: Organizational effective dates and known-at rules. M11/T_MKT start at day 75
    //      in static metadata; IN05 arrives on day 75; README says next-morning effect.
    //      Do not choose morning 75 or 76, or hard-code a final report count.
    // Q14: Internal Shared Insight Brief schema is not finalized.
    //      It is NOT output_contract/brief_schema.json.
    // Q17: Provider/model, gateway product and tracing stack are not selected.
    //      LiteLLM is a candidate only. No framework or provider is an approved dependency.
    // CONTRACT CONFLICT: brief p15 has new/escalated/suppressed; brief_schema.json has
    //      new/escalated/ongoing. Keep suppression history; do not invent an output mapping.
    //      The existing schema stays unchanged. An affected output needs explicit resolution.
    // OTHER OPEN DETAILS: source closure and unreliable-value release policy; authorized
    //      row/column projections for shared sources; capacity aggregation and inference
    //      controls; calendar known-at rules; report restatement approval/notification;
    //      retention, backup schedule and physical keys. Default-deny is not a new grant.
    //      Same-day Q09 precedes attachment IN07 in the supplied array. An array position
    //      does not establish attachment availability. Record receipt/dependency explicitly.
    // ROUNDING CONFLICT: brief p16 gives generic unit examples; several canonical SQL
    //      definitions use two decimal places. Retain canonical precision and flag any
    //      disputed comparison rule. Example brief values and dates are not test oracles.
    //
    // OFFICIAL STAGE TRACE:
    // S1 Data Integration and KPI Calculation -> ingestion, quality, snapshots, kpi.
    // S2 Signal Detection -> signals, workflows, stored recipient history.
    // S3 Manager Goals and Priorities -> managerConfig; versioned input, never a nightly wait.
    // S4 Evidence-Based Analysis -> evidence, queryGateway, agent, insights.
    // S5 Role-Based Reporting -> reportWriter and authorized Insight projections.
    // S6 Validation and Controls -> access, outputValidator, audit.
    // S7 Daily Brief Package -> publication and web interfaces.
    // S8 Human Decision and Follow-up -> decisions, human approval, later observations.
    //
    // ACCEPTANCE PROFILE: brief pp14-19. Preserve the current limits with a version.
    // 30 replay mornings: 62..91; development history days 1..60 plus initial CRM day_000.
    // Morning R sees committed drops <= R-1. At simulated 00:00 admit the previous day;
    // publish before 07:30 Asia/Tehran. Question on D sees operational drops <= D-1.
    // Validated uploads can enter a new interactive evidence revision on D immediately.
    // Manager inputs on D affect later morning reports from D+1, subject to open Q13.
    // No preload of future operational facts or future events as observed causes.
    // Ten base-manager valid reports each day remains an acceptance requirement.
    // Added active managers also need reports; roster precedence is pending.
    // Maximum five important items per report. Three workflow analyses are required.
    // At least 90% planted-event detection: correct owner and KPI/entity, plausible cause,
    // within 24 simulated hours. Hidden labels remain outside production evidence.
    // Zero unauthorized leakage. Zero wrong numbers after the specified rounding.
    // End-to-end intake through reports and JSON <=15 real minutes on reference hardware.
    // All daily LLM calls, scripted questions and retries share a total USD 5 limit.
    // Reference-question accuracy >=85% over about 60 organizer questions, including refusals.
    // The supplied 16 questions are not the full official acceptance set.
    // About 150 series, 25 signals and 8 deep analyses are estimates, not output quotas.
    // Page 19 requires organizer confirmation of numerical limits and reference hardware.
    // Docker-based, one-command, reproducible target deployment; no package is selected here.
    // Independent publication can yield partial failure. It cannot satisfy ten-valid-report
    // acceptance when a required manager has an error. Never label partial runs complete.
    //
    // DELIVERY SCOPE: Persian RTL reports/UI, report item, chart specification, decision
    // cards for escalated important issues, health overview, open actions and dashboard link.
    // Decision cards carry problem, options, supported impact/cost, risk, confidence,
    // execution owner, deadline, success criterion and evidence. No invented estimates.
    // Monthly board summary is optional at month end. Forecast, what-if, audio and messaging
    // integration are optional and are not target dependencies. No real-system connectors,
    // autonomous organizational actions, payroll, surveillance or employee ranking.

    model {
        supervisor = person "Team Supervisor" "Manages direct-team work. May see authorized individual task details for workload management only." "Human"
        unitManager = person "Unit Manager" "Reviews authorized unit and team aggregates. Decides, delegates, closes or escalates issues." "Human"
        executive = person "Senior Executive" "Reviews organization aggregates and all three cross-functional workflows. Makes executive decisions." "Human"

        sources = softwareSystem "Simulated Organizational Sources" "Supplies simulated read-only operational records, configuration and history." "External,Source" {
            properties {
                "responsibility.detail" "External source boundary for the DIDRAH dataset. CSV records, JSON manifests/configuration, organization metadata, calendar and historical business events. Read-only source access."
            }
        }
        inputDriver = softwareSystem "Scripted Manager Input Driver" "Replays authorized scripted manager inputs through application operations." "External,Source" {
            properties {
                "responsibility.detail" "Evaluation-side input boundary. Replays the 23 supplied inputs through the same authorized application operations; 16 inputs are questions. This is not an implemented live integration."
            }
        }
        providers = softwareSystem "Local or External AI Model Providers" "Serves local or external AI models. Provider and model choices remain open." "External,AI" {
            properties {
                "responsibility.detail" "Model-serving software outside the ARKA application boundary. Local inference or external APIs; exact model, provider and permitted routing are pending Q17."
            }
        }

        arka = softwareSystem "ARKA Executive Assistant" "Proposed decision intelligence for three management levels. Humans retain action authority." "Target" {
            properties {
                "responsibility.detail" "Proposed decision-intelligence application for the fictional retailer. One bounded AI Agent supports three management levels. Humans retain all organizational action authority."
            }
            web = container "Web Frontend" "Persian RTL interface. Three required user interfaces share one frontend. No browser-to-database or browser-to-model access." "Web application; framework pending" "Web" {
                chatUi = component "Conversational Assistant" "Reads morning reports, asks follow-up questions, shows charts and registered queries, accepts uploads and manager inputs." "Web interface" "Web"
                dashboardUi = component "Role-Based BI Dashboard" "Shows authorized KPI health, targets, trends, drill-downs, open actions and decision history." "Web interface" "Web"
                controlUi = component "Executive Workflow Control Room" "Senior Executive only. Shows WF1, WF2 and WF3, stage SLA, bottlenecks, escalations and pending decisions." "Web interface" "Web"
            }

            api = container "Backend API" "Serves both runtime paths. Owns the single Agent and report controls in one modular codebase." "Application runtime; framework pending" "API" {
                properties {
                    "responsibility.detail" "Modular application process. Serves both runtime paths and owns the single Agent, evidence controls, report validation and publication. Shares one codebase with the worker."
                }
                requests = component "Application API" "Routes authorized requests. Controls the total Agent execution budget, cancellation and failure state." "Deterministic module" "API" {
                    properties {
                        "responsibility.detail" "Routes authenticated manager and internal job requests with server identity, snapshot, scope and request IDs. Owns maximum tool calls, investigation steps, elapsed time, retries, cancellation and per-manager/daily execution budgets. Exact limits remain configurable and unresolved. Resolves selected shared analysis before costly work. Returns explicit answers or errors and propagates job failure to the worker."
                    }
                }
                access = component "Identity and Access Policies" "Authenticates callers and enforces row, column, role and purpose limits before evidence use." "Deterministic authorization" "Governance" {
                    properties {
                        "responsibility.detail" "Authenticates users and service callers. Builds server-side identity. Enforces role, row, column and purpose policies before evidence use. Executive control room is executive-only."
                    }
                }
                managerConfig = component "Manager Configuration" "Versions manager settings and controls registration, validation and activation of new KPI definitions." "Deterministic module" "Governance" {
                    properties {
                        "responsibility.detail" "Versions goals, priorities, targets, thresholds, escalation rules, hierarchy and grants. Checks human authority. Registers new inactive KPI candidates, requests worker validation, records approval and activates approved versions at a governed effective time. Preserves all 55 canonical formulas. Approval roles and detailed activation policy remain open. Supports organization changes without code changes."
                    }
                }
                documents = component "Document Intake and Evidence Registration" "Validates uploads. Registers document evidence or completed structured-data revisions within the authorized scope." "Deterministic document processing" "Processing" {
                    properties {
                        "responsibility.detail" "Validates upload type, size, identity, audience and content. Preserves original files. Treats Markdown and embedded instructions as untrusted data. Registers document fragments separately from structured uploads. Submits authorized CSV processing to the existing worker, checks completion/failure and registers successful interactive data revisions. Keeps uploads separate from canonical nightly sources and published report versions. No RAG assumption."
                    }
                }
                queryGateway = component "Query Gateway" "Runs approved analytical tools and validated read-only SQL with RLS, execution grants and query records." "Deterministic query execution" "Governance" {
                    properties {
                        "responsibility.detail" "Offers predefined analytical tools and constrained custom Text-to-SQL. Requires trusted server identity and an active execution grant. Validates relations, functions, SQL and limits. Uses read-only PostgreSQL roles and RLS, including approved upload-revision relations. Registers executed SQL, query_id, inputs, results, snapshot and reporting context for every published number. Has no calculation-only evidence path."
                    }
                }
                evidence = component "Evidence Service" "Retrieves authorized, traceable evidence before model use. Filters derived claims by audience." "Deterministic module" "Governance" {
                    properties {
                        "responsibility.detail" "Retrieves authorized KPI, workflow, calendar, capacity, document and decision evidence. Enforces source provenance, row/column scope and derived-claim visibility before any LLM call."
                    }
                }
                agent = component "Bounded AI Agent" "One AI Agent investigates selected evidence within controller limits. It cannot invent numbers or execute actions." "Bounded tool-using AI" "AI" {
                    properties {
                        "responsibility.detail" "The only AI Agent. Uses approved investigative tools under Application API execution grants. Drafts hypotheses, confidence, alternatives, decision options and conversational answers from authorized evidence and registered-query numbers. Checks cancellation/remaining limits and propagates failure. Has no database credentials or organizational execution tools."
                    }
                }
                insights = component "Shared Insight Brief Management" "Maintains the shared Insight source and reuses authorized analysis across role-specific reports." "Deterministic content management" "Processing" {
                    properties {
                        "responsibility.detail" "Versions one common analytical source per issue and snapshot: summary/impact, deviation, breakdown, possible causes/confidence, options, history, proposed owner and registered SQL queries. Reuses completed or in-flight authorized analysis across managers. Enforces permitted evidence audiences and role projections. Internal schema remains open under Q14."
                    }
                }
                reportWriter = component "Report Writer" "Builds Persian role reports, JSON twins, charts and decision cards from authorized shared Insights." "Deterministic report assembly" "Processing" {
                    properties {
                        "responsibility.detail" "Builds role-specific Persian reports, JSON twins, chart specifications and decision cards from authorized Shared Insight projections. Every numerical claim uses executed registered SQL. Reports affected KPIs/sources and last valid values with actual dates. Uses the same bounded Agent and parent execution grant for language drafting; does not repeat deep analysis per manager."
                    }
                }
                outputValidator = component "Output Validator" "Checks registered-query numbers, canonical units and rounding, output schemas, evidence and recipient access." "Deterministic validation" "Governance" {
                    properties {
                        "responsibility.detail" "Checks every published number against executed registered SQL, canonical KPI definition, unit-specific reference rounding and the same snapshot/evidence revision. Validates query_id, inputs, results and reporting context. Checks schemas, maximum five items, causal evidence, tone, fairness, recurrence and scope. Rejects stale-as-current values and unsupported numbers. Validates both report and interactive QA artifacts."
                    }
                }
                publication = component "Publication" "Publishes each valid package independently. Exports validated brief/QA JSON and records failed reports or exports." "Deterministic module" "Processing" {
                    properties {
                        "responsibility.detail" "Publishes individual valid manager packages and immutable versions. Serves authorized reports, dashboards and control-room data with fresh access checks. Records manager-specific failed report/export states, including failure before a draft. Generates required brief JSON at submission/briefs/day_XXX/<manager_id>.json and QA JSON at submission/qa/<input_id>.json using the supplied schemas. Export content must pass authorization and validation; no successful report is invented."
                    }
                }
                audit = component "Audit and Evaluation" "Records restricted diagnostics and evaluation evidence. Exports validated daily cost and replay results." "Deterministic audit and test runner" "Governance" {
                    properties {
                        "responsibility.detail" "Records provenance, query/result references, job and export outcomes, errors, traces, elapsed time and actual daily model token/cost usage. Owns daily cost records and replay execution/status evaluation exports. Validates query-backed totals, completeness and applicable contracts. Precise cost/status export paths and schemas are not supplied and remain open. Separates structural checks, numerical parity, source quality and official acceptance."
                    }
                }
                decisions = component "Decision and Follow-up" "Records human decisions and approved drafts. Monitors follow-up without executing actions." "Deterministic module" "Decision" {
                    properties {
                        "responsibility.detail" "Records human approvals, decisions, closure, escalation, delegation, deadlines and action status. Creates drafts only after a recorded decision. Tracks later observations and decision memory; never sends or executes actions."
                    }
                }
            }

            worker = container "Background Processing Worker" "Runs deterministic intake, analysis and replay in the same modular codebase." "Application runtime; Docker target" "Processing" {
                properties {
                    "responsibility.detail" "Deterministic scheduled/replay process in the same modular codebase. Runs intake and analytics, then requests scoped report jobs from the Backend API. No second Agent."
                }
                jobs = component "Schedule and Replay Control" "Controls replay and independent manager jobs. Records failures, cancellations and partial-run status." "Deterministic orchestration" "Processing" {
                    properties {
                        "responsibility.detail" "Uses simulated 00:00 intake and D-1 cutoff. Runs 30 replay mornings after history load. Persists leases, bounded retries, manager outcomes and partially failed run state, including failure before a draft. Reads versioned goals without waiting for human input. Dispatches deterministic selected analysis and independent report jobs. Uses only approved active KPI versions and sends audit/evaluation requests through the API."
                    }
                }
                ingestion = component "Ingestion Adapters" "Reads structured sources and isolated uploads. Preserves source bytes and delivery lineage." "Deterministic structured-data adapters" "Processing" {
                    properties {
                        "responsibility.detail" "Reads CSV operations and JSON manifests/configuration, org metadata and historical events. Checks expected/manifest/actual files. Routes operational documents separately. Preserves bytes and delivery lineage."
                    }
                }
                quality = component "Data Quality and Preprocessing" "Preserves RAW and detects duplicates, conflicts, late/missing data, corrections and schema changes." "Deterministic module" "Processing" {
                    properties {
                        "responsibility.detail" "Preserves RAW occurrences. Detects exact duplicates, conflicts, late arrivals, missing sources, corrections and schema changes. Applies only approved mappings; records issues and affected KPI dependencies. RAW/DEDUP and conflict precedence remain open."
                    }
                }
                snapshots = component "Snapshot Management" "Freezes committed input and policy versions. Preserves history without future-data leakage." "Deterministic module" "Processing" {
                    properties {
                        "responsibility.detail" "Freezes committed source versions, received cutoff, business horizon, organization/config versions and calculation policy. Rebuilds history without future leakage. Later corrections create new versions; published reports remain unchanged."
                    }
                }
                kpi = component "KPI Engine" "Computes the 55 canonical KPIs and approved additions in PostgreSQL. Validates new definition candidates." "Deterministic PostgreSQL SQL" "Analytics" {
                    properties {
                        "responsibility.detail" "Executes the unchanged 55 canonical KPI definitions with PostgreSQL-compatible SQL. Validates new inactive definitions for semantic inputs, units/rounding, authorized scope, rollups, SQL safety and deterministic execution. Returns validation receipts. Calculates only active approved versions and registers SQL, inputs, results, history and source lineage. Numerical equivalence remains open under Q03."
                    }
                }
                workflows = component "Workflow Engine" "Reconstructs WF1-WF3. Calculates stage timing, SLA and bottlenecks; stage ownership remains open." "Deterministic process analysis" "Analytics" {
                    properties {
                        "responsibility.detail" "Reconstructs WF1 Order to Delivery, WF2 Complaint to Resolution and WF3 Lead to Contract from event logs. Computes stage timing, SLA, open cases and bottleneck evidence; stage ownership is pending Q11."
                    }
                }
                signals = component "Signal Engine" "Detects, ranks and selects eligible signals deterministically before AI investigation. Applies R1-R8." "Deterministic rules and statistics" "Analytics" {
                    properties {
                        "responsibility.detail" "Detects deviations, trends and workflow problems without LLM. Applies R1-R8, ownership, suppression, history and rule-driven escalation. Ranks/selects eligible signals using deviation, supported impact, confidence, managerial priority and escalation context. Records reasons and versioned policy; exact weights/thresholds remain open. Data incidents are not business signals. Eight deep analyses is an estimate."
                    }
                }
            }

            postgres = container "PostgreSQL" "The only database engine. Stores versioned source, analytical, management, budget and audit data under restricted roles." "PostgreSQL" "Database" {
                    properties {
                        "responsibility.detail" "The ONLY database engine. Stores RAW structured payloads, history, snapshots, KPI/query results, workflow observations, signals, versioned definitions/configuration, shared Insights, immutable reports, decisions, jobs, audit and budget metadata. Separates upload-specific revisions from canonical source relations. Uses RLS and restricted roles."
                    }
                }
            rawFiles = container "Protected Raw File Storage" "Protects original source and upload files. Provides no direct manager or LLM access." "Protected file volume; product pending" "Storage" {
                properties {
                    "responsibility.detail" "Retains original CSV, JSON, Markdown and manager upload bytes with hashes, manifests and access controls. File archive only; not a second database. Managers and LLMs have no direct file access."
                }
            }
            modelGateway = container "LLM Gateway" "Routes local/external model calls. Enforces call limits and the shared daily cost budget; returns explicit failures." "Provider-neutral model API; product pending Q17" "AI" {
                    properties {
                        "responsibility.detail" "Model-agnostic runtime boundary. Controls per-call tokens, timeout, bounded provider retries, tracing and error monitoring within the parent execution grant. Reserves/settles total daily LLM cost in PostgreSQL. Propagates timeout, model API error and exhausted retry/cost budget to the Agent/controller. Does not own the full investigation budget. Product/model/tracing choice remains open under Q17; LiteLLM is only a candidate."
                    }
                }
        }

        // Relationships are defined once. Disable implicit relationships so each level is explicit.
        supervisor -> arka "Reviews team work and records human decisions"
        unitManager -> arka "Reviews unit aggregates and records human decisions"
        executive -> arka "Reviews organization health and cross-functional workflows"
        sources -> arka "Supplies simulated read-only data and operational attachments"
        inputDriver -> arka "Submits scripted authorized manager inputs"
        arka -> providers "Requests language analysis through controlled model routing"

        supervisor -> web "Uses authorized direct-team interfaces"
        unitManager -> web "Uses authorized unit interfaces"
        executive -> web "Uses executive interfaces and workflow control room"
        supervisor -> chatUi "Reads team briefs and asks authorized questions"
        unitManager -> chatUi "Reads unit briefs and records authorized decisions"
        executive -> chatUi "Reads executive briefs and asks aggregate questions"
        supervisor -> dashboardUi "Reviews direct-team workload and indicators"
        unitManager -> dashboardUi "Reviews authorized unit and team aggregates"
        executive -> dashboardUi "Reviews organization aggregates"
        executive -> controlUi "Monitors all three cross-functional workflows"
        sources -> worker "Provides scheduled CSV, JSON, organization and history deliveries"
        inputDriver -> api "Submits scripted inputs with trusted evaluation identity"
        web -> api "Requests authorized reports, analytics and manager operations" "HTTPS"
        worker -> api "Requests authorized evidence, per-manager generation, validation and publication" "Internal authenticated API"
        api -> worker "Submits approved structured uploads and configuration intake jobs" "PostgreSQL-backed job handoff"
        api -> postgres "Reads and writes application state under restricted service and user scopes"
        worker -> postgres "Reads committed snapshots and records deterministic job results"
        worker -> rawFiles "Archives original deliveries and reads authorized intake files"
        api -> rawFiles "Preserves uploads and retrieves approved operational document bytes"
        api -> modelGateway "Requests bounded analysis and language drafts with authorized evidence"
        modelGateway -> providers "Routes model requests and receives completions" "Local inference or external API"
        modelGateway -> postgres "Reserves and settles daily model cost; records usage, retries and traces"

        chatUi -> api "Uses conversation, reports, uploads and manager operations"
        dashboardUi -> api "Reads authorized KPI, chart, query and action data"
        controlUi -> api "Reads executive-only workflow and escalation data"

        web -> requests "Submits requests with session credentials"
        inputDriver -> requests "Replays manager inputs with explicit receipt order and authorized identity"
        worker -> requests "Requests scoped analysis, reports and evaluation outputs"
        requests -> access "Authenticates caller and obtains trusted identity and permissions"
        access -> postgres "Loads versioned hierarchy and grants; binds server-side scope and RLS"
        managerConfig -> access "Checks configuration authority and affected scope"
        managerConfig -> postgres "Versions settings and KPI candidates; activates approved validated definitions"
        requests -> managerConfig "Reads and records authorized manager context and versioned configuration"
        requests -> documents "Submits uploads for validation and evidence registration"
        documents -> access "Checks uploader, purpose and evidence audience before use"
        documents -> rawFiles "Preserves original upload bytes and reads approved documents"
        documents -> postgres "Registers document evidence or completed upload revisions; records failures"
        documents -> worker "Queues authorized structured uploads in a separate data namespace"
        requests -> insights "Resolves existing common Insight versions before requesting new analysis"
        requests -> agent "Requests scoped investigation, report language or conversational analysis"
        requests -> publication "Reads packages; publishes reports or exports validated QA"
        requests -> decisions "Records explicit human decisions, authorizations and status updates"
        requests -> outputValidator "Validates interactive content and QA export"
        requests -> audit "Records request outcomes and restricted failure diagnostics"
        requests -> postgres "Reserves execution budgets and reads ranked analysis candidates"
        agent -> requests "Checks execution grant; reports completion, cancellation or failure"
        modelGateway -> agent "Returns explicit provider or call-budget failure"
        requests -> worker "Reports manager-job failure to Schedule and Replay Control"
        worker -> documents "Reports structured-upload completion or failure"
        managerConfig -> worker "Submits inactive KPI candidates for deterministic validation"
        worker -> managerConfig "Returns KPI definition validation receipt or failure"
        managerConfig -> audit "Records definition registration, approval and activation"
        requests -> queryGateway "Cancels active request queries"
        requests -> modelGateway "Cancels active model calls under the execution grant"

        agent -> evidence "Requests scoped evidence and permitted investigative tools"
        agent -> queryGateway "Requests predefined analytical tools or proposes constrained custom SQL"
        agent -> modelGateway "Requests bounded analysis with authorized evidence and tool descriptions"
        evidence -> access "Checks audience, rows, columns, purpose and derived-claim authorization"
        evidence -> managerConfig "Reads authorized, versioned goals and evidence focus"
        evidence -> queryGateway "Runs registered evidence queries under the requesting manager scope"
        evidence -> postgres "Reads authorized evidence metadata and decision references"
        evidence -> rawFiles "Reads only approved document fragments after authorization"
        queryGateway -> access "Obtains trusted identity, relation/column allowlists and scope for every tool call"
        queryGateway -> postgres "Runs scoped read-only SQL; records query ID, inputs, result and context"
        queryGateway -> audit "Logs actual SQL, snapshot, policy, duration, row count, result hash and refusals"
        agent -> insights "Submits evidence-linked analytical content and role-scoped revisions"
        insights -> access "Checks evidence audience and permissions for every report projection"
        insights -> postgres "Stores shared versions and build state with separate evidence audiences"
        reportWriter -> insights "Reads an authorized projection of the common analytical source"
        reportWriter -> managerConfig "Reads versioned role, goals, preferences and priorities"
        reportWriter -> agent "Requests language drafting from the same bounded Agent"
        reportWriter -> outputValidator "Submits report text, JSON, chart specification and decision card"
        outputValidator -> queryGateway "Re-runs registered SQL with canonical units, rounding and pinned context"
        outputValidator -> access "Rechecks recipient scope, staff details and derived evidence"
        outputValidator -> evidence "Checks independent evidence groups, alternatives and provenance"
        outputValidator -> postgres "Reads rule/recipient history and stores validation receipts and precise failures"
        outputValidator -> reportWriter "Returns bounded repair instructions for invalid report drafts"
        publication -> reportWriter "Builds one manager package from authorized Insight content"
        publication -> outputValidator "Requires valid content, audience, snapshot and report/QA schema receipt"
        publication -> access "Rechecks audience for publication and every later read"
        publication -> queryGateway "Reads scoped dashboard and workflow observations with registered queries"
        publication -> postgres "Commits immutable packages and report/export success or failure"
        publication -> audit "Records independent publication outcomes and overall partial failure"

        decisions -> access "Checks the human actor, decision authority and delegated scope"
        decisions -> postgres "Records decision events, approved draft versions, deadlines, status and later observations"
        decisions -> agent "Requests task/message drafts after a recorded human decision"
        decisions -> evidence "Reads authorized decision memory and later KPI/workflow evidence for follow-up"
        decisions -> audit "Records human authorization and follow-up observations without an execution event"
        jobs -> ingestion "Starts idempotent intake for the current simulated cutoff"
        ingestion -> sources "Reads deliveries through source-specific adapters"
        ingestion -> rawFiles "Archives original bytes with file hashes and delivery occurrence IDs"
        ingestion -> quality "Validates parsed sources or isolated structured-upload records"
        ingestion -> api "Routes authorized operational Markdown to the document-processing boundary"
        quality -> postgres "Stores RAW payloads, normalized observations, lineage and DQ incidents"
        jobs -> snapshots "Freezes eligible committed deliveries and policy versions"
        snapshots -> postgres "Creates reproducible snapshot manifests and versioned reference relations"
        jobs -> kpi "Validates KPI candidates; computes canonical and approved active definitions"
        kpi -> postgres "Validates definitions; runs active PostgreSQL SQL and registers results"
        jobs -> workflows "Reconstructs all three business workflows for the same snapshot"
        workflows -> postgres "Reads events and workflow configuration; writes case/stage/SLA observations"
        jobs -> signals "Detects and ranks signals; selects eligible deep-analysis candidates"
        signals -> postgres "Stores deterministic signal state, rank, selection reasons and policy version"
        jobs -> api "Requests selected shared analysis and independent manager reports"
        jobs -> postgres "Reads active roster/configuration; stores leases, per-manager status and run outcome"
        // Worker job audit is submitted through the authenticated API boundary.
        audit -> postgres "Registers SQL for cost/replay exports; stores restricted diagnostics"

        // Meeting overview: logical summaries of existing elements, not new runtime units.
        // Custom elements keep this cross-container view outside C4 component scopes.
        // canonical.elements identifies the existing model elements behind each summary.
        overviewInputs = element "Sources & Manager Inputs" "Logical summary" "Simulated Organizational Sources; Scripted Manager Input Driver; manager uploads and settings." "Source,IntegratedOverview" {
            properties {
                "canonical.elements" "sources,inputDriver,web,requests,documents,managerConfig"
            }
        }
        overviewData = element "Intake & Trusted Data" "Logical summary" "Ingestion, quality, snapshots. Protected Raw File Storage; PostgreSQL only." "Database,IntegratedOverview" {
            properties {
                "canonical.elements" "ingestion,quality,snapshots,documents,rawFiles,postgres,jobs"
                "responsibility.detail" "Controlled intake preserves original RAW files and occurrences independently of analytical acceptance. Checks manifests and schemas, validates and normalizes structured records, stores accepted versioned records in PostgreSQL and freezes reproducible snapshots. Documents follow separate validation and registration. Missing or unreliable sources remain visible. Only approved data and policy versions feed analytics; RAW retention does not settle Q05 or Q08. Published history is immutable."
                "official.stages" "1: Data Integration & KPI Calculation (intake and snapshots)"
            }
        }
        overviewProcessing = element "Deterministic Analytics" "Logical summary" "KPI Engine; Workflow Engine (WF1-WF3); Signal Engine. No LLM." "Analytics,IntegratedOverview" {
            properties {
                "canonical.elements" "kpi,workflows,signals"
                "responsibility.detail" "The 55 canonical KPI definitions execute in PostgreSQL over reproducible snapshots. Workflow reconstruction supplies verified process observations. Deterministic rules evaluate deviations, suppress duplicates, assign ownership and escalate. Versioned goals, targets, thresholds, priorities and escalation rules shape signal evaluation, ranking and selection before AI investigation. PostgreSQL equivalence and detailed signal boundaries remain open."
                "official.stages" "1: KPI Calculation; 2: Signal Detection"
            }
        }
        overviewAccess = element "Authorized Evidence" "Logical summary" "Access Policy; Query Gateway; Evidence Service. Scoped read-only tools / SQL." "Governance,IntegratedOverview" {
            properties {
                "canonical.elements" "access,queryGateway,evidence"
                "responsibility.detail" "Server-side identity and role/row/column policies apply before evidence reaches the Agent or model. Uses predefined tools and constrained read-only Text-to-SQL with validation, limits and registered query results. Authorized manager focus guides evidence selection without widening access. Serves verified analytical observations, approved upload revisions and decision memory. Validated uploads can support interactive answers before the next nightly report."
            }
        }
        overviewAnalysis = element "AI Analysis & Shared Insight" "Logical summary" "One bounded AI Agent; LLM Gateway; Shared Insight Brief." "AI,IntegratedOverview" {
            properties {
                "canonical.elements" "agent,modelGateway,insights"
                "responsibility.detail" "Investigates selected authorized evidence under execution and cost limits. Shared Insights retain registered SQL references, possible causes, confidence, alternatives, options and prior decisions. A causal hypothesis requires at least two independent evidence groups; correlation alone proves no cause. Reuses permitted analysis across managers. Model routing remains provider-neutral; Q14 and Q17 remain open."
                "official.stages" "4: Evidence-Based Analysis"
            }
        }
        overviewReports = element "Role-Based Report Generation" "Logical summary" "Authorized shared Insight projections: Team Supervisor, Unit Manager, Senior Executive." "Processing,IntegratedOverview" {
            properties {
                "canonical.elements" "reportWriter,insights,access,managerConfig"
                "responsibility.detail" "Builds consistent role-specific reports from the common Shared Insight source and authorized projections. Manager goals guide report emphasis. Employee task details remain limited to the direct supervisor. Uses the existing Agent only for bounded language drafting; a separate deep investigation per manager is not required. Interactive Q&A is a separate output path and contract."
                "official.stages" "5: Role-Based Report Generation"
            }
        }
        overviewDelivery = element "Validation & Daily Brief" "Logical summary" "Output Validator gates publication. Per-manager Daily Brief: Persian + JSON." "Governance,IntegratedOverview" {
            properties {
                "canonical.elements" "outputValidator,publication"
                "responsibility.detail" "Final deterministic checks are separate from pre-analysis access checks. Validate numbers against registered SQL with canonical rounding, recipient access, duplicate/escalation consistency, evidence quality, confidence, unsupported causal claims and output contracts. Only successful validation permits publication. Rejected drafts return to Report Writer within the existing execution grant; exhausted limits produce an explicit failure. Each immutable manager package contains at most five important issues, relevant KPIs, pending decisions, options, open follow-ups and query references in Persian and corresponding JSON. Publication outcomes are independent; partial failure does not satisfy ten-valid-report acceptance. Interactive answers pass their own QA contract and access checks without rewriting a published morning report."
                "official.stages" "6: Validation & Controls; 7: Daily Brief Package"
            }
        }
        overviewInterfaces = element "User-Facing Interfaces" "Logical summary" "Conversational Assistant; Role-Based BI Dashboard; Executive Workflow Control Room." "Web,IntegratedOverview" {
            properties {
                "canonical.elements" "chatUi,dashboardUi,controlUi,requests,publication"
                "responsibility.detail" "Delivers authorized daily reports, dashboard views and interactive answers. The executive control room is executive-only. Interfaces are not the per-manager Daily Brief. Questions and uploads use the same authorization and evidence boundaries as scheduled reporting."
            }
        }
        overviewDecisions = element "Human Decision & Follow-up" "Logical summary" "Managers decide and authorize actions. System records decisions and monitors follow-up." "Decision,IntegratedOverview" {
            properties {
                "canonical.elements" "supervisor,unitManager,executive,decisions"
                "responsibility.detail" "Human managers approve, decide, escalate, close or delegate. The system can draft tasks and messages, but cannot send or execute organizational actions. Records authority, owner, deadline, action status and later observations in PostgreSQL. Authorized decision memory informs future analytical cycles."
                "official.stages" "8: Human Decision & Follow-up"
            }
        }
        overviewGoals = element "Manager Goals & Priorities" "Logical summary" "Shared, versioned targets, thresholds, priorities, escalation rules and focus." "Governance,IntegratedOverview" {
            properties {
                "canonical.elements" "managerConfig,access,postgres"
                "responsibility.detail" "Authorized manager changes pass configuration validation and governance before activation. Versions are stored in the existing PostgreSQL database and pinned to the reporting context. Goals shape deterministic evaluation and signal ranking, authorized evidence selection and role-report emphasis. Scheduled reporting consumes the applicable stored version; it never waits for live manager input. Effective-date details remain open under Q13."
                "official.stages" "3: Manager Goals & Priorities (shared configuration, not a blocking runtime step)"
            }
        }

        // These arrows show responsibility and information flow, not ordered runtime calls.
        // Existing intake, upload validation, access and human-approval controls still apply.
        overviewInputs -> overviewData "Controlled intake" "" "IntegratedOverviewFlow"
        overviewData -> overviewProcessing "Snapshots" "" "IntegratedOverviewFlow"
        overviewProcessing -> overviewAccess "Observations" "" "IntegratedOverviewFlow"
        overviewAccess -> overviewAnalysis "Authorized evidence" "" "IntegratedOverviewFlow"
        overviewAnalysis -> overviewReports "Shared Insight Brief" "" "IntegratedOverviewFlow"
        overviewReports -> overviewDelivery "Drafts" "" "IntegratedOverviewFlow"
        overviewDelivery -> overviewInterfaces "Valid outputs" "" "IntegratedOverviewFlow"
        overviewInterfaces -> overviewDecisions "Options" "" "IntegratedOverviewFlow"
        overviewInputs -> overviewGoals "Governed changes" "" "IntegratedOverviewFeedback"
        overviewGoals -> overviewProcessing "Targets / ranking" "" "IntegratedOverviewFeedback"
        overviewGoals -> overviewAccess "Evidence focus" "" "IntegratedOverviewFeedback"
        overviewGoals -> overviewReports "Report emphasis" "" "IntegratedOverviewFeedback"
        overviewInterfaces -> overviewAccess "Manager questions" "" "IntegratedOverviewFeedback"
        overviewAnalysis -> overviewDelivery "Q&A draft" "" "IntegratedOverviewFeedback"
        overviewDelivery -> overviewReports "Bounded rewrite" "" "IntegratedOverviewFeedback"
        overviewDecisions -> overviewData "Decision memory" "" "IntegratedOverviewFeedback"

    }

    // DATA CONTRACT NOTES:
    // Retain file/record occurrence IDs separately from business IDs. Do not deduplicate
    // events by entity ID. A retry of an identical delivery reuses its receipt.
    // Map calendar date to cal.d; retain supplied mdays. Derive CRM drop_day from a
    // validated manifest. Detect ticket create_time/event_time aliases by headers,
    // not by hard-coded incident dates. Preserve timestamps and Asia/Tehran semantics.
    // Exact duplicates, conflicts and late corrections remain distinct states.
    // Correction values replace the historical contract value; they are not new revenue.
    // Recompute affected historical facts/windows under a new snapshot; retain old reports.
    // Full recomputation is a safe design fallback until selective dependencies are proved.
    //
    // If a required source is missing/unreliable: identify source, affected KPI and actual
    // date; use null for unavailable current values in the output contract. Show the last
    // valid value with its own actual date where available. Never label it current.
    // Distinguish SQL no-row, SQL NULL, true zero and quality-withheld values.
    // Continue unaffected indicators and valid manager reports. Missing-source incidents
    // do not become business signals or silently close after any late file arrives.
    //
    // KPI ROLLUP: use canonical definitions and eligible populations, not sums of rates,
    // medians or duplicated organization measures. 55 definitions can produce many series.
    // WF stage targets are not the end-to-end KPI formula. WF2 canonical SLA is 48 hours,
    // not the sum of stage budgets. WF1 final delivery uses promised_by. No SLA is supplied
    // for its post-delivery follow-up stage. WF3 stage configuration and 7-day KPI differ.
    // Open/unknown stages and repeated/reopened events retain explicit state.
    // No fabricated lead-level join from advertising source aggregates to contracts.
    //
    // SIGNAL RULES from escalation_rules.csv:
    // R1 starts at owner_manager_id. R2 escalates at crit, more than configured warn days,
    // or >=20% deterioration since first report. R3 routes workflow/organization warn
    // crossings to M01. R4 suppresses unchanged repeats (<10%) for that same recipient.
    // R5 uses median of the same weekday over four prior weeks; holiday exception applies.
    // R6 limits a report to five important items and groups supported common-cause issues.
    // R7 info rules never alert. R8 starts threshold evaluation on Shamsi month day 8.
    // Check suppression/escalation at detection, report generation and final validation.
    // Persist episode AND recipient history. Q12 still governs incomplete/edge cases.
    //
    // EVIDENCE AND SECURITY:
    // F01 - NUMERICAL EVIDENCE: every published numerical value, including a baseline,
    // confidence score, capacity, estimated impact or cost, must trace to executed and
    // registered PostgreSQL SQL. No calculation-only exception exists. An underlying
    // calculation needs an equivalent executed, registered-query path. Retain query_id,
    // SQL/version, parameters and source inputs, result, unit, rounding rule, snapshot,
    // audience, report/answer context and evidence revision. The LLM cannot invent numbers.
    // Output Validator checks canonical KPI identity and unit-specific reference rounding;
    // additional measures have separately authorized definitions and registered SQL.
    // Use qualitative causal confidence unless an approved scoring definition has the
    // required executed registered-query path. Do not invent a numerical confidence score.
    // Display formatting cannot change the validated value. Q03 and rounding conflicts stay open.
    // Each causal hypothesis needs >=2 independent evidence groups, temporal fit,
    // confidence, alternatives and limitations. Two derivatives of one population are not
    // two independent groups. The dataset is one simulation, not proof of causal effect.
    // An authorized projection cannot retain a conclusion based on hidden evidence.
    // Rebuild the hypothesis from permitted evidence or omit it for that audience.
    // A report job resolves the common issue/snapshot Insight before new analysis. Reuse
    // that source across management levels; authorized private evidence may extend its
    // audience-controlled content. A separate unrelated narrative is not a second source
    // of truth. This is a logical responsibility, not an approved internal schema (Q14).
    // Shared Insight consistency does not grant shared raw prompts across roles.
    // Upper managers see aggregates only. Individual task detail is direct-supervisor
    // workload data, not employee performance or blame. Leave is team capacity only.
    // RLS also applies to conversation, drill-down, history, exports and cached results.
    // Cache keys, if used, include principal/scope, snapshot and policy revision.
    // User-facing errors and query logs cannot reveal another manager's data.
    // Query Gateway rejects DDL/DML, role/session changes, unapproved functions, catalog
    // access and unapproved relations. A SELECT prefix is not sufficient validation.
    // Server identity cannot be taken from model text or a client manager_id field.
    // Query roles cannot own protected tables or bypass RLS. Pool context is reset.
    // Full-source KPI service privileges never transfer to conversational SQL.
    // Source text and uploads cannot change tools, policy, report recipients or numbers.
    //
    // SHARED CODEBASE: process boundaries below are a target runtime allocation.
    // Backend/worker do not form independent business microservices. Components in the API
    // are reused through its authenticated interface by the worker. Audit is an API module.
    // Worker audit goes through the API; no separate audit microservice is required.
    // The single Agent is in the API. Report Writer and analytical engines are deterministic.
    // Model Gateway reserves the combined daily budget before EACH call and settles actual
    // usage, including retries and chat. Exact retry counts and tracing products are pending.
    // F02 - EXECUTION CONTROL: Application API (requests) is the deterministic controller
    // for every Agent investigation, including nested report-writing and decision drafts.
    // It reserves per-manager and daily execution budgets, and checks maximum tool calls,
    // investigation steps, total elapsed time, retry count and cancellation before each
    // tool/model step. Query Gateway and the Agent require a live execution grant.
    // Cancellation stops further work and cancels active queries/model requests where
    // supported; late results cannot publish after cancellation. Record final stop state.
    // Exact limits, budget allocations and retry counts remain configurable and unapproved.
    // LLM Gateway controls individual model calls, provider retries, tokens and USD usage.
    // Its retries consume the parent request budget; they cannot reset elapsed/step limits.
    // Schedule and Replay Control (jobs) owns nightly manager-job and overall run outcomes.
    //
    // F03 - SELECTION: Signal Engine ranks eligible signals deterministically before AI.
    // Use deviation, supported customer/financial impact, evidence confidence, versioned
    // manager priorities and escalation context. Store reasons and policy version.
    // Weights, thresholds and deep-analysis admission limits are not approved here.
    // Application API admits selected work within execution/cost budgets and resolves
    // shared Insight builds by issue/snapshot and permitted audience. Reuse completed
    // authorized content or join an in-flight build; do not repeat one deep investigation
    // for every manager. A different evidence audience may need a separate permitted
    // projection or missing evidence. Eight daily deep analyses is only an estimate.
    //
    // F04 - UPLOADS: Document Intake validates identity, scope, size, type and content.
    // Documents register authorized fragments; extracted numerical claims still need SQL.
    // Structured attachments use the existing worker adapters and quality checks under an
    // upload-specific namespace in PostgreSQL. They cannot join canonical nightly sources
    // or change a canonical KPI merely because a manager submitted them.
    // Worker records processing completion/failure and notifies Document Intake. Only
    // successful, quality-accepted data becomes an authorized interactive data revision.
    // Failed/pending data is not queryable evidence; expose an appropriate manager state.
    // Query Gateway uses approved upload relations with RLS and registered read-only SQL.
    // Document retrieval is not an embedding/RAG requirement. Neither path overwrites
    // an already published morning report or waits for the next reporting morning.
    //
    // F05 - FAILURES: provider timeout, model API error, retry exhaustion, execution-budget
    // exhaustion or cost-budget exhaustion can occur before a draft exists. Gateway
    // propagates model failures to Agent and Application API. The controller stops work,
    // records restricted diagnostics in Audit, records a manager-specific failed report
    // through Publication, and notifies Schedule and Replay Control through the worker.
    // The worker persists a partially failed run and continues independent manager jobs.
    // Validation failure follows the same failed-report path after bounded repair.
    // Never manufacture a successful report or count an error toward ten valid reports.
    //
    // HUMAN AUTHORITY: after a decision the system can prepare a task/message draft.
    // A manager approves that draft and sends/executes it outside ARKA. No outbound action
    // connector is modeled. Record execution status only from human or observed evidence.
    // Scripted decisions have pre-baked effects in later fixed data; do not alter source
    // data to simulate a response. Before/after observations are not proven causal effects.
    //
    // OUTPUT CONTRACTS: brief requires report_day, manager_id, items, numbers, data_issues,
    // text_fa. QA status is answered, refused_out_of_scope, refused_individual_data,
    // data_unavailable or clarification_requested. Show actual executed SQL, rows and
    // definition when permitted. query_id is stricter internally than the schema's optional
    // field because the official brief requires traceability for EVERY report number.
    // Both Persian text and its JSON twin come from the same validated content model.
    // Source enum is orders/tickets/crm/tasks/marketing/sessions/availability; include the
    // exact affected file in authorized detail without changing supplied schema enums.
    // Legacy and uploaded external sales reports are comparison evidence, not replacements
    // for canonical KPI definitions. Reconcile meaning, period and scope before comparison.
    // F06 - EVALUATION EXPORT: Publication owns generation of validated report and QA files:
    // submission/briefs/day_XXX/<manager_id>.json uses dataset/output_contract/brief_schema.json;
    // submission/qa/<input_id>.json uses dataset/output_contract/qa_answer_schema.json.
    // For scripted questions input_id is question_id (Q01..Q16 in this development set).
    // Use only the requesting manager's authorized, validated content for each artifact.
    // Publication reads stored validation receipts and records export success/failure;
    // a missing/failed export cannot be counted as a successful required deliverable.
    // Generated submission files are application outputs, separate from Protected RAW storage.
    // This model change creates none of those output files.
    // Audit and Evaluation owns daily token/cost records and replay execution/status exports,
    // including independent report/export failures and required acceptance evidence.
    // It obtains actual gateway usage from PostgreSQL and validates query-backed totals,
    // reporting day, completeness and declared output contracts before export.
    // No cost/status filename or schema is supplied in the inspected repository.
    // Their precise export paths/fields remain pending organizer confirmation.
    // Export access needs explicit evaluation authority; this is not a broader manager grant.
    //
    // F07 - KPI LIFECYCLE: Manager Configuration accepts authorized new-definition requests.
    // Access checks author and scope; no automatic formula editing follows a goal change.
    // It registers an inactive candidate with a new identity/version in PostgreSQL and
    // submits it to the worker. KPI Engine validates definition, unit/rounding, inputs,
    // scope/rollup semantics, SQL safety and deterministic execution; reports its receipt.
    // Manager Configuration versions the receipt and human approval. Activate only a
    // successfully validated and approved definition at its recorded effective time.
    // Failed/pending candidates remain inactive. Jobs loads only active approved versions;
    // KPI Engine computes them deterministically and registers SQL/results/provenance.
    // Audit records registration, validation, approval, activation and computation.
    // Preserve the original 55 canonical definitions and formulas unchanged. Additions
    // cannot replace them; future changes to a canonical formula need separate explicit
    // authority and validation and are not authorized by this lifecycle.
    // Exact new-definition approval roles and effective-time policy remain configurable
    // and unresolved; Q13 also remains open for organization timing.
    //
    // F08 - VIEW SCOPE: all 15 view keys are retained. Short visible descriptions retain
    // detailed responsibilities in element properties. Focused views omit unrelated
    // relationships; omission never deletes a relationship from the canonical model.
    // The unresolved signal-status conflict is a contract gate, not an invented translation.

    views {
        custom IntegratedOverview "ARKA - Integrated High-Level Architecture" "One-page unified architecture overview for team discussion." {
            title "ARKA - Integrated High-Level Architecture"
            include overviewInputs overviewData overviewProcessing overviewAccess overviewAnalysis overviewReports overviewDelivery overviewInterfaces overviewDecisions overviewGoals
            autoLayout tb 45 60
        }

        systemContext arka SystemContext "Human management roles and external source/model boundaries." {
            title "ARKA - People and External Systems"
            include arka supervisor unitManager executive sources inputDriver providers
            autoLayout lr
            default
        }

        container arka Containers "Six runtime containers; one modular codebase and one PostgreSQL database." {
            title "ARKA - Runtime Containers"
            include supervisor unitManager executive sources inputDriver web api worker postgres rawFiles modelGateway providers
            autoLayout lr
        }

        component web Interfaces "Three Persian RTL interfaces with API access controls." {
            title "ARKA - Three Management Interfaces"
            include supervisor unitManager executive chatUi dashboardUi controlUi api
            autoLayout lr
        }

        component worker DataIntake "Structured intake, RAW preservation, data quality and snapshots." {
            title "ARKA - Source Intake and Snapshots"
            include sources jobs ingestion quality snapshots postgres rawFiles api
            autoLayout lr
        }

        component worker DeterministicAnalytics "Deterministic KPI/workflow analysis, signal ranking and selection." {
            title "ARKA - Deterministic Analytics and Selection"
            include jobs kpi workflows signals postgres api
            autoLayout lr
        }

        component api EvidenceAndAnalysis "Authorized evidence, controlled SQL and a bounded investigation." {
            title "ARKA - Authorized Evidence and Bounded Analysis"
            include requests access queryGateway evidence agent insights postgres rawFiles modelGateway
            autoLayout lr
        }

        component api ReportDelivery "Role projection, validation and independent report/QA export." {
            title "ARKA - Validated Report Delivery"
            include publication reportWriter insights outputValidator queryGateway access audit postgres
            exclude "publication -> queryGateway"
            exclude "queryGateway -> access"
            exclude "insights -> access"
            exclude "insights -> postgres"
            exclude "outputValidator -> postgres"
            autoLayout lr
        }

        component api ManagerGovernance "Authorized manager inputs and the controlled new-KPI lifecycle." {
            title "ARKA - Manager Inputs and KPI Governance"
            include web inputDriver requests access managerConfig documents decisions worker postgres
            exclude "requests -> postgres"
            exclude "requests -> worker"
            exclude "documents -> postgres"
            exclude "worker -> postgres"
            autoLayout lr
        }

        // System-scoped dynamics use containers. Component detail is split by owner container
        // so a view never combines components from different container scopes.
        // Dynamic statements use supported implicit ordering, in the order shown.
        // Optional branches and per-manager repetition are stated in descriptions.
        dynamic arka NightlyReporting "Scheduled data processing, selected shared analysis and independent morning reports." {
            title "ARKA - Scheduled Reporting Overview"
            sources -> worker "At 00:00 admit D-1 deliveries"
            worker -> rawFiles "Preserve original delivery bytes"
            worker -> postgres "Validate data and freeze morning R snapshot"
            worker -> postgres "Compute 55 canonical KPIs and WF1-WF3"
            worker -> postgres "Detect, rank and select eligible signals using manager context"
            worker -> api "Request selected shared analysis and independent reports"
            api -> postgres "Resolve shared Insight and reserve execution budgets"
            api -> modelGateway "Analyze selected missing evidence within the execution grant"
            modelGateway -> postgres "Reserve combined daily LLM budget"
            modelGateway -> providers "Request model result with bounded retries"
            api -> postgres "Store shared Insight and validate each role package"
            api -> postgres "Publish valid packages; record report and JSON export outcomes"
            worker -> postgres "Record complete or partially failed run; check time targets"
            web -> api "Read authorized package or explicit failure state"
            autoLayout tb
        }

        dynamic worker NightlyData "D-1 intake, canonical calculations and deterministic deep-analysis selection." {
            title "ARKA - Nightly Data Processing"
            jobs -> ingestion "Start intake for morning R; cutoff R-1"
            ingestion -> sources "Read eligible CSV and JSON"
            ingestion -> rawFiles "Preserve bytes, hashes and delivery identity"
            ingestion -> quality "Check delivery and source contracts"
            quality -> postgres "Store RAW, valid observations and data issues"
            ingestion -> api "Route operational Markdown separately"
            jobs -> snapshots "Pin committed inputs and policy versions"
            snapshots -> postgres "Freeze reproducible snapshot; exclude future facts"
            jobs -> kpi "Compute unchanged 55 KPIs and approved active additions"
            kpi -> postgres "Register executed SQL, inputs, results and lineage"
            jobs -> workflows "Reconstruct WF1, WF2 and WF3"
            workflows -> postgres "Store stage timing, SLA and bottleneck evidence"
            jobs -> signals "Apply R1-R8; rank and select eligible deep analysis"
            signals -> postgres "Store selection reasons, priority context and policy version"
            jobs -> api "Dispatch shared-analysis work and independent manager reports"
            jobs -> api "Record replay and required evaluation/export status"
            autoLayout tb
        }

        dynamic api NightlyBrief "Reuse shared authorized analysis. Investigate selected gaps within limits, then validate each package." {
            title "ARKA - Shared Analysis and Manager Brief"
            worker -> requests "Start scoped manager job at a pinned snapshot"
            requests -> access "Authenticate caller and resolve manager scope"
            requests -> postgres "Read ranked candidates and context; reserve execution budgets"
            requests -> insights "Reuse shared Insight or join one authorized in-flight build"
            requests -> agent "Only if selected evidence is missing, start bounded investigation"
            agent -> evidence "Retrieve permitted evidence and decision history"
            evidence -> access "Authorize evidence before model use"
            evidence -> queryGateway "Request registered evidence SQL"
            queryGateway -> postgres "Execute scoped SQL; register inputs, results and context"
            agent -> requests "Check remaining steps, tools, time, retries and cancellation"
            agent -> modelGateway "Analyze selected evidence within the active execution grant"
            agent -> insights "Register shared analysis and audience references"
            requests -> publication "Build this manager package independently"
            publication -> reportWriter "Assemble role report and JSON twin"
            reportWriter -> insights "Read authorized projection of the shared source"
            reportWriter -> outputValidator "Submit report, chart and decision card"
            outputValidator -> queryGateway "Verify every number with canonical SQL, units and rounding"
            outputValidator -> evidence "Check two independent evidence groups per cause"
            outputValidator -> access "Check recipient scope and individual-data limits"
            publication -> outputValidator "Require valid content and brief-schema receipt"
            publication -> postgres "Commit package and required JSON export status"
            publication -> audit "Record independent success or failure"
            autoLayout tb
        }

        dynamic api InteractiveAssistant "Scoped questions use D-1 data and approved upload revisions. Validate the answer and export required QA JSON." {
            title "ARKA - Interactive Analytical Answer"
            supervisor -> web "Open assistant and submit credentials"
            web -> requests "Read my report and ask for a permitted analytical breakdown"
            requests -> access "Authenticate session and derive server-side manager identity"
            requests -> publication "Read authorized immutable morning report"
            publication -> access "Recheck current permission for the stored audience and evidence"
            requests -> postgres "Reserve manager/daily execution budget for the interactive snapshot"
            requests -> agent "Analyze the scoped question under the execution grant"
            agent -> evidence "Retrieve only permitted report, document and decision context"
            evidence -> access "Authorize context before any LLM call"
            agent -> modelGateway "Interpret the question using authorized context and tool definitions"
            agent -> queryGateway "Use a predefined tool, or propose a constrained custom Text-to-SQL query"
            queryGateway -> access "Resolve allowlisted relations, columns, functions and row policy"
            queryGateway -> postgres "Execute validated read-only SQL with RLS, timeout and result limits"
            queryGateway -> audit "Register actual SQL, result reference, identity, snapshot and outcome"
            agent -> modelGateway "Draft answer from authorized executed results; clarify or refuse when required"
            requests -> outputValidator "Validate numbers, scope, evidence, answer status and QA contract"
            outputValidator -> queryGateway "Verify referenced numbers and registered SQL"
            requests -> publication "Export validated QA to submission/qa/<input_id>.json"
            publication -> outputValidator "Require authorized qa_answer_schema.json validation"
            publication -> postgres "Record QA content and export success or failure"
            requests -> audit "Record answer/refusal and required QA export outcome"
            web -> requests "Read checked Persian answer, chart and permitted query references"
            autoLayout tb
        }

        dynamic api ManagerUpload "Document and structured paths are alternatives. Only successful authorized revisions become evidence." {
            title "ARKA - Document and Structured Upload Paths"
            unitManager -> web "Upload a business attachment"
            web -> requests "Submit bytes and attachment context"
            requests -> access "Authenticate uploader and derive scope"
            requests -> documents "Validate type, size, content and audience"
            documents -> access "Authorize ingestion and later evidence use"
            documents -> rawFiles "Preserve original bytes; ignore embedded instructions"
            // Path A: document content. Numerical claims still require registered SQL.
            documents -> postgres "A: register approved document evidence or an explicit failure"
            // Path B: structured records. Existing worker processing stays in an upload namespace.
            documents -> worker "B: queue authorized CSV intake; keep canonical sources separate"
            worker -> postgres "B: validate/process isolated rows; store completion or failure"
            worker -> documents "B: notify processing completion or failure"
            documents -> postgres "B: register only successful data revision; expose failure otherwise"
            // Continue only for a successful authorized revision; pending/failed input is unavailable.
            requests -> agent "Use the new interactive revision without a morning-report rewrite"
            agent -> evidence "Retrieve permitted document/data revision references"
            evidence -> access "Recheck evidence audience"
            evidence -> rawFiles "A only: read approved document fragments"
            agent -> queryGateway "Query B data, or registered numerical evidence from A"
            queryGateway -> access "Apply allowed upload relations, RLS and execution limits"
            queryGateway -> postgres "Execute read-only SQL at the selected evidence revision"
            queryGateway -> audit "Register SQL, inputs, result and context"
            agent -> modelGateway "Draft response from authorized evidence and SQL results"
            requests -> outputValidator "Check numbers, scope and QA contract"
            autoLayout tb
        }

        dynamic api HumanDecisionFollowUp "Humans decide, approve and execute. ARKA records drafts, status and later observations." {
            title "ARKA - Human Decision and Follow-up"
            unitManager -> web "Read recommendations and decision options"
            web -> requests "Fetch authorized report and decision card"
            requests -> publication "Read validated options from the published package"
            unitManager -> web "Select, delegate, escalate or close; explicitly record the decision"
            web -> requests "Submit human decision with report and option references"
            requests -> access "Authenticate actor and resolve decision authority"
            requests -> decisions "Record explicit human decision"
            decisions -> access "Check scope and authority for this decision"
            decisions -> postgres "Append decision event, owner, deadline and success criteria"
            decisions -> agent "Request task/message draft for the recorded decision only"
            agent -> modelGateway "Draft the proposed task/message without sending it"
            decisions -> postgres "Store draft linked to human decision and source report"
            unitManager -> web "Review and approve draft; record any human execution status"
            web -> requests "Record approval and any human-reported execution status"
            requests -> decisions "Append authorization/status event without external execution"
            decisions -> postgres "Persist authorization, deadline and action state"
            worker -> requests "On a later run, request follow-up context for the next report"
            requests -> decisions "Monitor open action and evaluate later observations"
            decisions -> evidence "Read authorized later KPI/workflow evidence and prior decision memory"
            decisions -> postgres "Append observed outcome and limitations; do not claim proven causality"
            agent -> evidence "Use authorized decision history as context for a future Shared Insight Brief"
            decisions -> audit "Record decision, approval and follow-up trace"
            autoLayout tb
        }

        dynamic api PartialPublication "Provider or budget failure may precede a draft. Report failures remain separate from ten-valid-report acceptance." {
            title "ARKA - Failed Job and Independent Publication"
            worker -> requests "Start manager A report job"
            requests -> agent "Begin selected bounded analysis"
            agent -> modelGateway "Request model result under the execution grant"
            modelGateway -> providers "Attempt call; timeout or API error may exhaust retries"
            modelGateway -> agent "Return timeout, API error or exhausted retry/cost budget"
            agent -> requests "Propagate failure or execution-budget/cancellation stop"
            requests -> audit "Record restricted diagnostics and exhausted limits"
            requests -> publication "Record manager A as failed; no draft is required"
            publication -> postgres "Persist failed report status and safe manager error"
            requests -> worker "Notify Schedule and Replay Control of A failure"
            worker -> postgres "Persist partially failed run and continue independent jobs"
            worker -> requests "Start independent manager B job"
            requests -> publication "Build manager B package"
            publication -> reportWriter "Assemble B from authorized shared Insight"
            reportWriter -> outputValidator "Validate any B draft"
            // If validation fails, repair remains bounded by B execution grant; otherwise skip repair.
            outputValidator -> reportWriter "If invalid, return precise errors for bounded repair"
            publication -> outputValidator "Require successful B receipt; record failure if absent"
            // Commit is conditional on a valid receipt. Never manufacture success after any failure.
            publication -> postgres "Only if valid, publish B and record JSON export outcome"
            publication -> audit "Record independent outcomes; ten-report acceptance may fail"
            web -> requests "Manager A reads report status"
            requests -> publication "Read A failure state within A scope"
            autoLayout tb
        }

        styles {
            element "Element" {
                shape RoundedBox
                color #ffffff
                background #334155
                fontSize 22
            }
            element "Target" {
                background #1e3a8a
            }
            element "Human" {
                shape Person
                background #7c2d12
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
            element "Processing" {
                background #0f766e
            }
            element "Database" {
                shape Cylinder
                background #5b21b6
            }
            element "Storage" {
                shape Folder
                background #6d28d9
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
            element "Governance" {
                background #92400e
            }
            // Only the ten logical summary blocks use this style.
            element "IntegratedOverview" {
                shape RoundedBox
                width 1000
                height 190
                fontSize 40
                metadata false
                description true
            }
            relationship "Relationship" {
                color #64748b
                routing Orthogonal
                fontSize 18
            }
            relationship "IntegratedOverviewFlow" {
                style solid
                thickness 2
                fontSize 30
            }
            relationship "IntegratedOverviewFeedback" {
                style dashed
                thickness 1
                color #64748b
                fontSize 28
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
