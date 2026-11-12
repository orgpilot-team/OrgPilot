# Didrah C4 Architecture - Structurizr DSL

This repository contains a complete C4 architecture model for **Didrah** (دیدراه) - an Agentic BI & Decision Intelligence Assistant for managers of the fictional Arka organization.

## Files

- `didrah-c4-architecture.dsl` - Main Structurizr DSL model

## Diagrams Included

### 1. System Context Diagram
Shows external actors and systems:
- **People**: Senior Manager (مدیر ارشد), Division Managers (مدیران کل واحد), Team Leads (سرپرست‌های تیم), Evaluator (ارزیاب)
- **External Systems**: Source Systems (CRM, Order/Warehouse, Ticket, Task), LLM Provider
- **Didrah System**: The modular monolith

### 2. Container Diagram
Shows the Modular Monolith architecture:
- **Web UI** (React/TypeScript, Persian RTL) - Dashboard, Chat Assistant, Workflow Control Room, Report Viewer
- **Backend API** (Node.js/TypeScript) - Auth, Manager Input API, Report & Query API
- **Background Worker** (Node.js/TypeScript) - Nightly ingestion, Deterministic Core, Agent Orchestration
- **SQLite Database** - Standardized data, Snapshots, KPIs, Signals, Decisions, Reports, Checkpoints
- **Protected File Archive** - Original bytes + hashes of source files and uploads

### 3. Component Diagrams (3 views)
- **Backend API Components**: Auth & AuthContext Builder, Manager Input API, Report & Query API
- **Background Worker Components**: Source Intake, Deterministic Core, Policy & Query Engine, Agent Orchestrator (LangGraph), Output Validator & Publisher, Decision Tracker, Replay & Evaluation Engine
- **Web UI Components**: Dashboard View, Chat Assistant, Workflow Control Room, Report Viewer

### 4. Dynamic/Sequence Diagrams
- **Nightly Report Generation**: Replay Clock → Source Intake → Deterministic Core → Policy & Query → Agent Orchestrator → Validator → Published Reports
- **Interactive Manager Flow**: Question/Settings/Decision paths with proper authorization and scoping

### 5. Deployment Diagram
- Single Docker container deployment (Modular Monolith pattern)
- Volume-mounted SQLite and File Archive
- External Source Systems (drop folders) and LLM Provider (HTTPS)

## How to View

### Option 1: Structurizr CLI (Recommended)
```bash
# Install Structurizr CLI
npm install -g @structurizr/cli

# Export to PNG/SVG
structurizr export -workspace didrah-c4-architecture.dsl -format png -output ./diagrams

# Or view in Structurizr Lite
structurizr serve -workspace didrah-c4-architecture.dsl
```

### Option 2: Structurizr Online
1. Go to https://structurizr.com
2. Create a workspace
3. Import the DSL file

### Option 3: VS Code Extension
Install "Structurizr" extension for VS Code and open the `.dsl` file for live preview.

## Architecture Highlights

| Aspect | Decision |
|--------|----------|
| **Style** | Modular Monolith (API + Worker separate at runtime) |
| **Database** | Single SQLite (versioned, recoverable) |
| **File Storage** | Protected File Archive (hash-indexed, no execution) |
| **LLM Integration** | LangGraph Agent Orchestrator with strict boundaries (no DB/credential access) |
| **Security** | Row/column/Purpose-level access via scoped SQLite views, deny-by-default |
| **Computation** | Deterministic Core: 55 KPIs, 3 Workflows, Signals R1-R8 - **no LLM** |
| **Localization** | Persian RTL throughout UI and reports |
| **Deployment** | Single Docker image, volume-mounted persistence |

## Key Flows

1. **Nightly**: Drop → Intake → Deterministic Core (KPI/Signal/Workflow) → Policy Scoping → Agent Analysis → Validation → Atomic Publish (10 managers × text + JSON)
2. **Interactive**: Manager Question → AuthContext → Scoped Query → Deterministic Core → Evidence → Agent → Answer (with registered query)
3. **Decision**: Manager Decision → Decision Tracker → Action Draft → Manager Confirms & Sends → Follow-up Tracking

## Tags for Filtering

Use tags to filter views:
- `manager`, `evaluator`, `external`, `source-system`, `llm`
- `container`, `component`, `ui`, `api`, `worker`, `database`, `storage`
- `auth`, `intake`, `core`, `policy`, `agent`, `validator`, `decision`, `replay`
- `dashboard`, `chat`, `workflow`, `report`

## Source Documents

This model is derived from:
1. `to-be-architecture.md` - Proposed architecture (To-Be)
2. `دیدراه-بریف-دستیار-ایجنتیک-مدیران.md` - Project brief (Source of Truth)