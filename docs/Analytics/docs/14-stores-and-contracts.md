# Stores and contracts

## Purpose and Scope

This document defines the two product stores and two external contracts that appear in the model. These elements are not Product Components.

## Runtime Technology

PostgreSQL 18, a protected mounted filesystem or compatible object storage, versioned input CSV/JSON, and a writable `OUTPUT_DIR` filesystem.

## Trust Boundary

Each store or contract has a fixed authority, access mode, and mutability rule. Reference output schemas and evaluation input contracts are read-only for architecture work.

## Allowed Responsibilities

- Persist product state and protected source bytes.
- Supply versioned evaluation input.
- Receive only validated output-contract files.

## Forbidden Responsibilities

- Treat a store or contract as a Component.
- Add a new store or claim a schema that the formal contracts do not define.
- Use SQLite as a product store.

## Component Map

| DSL identifier | Element | Kind |
|---|---|---|
| `postgres` | PostgreSQL | Product store |
| `fileArchive` | Protected File Archive | Product store |
| `inputDataset` | OrgPilot Input Dataset | External input contract |
| `submissionOutput` | Submission Output Directory | External output contract |

## Internal Relationships

PostgreSQL and Protected File Archive are inside the OrgPilot boundary. They do not call other elements.

## External Relationships

The OrgPilot Input Dataset is read-only. The Submission Output Directory accepts approved brief and QA artifacts from Submission Exporter only.

## Component Sections

<a id="postgresql-product-database"></a>

### PostgreSQL product database

- **DSL identifier:** `postgres`;
- **Display name:** PostgreSQL.
- **Purpose:** Be the only product database and source of truth for durable state.
- **Responsibilities:** Store product, analytical, access, job, checkpoint, receipt, audit, and internal chart-presentation records.
- **Inputs:** Authorized product writes and approved queries.
- **Outputs:** Scoped records, projections, job state, versioned `ChartSpec` records, and receipts.
- **Owned state:** Product state in proposed versioned schemas.
- **Dependencies:** PostgreSQL 18 runtime and controlled migrations.
- **Security boundary:** Roles, grants, views, RLS, and purpose checks limit access.
- **Forbidden responsibilities:** Store full telemetry or act as unrestricted Runtime business access.
- **Failure behavior:** Product operations fail explicitly and recover from durable state.
- **Idempotency:** Keys, versions, leases, and receipts control retries.
- **Observability:** Record database health and correlation metadata, not full telemetry.
- **Related ADRs:** ADR-0002, ADR-0005, ADR-0011, ADR-0018, ADR-0019, ADR-0028.
- **Open issues:** Runtime role names, retention, backup frequency, RPO, and RTO remain open.

<a id="protected-file-archive"></a>

### Protected File Archive

- **DSL identifier:** `fileArchive`;
- **Display name:** Protected File Archive.
- **Purpose:** Preserve original source and upload bytes with hashes and manifests.
- **Responsibilities:** Store immutable bytes and return controlled references.
- **Inputs:** Approved source or upload bytes and metadata.
- **Outputs:** Archive reference and read-only bytes for approved consumers.
- **Owned state:** Immutable source and upload objects, hashes, and manifests.
- **Dependencies:** Protected mounted filesystem or compatible object storage.
- **Security boundary:** Access is restricted and references do not grant broad listing.
- **Forbidden responsibilities:** Act as a query database, execute content, or overwrite history.
- **Failure behavior:** Reject partial writes and return explicit read or integrity failure.
- **Idempotency:** Content hash and source identity prevent duplication.
- **Observability:** Record object reference, hash, size, action, result, and trace ID.
- **Related ADRs:** ADR-0001, ADR-0010, ADR-0011, ADR-0018.
- **Open issues:** Retention, backup frequency, RPO, and RTO remain open.

<a id="input-dataset-contract"></a>

### Input Dataset Contract

- **DSL identifier:** `inputDataset`;
- **Display name:** OrgPilot Input Dataset.
- **Purpose:** Supply versioned source, replay, upload, configuration, and history data.
- **Responsibilities:** Define evaluation input files and versions.
- **Inputs:** Formal evaluation dataset contents.
- **Outputs:** Read-only CSV and JSON files for ingestion, replay, and acceptance.
- **Owned state:** External versioned evaluation data.
- **Dependencies:** Formal dataset and machine-readable contracts.
- **Security boundary:** Product containers mount input read-only.
- **Forbidden responsibilities:** Accept product writes or become product truth after ingestion.
- **Failure behavior:** A missing expected source file creates a `missing` data issue, makes dependent KPIs `null`, and does not stop publication. An invalid dataset root, manifest, or global contract produces a terminal input failure. Invalid source records remain outside the valid snapshot and are reported explicitly.
- **Idempotency:** Dataset version and file hashes identify the input.
- **Observability:** Record version, file hash, read result, and trace ID.
- **Related ADRs:** ADR-0001, ADR-0002, ADR-0004, ADR-0011, ADR-0012.
- **Open issues:** None.

<a id="submission-output-contract"></a>

### Submission Output Contract

- **DSL identifier:** `submissionOutput`;
- **Display name:** Submission Output Directory.
- **Purpose:** Receive approved brief and QA files under `OUTPUT_DIR`.
- **Responsibilities:** Provide the writable evaluator mount for formal output paths.
- **Inputs:** Validated contract files from Submission Exporter.
- **Outputs:** `/briefs/day_XXX/<manager_id>.json` and `/qa/<question_id>.json` below `OUTPUT_DIR`.
- **Owned state:** External output files and their filesystem metadata.
- **Dependencies:** Read-only formal schemas and writable evaluator output mount.
- **Security boundary:** Only resolved contained paths and approved schemas can be written.
- **Forbidden responsibilities:** Accept internal fields, `ChartIntent`, `ChartSpec`, Presentation responses, ECharts options, partial files, or `OUTPUT_DIR/submission/...` paths.
- **Failure behavior:** Export fails without a partial final file and stores an Export Receipt failure.
- **Idempotency:** Relative path, version, and content hash control replacement.
- **Observability:** Record relative path, hash, receipt, result, and trace ID.
- **Related ADRs:** ADR-0011, ADR-0013, ADR-0015.
- **Open issues:** None.

## Container-level Open Issues

- Retention, backup frequency, RPO, and RTO remain open.
- No new value is set for any open decision in this document.
