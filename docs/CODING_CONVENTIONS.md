# Coding conventions

Apply these conventions to new code and use them when refactoring existing code. The accepted architecture, domain model, and implementation contracts in `Analytics/` remain authoritative for responsibilities and behavior.

## Repository and service directories

- Keep repository organization directories lowercase, such as `src`, `docs`, and `deploy`.
- Under `src`, use short PascalCase names for each top-level application or service directory, such as `BackendApi`, `AgentRuntime`, and `WebApp`. The repository already identifies the product, so source directories do not repeat the product prefix.
- Keep Docker Compose service identifiers, container names, and other deployment identifiers lowercase kebab-case, independently of source directory names.
- When renaming source directories, update solution references, Docker build paths, and documentation together.

## .NET naming

| Item | Convention | Example |
|---|---|---|
| Project and project directory | PascalCase; project and assembly names use the product namespace, directories use the short service name | `BackendApi/OrgPilot.BackendApi.csproj` |
| Internal directories and namespaces | PascalCase | `Modules/IdentityAccess`, `OrgPilot.BackendApi.Modules.IdentityAccess` |
| Source files and types | PascalCase; file name matches its primary type | `FoundationDbContext.cs` |
| Methods, properties, and public members | PascalCase | `ConfirmDecisionAsync` |
| Parameters and local variables | camelCase | `businessDate` |
| Private fields | camelCase with a leading underscore | `_repository` |
| Interfaces | PascalCase with an `I` prefix | `IBusinessClock` |
| Asynchronous methods | `Async` suffix when the method returns an awaitable | `StoreAsync` |

Keep project names aligned with their responsibilities: `OrgPilot.BackendApi`, `OrgPilot.BackgroundWorker`, `OrgPilot.SchedulerReplay`, and `OrgPilot.Foundation`.

## Python naming

- Use short lowercase package and module names, with underscores where they improve readability, such as `model_gateway` and `job_runner.py`.
- Use PascalCase for classes and snake_case for functions, methods, parameters, and variables. Use UPPER_CASE for constants.
- The outer `AgentRuntime` service directory is a repository grouping, not an importable package name. Follow [PEP 8](https://peps.python.org/pep-0008/#package-and-module-names) for internal Python naming.

## React and TypeScript naming

- Keep internal feature and shared directories lowercase; use kebab-case for multiword feature names, such as `workflow-control`. Preserve conventional directories such as `src`, `features`, and `shared`.
- Use PascalCase for React component names and their component files, such as `ManagerDashboard.tsx`. Use camelCase for functions, variables, and custom hooks (for example, `useReport`).
- Keep the npm package name lowercase and use kebab-case for multiword package names, such as `orgpilot-web-app`. The outer `WebApp` service directory does not change that package name.

## General implementation rules

- Keep module ownership and dependencies aligned with the accepted domain model. Shared projects contain only genuinely shared contracts and infrastructure.
- Use nullable reference types and the centrally declared SDK, build settings, and package versions.
- Prefer clear names and small, focused implementations. Introduce abstractions when a real boundary or invariant requires them.
- Keep configuration and secrets outside source code. Commit environment examples only, never actual credentials.
- Preserve deterministic business time and pinned inputs. Do not use the host clock as business time.

## Completion criteria

The accepted architecture and applicable installed skills are the basis for design and implementation. Use them from the start of the work and verify conformance before closing it.

1. **Before design.** Read the relevant code, stage scope, accepted contracts, domain model, ADRs, and repository instructions. Identify the owning modules, existing callers, and invariants affected by the change. Check the scope of every installed skill available in the repository, directory, and session. Read each applicable skill in full and record the requirements it brings to the design. Record `Not applicable` and a reason for every remaining skill.
2. **Before and during coding.** Design the change using that context, including the accepted Clean Architecture principles for ownership, separation of responsibilities, and dependency direction. Check the design against the applicable skill requirements before writing code, then follow those requirements throughout implementation. When a new constraint appears, revisit the affected design before proceeding with that part of the code.
3. **Before completion.** Build the affected components and verify behavior and acceptance criteria. Review the implemented structure against the accepted architecture and verify conformance to each applicable skill against the requirements recorded at the start. Record evidence for all three checks and resolve in-scope findings before closing the work.

**Passing tests alone is insufficient to mark a change, feature, or stage complete.** Keep completion open if behavior, architecture, or skill conformance fails or lacks evidence. Record the results in the change review or pull request and link the evidence from [development stages](DEVELOPMENT_STAGES.md) when closing a stage.
