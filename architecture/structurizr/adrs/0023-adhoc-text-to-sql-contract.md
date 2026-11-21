# 23. Ad-hoc Text-to-SQL contract for scoped manager questions

Date: 2026-11-19

## Status

Accepted

## Context

The brief requires a conversational assistant for follow-up questions such as "show this by channel" or "compare with last week." For these ad-hoc numbers, the language model writes SQL, the number comes from executing that SQL against the database, and the query is registered and displayed beside the answer. The acceptance suite contains roughly sixty reference questions with at least eighty-five percent accuracy, including rejected out-of-scope requests.

The current sources are incomplete on this point. ADR-0005 permits only registered read-only queries, which describes the pre-approved reference KPI world. ADR-0002 states that "the complete contract for ad hoc numbers remains open in `ISSUE-V3-02`." Without a decision, the team must choose between answering no follow-up questions and letting the model query business tables with weak controls. Both fail acceptance.

The distinction to settle is the meaning of "registered." A reference KPI query is pre-approved and stable. An ad-hoc query is generated at question time and becomes registered by being persisted and auditable after validation. Both are read-only and both pass through the same gateway, but they are not the same approval class.

## Decision

Ad-hoc questions use a deterministic, scoped Text-to-SQL lifecycle. The language model generates SQL only; it never produces a business number and never widens access. This closes `ISSUE-V3-02`.

1. **Pin scope before generation.** The Authorization Service first produces a trusted context containing actor, purpose, policy version, snapshot, and row and column predicates. No SQL is generated without this context.

2. **Generate against a restricted semantic layer.** The model may name only approved semantic views and KPI definitions: the drill dimensions exposed by the KPI Dictionary, such as team, channel, product, and day. It has no access to raw business tables and no database credential.

3. **Validate before execution.** The SQL AST validator (a module inside the Query Gateway in the implementation model) and the Query Gateway enforce SELECT-only statements, relation and column allowlists, scope predicate injection, rejection of scope-escaping subqueries and `UNION` smuggling, no side-effecting functions, and a row and cost limit. The Backend injects the scope predicate so the model cannot omit it. PostgreSQL row-level security with `FORCE ROW LEVEL SECURITY` and a non-owner role is the physical backstop from ADR-0005. The controls are unchanged; only the component boundary changes (doc 16 §6.2).

4. **Execute on the pinned snapshot.** The Query Gateway executes the validated SQL on the pinned snapshot. The number comes only from execution. The model never supplies, estimates, or rounds a value.

5. **Register the query after validation.** The system persists the generated SQL, a new `query_id`, the scope, the result hash, and the link to the question. "Registered" for an ad-hoc query means persisted, validated, and auditable and displayed beside the answer. It does not mean pre-approved in the KPI Dictionary. The brief example `Q-1187` is an identifier of this kind.

6. **Validate the answer.** The Output Validator checks that every number in the Persian answer maps to a `value` and `query_id` pair, that no out-of-scope data reached the narrative, and that the response follows the required status rules. This is the same number-to-JSON rule used for reports.

7. **Response statuses.** `refused_out_of_scope` is used when the data exists but lies outside the manager's subset. `data_unavailable` is used when the data is not present in the system sources or has not yet arrived. A generation or validation failure returns an explicit failure with no guessed number and no external data.

8. **Determinism.** Generation uses temperature zero, the pinned snapshot, and a versioned prompt template. Repeated runs of the same question must produce the same SQL and number.

## Consequences

Follow-up questions can be answered with execution-derived numbers while the zero-wrong-number and zero-leakage rules remain intact. Reference KPI queries and ad-hoc queries are distinct approval classes but share the Query Gateway, AST Guard, row-level security, and Output Validator.

The semantic layer must expose the drill dimensions used by the reference questions. If a dimension such as channel, product, or day is not queryable through an approved view, no SQL contract can answer questions about it. This is a data-contract check for implementation, not a change to this decision.

Every ad-hoc number is traceable from the answer text to a persisted query and result. These calls share the single five-dollar ceiling for the complete 30-day run.

## Related requirements

- Numbers come from SQL execution, not from the language model.
- Ad-hoc queries are registered, displayed, and auditable.
- Access is enforced before generation and again before delivery.
- Out-of-scope and unavailable data have distinct, explicit statuses.
- At least eighty-five percent accuracy on the reference question set.

## Related model elements

- Backend API: Authorization Service
- Backend API: Evidence Service
- Backend API: Query Gateway (includes SQL AST validation)
- Backend API: Output Validator
- Agent Runtime: Bounded Agent Orchestrator
- Agent Runtime: Model Gateway
- PostgreSQL row-level security

## Closes

`ISSUE-V3-02` from [ADR-0002](0002-use-postgresql-and-verify-kpi-parity.md).
