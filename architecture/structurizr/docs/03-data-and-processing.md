# Data and processing

The data path is deterministic. It uses this sequence:

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

PostgreSQL is the product calculation engine. The KPI parity suite compares PostgreSQL results with the SQLite reference calculations. The maximum accepted evaluation tolerance is one percent.
