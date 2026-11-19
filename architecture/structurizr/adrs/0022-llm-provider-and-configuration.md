# 22. LLM provider and configuration for the evaluation profile

Date: 2026-11-19

## Status

Accepted

## Context

The TA permits any API-accessible language-model provider. The model and version must be declared in documentation. No API key may exist inside the project or repository; only `.env.example` lists variable names. At run time the key is injected as an environment variable and revoked after Demo Day.

The evaluation host has no GPU and only the language-model API is reachable. The Model Gateway already applies token, time, retry, and cost limits (ADR-0008, ADR-0020). A model failure must not stop deterministic calculation or valid canonical JSON (ADR-0009). The TA recommends temperature zero for stable text, and the container is executed twice; generated text must not introduce instability into numbers or discovered signals.

The team has selected a concrete model for the current profile. Remaining operational values are intentionally left at defaults until implementation tuning.

## Decision

The evaluation profile uses the following model configuration:

| Setting | Value | Source |
|---|---|---|
| `LLM_MODEL` | `deepseek/deepseek-v4.1-flash-1017` | Selected for this profile |
| `LLM_BASE_URL` | OpenAI-compatible endpoint of the provider | Injected at run time |
| `LLM_API_KEY` | Provider key | Injected at run time; never stored |
| `temperature` | `0` | TA recommendation for stable text |
| Other generation parameters | Provider and client defaults | Explicitly provisional |
| Model call timeout | Default client value | Provisional; tune in implementation |
| Retry count | Default client value | Provisional; tune in implementation |
| Fallback content | No LLM narrative; deterministic canonical JSON remains valid | Required by ADR-0009 |

The three environment variable names are declared in `.env.example` with no secret values. The provider, model identifier, and version are declared in this ADR and in the deployment documentation.

The Model Gateway is the only model path. It applies the approved token, time, retry, and cost controls to every call and records provider, model, token counts, cost, latency, status, and trace context for each call. It does not select scope, calculate numbers, or treat a completion as validated output.

All other generation parameters are defaults for now. They are not accepted architectural values. Implementation may tune them without an ADR change as long as the model identity, environment-variable contract, cost ceiling, and fail-open behavior are preserved.

## Consequences

The professor can run the image with the documented environment variables and no repository secret. The declared model and version satisfy the TA documentation requirement. Temperature zero and a pinned snapshot make repeated runs produce stable text where the model is used.

A provider or API failure produces reports with correct deterministic numbers and without LLM narrative. It does not stop publication or export.

The provisional values must not be reported as final tuned decisions. Any change to the model identity or the environment-variable names requires a new ADR.

## Related requirements

- No API key inside the project or repository; `.env.example` only.
- Model and version declared in documentation.
- Timeout and retry behavior on every model call.
- Model failure must not stop deterministic reports.
- Daily cost logging and the five-dollar ceiling remain in force.

## Related model elements

- Agent Runtime: Model Gateway
- Agent Runtime: Bounded Agent Orchestrator
- Backend API: Output Validator
- Evaluation deployment entrypoint
