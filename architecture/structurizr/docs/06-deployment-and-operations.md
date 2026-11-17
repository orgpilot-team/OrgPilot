# Deployment and operations

The evaluation environment uses one reference host and Docker Compose. The deployment model contains these runtime nodes:

- Web Container
- API Container
- Worker Container
- Scheduler Container or Command
- PostgreSQL Container
- Archive Volume

Web can call only the Backend API. Web has no direct database connection. PostgreSQL and the Archive are not public services. API and Worker use separate PostgreSQL runtime roles.

API, Worker, and Scheduler can use the same application artifact. They run as separate processes. The Scheduler can also run as a command in the Worker image if the approved deployment keeps the same control boundary.

The reference execution contract is:

- Four CPU cores
- Sixteen GB RAM
- No GPU
- Network access only for the language-model API
- Read-only `/data`
- Writable `/submission`
- One-command execution
- Dependencies installed during image build
- UTF-8 input and output
- Business timezone `Asia/Tehran`

The system records stage duration, accepted and rejected rows, query results, KPI counts, signal changes, report results, model tokens, model cost, retries, access denial, result hashes, and artifact versions.

Failed jobs move to a terminal failure or dead-letter state after the approved retry limit. The exact retry, timeout, and fallback policy remains open in `ISSUE-V3-06`.

Retention periods, backup frequency, audit access, and the restore policy remain proposed in ADR 11 and open in `ISSUE-V3-09`.
