# 12. Evaluation Deployment Profile

Date: 2026-11-17

## Status

Accepted

## Context

The evaluation environment requires a single Docker image that runs with one `docker run` command. The TA only executes `docker run team_x ...` with no Docker Compose or second container guaranteed.

## Decision

The evaluation deployment packages the Backend API, Agent Runtime, and PostgreSQL into a single Docker image. The logical C4 boundaries remain separate (Backend API, Agent Runtime, PostgreSQL as Containers), but in the evaluation profile they co-locate in one image.

```
Evaluation Docker Image
├── Entry Point (Evaluation Entrypoint)
├── .NET Batch Orchestrator / Backend API
├── Python Agent Runtime
└── Local PostgreSQL
```

Data flows:

- `/data` (read-only) → Entry Point → Backend → PostgreSQL
- Backend → Agent Runtime
- Agent Runtime → LLM API (external)
- Backend → `/submission` (write)

In production, the three containers can be deployed separately. In evaluation, the same logical boundaries co-locate in one image.

## Consequences

- The `Evaluation Deployment Profile` documents this co-location
- C4 model shows logical separation; deployment view shows evaluation co-location
- No Docker Compose or second container required for evaluation
- The `docker run` command starts all three logical components

## Source

Addresses Gap 1 from architectural review: "Agent Runtime و Container ارزیابی"
