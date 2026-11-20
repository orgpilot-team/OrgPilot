# Data and processing

## Daily data plane

The daily data path is deterministic. It uses this sequence:

```text
Source Intake
  -> Schema Registry
  -> Normalizer
  -> Data Quality
  -> Deduplication and Conflict Handling
  -> Canonical Storage
  -> Daily Snapshot
  -> KPI Engine
  -> Signal and Workflow Engine
  -> Evidence and Agent
  -> Validator and Publisher
```

The system reads input only from `DATA_DIR`. It writes delivery output only to `OUTPUT_DIR`. It processes drops from `day_000` through `day_090` in order.

A report for the morning of business day D can use valid data and manager input through the end of day D-1. Data that arrives during a run does not change that run. Each run pins the data, organization, policy, and configuration versions.

Each source has a versioned schema contract. The contract defines required columns, canonical names, aliases, types, formats, units, null rules, allowed values, primary keys, and error behavior. Unknown structures are not guessed.

Raw source data and canonical data remain separate. Each canonical record keeps a link to its source file, drop, and hash. Invalid or conflicting records are quarantined and do not enter a valid snapshot.

Missing data does not stop all publication. A dependent KPI is `null`. The system records the condition as a data issue. A data issue is not a business signal.

Late or corrected data causes a complete rebuild in the first version. A rebuild creates a new restated report version. It does not overwrite the original published report.

PostgreSQL 18 is the only product database and the product calculation engine. It stores canonical data, snapshots, KPI results, workflow and signal state, durable jobs, receipts, reports, and audit records. Normal .NET transactions use EF Core and Npgsql. Job claims and approved KPI SQL can use Npgsql directly.

## Normalization boundary

Source Intake verifies the manifest and source hash. Schema Registry selects the versioned source contract. Normalizer converts accepted source fields to canonical names, types, formats, units, and timezone rules. Data Quality and Deduplication and Conflict Handling run after normalization and before a record enters canonical storage.

The pipeline does not infer an unknown schema, unit, key, or alias. A failed source record remains outside the valid snapshot and has a traceable issue receipt.

## KPI acceptance plane

KPI acceptance is separate from the daily product path:

```text
Read-only reference SQL
  -> SQLite inside Acceptance Test Harness
  -> reference result

Equivalent pinned snapshot
  -> translated PostgreSQL SQL
  -> product result

Reference result + product result
  -> Acceptance Test Harness (parity check)
  -> Parity Receipt
```

SQLite is embedded only in the Acceptance Test Harness. It is not a product database, product container, or daily runtime dependency. The reference SQL and KPI Dictionary remain read-only.

The parity check inside the Acceptance Test Harness compares row sets, nulls, values, median translation, time intervals, decimal division, timezone behavior, and date boundaries. The maximum accepted evaluation tolerance is one percent. A PostgreSQL translation is not accepted until its parity evidence passes. Parity is one acceptance check, not a separate product component; the former KPI Parity Validator is folded into the harness (ADR-0016 amended, doc 16 §6.3).

Agent Runtime has no role in SQL translation, KPI calculation, or parity repair.
