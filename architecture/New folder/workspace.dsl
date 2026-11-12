workspace "Didrah Architecture" "C4 model for Didrah - Agentic BI & Decision Intelligence Assistant for Arka organization managers" {

    model {
        // ==========================================
        // ACTORS (People)
        // ==========================================
        person "Senior Manager" "مدیر ارشد" "Sets organizational goals, decides on escalated items, monitors cross-division workflows and decision impact" {
            tags "manager,senior"
        }
        
        person "Division Manager" "مدیر کل واحد" "Manages two teams, views division-level signals and escalated items from teams, proposes resource reallocation" {
            tags "manager,division"
        }
        
        person "Team Lead" "سرپرست تیم" "Manages 3-5 specialists, views today's tasks and backlogs, member workload and blockers, team KPIs vs targets" {
            tags "manager,teamlead"
        }
        
        person "Evaluator" "ارزیاب و Replay Runner" "Runs 90-day replay, evaluates system output against hidden test data" {
            tags "evaluator"
        }

        // ==========================================
        // EXTERNAL SYSTEMS
        // ==========================================
        softwareSystem "Source Systems" "سیستم‌های منبع" "CRM, Order & Warehouse, Ticket, Task Management systems providing nightly data drops" {
            tags "external,source-system"
        }
        
        softwareSystem "LLM Provider" "LLM Provider" "External LLM service for structured analysis and insight generation (no direct DB/credential access)" {
            tags "external,llm"
        }

        // ==========================================
        // DIDRAH SYSTEM (Modular Monolith)
        // ==========================================
        softwareSystem "Didrah" "دیدراه" "Agentic BI & Decision Intelligence Assistant - Modular Monolith with separate API and Worker at runtime" {
            
            // Containers
            container "Web UI" "Web UI" "React/TypeScript, Persian RTL" "Dashboard, Chat Assistant, Workflow Control Room, Report viewing" {
                tags "container,ui,frontend"
            }
            
            container "Backend API" "Backend API" "Node.js/TypeScript, Express/Fastify" "Authentication, AuthContext, Manager input API, Query responses, Report reading" {
                tags "container,api,backend"
            }
            
            container "Background Worker" "Background Worker" "Node.js/TypeScript" "Nightly ingestion, Deterministic Core computation, Signal detection, Agent orchestration, Report generation" {
                tags "container,worker,backend"
            }
            
            containerDb "SQLite Database" "SQLite" "SQLite" "Standardized data, Snapshots, Config, KPIs, Signals, Decisions, Reports, Checkpoints, Graph state" {
                tags "container,database"
            }
            
            container "Protected File Archive" "Protected File Archive" "File system + Hash index" "Original bytes and hash of source files and manager uploads, no execution of untrusted files" {
                tags "container,storage"
            }

            // Components inside Backend API
            component "Auth & AuthContext Builder" "Auth & AuthContext Builder" "TypeScript" "Validates manager identity, builds AuthContext with role, scope, division/team membership" {
                tags "component,api,auth"
            }
            
            component "Manager Input API" "Manager Input API" "TypeScript" "Handles questions, priority/threshold changes, file uploads, decisions, org changes" {
                tags "component,api,input"
            }
            
            component "Report & Query API" "Report & Query API" "TypeScript" "Serves daily reports, JSON output, dashboard data, drill-down queries with row/column security" {
                tags "component,api,query"
            }

            // Components inside Background Worker
            component "Source Intake" "Source Intake" "TypeScript" "Archives files, validates manifests, schema mapping, records Data Issues, produces batch receipts" {
                tags "component,worker,intake"
            }
            
            component "Deterministic Core" "Deterministic Core" "TypeScript + SQL" "Snapshots, 55 KPIs, 3 Workflows, Signals R1-R8, hierarchical rollups, no LLM" {
                tags "component,worker,core"
            }
            
            component "Policy & Query Engine" "Policy & Query Engine" "TypeScript + SQLite Views" "Scoped views, row/column/Purpose access control, registered queries, evidence retrieval, deny-by-default" {
                tags "component,worker,policy"
            }
            
            component "Agent Orchestrator" "Agent Orchestrator" "TypeScript + LangGraph" "Coordinates analysis, draft generation, QA, limited repair; two graphs: Manager Report & Interactive" {
                tags "component,worker,agent,langgraph"
            }
            
            component "Output Validator & Publisher" "Output Validator & Publisher" "TypeScript" "Schema, numeric, evidence, scope, tone, recurrence validation; atomic publish of text + JSON per manager" {
                tags "component,worker,validator"
            }
            
            component "Decision Tracker" "Decision Tracker" "TypeScript" "Records verified decisions, creates action drafts, tracks follow-up and impact observation" {
                tags "component,worker,decision"
            }
            
            component "Replay & Evaluation Engine" "Replay & Evaluation Engine" "TypeScript" "Simulated clock execution, timing/cost tracking, output verification against hidden labels" {
                tags "component,worker,replay"
            }

            // Components inside Web UI
            component "Dashboard View" "Dashboard View" "React/TS" "Role-based KPIs vs targets, drill-down with access control, open decisions/actions" {
                tags "component,ui,dashboard"
            }
            
            component "Chat Assistant" "Chat Assistant" "React/TS" "Natural language questions, Text-to-SQL, registered query display, decision/referral in chat" {
                tags "component,ui,chat"
            }
            
            component "Workflow Control Room" "Workflow Control Room" "React/TS" "Senior Manager only: 3 cross-division workflows, SLA%, bottleneck per stage from event log analysis" {
                tags "component,ui,workflow"
            }
            
            component "Report Viewer" "Report Viewer" "React/TS" "Persian RTL daily brief package: health, top 5 items, decision cards, follow-ups, JSON download" {
                tags "component,ui,report"
            }
        }
    }

    views {
        // ==========================================
        // SYSTEM CONTEXT VIEW
        // ==========================================
        systemContext "Didrah" "System Context" "External actors and systems interacting with Didrah" {
            include *
            autoLayout lr
            style {
                element "Senior Manager" {
                    shape person
                    color "#1B5E20"
                    fontColor "#FFFFFF"
                }
                element "Division Manager" {
                    shape person
                    color "#2E7D32"
                    fontColor "#FFFFFF"
                }
                element "Team Lead" {
                    shape person
                    color "#388E3C"
                    fontColor "#FFFFFF"
                }
                element "Evaluator" {
                    shape person
                    color "#1565C0"
                    fontColor "#FFFFFF"
                }
                element "Source Systems" {
                    shape box
                    color "#E65100"
                    fontColor "#FFFFFF"
                }
                element "LLM Provider" {
                    shape box
                    color "#6A1B9A"
                    fontColor "#FFFFFF"
                }
                element "Didrah" {
                    shape box
                    color "#0D47A1"
                    fontColor "#FFFFFF"
                }
            }
        }

        // ==========================================
        // CONTAINER VIEW
        // ==========================================
        container "Didrah" "Container View" "Modular Monolith: Web UI, Backend API, Background Worker, SQLite, Protected File Archive" {
            include *
            autoLayout tb
            style {
                element "Web UI" {
                    shape webBrowser
                    color "#1565C0"
                    fontColor "#FFFFFF"
                }
                element "Backend API" {
                    shape process
                    color "#2E7D32"
                    fontColor "#FFFFFF"
                }
                element "Background Worker" {
                    shape process
                    color "#2E7D32"
                    fontColor "#FFFFFF"
                }
                element "SQLite Database" {
                    shape cylinder
                    color "#F57F17"
                    fontColor "#FFFFFF"
                }
                element "Protected File Archive" {
                    shape folder
                    color "#E65100"
                    fontColor "#FFFFFF"
                }
                element "Source Systems" {
                    shape box
                    color "#E65100"
                    fontColor "#FFFFFF"
                }
                element "LLM Provider" {
                    shape box
                    color "#6A1B9A"
                    fontColor "#FFFFFF"
                }
                element "Senior Manager" {
                    shape person
                    color "#1B5E20"
                    fontColor "#FFFFFF"
                }
                element "Division Manager" {
                    shape person
                    color "#2E7D32"
                    fontColor "#FFFFFF"
                }
                element "Team Lead" {
                    shape person
                    color "#388E3C"
                    fontColor "#FFFFFF"
                }
                element "Evaluator" {
                    shape person
                    color "#1565C0"
                    fontColor "#FFFFFF"
                }
            }
        }

        // ==========================================
        // COMPONENT VIEW - BACKEND API
        // ==========================================
        component "Backend API" "Backend API Components" "Internal components of the Backend API container" {
            include *
            autoLayout lr
            style {
                element "Auth & AuthContext Builder" {
                    shape component
                    color "#1B5E20"
                    fontColor "#FFFFFF"
                }
                element "Manager Input API" {
                    shape component
                    color "#2E7D32"
                    fontColor "#FFFFFF"
                }
                element "Report & Query API" {
                    shape component
                    color "#388E3C"
                    fontColor "#FFFFFF"
                }
            }
        }

        // ==========================================
        // COMPONENT VIEW - BACKGROUND WORKER
        // ==========================================
        component "Background Worker" "Background Worker Components" "Internal components of the Background Worker container" {
            include *
            autoLayout lr
            style {
                element "Source Intake" {
                    shape component
                    color "#E65100"
                    fontColor "#FFFFFF"
                }
                element "Deterministic Core" {
                    shape component
                    color "#1B5E20"
                    fontColor "#FFFFFF"
                }
                element "Policy & Query Engine" {
                    shape component
                    color "#2E7D32"
                    fontColor "#FFFFFF"
                }
                element "Agent Orchestrator" {
                    shape component
                    color "#6A1B9A"
                    fontColor "#FFFFFF"
                }
                element "Output Validator & Publisher" {
                    shape component
                    color "#4A148C"
                    fontColor "#FFFFFF"
                }
                element "Decision Tracker" {
                    shape component
                    color "#3E2723"
                    fontColor "#FFFFFF"
                }
                element "Replay & Evaluation Engine" {
                    shape component
                    color "#0D47A1"
                    fontColor "#FFFFFF"
                }
            }
        }

        // ==========================================
        // COMPONENT VIEW - WEB UI
        // ==========================================
        component "Web UI" "Web UI Components" "Internal components of the Web UI container" {
            include *
            autoLayout lr
            style {
                element "Dashboard View" {
                    shape component
                    color "#1565C0"
                    fontColor "#FFFFFF"
                }
                element "Chat Assistant" {
                    shape component
                    color "#2E7D32"
                    fontColor "#FFFFFF"
                }
                element "Workflow Control Room" {
                    shape component
                    color "#E65100"
                    fontColor "#FFFFFF"
                }
                element "Report Viewer" {
                    shape component
                    color "#6A1B9A"
                    fontColor "#FFFFFF"
                }
            }
        }

        // ==========================================
        // DYNAMIC VIEWS (Sequences)
        // ==========================================
        
        // Nightly Flow
        dynamic "Nightly Report Generation" "Nightly Flow" "Sequence from nightly drop to published reports" {
            participant "Replay Clock" "Replay Clock" "Simulated clock triggering nightly run"
            participant "Source Intake" "Source Intake" "Archives drops, validates manifests"
            participant "Deterministic Core" "Deterministic Core" "Snapshots, KPIs, Workflows, Signals"
            participant "Policy & Query Engine" "Policy & Query Engine" "Scopes signals per manager"
            participant "Agent Orchestrator" "Agent Orchestrator" "Analysis, Draft with budget"
            participant "Output Validator & Publisher" "Output Validator & Publisher" "Validation & atomic publish"
            participant "SQLite Database" "SQLite Database" "Persistent storage"
            
            "Replay Clock" -> "Source Intake" "Allowed drops up to R-1"
            "Source Intake" -> "SQLite Database" "Archive receipts & Data Issues"
            "Source Intake" -> "Deterministic Core" "Accepted batches"
            "Deterministic Core" -> "SQLite Database" "Snapshot, KPIs, Workflows, Signals"
            "Deterministic Core" -> "Policy & Query Engine" "Signals in manager scope"
            "Policy & Query Engine" -> "Agent Orchestrator" "Allowed evidence & references"
            "Agent Orchestrator" -> "Agent Orchestrator" "Analysis & Draft (budget-limited)"
            "Agent Orchestrator" -> "Output Validator & Publisher" "Insight content & report candidate"
            "Output Validator & Publisher" -> "Deterministic Core" "Numeric & rule review"
            "Output Validator & Publisher" -> "Policy & Query Engine" "Scope & evidence review"
            "Output Validator & Publisher" -> "SQLite Database" "Atomic publish text + JSON per manager"
            "Output Validator & Publisher" -> "SQLite Database" "Daily coverage record"
            
            autoLayout tb
        }

        // Interactive Flow
        dynamic "Interactive Manager Flow" "Interactive Flow" "Manager question, settings change, or decision" {
            participant "Manager" "Manager" "Senior/Division/Team Lead"
            participant "Web UI" "Web UI" "Auth + UI components"
            participant "Backend API" "Backend API" "AuthContext + Input/Query APIs"
            participant "Agent Orchestrator" "Agent Orchestrator" "Interactive Graph"
            participant "Policy & Query Engine" "Policy & Query Engine" "Scoped read-only queries"
            participant "Deterministic Core" "Deterministic Core" "Snapshot queries"
            participant "Decision Tracker" "Decision Tracker" "Decision recording"
            
            "Manager" -> "Web UI" "Question / Setting / Decision"
            "Web UI" -> "Backend API" "Authenticated request"
            "Backend API" -> "Backend API" "Build AuthContext"
            
            // Question path
            "Backend API" -> "Agent Orchestrator" "Question + valid scope"
            "Agent Orchestrator" -> "Policy & Query Engine" "Limited QuerySpec"
            "Policy & Query Engine" -> "Deterministic Core" "Read-only query on Snapshot"
            "Deterministic Core" --> "Policy & Query Engine" "Result + Query receipt"
            "Policy & Query Engine" --> "Agent Orchestrator" "Allowed evidence"
            "Agent Orchestrator" --> "Backend API" "Persian answer + JSON QA"
            "Backend API" --> "Web UI" "Response"
            "Web UI" --> "Manager" "Display answer"
            
            // Settings change path
            "Backend API" -> "Deterministic Core" "Candidate config version"
            "Deterministic Core" --> "Backend API" "Validation + effective time or rejection"
            "Backend API" --> "Web UI" "Result"
            "Web UI" --> "Manager" "Confirmation"
            
            // Decision path
            "Backend API" -> "Decision Tracker" "Verified decision event"
            "Decision Tracker" --> "Backend API" "Action draft / message"
            "Backend API" --> "Web UI" "Draft for confirmation"
            "Web UI" --> "Manager" "Review & send"
            
            autoLayout tb
        }

        // ==========================================
        // DEPLOYMENT VIEW
        // ==========================================
        deployment "Deployment" "Deployment View" "Single Docker container deployment (Modular Monolith)" {
            deploymentNode "Docker Host" "Docker Host" "Reference machine for Demo Day" {
                deploymentNode "Didrah Container" "Didrah Container" "Single image: Web UI + API + Worker + SQLite + File Archive" {
                    containerInstance "Web UI Instance" "Web UI" "React build served via static file server"
                    containerInstance "API Instance" "Backend API" "Node.js process"
                    containerInstance "Worker Instance" "Background Worker" "Node.js process"
                    containerInstance "SQLite Instance" "SQLite" "File-based database (volume mounted)"
                    containerInstance "File Archive Instance" "Protected File Archive" "File system (volume mounted)"
                }
            }
            
            deploymentNode "External" "External Systems" "Outside Docker" {
                deploymentNode "Source Systems Instance" "Source Systems" "Nightly drop folders (volume mounted)"
                deploymentNode "LLM Provider Instance" "LLM Provider" "HTTPS API"
            }
            
            "Source Systems Instance" -> "File Archive Instance" "Nightly drops (read-only)"
            "Source Systems Instance" -> "Worker Instance" "Manifest + data files"
            "LLM Provider Instance" <-> "Worker Instance" "Structured prompts / drafts"
            "API Instance" <-> "Web UI Instance" "REST/GraphQL"
            "API Instance" <-> "SQLite Instance" "SQL"
            "Worker Instance" <-> "SQLite Instance" "SQL"
            "Worker Instance" <-> "File Archive Instance" "File pointers + hashes"
            
            autoLayout lr
        }
    }

    // ==========================================
    // RELATIONSHIPS (explicit for clarity)
    // ==========================================
    
    // People -> Didrah
    rel "Senior Manager" "Web UI" "Views reports, dashboard, workflow control room, asks questions, sets goals, makes decisions" "HTTPS/REST"
    rel "Division Manager" "Web UI" "Views division reports, dashboard, asks questions, sets priorities, makes decisions" "HTTPS/REST"
    rel "Team Lead" "Web UI" "Views team reports, dashboard, chat assistant, views assigned actions" "HTTPS/REST"
    rel "Evaluator" "Backend API" "Triggers replay, reads output & receipts" "HTTPS/REST"
    
    // Source Systems -> Didrah
    rel "Source Systems" "Protected File Archive" "Nightly drops: CRM, Order/Warehouse, Ticket, Task files + manifests" "File system (drop folder)"
    rel "Source Systems" "Background Worker" "Data files for ingestion" "File read"
    
    // Didrah -> LLM
    rel "Background Worker" "LLM Provider" "Allowed evidence + prompt for analysis (structured draft)" "HTTPS/REST"
    rel "LLM Provider" "Background Worker" "Structured draft (no numbers, no permissions)" "HTTPS/REST"
    
    // Internal container relationships
    rel "Web UI" "Backend API" "REST/GraphQL: auth, questions, settings, decisions, report reading" "HTTPS"
    rel "Backend API" "SQLite Database" "Read/write: auth, config, queries, reports" "SQL"
    rel "Backend API" "Background Worker" "Triggers nightly run, passes manager inputs" "In-process / message queue"
    rel "Background Worker" "SQLite Database" "Read/write: snapshots, KPIs, signals, decisions, checkpoints" "SQL"
    rel "Background Worker" "Protected File Archive" "Reads source files, writes uploads, stores hashes" "File I/O"
    rel "Background Worker" "LLM Provider" "Analysis requests with allowed evidence" "HTTPS/REST"
    
    // Component relationships (API)
    rel "Manager Input API" "Auth & AuthContext Builder" "Validates identity, builds context" "In-process"
    rel "Report & Query API" "Auth & AuthContext Builder" "Validates identity, builds context" "In-process"
    rel "Manager Input API" "Decision Tracker" "Records verified decisions" "In-process"
    rel "Manager Input API" "Deterministic Core" "Validates config changes" "In-process"
    rel "Report & Query API" "Policy & Query Engine" "Executes scoped read-only queries" "In-process"
    rel "Report & Query API" "SQLite Database" "Reads reports, dashboard data" "SQL"
    
    // Component relationships (Worker)
    rel "Source Intake" "SQLite Database" "Writes batch receipts, data issues" "SQL"
    rel "Source Intake" "Protected File Archive" "Archives original files, stores hashes" "File I/O"
    rel "Source Intake" "Deterministic Core" "Passes accepted batches" "In-process"
    rel "Deterministic Core" "SQLite Database" "Writes snapshots, KPIs, workflows, signals" "SQL"
    rel "Deterministic Core" "Policy & Query Engine" "Provides signals in manager scope" "In-process"
    rel "Policy & Query Engine" "SQLite Database" "Scoped views, registered queries, evidence" "SQL"
    rel "Policy & Query Engine" "Agent Orchestrator" "Allowed evidence & references" "In-process"
    rel "Agent Orchestrator" "Output Validator & Publisher" "Insight content & report candidates" "In-process"
    rel "Output Validator & Publisher" "Deterministic Core" "Numeric & rule validation" "In-process"
    rel "Output Validator & Publisher" "Policy & Query Engine" "Scope & evidence validation" "In-process"
    rel "Output Validator & Publisher" "SQLite Database" "Atomic publish: text + JSON per manager" "SQL"
    rel "Decision Tracker" "SQLite Database" "Writes decision events, action drafts, follow-ups" "SQL"
    rel "Replay & Evaluation Engine" "SQLite Database" "Reads/writes run receipts, checkpoints, results" "SQL"
    
    // Component relationships (UI)
    rel "Dashboard View" "Backend API" "Dashboard data, drill-down queries" "HTTPS/REST"
    rel "Chat Assistant" "Backend API" "Questions, Text-to-SQL, decisions" "HTTPS/REST"
    rel "Workflow Control Room" "Backend API" "Workflow SLA%, bottlenecks from event log" "HTTPS/REST"
    rel "Report Viewer" "Backend API" "Daily brief package, JSON download" "HTTPS/REST"
    
    // Tags for filtering
    tags {
        "manager" "Managers (Senior, Division, Team Lead)"
        "evaluator" "Evaluator/Replay Runner"
        "external" "External systems"
        "source-system" "Source data systems"
        "llm" "LLM Provider"
        "container" "Container-level elements"
        "component" "Component-level elements"
        "ui" "User interface"
        "api" "Backend API"
        "worker" "Background Worker"
        "database" "Database"
        "storage" "File storage"
        "auth" "Authentication/Authorization"
        "intake" "Source intake"
        "core" "Deterministic core computation"
        "policy" "Policy & query engine"
        "agent" "Agent orchestrator"
        "validator" "Output validator"
        "decision" "Decision tracker"
        "replay" "Replay & evaluation"
        "dashboard" "Dashboard view"
        "chat" "Chat assistant"
        "workflow" "Workflow control room"
        "report" "Report viewer"
    }
}