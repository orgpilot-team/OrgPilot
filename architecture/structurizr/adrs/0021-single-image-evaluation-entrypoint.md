# 21. Package the evaluation run as one image with one entrypoint

Date: 2026-11-19

## Status

Accepted

## Context

The TA evaluation command is fixed. The evaluator runs `docker build -t team_x .` and then one `docker run` with `DATA_DIR`, `OUTPUT_DIR`, and LLM environment variables. That single command must process every drop from `day_000` through `day_090`, apply scripted manager inputs on their own days, produce reports for mornings 62 through 91, write contract files below `OUTPUT_DIR`, and exit with code zero. No `docker compose` invocation and no second container are available in the graded run.

ADR-0018 correctly established separate logical containers and separate runtime processes. It also selected Docker Compose as the evaluation deployment. That packaging choice does not satisfy the fixed evaluator command: with Compose as the only entry path, the graded `docker run` produces no submission. ADR-0012 had the single-image shape, but it co-located the logical components inside one process and was rejected by ADR-0018 for hiding the approved boundaries.

The two requirements are compatible. Physical packaging in one image does not require collapsing the logical C4 containers or the separate runtime processes.

## Decision

The graded evaluation uses one Docker image with one batch entrypoint. This decision supersedes only the evaluation-packaging clause of ADR-0018. The logical container model and the separate-process requirement of ADR-0018 remain accepted and unchanged.

- One image is built from the repository root with `docker build -t team_x .`.
- All runtime dependencies are installed during image build. No package installation occurs at run time.
- One `ENTRYPOINT` batch orchestrator performs the complete run without manual or interactive steps.
- The orchestrator reads `DATA_DIR` and `OUTPUT_DIR` from environment variables. It does not hardcode `/data` or `/submission` in code.
- The orchestrator starts and coordinates the logical product processes inside the image: Backend API, Background Worker, Scheduler and Replay Runner, Agent Runtime, and a local PostgreSQL instance. These remain separate processes with explicit contracts. The C4 Containers are unchanged.
- The entrypoint processes drops in order from `day_000` through `day_090`, applies scripted manager input on its scheduled day, and produces the morning reports for days 62 through 91.
- The PostgreSQL data directory is created fresh inside the container at run time. It is not baked into the image. Each of the two evaluator runs starts from the same initial state.
- Submission Exporter is the only writer of contract output and writes directly below `OUTPUT_DIR` as defined in ADR-0013.
- The run completes with exit code zero when all required contract artifacts are exported. Product logs, database files, and receipts remain inside the container.
- Docker Compose remains the supported local development and UI demonstration deployment. It is not part of the graded evaluation command.

The evaluator command is:

```powershell
docker build -t team_x .

docker run --rm `
  --cpus=4 --memory=16g `
  -v /eval/holdout/arka_dataset:/data:ro `
  -v /eval/results/team_x:/submission `
  -e LLM_API_KEY=*** -e LLM_BASE_URL=... -e LLM_MODEL=deepseek/deepseek-v4.1-flash-1017 `
  -e DATA_DIR=/data -e OUTPUT_DIR=/submission `
  team_x
```

## Consequences

The professor receives one build command and one run command that produce the full submission. The graded run does not serve the three web interfaces because the evaluator reads only `/submission` JSON. The web interfaces remain available through the Compose development profile.

Physical co-location must not weaken the boundaries. Each process keeps its own database role, permissions, and contracts. The restricted Agent Runtime role from ADR-0019 still applies. The agent still cannot calculate KPIs, widen scope, publish output, or confirm decisions.

A fresh runtime database makes two evaluation runs comparable. Replay state, job state, and receipts are created inside the container and are not reused between runs.

The C4 deployment view changes from separate Compose containers to one evaluation image hosting the logical processes. The static model and all component contracts are unchanged.

## Related requirements

- One image, one non-interactive `docker run`, exit code zero.
- `DATA_DIR` and `OUTPUT_DIR` are read from environment variables.
- All dependencies are installed at image build time.
- Two evaluation runs must produce identical numbers and discovered signals.
- The logical boundaries of ADR-0018 remain observable as separate processes.

## Related model elements

- Evaluation deployment view `D1_EvaluationCompose`
- Scheduler and Replay Runner
- Backend API
- Background Worker
- Agent Runtime
- PostgreSQL
- Submission Exporter

## Supersedes

[ADR-0018](0018-adopt-modular-monolith-and-compose-runtime.md), evaluation-packaging clause only.
