# 18. Adopt a modular monolith and Docker Compose runtime

Date: 2026-11-19

## Status

Accepted

## Context

DIDRAH needs separate runtime processes for the Web Application, Backend API, Background Worker, Scheduler and Replay Runner, Agent Runtime, and PostgreSQL. The previous evaluation profile put several logical containers in one image. That profile does not match the approved runtime architecture.

The product also needs one consistent technology stack. The stack must support deterministic processing, durable PostgreSQL state, bounded agent work, and local evaluation without a message broker or a service mesh.

## Decision

DIDRAH uses a modular monolith with shared libraries and separate deployable processes.

- The Web Application uses React, TypeScript, and Vite.
- The Backend API uses ASP.NET Core on .NET 10 LTS.
- The Background Worker uses a .NET 10 Worker Service.
- The Scheduler and Replay Runner uses a .NET 10 console or worker process.
- The Agent Runtime uses Python 3.12, LangGraph, and Pydantic.
- PostgreSQL 18 is the only product database.
- Normal .NET data access uses EF Core and Npgsql.
- Job claims and approved SQL execution use Npgsql directly where required.
- APIs use REST/JSON and OpenAPI.
- Docker Compose defines the runtime services, networks, volumes, and optional observability profile.

The Backend API, Background Worker, Scheduler and Replay Runner, and Agent Runtime run as separate processes and containers. Shared .NET libraries can contain domain contracts, application contracts, persistence primitives, OpenAPI DTOs, authorization primitives, job-state contracts, output-validation interfaces, and observability conventions. A shared library does not give shared ownership of data or place separate processes in one deployment unit.

## Alternatives rejected

- The single-image deployment in ADR-0012 is rejected because it hides the approved runtime boundaries.
- New microservices are rejected because the required boundaries can be implemented in the modular monolith.
- Hangfire, Redis, RabbitMQ, Kafka, Kubernetes, and a service mesh are rejected because they are outside the approved scope.

## Consequences

The logical C4 containers match the runtime processes. Docker Compose can start the required services together. Shared contracts can be reused without adding network boundaries. Each process must use explicit contracts for its data and runtime responsibilities.

[ADR-0012](0012-evaluation-deployment-profile.md) is superseded by this decision.

## Security impact

Separate processes and containers require explicit network and database permissions. Secrets must be supplied to the service that needs them. Shared libraries must not bypass authorization or database ownership rules.

## Operational impact

Docker Compose becomes the supported deployment and local-validation method. PostgreSQL data and protected files use explicit volumes. API, Worker, Scheduler, and Agent Runtime failures can be observed and restarted independently.

## Related requirements

- The evaluation architecture requires reproducible local startup and separate runtime responsibilities.
- PostgreSQL must remain the source of truth for jobs, leases, attempts, dependencies, and replay state.
- SQLite must remain inside the Acceptance Test Harness only.

## Related model elements

- Web Application
- Backend API
- Background Worker
- Scheduler and Replay Runner
- Agent Runtime
- PostgreSQL
- Evaluation Docker Compose deployment view

## Open decisions

- The Scheduler and Replay Runner implementation can be a .NET console process or a .NET Worker Service. This choice is not accepted by this ADR.
