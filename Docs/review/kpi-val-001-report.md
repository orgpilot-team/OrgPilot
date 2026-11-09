# KPI-VAL-001: Exact order repeats change eight reference KPIs

Validation date: 2026-11-02, Asia/Tehran. Dataset: synthetic ARKA data.

All 55 reference KPI definitions ran in RAW and DEDUP modes. All 30 mornings, 62 through 91, were replayed. No SQL failure remains. The full-data snapshot has **41 numerical differences across 8 KPIs and 4 assigned managers**. The replay has **418 morning/date/dimension differences**. The first difference appears at morning 77, after drop 076.

Calculation parity, source quality, and the accepted order-input rule are separate questions. Mode agreement does not prove business accuracy. No production pipeline or business rule was changed.

The detailed outputs are the [results CSV](kpi-val-001-results.csv) and [evidence JSON](kpi-val-001-evidence.json).

## 1. Execution coverage and failed KPI definitions

The controlling sources are [README_FA.md](../../DataSet/arka_dataset/README_FA.md), [kpi_dictionary.csv](../../DataSet/arka_dataset/config/kpi_dictionary.csv), and [reference_views.sql](../../DataSet/arka_dataset/config/reference_views.sql). All SQL strings were executed without formula changes. Targets, warning limits, critical limits, dimensions, and units were retained. This task did not evaluate alert repetition, escalation, or manager brief selection.

| Phase | Cutoff | Definitions per mode | Scheduled KPI cases | SQL failures |
| --- | --- | --- | --- | --- |
| Smoke | day 090 | 5 | 10 | 0 |
| Full | day 090 | 55 | 110 | 0 |
| Replay | day 061–090 | 55 × 30 mornings | 3,300 | 0 |
| Total |  |  | 3,420 | 0 |

Phase 1 used the five core organization KPIs below. Each query returned unique business-date keys. All five have no dimension. Independent checks and the median rank check found no mismatch.

| Smoke KPI | RAW rows | DEDUP rows | Date coverage |
| --- | --- | --- | --- |
| K_ORG_NET_REV | 90 | 90 | All 90 calendar dates |
| K_ORG_REV_MTD_ATTAIN | 90 | 90 | All 90 calendar dates |
| K_ORG_ONTIME | 89 | 89 | No row for 2026-07-23; other 89 dates present |
| K_ORG_CSAT | 90 | 90 | All 90 calendar dates |
| K_ORG_FRT_MED | 90 | 90 | All 90 calendar dates |

The on-time KPI has no row on the first calendar date. Its query groups delivered orders. The CSV marks that key as no_reference_row. It does not replace it with zero.

An initial validation assertion incorrectly required every output date to occur in cal. K_ENT_FC_SLA correctly returns initial CRM history before the calendar starts. Its SQL executed, but that date assertion failed. The assertion was corrected. All 62 full/replay cases for this KPI were repeated. The evidence retains these initial harness errors separately from SQL failures. No reference formula was changed. The final SQL-failure list is empty.

The output retains 40 initial-history dates, starting on 2026-06-13, for each full/replay snapshot. These contribute 1,240 comparison rows. The calendar remains unchanged.

The next table covers all 55 definitions. Row counts are actual reference SQL output at the full-data cutoff. They exclude grid keys added only to record missing query rows.

| KPI ID | Owner | Dimension | RAW rows | DEDUP rows | Different full keys |
| --- | --- | --- | --- | --- | --- |
| K_ORG_NET_REV | M01 | none | 90 | 90 | 4 |
| K_ORG_REV_MTD_ATTAIN | M01 | none | 90 | 90 | 15 |
| K_ORG_ONTIME | M01 | none | 89 | 89 | 0 |
| K_ORG_CSAT | M01 | none | 90 | 90 | 0 |
| K_ORG_FRT_MED | M01 | none | 90 | 90 | 0 |
| K_ORG_ORDERS | M01 | none | 90 | 90 | 1 |
| K_WF1_SLA | M01 | none | 89 | 89 | 0 |
| K_WF2_SLA | M01 | none | 89 | 89 | 0 |
| K_WF3_SLA_7D | M01 | none | 90 | 90 | 0 |
| K_SAL_B2C_REV | M02 | none | 90 | 90 | 4 |
| K_SAL_CONV | M02 | none | 90 | 90 | 1 |
| K_SAL_PAYFAIL | M02 | none | 90 | 90 | 0 |
| K_SAL_PAYFAIL_BY_CH | M02 | channel | 196 | 196 | 0 |
| K_ENT_FC_SLA | M05 | none | 130 | 130 | 0 |
| K_ENT_WINRATE_30D | M05 | none | 90 | 90 | 0 |
| K_ENT_PIPELINE | M05 | none | 90 | 90 | 0 |
| K_ENT_CONTRACT_MTD | M05 | none | 90 | 90 | 0 |
| K_TASK_OVERDUE_T_ENT | M05 | none | 90 | 90 | 0 |
| K_DIG_LEADS | M06 | none | 90 | 90 | 0 |
| K_DIG_CPL_7D | M06 | none | 90 | 90 | 0 |
| K_DIG_SPEND | M06 | none | 90 | 90 | 0 |
| K_TASK_OVERDUE_T_DIG | M06 | none | 90 | 90 | 0 |
| K_MKT_ORDERS | M11 | none | 16 | 16 | 1 |
| K_MKT_REV | M11 | none | 16 | 16 | 1 |
| K_TASK_OVERDUE_T_MKT | M11 | none | 90 | 90 | 0 |
| K_OPS_ONTIME | M03 | none | 89 | 89 | 0 |
| K_OPS_PICK_MED | M03 | none | 90 | 90 | 0 |
| K_WH_PICK_MED | M07 | none | 90 | 90 | 0 |
| K_WH_PICK_12H_PCT | M07 | none | 90 | 90 | 0 |
| K_WH_BACKLOG | M07 | none | 90 | 90 | 0 |
| K_WH_DAMAGE_RATE | M07 | none | 89 | 89 | 0 |
| K_WH_DAMAGE_BY_CAT_7D | M07 | category | 534 | 534 | 14 |
| K_WH_INSPECT_MED | M07 | none | 88 | 88 | 0 |
| K_TASK_OVERDUE_T_WH | M07 | none | 90 | 90 | 0 |
| K_SHP_HANDOVER_MED | M08 | none | 90 | 90 | 0 |
| K_SHP_ONTIME | M08 | none | 89 | 89 | 0 |
| K_SHP_ONTIME_BY_CITY | M08 | city | 533 | 533 | 0 |
| K_SHP_DELIV_DAYS_MED | M08 | none | 89 | 89 | 0 |
| K_TASK_OVERDUE_T_SHP | M08 | none | 90 | 90 | 0 |
| K_SUP_FRT_MED | M04 | none | 90 | 90 | 0 |
| K_SUP_CSAT | M04 | none | 90 | 90 | 0 |
| K_SUP_TICKETS | M04 | none | 90 | 90 | 0 |
| K_SUP_BACKLOG | M04 | none | 90 | 90 | 0 |
| K_RSP_FRT_MED | M09 | none | 90 | 90 | 0 |
| K_RSP_FRT_2H_PCT | M09 | none | 90 | 90 | 0 |
| K_RSP_TICKETS | M09 | none | 90 | 90 | 0 |
| K_RSP_TICKETS_BY_CAT | M09 | category | 268 | 268 | 0 |
| K_RSP_BACKLOG | M09 | none | 90 | 90 | 0 |
| K_RSP_CSAT | M09 | none | 90 | 90 | 0 |
| K_TASK_OVERDUE_T_RSP | M09 | none | 90 | 90 | 0 |
| K_CMP_RES_48H_PCT | M10 | none | 89 | 89 | 0 |
| K_CMP_RES_MED | M10 | none | 89 | 89 | 0 |
| K_CMP_TICKETS | M10 | none | 90 | 90 | 0 |
| K_CMP_BACKLOG | M10 | none | 90 | 90 | 0 |
| K_TASK_OVERDUE_T_CMP | M10 | none | 90 | 90 | 0 |

## 2. Raw vs deduplicated numerical comparisons

RAW exposes every delivered order row. DEDUP excludes only order payloads whose original CSV fields are completely identical to an earlier delivered payload. Comparison occurs before numeric conversion. Source path, CSV line, and delivery day are excluded from payload equality. No business-key-only deduplication was used.

Every other input is identical between modes. All delivered order, ticket, CRM, and task event rows remain. Comparisons use the same phase, report morning, KPI, business date, and dimension value.

| Comparison class | Smoke | Full | Replay |
| --- | --- | --- | --- |
| equal_numeric | 430 | 5961 | 148134 |
| different | 19 | 41 | 418 |
| no_reference_row | 1 | 338 | 8405 |
| unavailable | 0 | 0 | 1848 |
| future_business_date | 0 | 0 | 10407 |

The full-data run has 6,002 numeric comparison keys: 5,961 agree and 41 differ. Another 338 keys have no row in either reference output. No full-data result is a SQL NULL. These counts do not prove source completeness.

The CSV has **176,002 comparison rows**: 450 smoke rows, 6,340 full-data rows, and 169,212 replay rows. Each wide row contains both modes.

- raw_sql_value and dedup_sql_value retain executed query values.
- raw_value and dedup_value contain reportable values under the stated availability policy.
- raw_reference_row and dedup_reference_row distinguish absent query rows from returned NULLs.
- raw_status and dedup_status identify numeric values, missing sources, future dates, absent query rows, and SQL failures.
- raw_minus_dedup uses the decimal representations of the SQL outputs. It adds no KPI rounding. Percentage-unit differences are percentage points.
- business_date_scope identifies initial CRM history, the current calendar period, or a future business date.

An empty numeric cell is not zero. Read its status and row-presence flag. Grid rows record missing query keys; they do not claim that SQL returned those rows. Dimensional grids use dimension values known in the current output union. They do not invent future categories.

## 3. KPI differences by date and manager

All full-data differences belong to these eight definitions:

| Changed KPI | Owner | Different keys | Largest absolute difference | Reference unit |
| --- | --- | --- | --- | --- |
| K_ORG_NET_REV | M01 | 4 | 340.2 | میلیون تومان |
| K_ORG_REV_MTD_ATTAIN | M01 | 15 | 3.7 | % |
| K_ORG_ORDERS | M01 | 1 | 262 | عدد |
| K_SAL_B2C_REV | M02 | 4 | 340.2 | میلیون تومان |
| K_SAL_CONV | M02 | 1 | 1.46 | % |
| K_MKT_ORDERS | M11 | 1 | 27 | عدد |
| K_MKT_REV | M11 | 1 | 40.8 | میلیون تومان |
| K_WH_DAMAGE_BY_CAT_7D | M07 | 14 | 0.61 | % |

Forty-seven definitions have no RAW/DEDUP numerical difference in the full-data run. Agreement shows only that this order-input change did not change their output.

The next table uses morning 91. Zero means a verified zero mode difference for that KPI/date. It is not a substituted KPI value.

| Business date | Organization net difference, million toman | MTD attainment difference, percentage points | Changed warehouse category keys |
| --- | --- | --- | --- |
| 2026-10-06 | 340.2 | 3.7 | 0 |
| 2026-10-07 | 0.8 | 3.5 | 0 |
| 2026-10-08 | 0 | 3.3 | 2 |
| 2026-10-09 | 0 | 3 | 2 |
| 2026-10-10 | -2 | 2.9 | 2 |
| 2026-10-11 | 0 | 2.7 | 2 |
| 2026-10-12 | -7 | 2.5 | 2 |
| 2026-10-13 | 0 | 2.4 | 2 |
| 2026-10-14 | 0 | 2.3 | 2 |
| 2026-10-15 | 0 | 2.2 | 0 |
| 2026-10-16 | 0 | 2.1 | 0 |
| 2026-10-17 | 0 | 2 | 0 |
| 2026-10-18 | 0 | 2 | 0 |
| 2026-10-19 | 0 | 1.9 | 0 |
| 2026-10-20 | 0 | 1.8 | 0 |

Manager grouping uses owner_manager_id from the KPI dictionary. It does not copy each KPI to parent managers. The CSV records whether the owner is active on the report morning, using org/managers.csv. All definitions were calculated even before an assigned manager became active. This is validation coverage, not a generated manager brief.

| Assigned manager | Full differences | Replay differences | KPI IDs |
| --- | --- | --- | --- |
| M01 | 20 | 184 | K_ORG_NET_REV, K_ORG_ORDERS, K_ORG_REV_MTD_ATTAIN |
| M02 | 5 | 64 | K_SAL_B2C_REV, K_SAL_CONV |
| M07 | 14 | 140 | K_WH_DAMAGE_BY_CAT_7D |
| M11 | 2 | 30 | K_MKT_ORDERS, K_MKT_REV |

Mornings 62 through 76 have no mode difference. Later replay counts are:

| Morning | Last drop | Different historical keys |
| --- | --- | --- |
| 77 | 76 | 7 |
| 78 | 77 | 10 |
| 79 | 78 | 13 |
| 80 | 79 | 16 |
| 81 | 80 | 21 |
| 82 | 81 | 24 |
| 83 | 82 | 29 |
| 84 | 83 | 32 |
| 85 | 84 | 35 |
| 86 | 85 | 36 |
| 87 | 86 | 37 |
| 88 | 87 | 38 |
| 89 | 88 | 39 |
| 90 | 89 | 40 |
| 91 | 90 | 41 |

These counts describe each morning snapshot. Do not sum financial differences across mornings. A historical amount can occur in several snapshots.

## 4. Financial and operational impact

The next diagnostic uses exact underlying amounts in toman, before KPI conversion and rounding. It joins paid/refunded order events to the two order inputs.

| Exact diagnostic | RAW, toman | DEDUP, toman | Difference, toman |
| --- | --- | --- | --- |
| Paid gross | 45,260,316,000 | 44,912,862,000 | 347,454,000 |
| Refund subtraction | 2,219,316,000 | 2,203,922,000 | 15,394,000 |
| B2C paid less refunds | 43,041,000,000 | 42,708,940,000 | 332,060,000 |

The gross difference is **347,454,000 toman**. Repeated order rows also increase refund subtraction by **15,394,000 toman**. The B2C net difference is **332,060,000 toman**. Gross payment is not final net revenue.

The reference organization net KPI also includes B2B contract values. Those inputs are identical between modes. Their equality does not establish CRM business-rule correctness. The independent smoke check reproduced organization revenue, including the current correction rule.

Actual daily net KPI outputs are below. Their reference SQL already rounds to 0.1 million toman.

| KPI | Date | RAW | DEDUP | Difference, million toman |
| --- | --- | --- | --- | --- |
| K_ORG_NET_REV | 2026-10-06 | 889.1 | 548.9 | 340.2 |
| K_ORG_NET_REV | 2026-10-07 | 598.6 | 597.8 | 0.8 |
| K_ORG_NET_REV | 2026-10-10 | 377.5 | 379.5 | -2 |
| K_ORG_NET_REV | 2026-10-12 | 572.4 | 579.4 | -7 |
| K_SAL_B2C_REV | 2026-10-06 | 861.5 | 521.3 | 340.2 |
| K_SAL_B2C_REV | 2026-10-07 | 569 | 568.2 | 0.8 |
| K_SAL_B2C_REV | 2026-10-10 | 274.9 | 276.9 | -2 |
| K_SAL_B2C_REV | 2026-10-12 | 530 | 537 | -7 |

The four rounded daily organization differences total 332.0 million toman. The exact B2C diagnostic difference is 332.06 million toman. This follows from separate daily rounding. It does not identify a missing event.

| Full-data KPI/date | RAW | DEDUP | Difference |
| --- | --- | --- | --- |
| Organization orders, 2026-10-06 | 699 | 437 | 262 orders |
| Sales conversion, 2026-10-06 | 3.89% | 2.43% | 1.46 percentage points |
| Marketplace orders, 2026-10-06 | 70 | 43 | 27 orders |
| Marketplace net revenue, 2026-10-06 | 97.8 million toman | 57.0 million toman | 40.8 million toman |
| Organization MTD attainment, 2026-10-06 | 101.7% | 98.0% | 3.7 percentage points |
| Organization MTD attainment, 2026-10-20 | 94.6% | 92.8% | 1.8 percentage points |

The October 6 attainment output moves from above the existing 100% target to below it. This observation does not change the target or select an alert policy.

K_WH_DAMAGE_BY_CAT_7D changes at 14 keys: two categories over seven dates, October 8 through 14. The categories are ظروف شیشه‌ای و آشپزخانه and کتاب و لوازم تحریر. For the first category on October 9, RAW is 3.03% and DEDUP is 2.42%. The difference is 0.61 percentage points.

Its numerator joins tickets to orders. The denominator uses grouped order facts. Repeated order rows can therefore increase the defect-rate numerator without the same increase in the denominator.

Order-fact-only metrics, including order medians, do not change. The view groups by order_id and takes MAX event timestamps. Current duplicate payloads are identical, so those fact fields collapse to the same values. This result does not justify removing event history.

## 5. Data-quality incident: duplicate orders on day 076

Sources: [day 076 orders](../../DataSet/arka_dataset/drops/day_076/orders.csv), [day 076 manifest](../../DataSet/arka_dataset/drops/day_076/manifest.json), and [reference_views.sql](../../DataSet/arka_dataset/config/reference_views.sql).

The complete order input has 37,851 rows. DEDUP retains 37,589 payloads and excludes 262 exact repeated occurrences from the analytical input. All exclusions occur within day 076. Its order file has 699 raw rows and 437 distinct payloads. The manifest correctly declares 699 rows. Manifest agreement does not prove unique order grain.

Every affected order ID occurs twice with identical original field values. There are no conflicting payloads or cross-day order repeats in these files. The evidence records each retained and excluded source path, CSV line, and manifest day. For example, O031155 occurs at lines 2 and 3 in the day 076 file. Neither source occurrence was deleted.

RAW produces two order matches for each event of an affected order. The revenue_daily SUM counts the paid value or refund subtraction twice. Its reference SQL does not deduplicate orders. The paired results confirm financial and operational effects. No event history was deduplicated.

A repeated partial export is consistent with the records and the README warning. Exporter logs are absent. The exporter mechanism remains a hypothesis. The confirmed issue is repeated analytical order grain in RAW.

## 6. Historical availability and missing-source findings

Each exposed source relation uses manifest.drop_day <= report_morning - 1. Folder numbers and manifest days agree. The 90 dated manifests agree with the calendar. Actual CSV file sets and row counts match their manifests.

Source files were read into isolated SQLite memory. Only cutoff-filtered relations were exposed to reference views. Cached facts were rebuilt after every cutoff or mode change. Reading later files for validation did not make them eligible for an earlier calculation.

### Missing support delivery

[Day 066 manifest](../../DataSet/arka_dataset/drops/day_066/manifest.json) and its directory omit tickets.csv, ticket_events.csv, and csat.csv. At morning 67, support-dependent outputs have status unavailable_missing_support. Raw SQL values remain for audit. Reportable values are empty.

This validation uses a conservative source-level mask for all historical outputs of the 20 support-dependent KPIs in that one snapshot. It masks 1,848 comparison keys, or 3,696 mode values. The README requires NULL for unavailable data and a data issue. It does not specify this exact historical invalidation boundary.

The broad mask is a disclosed validation safeguard. It does not claim that every earlier value is wrong. A narrower mask needs checked dependencies and engineer approval.

Affected definitions:

- K_ORG_CSAT
- K_ORG_FRT_MED
- K_WF2_SLA
- K_WH_DAMAGE_RATE
- K_WH_DAMAGE_BY_CAT_7D
- K_WH_INSPECT_MED
- K_SUP_FRT_MED
- K_SUP_CSAT
- K_SUP_TICKETS
- K_SUP_BACKLOG
- K_RSP_FRT_MED
- K_RSP_FRT_2H_PCT
- K_RSP_TICKETS
- K_RSP_TICKETS_BY_CAT
- K_RSP_BACKLOG
- K_RSP_CSAT
- K_CMP_RES_48H_PCT
- K_CMP_RES_MED
- K_CMP_TICKETS
- K_CMP_BACKLOG

[Day 067](../../DataSet/arka_dataset/drops/day_067/manifest.json) contains 104 tickets, 229 ticket events, and 25 CSAT rows dated 2026-09-26, the day 066 business date. They become available at morning 68. They were not admitted to morning 67.

Later delivery is verified. Completeness against an independent source total is not verified. After this observed backfill, the validation calculates on delivered rows. It does not certify source completeness.

### CRM correction availability

CRM events expose drop_day from verified manifest metadata. The original at timestamp remains unchanged. The correction subquery retains its reference ORDER BY drop_day DESC rule.

| Morning | Last drop | L02045 contract value, toman |
| --- | --- | --- |
| 64 | 63 | NULL |
| 65 | 64 | 27,300,000 |
| 70 | 69 | 27,300,000 |
| 71 | 70 | 15,000,000 |

The day 070 correction changes L02045 from 27,300,000 to 15,000,000 toman. It first appears at morning 71. Its event timestamp equals the original won timestamp. Event-date filtering alone would leak that correction into earlier reports. Delivery cutoffs are applied before fact calculation.

### Schema and date boundaries

The [calendar](../../DataSet/arka_dataset/calendar/calendar_days.csv) is exposed as cal, with date named d. Its other fields and all 90 rows are retained.

Some calendar joins return future-date zero rows in an early snapshot. The CSV preserves those SQL outputs. It marks 10,407 replay keys as future_business_date. Reportable values and deltas are empty. These keys are excluded from numerical agreement counts.

Initial CRM dates before the calendar are valid reference output. Their scope is initial_crm_history. They are separate from future dates.

From day 082, tickets.create_time is exposed as created_at. ticket_events.event_time is exposed as at. These aliases exist only in memory. The source inventory retains original headers. Header checks cover every delivered CSV.

## 7. Calculation parity evidence

The validation used Python 3.13.15 and SQLite 3.50.4. The database and temporary storage were in memory. No package was installed. No persistent database was created.

A connection-local median aggregate ignores NULL inputs. It returns the middle value for an odd sample and the mean of the middle two for an even sample. Empty and all-NULL inputs return NULL. Boundary tests covered empty, all-NULL, odd, even, mixed-NULL, negative, and fractional samples.

Original julianday expressions, division order, filters, grouping, and SQLite ROUND calls were preserved. Python datetime differences and Python round were not substituted.

| Check | Scope | Result |
| --- | --- | --- |
| View cache parity | Five reference views in both modes at smoke cutoff | 10 direct/cached row-set hashes agree |
| Independent organization revenue | Both modes, 90 dates | No mismatch |
| Independent organization MTD attainment | Both modes, 90 dates | No mismatch |
| Independent on-time calculation | Both modes, 89 dates | No mismatch |
| Independent CSAT calculation | Both modes, 90 dates | No mismatch |
| Median vs ranked SQL middle-value calculation | 92 KPI cases, 6,916 date groups | No rounded mismatch |
| Full-data run vs replay morning 91 | All 55 KPIs in both modes | 110 result hashes agree |
| Before duplicate delivery | Replay mornings 62–76 | No numerical mode difference |

Median checks cover smoke FRT, all nine full-run median definitions, and replay cutoffs 66, 69, 70, and 82. Ranked SQL uses the same samples. It tests median selection and final rounding. It does not independently prove source quality.

For speed, original view outputs were materialized once per cutoff and mode, in memory. Each cache contains the exact SELECT output of that reference view. Direct and cached row-set hashes were checked at the smoke cutoff. All KPI SQL strings remain unchanged.

The independent revenue check uses Python source-event joins and CRM correction selection. SQLite still performs final reference arithmetic and rounding. The on-time and CSAT checks use source records rather than cached facts.

Every raw input row retains source path, CSV line, and delivery day in the memory backing tables. The evidence exports 1,079 CSV inventory entries. Each includes original headers, row count, delivery day, and SHA-256 hash. All order exclusions retain their matching source coordinates.

The exact calculation and correction programs are embedded in the evidence. They reproduce numerical outputs without an additional script deliverable. Final file checks verify that pre-existing workspace files outside the Python environment are unchanged. This includes source data, SQL, KPI files, manifests, and prior RCA outputs.

Calculation parity does not prove input quality or business-rule correctness. Those limits remain even when the two modes agree.

## 8. Remaining uncertainties

- **Accepted order-input rule:** Both modes were authorized for comparison. The supplied documents do not select the accepted derived order grain for evaluation.
- **Support completeness:** Later delivery of day 066 records is verified. Independent expected source totals are absent.
- **Historical invalidation scope:** This task uses a broad morning 67 support mask. It does not prove the minimal affected set for all earlier dates and dimensions.
- **Correction ties:** The data has one value correction. It does not test conflicting same-lead corrections in one delivery. No secondary rule was invented.
- **Hidden data and other engines:** Tests cover supplied records and the local SQLite build. They do not prove parity for another engine or hidden dataset.
- **Business meaning:** No independent ground-truth labels prove that every unchanged formula, event, threshold, or definition is correct.

The mode differences are verified calculation results. A repeated exporter mechanism is a hypothesis. The accepted production input mode remains unknown.

## 9. Decisions requiring engineer approval

These concern later implementation. No production pipeline is authorized or implemented by this validation.

| ID | Engineering decision | Evidence | Potential options |
| --- | --- | --- | --- |
| E1 | Select the production execution method. | Section 7; reference SQL and parity checks. | Retain a tested SQLite aggregate and input types. Approve another method only after parity checks. |
| E2 | Define precise source availability and historical invalidation. | Section 6; withheld morning 67 keys and later delivery. | Retain a broad source-level hold, or approve a checked dependency-based scope. Keep missing data separate from zero. |
| E3 | Design the order-input control after Q1. | Sections 2–5; 262 exact repeats and eight changed KPIs. | Preserve RAW with an explicit issue, or expose approved exact-repeat exclusion. Preserve source rows, lineage, and event histories. |

The report cutoff, calendar mapping, observed timestamp aliases, and current correction delivery order are supported by existing documentation and records. They do not require new business rules.

## 10. Questions genuinely requiring project support

**Q1: Which order-input grain must be supplied to the unchanged KPI SQL after an exact repeated export?**

For day 076, must orders retain 699 raw rows or expose 437 distinct payloads? Specify the accepted input mode or an expected reference result. This choice changes eight KPI outputs. The exact B2C paid-minus-refund diagnostic changes by 332,060,000 toman.

Owner: project support. Evidence: the README KPI contract, day 076 records and manifest, the unchanged revenue view, and these paired results. The comparison selects neither mode as a production business rule.

No support question is raised for the calendar mapping, median formula, documented cutoff, observed schema aliases, or current correction ordering. Their evidence is sufficient. Hypothetical future cases remain limits rather than active support requests.

The investigation is complete. No source record was removed. No KPI formula, threshold, production component, commit, or push was changed.

