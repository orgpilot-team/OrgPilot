# RCA-001: Data and SQL investigation

Investigation date: 2026-11-02, Asia/Tehran. Data cutoff: drop 090, 2026-10-20.
The supplied data is synthetic. This investigation does not change source data, SQL, KPI definitions, or business rules.

## 1. Executive summary

The calendar interface is documented. The README requires `cal` to expose `calendar_days.csv` with `date` named `d`. All required fields exist. The calendar has 90 unique consecutive dates. There is no verified calendar data defect.

The CRM view requires delivery metadata that the raw CSV does not contain. Its query fails on `x.drop_day`. One correction for lead L02045 arrived in drop 070, six days after its event date. It reduces the contract value by 12,300,000 toman. The README already defines which morning can use it.

The local SQLite 3.50.4 connection does not contain `median()`. Nine KPI definitions require it. Three methods agree across 806 KPI/date groups when they use the same SQL input values and SQLite rounding. Python timestamp arithmetic changes eight rounded KPI/date outputs. A method change can therefore change reference results.

The order files contain 262 extra exact rows. All occur in `day_076/orders.csv`. A raw paid-event join increases diagnostic gross by 347,454,000 toman. The B2C diagnostic amount after refund subtraction increases by 332,060,000 toman. These amounts are different measures.

The day 066 support files are absent. Day 067 contains records dated day 066. Support timestamp names also change from day 082. Both conditions need delivery and schema lineage.

There are **5 engineering decisions** and **1 project-support question**. No option has been selected or implemented.

## 2. Sources and methods

The controlling sources are [README_FA.md](../../DataSet/arka_dataset/README_FA.md), [kpi_dictionary.csv](../../DataSet/arka_dataset/config/kpi_dictionary.csv), [reference_views.sql](../../DataSet/arka_dataset/config/reference_views.sql), the calendar, the original drop files, and their manifests. The [project brief](../%D8%A8%D8%B1%DB%8C%D9%81%20%D9%BE%D8%B1%D9%88%DA%98%D9%87%20%D8%A8%D9%88%D8%AA%DA%A9%D9%85%D9%BE%20_%20%D8%AF%D8%B3%D8%AA%DB%8C%D8%A7%D8%B1%20%D8%A7%DB%8C%D8%AC%D9%86%D8%AA%DB%8C%DA%A9%20%D9%85%D8%AF%DB%8C%D8%B1%D8%A7%D9%86%20%D8%B3%D8%A7%D8%B2%D9%85%D8%A7%D9%86%DB%8C%20_%20%D8%AF%DB%8C%D8%AF%D8%B1%D8%A7%D9%87.pdf) was also examined. Its pages 14 and 17 classify late records, historical corrections, repeated exports, and schema changes as data issues. Page 16 requires agreement with reference queries. These pages do not supply an order deduplication rule or a same-drop correction tie rule.

The investigation excluded `dataset/explore_data.py` as an authority. It did not use prior audit reports or generated profiles as proof. No web source, package installation, download, persistent database, commit, or push was used.

Python 3.13.15, its standard library, SQLite 3.50.4, and the installed pandas 3.1.0 performed the diagnostics. The installed Python 3.14 PDF reader extracted the project brief. CSV values were read without source normalization. Empty numeric values became SQL NULL only in diagnostic memory tables. Header aliases and aggregate registration existed only in the isolated diagnostic connection. They are experiments, not installed fixes.

The evidence file stores complete source hashes, duplicate row locations, CRM event records, SQL checks, median group results, and the exact Python diagnostic program. To repeat the checks, execute `reproduction.python_code` from this workspace with the existing Python environment. The program reads source files and prints a compact result. It creates tables only in `:memory:`. The supplied source hashes identify the checked inputs. Source line numbers are one-based CSV record lines, including the header.

Status terms: **verified** means that a source rule or executed check supports the statement. **Hypothesis** means that the mechanism has not been proved. **Unknown** means that the supplied material does not resolve the statement. Confidence describes the evidence coverage, not a probability.

## 3. Calendar RCA

### CAL-01: The README defines cal and the date alias.

- Status: verified.
- Evidence: [dataset/README_FA.md:54-57](../../DataSet/arka_dataset/README_FA.md); [dataset/config/reference_views.sql:45-45](../../DataSet/arka_dataset/config/reference_views.sql); [dataset/calendar/calendar_days.csv:1-2](../../DataSet/arka_dataset/calendar/calendar_days.csv).
- Reproduction: Search every UTF-8 original dataset file for the word cal. Exclude explore_data.py. Extract c.<column> from each KPI SQL string.
- Impact: 23 KPI definitions directly need cal. revenue_daily also needs it. Loading the CSV with its original date name does not meet the SQL interface.
- Confidence: High: explicit source rule and complete local search.
- Decision owner: A. ENGINEERING (E1).
- Potential options: Expose an in-memory or future loader alias named d. Expose a future relation or adapter that preserves all calendar columns. Do not change the reference SQL.

The full original dataset text search found 25 lines that contain the word `cal`: 23 KPI rows, the README prerequisite, and the `revenue_daily` reference. It found no explicit CREATE TABLE, CREATE VIEW, or CTE definition for `cal`. The absence of DDL does not mean that the calendar contract is absent.

The exact direct column requirements are below. The evidence JSON also retains each full SQL string and source line.

| KPI ID | Dictionary line | Expected cal columns |
| --- | ---: | --- |
| K_ORG_REV_MTD_ATTAIN | 3 | `d`, `day_in_month`, `jmonth`, `mdays` |
| K_ORG_ORDERS | 7 | `d` |
| K_WF3_SLA_7D | 10 | `d` |
| K_ENT_WINRATE_30D | 16 | `d` |
| K_ENT_PIPELINE | 17 | `d` |
| K_ENT_CONTRACT_MTD | 18 | `d`, `jmonth` |
| K_TASK_OVERDUE_T_ENT | 19 | `d` |
| K_DIG_CPL_7D | 21 | `d` |
| K_TASK_OVERDUE_T_DIG | 23 | `d` |
| K_TASK_OVERDUE_T_MKT | 26 | `d` |
| K_WH_BACKLOG | 31 | `d` |
| K_WH_DAMAGE_RATE | 32 | `d` |
| K_WH_DAMAGE_BY_CAT_7D | 33 | `d` |
| K_TASK_OVERDUE_T_WH | 35 | `d` |
| K_TASK_OVERDUE_T_SHP | 40 | `d` |
| K_SUP_TICKETS | 43 | `d` |
| K_SUP_BACKLOG | 44 | `d` |
| K_RSP_TICKETS | 47 | `d` |
| K_RSP_BACKLOG | 49 | `d` |
| K_TASK_OVERDUE_T_RSP | 51 | `d` |
| K_CMP_TICKETS | 54 | `d` |
| K_CMP_BACKLOG | 55 | `d` |
| K_TASK_OVERDUE_T_CMP | 56 | `d` |

`revenue_daily`, at SQL line 45, needs `cal.d`. The complete union of direct SQL requirements is `d, jmonth, day_in_month, mdays`. Only `d` requires a name mapping. The other fields already exist. No derived month length or calendar conversion is required by the supplied SQL. The remaining CSV fields are `day_idx, jdate, iwd, is_holiday`. Their absence from the direct queries is not permission to remove them.

Possible interpretations are a loader relation, an adapter view, or a query-time alias. All must expose the same documented column meanings. The investigation does not select the mechanism.

### CAL-02: Calendar coverage meets the documented 90-day input period.

- Status: verified.
- Evidence: [dataset/calendar/calendar_days.csv:1-91](../../DataSet/arka_dataset/calendar/calendar_days.csv); [dataset/README_FA.md:7-16](../../DataSet/arka_dataset/README_FA.md); [dataset/config/monthly_targets.csv](../../DataSet/arka_dataset/config/monthly_targets.csv).
- Reproduction: Parse ISO dates; compare the set with each date from minimum to maximum; check day_idx sequence and all numbered manifest dates.
- Impact: No date gap or duplicate explains the cal failure. Morning 91 uses drop 90. The initial CRM history is outside the calendar by design.
- Confidence: High: all 90 calendar rows and 90 dated manifests checked.
- Decision owner: C. NO DECISION REQUIRED.
- Potential options: Use the supplied date and month boundaries. Do not add day 000 or morning 91 to business-date coverage without a new requirement.

| Check | Verified result |
| --- | --- |
| Schema | date, day_idx, jdate, jmonth, day_in_month, mdays, iwd, is_holiday |
| Rows / unique dates / unique day indices | 90 / 90 / 90 |
| Date limits | 2026-07-23 through 2026-10-20, inclusive |
| Missing dates / empty cells | 0 / 0 |
| Day-index sequence | 1 through 90, in order |
| Manifest/calendar date differences | 0 |
| Supplied months | 1405-05: 31 days; 1405-06: 31 days; 1405-07: 28 supplied days |
| Monthly target coverage | All three supplied jmonth values exist in monthly_targets |

The last month is a partial observation month. Its supplied `mdays=30` must remain the MTD denominator. The observed count of 28 must not replace it. Initial CRM leads have creation times from 2026-06-13 through 2026-07-22. The README assigns these to initial history, not to missing calendar dates. Morning 91 is 2026-10-21; it reports with drops through 90. A business-date row for morning 91 is not needed to report day 90.

## 4. Drop-day RCA

### CRM-01: The raw CRM event schema omits the delivery field used by lead_fact.

- Status: verified.
- Evidence: [dataset/config/reference_views.sql:20-32](../../DataSet/arka_dataset/config/reference_views.sql); [dataset/drops/day_070/crm_lead_events.csv:1-1](../../DataSet/arka_dataset/drops/day_070/crm_lead_events.csv); [dataset/drops/day_070/manifest.json:2-3](../../DataSet/arka_dataset/drops/day_070/manifest.json).
- Reproduction: Compare every CRM event header. Execute the original lead_fact definition against the raw event columns in an isolated memory database.
- Impact: The view query fails with no such column: x.drop_day. Event time cannot replace delivery time.
- Confidence: High: header scan and SQL failure reproduced.
- Decision owner: A. ENGINEERING (E2).
- Potential options: Retain manifest drop_day and source row coordinates in a future ingestion layer. Use folder numbers only after checking their agreement with manifests. Apply the documented cutoff before building facts.

Every CRM event file has the same four columns: `lead_id, event, at, contract_value_toman`. None has `drop_day`. The folder number and manifest `drop_day` supply delivery order. The manifest date supplies the delivery date, except for `day_000`, whose date is `initial_load`. The 90 dated manifests agree with the calendar. There is no record-level ingestion timestamp, correction version, or unique CRM event ID.

The reference subquery orders corrections by `drop_day DESC`. That rule is explicit. It does not order by `at`. The missing field is a technical interface dependency, not an unresolved business precedence rule.

### CRM-02: One correction arrives six days late and changes earlier revenue after it becomes available.

- Status: verified.
- Evidence: [dataset/drops/day_064/crm_lead_events.csv:8-8](../../DataSet/arka_dataset/drops/day_064/crm_lead_events.csv); [dataset/drops/day_070/crm_lead_events.csv:50-50](../../DataSet/arka_dataset/drops/day_070/crm_lead_events.csv); [dataset/README_FA.md:16-16](../../DataSet/arka_dataset/README_FA.md); [dataset/config/reference_views.sql:28-31](../../DataSet/arka_dataset/config/reference_views.sql); [dataset/config/reference_views.sql:43-45](../../DataSet/arka_dataset/config/reference_views.sql).
- Reproduction: Group value_corrected rows by lead; compare delivery date with event date; run the original lead_fact select at event cutoffs 63,64,69,70,90 in memory.
- Impact: L02045 changes from 27,300,000 to 15,000,000 toman. Morning reports 65 through 70 must not use this correction. It first becomes available in morning 71. revenue_daily assigns it to the won date, 2026-09-24.
- Confidence: High: complete correction scan and target-lead SQL checks.
- Decision owner: C. NO DECISION REQUIRED.
- Potential options: Preserve the original morning cutoff when reproducing a report. A later report can reflect the correction on the original won date under the reference SQL. Do not overwrite a prior report as part of this task.

The full scan contains 6,208 CRM event rows. There is one `value_corrected` row, for one lead. The correction value is non-NULL. No other CRM row has a nonzero delivery-date lag.

| L02045 event | Source drop | Event time | Value, toman | Source CSV line |
| --- | ---: | --- | ---: | ---: |
| first_contact | 048 | 2026-09-08 19:49:27 | NULL | 43 |
| qualified | 051 | 2026-09-11 16:49:42 | NULL | 31 |
| proposal_sent | 055 | 2026-09-15 18:07:23 | NULL | 20 |
| won | 064 | 2026-09-24 19:36:25 | 27,300,000 | 8 |
| value_corrected | 070 | 2026-09-24 19:36:25 | 15,000,000 | 50 |

Each row is in `dataset/drops/day_XXX/crm_lead_events.csv` for the stated drop. The won and corrected timestamps are identical. They do not show when the correction was issued. Delivery day resolves availability.

The original lead-view SQL was run in memory with delivery metadata added only to the diagnostic input. It returned:

| Last available drop | Morning report | won_at | Contract value, toman |
| ---: | ---: | --- | ---: |
| 63 | 64 | NULL | NULL |
| 64 | 65 | 2026-09-24 19:36:25 | 27,300,000 |
| 69 | 70 | 2026-09-24 19:36:25 | 27,300,000 |
| 70 | 71 | 2026-09-24 19:36:25 | 15,000,000 |
| 90 | 91 | 2026-09-24 19:36:25 | 15,000,000 |

Calculation: `15,000,000 - 27,300,000 = -12,300,000` toman. This is a correction to total contract value. The reference `COALESCE` selects the correction value instead of adding a correction delta. The B2B revenue CTE groups it by `date(won_at)`, so a later snapshot can revise the September 24 revenue bucket and its MTD totals. It does not book a separate September 30 delta.

For morning R, the README permits only drops 000 through R-1. Morning 65 through 70 must retain the original known contract value. Morning 71 can use the corrected value. Filtering only `at <= report_date` would incorrectly admit the later correction to an earlier report. Retaining a full-history fact and then filtering its output date would have the same risk. Recompute or select facts from the permitted input snapshot before using the reference formulas. This is an existing requirement, not a new reporting policy.

The target-lead experiment loads all lead base rows but filters CRM events at each cutoff. L02045 exists before all tested cutoffs. These results verify this lead only; they are not a full replay of all reports.

### CRM-03: The supplied rows do not test multiple-correction precedence.

- Status: unknown.
- Evidence: [dataset/config/reference_views.sql:28-31](../../DataSet/arka_dataset/config/reference_views.sql); [dataset/drops/day_070/crm_lead_events.csv:50-50](../../DataSet/arka_dataset/drops/day_070/crm_lead_events.csv).
- Reproduction: Count correction rows per lead and per lead/drop. Inspect all event fields and the ORDER BY clause.
- Impact: There is one correction and no observed tie. Same-drop corrections with different values would have no documented secondary order. at is an effective event timestamp, not proof of correction issue order.
- Confidence: High for the absence of observed ties; the intended tied-case behavior is unknown.
- Decision owner: A. ENGINEERING (E2).
- Potential options: Detect and report a tied correction if one occurs. Do not use row position, value size, or at as business precedence without evidence. Seek a support rule only if a real or required tied case remains.

There are zero leads with two corrections and zero same-lead/same-drop correction ties. No current record forces a choice between conflicting corrections. For a hypothetical tie, the SQL has no secondary ordering key. CSV position is source lineage, not a documented correction priority. A latest NULL correction would fall back to the won amount through `COALESCE`; it would not automatically search for an earlier non-NULL correction. No current correction tests that case. Do not invent either a tie rule or a NULL-correction rule.

## 5. Median RCA

### MED-01: The local SQLite build lacks the required median aggregate.

- Status: verified.
- Evidence: [dataset/README_FA.md:54-57](../../DataSet/arka_dataset/README_FA.md); [dataset/config/reference_views.sql:2-2](../../DataSet/arka_dataset/config/reference_views.sql); [dataset/config/kpi_dictionary.csv:6-53](../../DataSet/arka_dataset/config/kpi_dictionary.csv).
- Reproduction: Call median in the unmodified local SQLite connection. Compare an isolated diagnostic aggregate, a ranked SQL middle-row average, and pandas on the same Julian-day samples.
- Impact: Nine KPI definitions cannot run in the unmodified connection. All 806 observed KPI/date groups agree after SQLite rounding when their input expressions stay the same.
- Confidence: High for the tested SQLite build and supplied data. PostgreSQL equivalence was not executed.
- Decision owner: A. ENGINEERING (E3).
- Potential options: Register a compatible aggregate in a future SQLite connection. Use a ranked SQL calculation in an approved execution adapter. Use an external local calculation that preserves SQL filters, NULLs, expressions, and rounding. No option is selected.

| KPI ID | Dictionary line | Daily groups | Non-NULL samples | Odd / even groups |
| --- | ---: | ---: | ---: | --- |
| K_ORG_FRT_MED | 6 | 90 | 5,179 | 35 / 55 |
| K_OPS_PICK_MED | 28 | 90 | 35,282 | 38 / 52 |
| K_WH_PICK_MED | 29 | 90 | 35,282 | 38 / 52 |
| K_WH_INSPECT_MED | 34 | 88 | 1,272 | 44 / 44 |
| K_SHP_HANDOVER_MED | 36 | 90 | 35,226 | 40 / 50 |
| K_SHP_DELIV_DAYS_MED | 39 | 89 | 34,521 | 37 / 52 |
| K_SUP_FRT_MED | 41 | 90 | 5,179 | 35 / 55 |
| K_RSP_FRT_MED | 45 | 90 | 5,179 | 35 / 55 |
| K_CMP_RES_MED | 53 | 89 | 1,791 | 51 / 38 |

There are nine definitions and six distinct formulas. The three FRT definitions use the same query. The two pick-time definitions use the same query. The group total of 806 includes these repeated definitions. It is not a count of independent samples. No observed selected expression is NULL or negative. The actual data therefore does not test NULL handling by itself.

The README and the SQL comment define median as the continuous 0.5 percentile. For numeric values, this means the middle value for an odd count and the mean of the two middle values for an even count. NULL inputs must not enter the numeric count. The isolated aggregate uses `statistics.median`; pandas uses its numeric median; the SQL method ranks non-NULL inputs and averages ranks `(n+1)/2` and `(n+2)/2` with integer division. Each method uses the same per-date selection, the same reference Julian-day expression, and final SQLite `ROUND`.

| Boundary input | Aggregate / ranked SQL / pandas result |
| --- | --- |
| Empty input | NULL / no group row / NULL |
| NULL, NULL | NULL / no non-NULL group row / NULL |
| 1, 3, 9 | 3 / 3 / 3 |
| 1, 3, 9, 11 | 6 / 6 / 6 |
| NULL, 1, 3, NULL | 2 / 2 / 2 |
| -4, -2, 8 | -2 / -2 / -2 |
| 0.1, 0.2, 0.3, 0.4 | 0.25 / 0.25 / 0.25 |

For comparison, the experiment records a missing ranked group as NULL. That lookup does not make the row sets identical. A future adapter must preserve empty and all-NULL group behavior explicitly. These cases were synthetic diagnostics, not inserted source records.

The unmodified local call fails with `no such function: median`. After diagnostic registration, the original median KPI queries execute. No production aggregate, extension, or SQL rewrite was installed. PostgreSQL was not available for execution; its documented equivalent is an option that would need engine-specific parity checks. No engine choice is made.

### MED-02: Equivalent median selection does not guarantee equivalent timestamp arithmetic or rounding.

- Status: verified.
- Evidence: [dataset/config/kpi_dictionary.csv:6-6](../../DataSet/arka_dataset/config/kpi_dictionary.csv); [dataset/config/kpi_dictionary.csv:39-39](../../DataSet/arka_dataset/config/kpi_dictionary.csv); [dataset/config/kpi_dictionary.csv:53-53](../../DataSet/arka_dataset/config/kpi_dictionary.csv).
- Reproduction: Compare SQLite julianday differences with Python datetime differences; apply final SQLite ROUND in both paths. Test empty, all-NULL, odd, even, mixed-NULL, negative, and fractional samples.
- Impact: Native datetime arithmetic changes 8 KPI/date outputs across the repeated FRT definitions and complaint resolution. Rounding with Python can also differ. The final delivery-days formula divides by 24 before final rounding.
- Confidence: High: actual rounded differences and boundary experiments retained.
- Decision owner: A. ENGINEERING (E3).
- Potential options: Preserve the reference Julian-day expression and SQLite rounding. Require explicit parity evidence before any engine or timestamp method change.

The largest observed difference between a Julian-day median and a Python datetime median is about `1.05e-8` hours. The difference is small, but it can cross a rounding boundary.

| Formula | Date | Reference rounded value | Native datetime value after SQLite rounding |
| --- | --- | ---: | ---: |
| FRT: K_ORG_FRT_MED, K_SUP_FRT_MED, K_RSP_FRT_MED | 2026-08-18 | 1.99 | 2.00 |
| FRT: same three definitions | 2026-09-17 | 2.35 | 2.34 |
| K_CMP_RES_MED | 2026-08-11 | 32.40 | 32.41 |
| K_CMP_RES_MED | 2026-08-28 | 25.28 | 25.27 |

These are four formula/date cases and eight KPI/date outputs. For example, the first reference median is `1.994999997317791` hours. The exact-duration method yields a value at the rounding boundary. Python `round(1.125,2)` returns 1.12; this SQLite build returns 1.13. Thus, moving only the rounding step can also change results.

For `K_SHP_DELIV_DAYS_MED`, the formula is `ROUND(median(hours)/24,2)`. The division occurs before the final rounding. Rounding the hours first is not equivalent. Computing the median of days directly gave no rounded difference on the current samples, but this does not establish parity for all floating-point boundary cases. Timestamp parsing, timezone conversion, missing start timestamps, integer division, and early rounding must remain visible in any later comparison. The CSV timestamps have no explicit timezone offsets; the experiment does not assign them a new timezone.

## 6. Duplicate orders RCA

### ORD-01: One delivery contains 262 extra exact order rows.

- Status: verified.
- Evidence: [dataset/drops/day_076/orders.csv:1-700](../../DataSet/arka_dataset/drops/day_076/orders.csv); [dataset/drops/day_076/manifest.json](../../DataSet/arka_dataset/drops/day_076/manifest.json).
- Reproduction: Count full-row tuples and order_id groups across all order deliveries. Record every duplicate row path and line. Compare business-key groups with exact-row groups.
- Impact: There are 37,851 raw rows and 37,589 order IDs. All duplicate keys have identical source values. All 262 extra rows occur within day 076; there are no cross-day order duplicates.
- Confidence: High: complete scan, row locations, and matching manifest count.
- Decision owner: C. NO DECISION REQUIRED.
- Potential options: Retain the raw rows as evidence. Treat repeated-export origin as a hypothesis; source generator logs are not supplied.

| Order input check | Result |
| --- | ---: |
| Raw rows | 37,851 |
| Unique order IDs | 37,589 |
| Duplicate order IDs | 262 |
| Extra exact rows | 262 |
| Extra business-key rows | 262 |
| Conflicting duplicate IDs | 0 |
| Cross-day duplicate IDs | 0 |
| day 076 raw / unique rows | 699 / 437 |
| day 076 manifest row count | 699 |
| Duplicate IDs with a paid event | 255 |
| Duplicate IDs with a refund event | 12 |

Every duplicate ID occurs twice. The 524 affected row occurrences are all in one file. There are 229 adjacent duplicate pairs; the other pairs are also within that delivery. For example, O031155 appears at lines 2 and 3, and O031405 appears at lines 5 and 6. The evidence JSON contains every affected ID, row, path, and line. Manifest agreement confirms the export row count; it does not establish unique order grain.

A repeated export of part of the delivery is consistent with these rows and the documented class of data issues. The actual exporter mechanism is unknown. No generator or operational export log was supplied.

### ORD-02: Raw order joins inflate both payments and refund subtraction.

- Status: verified.
- Evidence: [dataset/config/reference_views.sql:36-45](../../DataSet/arka_dataset/config/reference_views.sql); [dataset/drops/day_076/orders.csv](../../DataSet/arka_dataset/drops/day_076/orders.csv); [dataset/drops](../../DataSet/arka_dataset/drops) (day_*/order_events.csv); [dataset/README_FA.md:54-57](../../DataSet/arka_dataset/README_FA.md).
- Reproduction: Compute paid event gross with Python counters and independent SQLite joins. Repeat with full-row DISTINCT only inside the diagnostic query. Repeat the B2C paid-minus-refunded expression.
- Impact: Gross rises by 347,454,000 toman with raw order rows. Refund subtraction rises by 15,394,000 toman. The B2C net diagnostic difference is 332,060,000 toman. The input relation to the authoritative SQL needs an acceptance rule.
- Confidence: High for the diagnostic sums; accepted deduplication behavior is unknown.
- Decision owner: B. PROJECT SUPPORT (Q1); engineering work depends on E5.
- Potential options: Confirm that the reference orders relation contains raw rows. Confirm that exact repeated exports must be excluded from the reference input. Preserve the source and reference SQL in either case.

| Diagnostic measure, all delivered events through day 090 | Raw orders, toman | Full-row DISTINCT diagnostic, toman | Difference, toman |
| --- | ---: | ---: | ---: |
| Paid-event gross | 45,260,316,000 | 44,912,862,000 | 347,454,000 |
| Refund amount subtracted | 2,219,316,000 | 2,203,922,000 | 15,394,000 |
| B2C paid less refunds | 43,041,000,000 | 42,708,940,000 | 332,060,000 |

Python calculates gross as `sum(order_value * paid_event_count)` over the order rows. The independent SQLite check is:

```sql
SELECT SUM(o.order_value_toman)
FROM orders o JOIN order_events e USING(order_id)
WHERE e.event='paid';
```

The comparison query uses `(SELECT DISTINCT * FROM orders)` in the same join. DISTINCT is confined to the diagnostic query. No order row was removed. The B2C comparison uses the exact reference expression: `SUM(CASE WHEN event='paid' THEN order_value_toman ELSE -amount_toman END)` over paid and refunded events.

| Event date | Extra gross, toman | Extra refund subtraction, toman |
| --- | ---: | ---: |
| 2026-10-06 | 345,279,000 | 5,061,000 |
| 2026-10-07 | 2,175,000 | 1,350,000 |
| 2026-10-10 | 0 | 2,016,000 |
| 2026-10-12 | 0 | 6,967,000 |

The extra gross also affects marketplace revenue: its gross component is 43,117,000 toman; web and app gross components are 167,971,000 and 136,366,000 toman. Refunds must still be applied to the relevant channel before a net comparison.

Diagnostic paid gross is not the final net revenue KPI. `revenue_daily` subtracts B2C refunds, adds B2B contract values, aligns dates to `cal`, and feeds rounded daily or MTD KPI formulas. The table isolates the B2C join effect. It is not a certified organization net revenue result. The CRM correction also changes B2B values at later cutoffs.

The README warns that exports can repeat. The brief says to report duplicate output as a data issue. Neither states whether exact order repeats must be excluded before the authoritative reference SQL runs. The SQL itself does not deduplicate the `orders` input to `revenue_daily`. Q1 asks for the expected input contract; it does not ask to change the KPI formula.

### ORD-03: order_fact removes repeated keys after the join, but raw-order KPIs still count them.

- Status: verified.
- Evidence: [dataset/config/reference_views.sql:3-12](../../DataSet/arka_dataset/config/reference_views.sql); [dataset/config/kpi_dictionary.csv:7-7](../../DataSet/arka_dataset/config/kpi_dictionary.csv); [dataset/config/kpi_dictionary.csv:12-12](../../DataSet/arka_dataset/config/kpi_dictionary.csv); [dataset/config/kpi_dictionary.csv:24-24](../../DataSet/arka_dataset/config/kpi_dictionary.csv); [dataset/config/kpi_dictionary.csv:33-33](../../DataSet/arka_dataset/config/kpi_dictionary.csv).
- Reproduction: Count left-join rows before and after a full-row DISTINCT diagnostic; count grouped order_fact rows. Scan event tuples and order/event keys.
- Impact: The raw left join produces 146,054 rows versus 145,027 in the diagnostic. GROUP BY order_id returns 37,589 rows. MAX event timestamps stay the same for current exact duplicates. COUNT on orders and the damage-category ticket/orders join can still be inflated.
- Confidence: High for current exact duplicates. Conflicting future order versions are not tested.
- Decision owner: C. NO DECISION REQUIRED.
- Potential options: Keep distinct event types for an order. Do not remove event rows just because the same order_id occurs more than once. Inspect future conflicting order versions separately.

`order_fact` first joins each order row to each matching event. It then groups by order_id. The current exact duplicate values and MAX event timestamps therefore collapse to one fact row per order. Intermediate join size increases by 1,027 rows, but these MAX fields do not increase. This protection does not apply to the SUM in `revenue_daily`.

The raw-order paths include `K_ORG_ORDERS`, `K_SAL_CONV`, `K_MKT_ORDERS`, and the ticket/orders join in `K_WH_DAMAGE_BY_CAT_7D`. In the last query, duplicate order rows can multiply matching ticket rows in the numerator while the delivered denominator comes from grouped `order_fact`. The exact financial diagnostic does not quantify that separate damage-rate effect.

There are 145,022 order event rows. They have zero extra exact event rows, zero repeated `(order_id,event)` pairs, and zero orders with multiple paid events. Multiple different event types for one order are valid lifecycle records in the README. Dropping those records by order_id would remove history. The current evidence does not require a rule for repeated instances of the same event type. If conflicting future order versions arrive, the bare `o.*` fields in a grouped view require a separate review; that conflict is absent here.

## 7. Cross-cutting risks

### CROSS-01: The day 066 support gap is followed by dated records in day 067.

- Status: verified.
- Evidence: [dataset/drops/day_066/manifest.json](../../DataSet/arka_dataset/drops/day_066/manifest.json); [dataset/drops/day_067/manifest.json](../../DataSet/arka_dataset/drops/day_067/manifest.json); [dataset/drops/day_067/tickets.csv:2-4](../../DataSet/arka_dataset/drops/day_067/tickets.csv); [dataset/drops/day_067/ticket_events.csv:9-11](../../DataSet/arka_dataset/drops/day_067/ticket_events.csv); [dataset/drops/day_067/csat.csv:2-4](../../DataSet/arka_dataset/drops/day_067/csat.csv); [dataset/README_FA.md:41-51](../../DataSet/arka_dataset/README_FA.md); [dataset/README_FA.md:89-91](../../DataSet/arka_dataset/README_FA.md).
- Reproduction: Compare expected source files with each manifest and directory. Group support rows dated 2026-09-26 by their actual delivery drop.
- Impact: Day 067 contains 104 tickets, 229 ticket events, and 25 CSAT rows dated day 066. They are unavailable for morning 67 and available for morning 68. Event-date-only reconstruction would leak these rows into morning 67. Completeness against an independent source total is not known.
- Confidence: High for missing files and delivered rows; full source completeness is unknown.
- Decision owner: C. NO DECISION REQUIRED.
- Potential options: Report the unavailable source and NULL affected values as required by the README. Retain delivery metadata when later records arrive. Do not infer a zero from a missing file.

The day 066 manifest and directory both omit `tickets.csv, ticket_events.csv, csat.csv`. The initial day 000 has only CRM files, as documented; its absent non-CRM files are not an incident. All declared CSV row counts agree with the actual files.

All observed support rows dated 2026-09-26 arrive in drop 067: 104 tickets, 229 events, and 25 CSAT rows. The next manifest contains 221 tickets, 459 events, and 58 CSAT rows in total. These counts show later delivery, not an independent guarantee that every source record was recovered. At the full-data cutoff there are no orphan ticket-event IDs and no orphan CSAT records relative to supplied ticket IDs. That check does not prove completeness.

For morning 67, affected support values are unavailable. A calendar LEFT JOIN can return a zero count even though the source is absent. The README requires NULL for unavailable data and a data issue. A later recomputation can use the day 067 records for their original dates, but it must not replace the inputs used to reproduce morning 67. Backlog, response and resolution times, CSAT, SLA, and ticket-based damage metrics can all depend on the delayed records. Other late support events also exist; the evidence file retains delivery-lag distributions. A complete response-time series is not proof that each morning had complete data.

### CROSS-02: Two support timestamp columns change at day 082.

- Status: verified.
- Evidence: [dataset/drops/day_081/tickets.csv:1-1](../../DataSet/arka_dataset/drops/day_081/tickets.csv); [dataset/drops/day_082/tickets.csv:1-1](../../DataSet/arka_dataset/drops/day_082/tickets.csv); [dataset/drops/day_081/ticket_events.csv:1-1](../../DataSet/arka_dataset/drops/day_081/ticket_events.csv); [dataset/drops/day_082/ticket_events.csv:1-1](../../DataSet/arka_dataset/drops/day_082/ticket_events.csv); [dataset/config/reference_views.sql:14-19](../../DataSet/arka_dataset/config/reference_views.sql).
- Reproduction: Compare every delivered CSV header. Count rows under each changed schema. Use aliases only within the temporary median experiment.
- Impact: tickets.created_at becomes create_time for 745 rows. ticket_events.at becomes event_time for 1,692 rows. Ignoring the new fields loses support times and can bias medians, backlog, SLA, and damage-rate metrics.
- Confidence: High: all delivered headers checked.
- Decision owner: A. ENGINEERING (E4).
- Potential options: Use a version-aware alias adapter in a future loader. Detect the source columns and expose the established reference names. Keep original names and provenance.

The header scan found no other schema transition in the delivered table families. The median experiment maps the two changed names only in memory. The order schema and CRM event schema do not change at day 082. Thus, this support change does not explain the missing CRM delivery field or the duplicate order rows. It can still affect ticket-based warehouse metrics.

Delivery provenance must remain attached to every record: source path, source row, manifest drop_day, manifest date, original header, and event timestamp. These are technical lineage fields. Event date determines the business bucket; delivery cutoff determines when the record can be used. Both are necessary for the CRM correction and the support backfill. Calendar joins and valid median arithmetic do not repair an unavailable source or a multiplied join.

A historical report and a later view of the same business date can therefore differ for valid reasons. The existing README resolves historical input availability. This investigation does not define a new historical restatement product or a new business policy.

## 8. Verified facts vs hypotheses vs unknowns

| Class | Statement | Evidence or limit |
| --- | --- | --- |
| Verified | cal requires the documented date-to-d alias. | CAL-01; README line 56. |
| Verified | The supplied calendar has no date gaps or duplicate dates. | CAL-02; all 90 rows. |
| Verified | lead_fact queries a delivery column absent from every raw CRM event header. | CRM-01; reproduced SQLite error. |
| Verified | One correction arrives six days late; no multiple corrections exist. | CRM-02 and CRM-03; full event scan. |
| Verified | Local median support is absent; same-input alternatives agree. | MED-01; 806 groups and boundary tests. |
| Verified | Native datetime arithmetic changes eight rounded KPI/date values. | MED-02; retained differences. |
| Verified | Exact duplicate order rows multiply the raw revenue join. | ORD-01 through ORD-03; Python and SQL agree. |
| Verified | Support data dated day 066 is delivered in day 067. | CROSS-01; exact source records. |
| Verified | Support timestamp column names change on day 082. | CROSS-02; all delivered headers. |
| Hypothesis | An exporter repeated part of the day 076 order output. | Consistent with exact repeats; exporter logs are absent. |
| Hypothesis | A loader was intended to add drop_day from delivery metadata. | The reference requires it and manifests provide it; loader implementation is not supplied as an authority. |
| Unknown | Whether accepted reference input must retain or exclude exact repeated order exports. | No input deduplication rule found; Q1. |
| Unknown | Required result for two conflicting corrections in the same drop. | No observed case or secondary SQL ordering rule. Conditional future gap only. |
| Unknown | Whether all source support records were recovered after day 066. | Later records exist, but independent expected source totals are absent. |
| Unknown | Bit-for-bit parity on a different SQL engine or hidden data. | Only installed local tools and supplied data were tested. |

Every finding's evidence, method, impact, confidence, decision owner, and options appear in its numbered section and in `findings` in the evidence JSON. Hypotheses are not accepted root causes.

## 9. Engineering decisions requiring approval

No decision below authorizes implementation. These are five distinct choices for an engineer to approve after this investigation.

| ID | Technical choice | Evidence | Potential options and limits |
| --- | --- | --- | --- |
| E1 | How to expose the documented cal interface. | CAL-01, CAL-02. | Loader alias or adapter relation. Keep the documented dates and month fields. |
| E2 | How to retain delivery lineage and enforce report cutoffs before fact calculation. | CRM-01 to CRM-03; CROSS-01. | Snapshot-filtered inputs or an equivalent versioned representation. Retain missing-source state and reject or flag unresolved ties. The cutoff rule is already fixed. |
| E3 | How to supply a compatible median execution method. | MED-01, MED-02. | Compatible aggregate, SQL execution adapter, or local calculation. Preserve reference arithmetic, NULL behavior, grouping, and SQLite rounding. No engine change is selected. |
| E4 | How to map versioned support timestamp fields. | CROSS-02. | Version-aware mapping or checked header-based mapping. Preserve the original names in lineage. |
| E5 | How to enforce the accepted order-input grain after Q1 is answered. | ORD-01 to ORD-03; Q1. | If raw rows are required, retain them and expose the known issue. If exact-repeat exclusion is required, design an idempotent derived input while preserving raw records. Do not suppress legitimate lifecycle events. |

## 10. Questions genuinely requiring project support

**Q1: What is the accepted input contract for exact repeated order exports?**

For drop 076, must the `orders` relation supplied to the reference queries contain all 699 raw rows, or 437 distinct order records? The reference revenue SQL returns different values for these inputs. The README requires the SQL result, warns of repeated exports, and requires a data issue, but does not specify the input grain after repeated delivery. Please specify this acceptance rule without changing the KPI formula.

Owner: project support. Evidence: ORD-01, ORD-02, the README KPI contract, and project brief pages 14, 16, and 17. Impact: 347,454,000 toman in diagnostic gross and 332,060,000 toman in the isolated B2C net calculation across supplied events. Options: raw input with the issue recorded, or approved exact-repeat exclusion in a derived input. No option is assumed.

No support question is needed for the calendar alias, dialect, report cutoff, correction amount semantics, missing-source reporting, or the observed support column names. Their evidence is sufficient. The hypothetical correction tie is recorded as a limit. It is not an active support request for this dataset.

## 11. Recommended next investigation steps

1. Resolve Q1 with the expected input grain or an accepted result for drop 076. Stop this step when the reference-input contract is explicit.
2. Before an approved implementation, prepare parity cases for E3. Include the four timestamp-rounding cases above, empty and all-NULL groups, even samples, and the division order for delivery days. Stop when the selected method reproduces the unchanged reference expressions.
3. After approval for further work, replay morning 67 and 68 with their permitted deliveries. Trace the delayed support rows to ticket counts, medians, backlog, CSAT, and damage metrics. Do not use drop 067 rows in morning 67.
4. If a future dataset contains multiple same-drop corrections or conflicting order versions, collect those exact rows and any source sequence field before asking for a new precedence rule. Do not derive priority from file position.

The investigation ends with this report and its evidence JSON. No fix, source rewrite, SQL edit, KPI change, or business decision has been applied.

