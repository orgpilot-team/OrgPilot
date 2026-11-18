# Architecture Registry

State: **Draft / Pending Review**. Tasks: `ARCH-REG-001` extraction; `ARCH-REG-002` semantic audit. Date: 2026-11-09. Time zone: `Asia/Tehran`.

The team designates this Registry as the documentation location for architecture decisions, unresolved issues, risks, acceptance tests and traceability. ARCH-DOC-004 approves a source-preserving structural reorganization only. This designation approves no Open choice, Proposed mechanism, inferred link, missing contract or product test result. The former combined file has been removed after its content and references were checked. Use the current roadmap and Registry records.

## Files and responsibilities

| File | Responsibility |
|---|---|
| [decisions-registry.md](decisions-registry.md) | All 17 ADRs, with numbered status statements, source extracts, consequences, source roles and closure gates. |
| [open-issues-registry.md](open-issues-registry.md) | All 19 DLs and ten temporary Registry issues. Facets retain semantic differences within each main issue. |
| [risk-register.md](risk-register.md) | 20 risks; controls, pending evidence and unassessed severity. Risks stay separate from issues. |
| [acceptance-register.md](acceptance-register.md) | All 30 ATs, full source criteria, shared supplements, management-level matrix, rule cases and delivery checks. |
| [traceability-matrix.csv](traceability-matrix.csv) | Generated source/record/relationship index. It is not a second decision authority. |
| [source-inventory.md](source-inventory.md) | S01-S19 members, authority, missing evidence and source limits. |
| [deduplication-ledger.md](deduplication-ledger.md) | Explicit duplicate placements and their main records. |
| [preflight.json](preflight.json) | Initial Git state, 141 prior untracked files and source hashes. Registry files are excluded from this initial inventory. |
| [untracked-source-dependencies.csv](untracked-source-dependencies.csv) | Untracked source dependencies and all 141 preserved untracked files. |
| [extraction-summary.json](extraction-summary.json) | Counts from the generated records. |
| [validation-report.md](validation-report.md) | Extraction checks, limits, remaining conflicts and baseline comparison. |
| [validation-results.json](validation-results.json) | Machine-readable documentation checks and new-file hashes. |
| [baseline-comparison.csv](baseline-comparison.csv) | Initial-source hashes, final hashes and every new Registry file. |
| [capture_preflight.py](capture_preflight.py), [build_registry.py](build_registry.py), [validate_registry.py](validate_registry.py) | Local documentation extraction/check scripts. They execute no product tests and write only in this folder. |

## Status rules

- `Requirement`: an explicit applicable brief or dataset contract rule.
- `Accepted`: a recorded team choice with clear supporting evidence.
- `Proposed`: an unapproved option or engineering mechanism.
- `Open`: an unresolved choice, conflict or evidence gap.

`Observation` describes source/audit evidence. It is not a decision approval status. `Evidence Pending` means the required evidence is absent. It does not turn a Requirement or Accepted boundary into Open. A source question or ADR can contain several independent status statements. Repeated text and a target model alone do not prove approval.

The five Accepted boundaries remain fixed: one bounded Agent; PostgreSQL-only product execution; independent valid-report publication; deterministic calculation/Signal/authorization/final validation; human-controlled organizational decisions. S16, S19 and document 003 section 1 support these boundaries. Original approver names and approval dates are absent. Unapproved technical details stay separate.

## Closure

An issue needs the applicable source answer or recorded team decision, the named policy/contract version, and inspectable evidence for its linked acceptance gate. Organizer/source questions need an answer from the relevant authority. Engineering gates need actual product receipts. A document check cannot close an issue or pass a product AT. No record is closed by this extraction. No test is Passed.

Route classes are `Team Decision Required`, `Organizer / Source Clarification Required` and `Engineering Evidence Required`. Classes can overlap. Source role names are preserved; no person is appointed. An `Open` statement count differs from an Open issue count because several statements can belong to one issue.

## Source and quotation rules

The extraction baseline is `0a42950d1ce9734433d961540af9ab4be21573b2`. Read [001](../001-system-blueprint.md), [002](../002-data-architecture.md), [003](../003-roadmap.md) and [004](../004-reconciliation-review.md), plus the [S01-S19 inventory](source-inventory.md).

English text provides the Registry index. Full ADRs, DL source rows, risk conditions, AT criteria and supplemental matrices are now readable Markdown. Their original source language, numbers, conditions and exceptions are retained. Relative navigation links are rebased. Other quoted data-model extracts remain historical evidence; 002 keeps the data contracts. Former source links through 003 use its compatibility anchors. The before snapshot and content-location map preserve exact origin evidence.

The existing audit requirement matrix is reused as evidence. Its former source paths remain in `source_ref`; current paths are listed in the source inventory. Audit observations are not rerun calculations. The brief PDF and its conversion are present; no fresh PDF visual audit is claimed.

## CSV contract

Encoding is UTF-8. CSV quoting follows the standard library CSV writer. Each row has one `row_kind`: `record`, `evidence` or `relationship`. A `record` row defines the main identity. Each evidence row adds one source location. Each relationship row has exactly one target. This permits many-to-many relations without positional lists or cross-products. Source-member records use one main Sxx identity and separate evidence rows.

Required columns are retained: `record_id,record_type,title,status,source_file,source_anchor,source_ref,related_adr,related_dl,related_at,related_risk,roadmap_phase,evidence_state`. Extra columns identify row kind, target identity/type, relationship type/status, component, local Registry location and source tracking state. `source_file` is relative to the repository root. `source_anchor` is an existing explicit Markdown anchor, or empty for CSV/DSL/files. `source_ref` identifies a source row, field, page or retained legacy path. `registry_file` is relative to this folder.

`relationship_status=Documented` means that the source explicitly supplies the association. It does not approve the proposed design. `Proposed Relationship` marks an extraction review aid with no explicit source mapping. In particular, risk-to-ADR/DL/AT links are proposed unless a source names them. Empty roadmap cells mean no proven phase assignment. The phase plan stays Proposed.

## Validity limits

This draft has 5 Accepted, 24 Proposed, 24 Open and 16 Requirement statements in the numbered ADR statement tables. Counts include only those explicit rows, not repeated quotations. The full source extracts retain finer conditions. There are 29 Open main issues, including all 19 DLs; route totals overlap. All 30 ATs remain Planned / Not Executed. Severity is Not Assessed for every risk.

ARCH-REG-002 provenance checks and ARCH-REG-003 triage are historical snapshots. ARCH-DOC-004 changes documentation locations and active navigation only. All original records, source conditions and limitations remain. No product implementation, Dataset/SQL/DSL change, commit or push is part of the reorganization.


## Current semantic audit

Read [semantic-audit-report.md](semantic-audit-report.md). The audit keeps this schema and all original record IDs. Five `DEC-*` records now use `Decision Boundary`, with Accepted status. They are not Requirement records. The original audit index has 339 IDs: 334 Requirements and five Accepted boundaries.

All relationship endpoints now have main records. Ten existing DSL elements and seven existing acceptance supplements were missing from the main-record index. Adding their index records creates no architecture component or acceptance requirement. Imported audit mappings are Proposed Relationships unless there is direct source proof. Unsupported removed edges remain in the correction ledger and before snapshot. A source attribution is not a proof of every claim in a referenced document.

The [edge review](audit-ARCH-REG-002/relationship-review.csv) separates Explicit Source Relationship, Proposed / Inferred Relationship, and unsupported edges. The [correction ledger](audit-ARCH-REG-002/corrections.csv) retains before/after values. The [source checks](audit-ARCH-REG-002/source-locator-checks.csv) resolve current paths and source locations. Review scope and limits are stated in the semantic report; automated checks do not constitute exhaustive semantic approval.

Organizer routes are unconditional only for eight issues. Two further routes are conditional. Model/provider/internal-limit choices stay with the team. REG-ISS-010 now needs engineering evidence for historical content comparison; user confirmation resolves current S01 identification. All 29 issues remain Open, all 30 ATs remain Planned / Not Executed, and all 20 risks retain Not Assessed severity.

All earlier generators, audit scripts and validation outputs belong to their recorded snapshots. Do not run an old generator over the reorganized sources. Use the [ARCH-DOC-004 validation](../restructure-ARCH-DOC-004/validate_restructure.py) for the current structure. No old verification result approves the current layout or product.


## Current document responsibilities

| Location | Responsibility |
|---|---|
| [001](../001-system-blueprint.md) | System architecture, modules, Workflows, interfaces and security. |
| [002](../002-data-architecture.md) | Data model, intake, snapshots, canonical calculations and lineage. |
| [003 roadmap](../003-roadmap.md) | Proposed phases, milestones, gates, measured execution and delivery sequence. |
| [004](../004-reconciliation-review.md) | Historical reconciliation, source authority and Q01-Q17 evidence. |
| This Registry | Governance records, full acceptance criteria and traceability. |

Location designation is approved. Record state remains **Draft / Pending Review**. The five Accepted boundaries remain fixed. All 29 issues stay Open. All 30 ATs stay Planned / Not Executed. All 20 risk severities stay Not Assessed. All 2,470 inferred links stay unconfirmed. Source/evaluation contracts are not invented. A navigation update is not an implementation dependency.

The [triage queue](traceability-review-queue.csv), [readiness note](approval-readiness.md) and previous audit reports retain their historical conclusions. The present user approval supersedes only the earlier structural-authorization prerequisite. It does not approve their unresolved semantic content. No earlier audit evidence file is edited.

Read the [reorganization report](../restructure-ARCH-DOC-004/report.md), [complete content-location map](../restructure-ARCH-DOC-004/content-location-map.csv) and [historical reference catalog](../restructure-ARCH-DOC-004/historical-reference-catalog.md).

<a id="source-context"></a>

## Retained source context

The following original text preserves source rules, boundaries and metadata from the former 003. Its document identifier and references to the audit describe that source snapshot. The current Decision Log is [here](open-issues-registry.md#decision-log). The current roadmap is [here](../003-roadmap.md).

### Former 003 source title: ARCH-001: تصمیم‌ها، ریسک‌ها و مسیر پیاده‌سازی

شناسه سند: `003-decisions-and-roadmap`. خانواده مشترک معماری: `ARCH-001`.

تاریخ بازبینی: 2026-11-09. منطقه زمانی: `Asia/Tehran`. برای هر گزاره از Requirement، Accepted، Proposed و Open استفاده کنید. پذیرش موتور اجرا یا مرز انتشار، آزمون‌های پذیرش فنی آن را نمی‌بندد.

این سند را همراه [طرح سیستم](../001-system-blueprint.md)، [معماری داده](../002-data-architecture.md) و [بازبینی Q01-Q17](../004-reconciliation-review.md#question-map) بخوانید. منابع S01-S19 در سند 001 فهرست شده‌اند. این کار فقط مستندات را تغییر می‌دهد و مجوز پیاده‌سازی محصول نیست.

<a id="decisions-1"></a>

## 1. تصمیم‌های ثبت‌شده و طراحی باقی‌مانده

کاربر پنج مرز Accepted را تأیید می‌کند: یک AI Agent با حدود مشخص و ماژول‌های قطعی؛ اجرای محصول فقط با PostgreSQL؛ انتشار مستقل گزارش معتبر هر مدیر؛ محاسبه، تشخیص Signal، مجوزسنجی و Validation نهایی به‌صورت قطعی؛ و تصمیم‌های سازمانی تحت کنترل انسان. این تصمیم‌ها در S16 Q01/Q03/Q16 ثبت شده‌اند. S17 آن‌ها را تأیید می‌کند. پیشنهاد قبلی محاسبه‌گر دوموتوره محصول دیگر گزینه جاری نیست.

رخدادهای منبع، نسخه‌های Snapshot و گزارش‌های منتشرشده حفظ شوند. موفقیت محاسبه، کامل‌بودن منبع، مجازبودن انتشار و پوشش روز از هم جدا بمانند. مرزهای قطعی موجود برای محاسبه، Signal، دسترسی و Validation حفظ شوند. الگوریتم‌های تفصیلی همچنان Proposed هستند، مگر آنکه منبع، تصویب آن‌ها را ثبت کرده باشد.

Decision Log زیر مرجع انتخاب‌های حل‌نشده است. بازبودن آزمون پذیرش، مجوز انتخاب پیش‌فرض مستندنشده نیست.

<a id="decisions-2"></a>

## ۲. موارد روشن که نیاز به اختراع قاعده ندارند

| موضوع | نتیجهٔ مستند |
|---|---|
| cutoff گزارش | صبح R از dropهای تا R-1 استفاده می‌کند؛ S02. |
| پرسش مدیر | روز D از dropهای تا D-1 استفاده می‌کند؛ S02. |
| زمان اثر ورودی | ورودی روز D بر گزارش D+1 اثر دارد؛ S02. اختلاف مورد سازمان در ADR-08 باقی است. |
| تقویم | `date` به `cal.d` نگاشت می‌شود؛ `mdays` عرضه‌شده جایگزین نمی‌شود. |
| CRM | `drop_day` از manifest معتبر می‌آید؛ اصلاح value_corrected، replacement است و به تاریخ won منتسب می‌شود. |
| schema مشاهده‌شده | `create_time -> created_at` و `event_time -> at` با حفظ raw؛ تشخیص بر اساس header. |
| فرمول | ۵۵ تعریف موجود تغییر نمی‌کند؛ عدد LLM یا نمونهٔ بریف جای SQL نیست. |
| نبود داده | `null` و data issue؛ منبع غایب نباید کل گزارش صبح را متوقف کند. |
| تصمیم اجرایی | مدیر تصمیم می‌گیرد؛ سیستم فقط draft وظیفه/پیام و پیگیری می‌سازد. |

انتخاب روش فنی اجرای این موارد هنوز باید review شود. ولی وجود قاعدهٔ اصلی نباید دوباره به یک پرسش کسب‌وکار تبدیل شود.

## Current navigation maintenance

ARCH-DOC-005 repairs navigation only. Use the [cleanup report](../cleanup-ARCH-DOC-005/report.md) for current link checks and the section map. Earlier audit reports, hashes, source paths and generator scripts describe their historical snapshots. Their findings and status records remain evidence. Do not run an earlier extraction script against the current document layout.
