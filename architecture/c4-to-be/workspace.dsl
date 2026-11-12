workspace "Didrah - To-Be C4" "Proposed MVP architecture for team review; not a description of an implemented system." {
    model {
        manager = person "Manager" "Executive,unit manager or team lead with access limited to their authorized scope."
        evaluator = person "Evaluator / Replay Operator" "Runs data replays and reviews outputs and execution receipts."
        inputs = softwareSystem "Dataset and manager input files" "Nightly drops, configuration and replayed manager inputs." "External"
        llm = softwareSystem "LLM provider" "Produces structured drafts from permitted evidence and has no direct data or action access." "External"

        didrah = softwareSystem "Didrah" "Managerial assistant for deterministic measurement, permitted evidence analysis, reporting and decision tracking." {
            web = container "Web UI" "Persian RTL dashboard, assistant and workflow control room." "Web application"
            api = container "Backend API" "Authenticates managers, accepts inputs and serves authorized data and reports." "Modular monolith API process" {
                auth = component "Authentication and request handling" "Builds AuthContext from verified identity and handles manager requests."
                managerInput = component "Manager input handling" "Validates and records questions, uploads, configuration candidates and organization changes."
                apiPolicy = component "Policy and query gateway" "Applies row, column and purpose restrictions; runs bounded read-only queries and records receipts."
                interactive = component "Interactive agent flow" "Coordinates permitted evidence, clarification and structured answers; cannot grant access or invent numbers." "LangGraph"
                decisions = component "Decision tracker" "Records authenticated decisions, drafts actions and tracks subsequent effects; does not execute organizational actions."
                reportAccess = component "Report access" "Serves published manager reports and dashboard data within authorized scope."
            }
            worker = container "Background Worker" "Processes nightly and replay data, generates reports and evaluates runs." "Modular monolith worker process" {
                replay = component "Replay and evaluation" "Controls simulated time, runs batches and records timing, cost and run receipts."
                intake = component "Source intake" "Archives original files, checks manifest and schema, records issues and accepts valid batches."
                core = component "Deterministic core" "Builds snapshots and computes reference KPIs, workflow observations, signals and rules without an LLM."
                workerPolicy = component "Policy and evidence gateway" "Retrieves role-scoped evidence with row, column and purpose controls and query receipts."
                reportAgent = component "Manager report agent flow" "Coordinates bounded analysis and structured report drafts from permitted evidence." "LangGraph"
                validator = component "Output validator and publisher" "Checks schema, numbers, evidence, scope and recurrence; atomically publishes valid manager packages or records failure."
            }
            db = container "SQLite" "Versioned source records, snapshots, configuration, observations, decisions, reports and checkpoints." "SQLite" "Database"
            archive = container "Protected file archive" "Original source and upload files with hashes and references; not a second database." "File storage" "Database"
        }

        manager -> didrah "Submits questions, configuration and decisions"
        didrah -> manager "Provides scoped reports, dashboards and answers"
        evaluator -> didrah "Runs replays and evaluations"
        didrah -> evaluator "Provides outputs and execution receipts"
        inputs -> didrah "Supplies nightly files, configuration and replay inputs"
        didrah -> llm "Sends a structured analysis request with permitted evidence"
        llm -> didrah "Returns a structured analysis draft"

        manager -> web "Enters requests, questions and decisions" "HTTPS"
        web -> manager "Displays dashboards, reports and answers" "HTTPS"
        evaluator -> api "Requests replay execution and retrieves results"
        api -> evaluator "Returns outputs and execution receipts"
        web -> api "Sends authenticated requests" "HTTPS / JSON"
        api -> web "Returns results scoped to the user's permissions" "HTTPS / JSON"
        api -> db "Reads and writes application data and checkpoints"
        api -> archive "Stores and retrieves manager uploads"
        api -> worker "Requests background processing through persisted work"
        inputs -> worker "Supplies nightly files, configuration and replay inputs"
        worker -> db "Reads and writes snapshots, observations, reports and receipts"
        worker -> archive "Stores original files and retrieves protected inputs"
        api -> llm "Sends permitted evidence and a structured request for an interactive answer"
        llm -> api "Returns a draft interactive answer"
        worker -> llm "Sends permitted evidence and an analysis request for a report"
        llm -> worker "Returns a structured report draft"

        web -> auth "Sends authenticated requests"
        evaluator -> auth "Requests replay and output access"
        auth -> managerInput "Passes authenticated manager inputs"
        auth -> interactive "Passes questions and verified context"
        auth -> decisions "Passes authenticated decision commands"
        auth -> reportAccess "Passes authenticated report requests"
        managerInput -> db "Records validated input and configuration candidates"
        managerInput -> archive "Stores original uploads"
        managerInput -> worker "Queues accepted inputs for processing"
        interactive -> apiPolicy "Requests scoped evidence and query receipts"
        interactive -> llm "Requests a structured response using permitted evidence"
        interactive -> db "Persists scoped conversation checkpoints"
        apiPolicy -> db "Executes bounded read-only queries against permitted data"
        decisions -> db "Records decisions and follow-up observations"
        reportAccess -> apiPolicy "Checks scope and retrieves authorized data"
        reportAccess -> db "Reads published reports"

        inputs -> intake "Supplies drops and replay inputs"
        replay -> intake "Starts intake for the simulated cutoff"
        replay -> db "Records run state, timing and evaluation receipts"
        intake -> archive "Archives original files and hashes"
        intake -> db "Records batch receipts and data issues"
        intake -> core "Supplies accepted batches"
        core -> db "Reads configuration and writes snapshots, KPIs, workflows and signals"
        core -> workerPolicy "Requests evidence for a manager scope"
        workerPolicy -> db "Retrieves scoped evidence and records query receipts"
        workerPolicy -> reportAgent "Supplies permitted evidence and references"
        reportAgent -> llm "Requests structured draft from permitted evidence"
        reportAgent -> db "Persists scoped graph checkpoints"
        reportAgent -> validator "Submits report candidate and evidence references"
        validator -> core "Checks deterministic values and rules"
        validator -> workerPolicy "Checks scope and evidence"
        validator -> db "Publishes valid text and JSON atomically or records failure"
    }

    views {
        systemContext didrah "1-SystemContext" {
            include *
            title "C4 Level 1 - System Context"
            description "دیدراه و ارتباط آن با کاربران، فایل‌های ورودی و ارائه‌دهنده بیرونی مدل زبانی."
        }
        container didrah "2-Containers" {
            include *
            title "C4 Level 2 - Containers"
            description "مرزهای اجرایی شامل رابط وب، پردازه‌های API و Worker، پایگاه SQLite و آرشیو فایل محافظت‌شده."
        }
        component api "3-API-Components" {
            include *
            title "C4 Level 3 - Backend API Components"
            description "Logical modules used by the API process, including authorization and the interactive flow."
        }
        component worker "3-Worker-Components" {
            include *
            title "C4 Level 3 - Background Worker Components"
            description "Logical modules of the nightly and replay processing flow."
        }
        styles {
            element "Person" {
                shape person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "External" {
                background #777777
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Component" {
                background #85bbf0
                color #111111
            }
            element "Database" {
                shape cylinder
            }
        }
    }
}
