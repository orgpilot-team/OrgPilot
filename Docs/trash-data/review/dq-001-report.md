# DQ-001: Late support records change two historical business dates

Analysis date: 2026-11-02, Asia/Tehran. The ARKA data is synthetic.

## 1. Executive summary

All **20 support-dependent KPIs** have at least one changed historical output when the observed late records arrive. The real morning 68 calculation changes **32 support output keys** from morning 67: seven on day 065 and 25 on day 066. Seventeen existing numeric results change. Fifteen previously absent query rows appear.

The earlier validation masked 1,848 support keys at morning 67. Of these, 1,816 have the same output under the observed supplement. This is not proof of completeness. Seven keys are proved to return no SQL row because the order denominator has no group. The other 1,809 unchanged keys remain unresolved.

**No previously masked numeric value is proved unnecessarily withheld.** This is a limit of the supplied evidence. It does not mean that all earlier values are wrong. In particular, 1,792 keys before day 065 are unchanged by the observed records. No maximum lateness or source closure guarantee proves them complete.

The 35 KPIs without a support dependency remain outside this incident. At morning 67, they provide 2,602 numeric results and 144 absent-query states. The seven independent support no-row states give 2,753 demonstrably unaffected output keys in total.

A dependency-aware policy can distinguish confirmed effects, uncertainty, and independent results. It cannot yet justify releasing every unchanged support value. Three engineering decisions and one source-closure question remain. No policy was approved or implemented.

Files: [impact CSV](dq-001-kpi-impact.csv) and [evidence JSON](dq-001-evidence.json).

## 2. Source and dependency map

Authorities are [README_FA.md](../../DataSet/arka_dataset/README_FA.md), [kpi_dictionary.csv](../../DataSet/arka_dataset/config/kpi_dictionary.csv), and [reference_views.sql](../../DataSet/arka_dataset/config/reference_views.sql). Relevant manifests and source records were read directly. The [RCA report](rca-001-report.md), [KPI validation report](kpi-val-001-report.md), and [prior results CSV](kpi-val-001-results.csv) supplied the previous findings and masking states. They do not replace the original definitions.

The analysis executes all 55 original SQL definitions in five isolated scenarios: 275 successful query cases. It uses SQLite memory, the compatible median aggregate, original julianday expressions, and SQLite ROUND. Calendar date is exposed as d. CRM delivery day comes from manifests. Historical ticket aliases are mapped only in memory.

The original source path, CSV line, delivery day, header, and file hash remain available. Exact source rows admitted from day 067 are recorded for each scenario. No source, reference SQL, KPI file, or previous audit file was changed.

A relation-level dependency is not always a value-level dependency. For example, revenue_daily contains B2C and B2B branches. A KPI selecting only b2b does not acquire a ticket dependency. The evidence separates direct relations, expanded view sources, and projected value sources.

The verified 20-KPI support map is below. The JSON stores each full query, dictionary line, joins, team filters, required event types, date predicates, and snapshot rule.

| KPI | Direct relations | Value source tables | Required event/time fields | Window / output clock |
| --- | --- | --- | --- | --- |
| K_ORG_CSAT | csat | csat | answered_at | answered_at |
| K_ORG_FRT_MED | ticket_fact | ticket_events, tickets | created_at, first_response_at | first_response_at |
| K_WF2_SLA | ticket_fact | ticket_events, tickets | created_at, resolved_at | resolved_at |
| K_WH_DAMAGE_RATE | cal, order_fact, tickets | cal, order_events, orders, tickets | created_at, delivered_at | cal.d |
| K_WH_DAMAGE_BY_CAT_7D | cal, order_fact, orders, tickets | cal, order_events, orders, tickets | created_at, delivered_at | 7 inclusive days; cal.d |
| K_WH_INSPECT_MED | ticket_fact | ticket_events, tickets | first_response_at, inspected_at | inspected_at |
| K_SUP_FRT_MED | ticket_fact | ticket_events, tickets | created_at, first_response_at | first_response_at |
| K_SUP_CSAT | csat | csat | answered_at | answered_at |
| K_SUP_TICKETS | cal, tickets | cal, tickets | created_at | cal.d |
| K_SUP_BACKLOG | cal, ticket_fact | cal, ticket_events, tickets | created_at, resolved_at | 22:00 state; cal.d |
| K_RSP_FRT_MED | ticket_fact | ticket_events, tickets | created_at, first_response_at | first_response_at |
| K_RSP_FRT_2H_PCT | ticket_fact | ticket_events, tickets | created_at, first_response_at | first_response_at |
| K_RSP_TICKETS | cal, tickets | cal, tickets | created_at | cal.d |
| K_RSP_TICKETS_BY_CAT | tickets | tickets | created_at | created_at |
| K_RSP_BACKLOG | cal, ticket_fact | cal, ticket_events, tickets | created_at, first_response_at | 22:00 state; cal.d |
| K_RSP_CSAT | csat, tickets | csat, tickets | answered_at | answered_at |
| K_CMP_RES_48H_PCT | ticket_fact | ticket_events, tickets | created_at, resolved_at | resolved_at |
| K_CMP_RES_MED | ticket_fact | ticket_events, tickets | created_at, resolved_at | resolved_at |
| K_CMP_TICKETS | cal, tickets | cal, tickets | created_at | cal.d |
| K_CMP_BACKLOG | cal, ticket_fact | cal, ticket_events, tickets | created_at, resolved_at | 22:00 state; cal.d |

Important join and time rules:

- ticket_fact starts with tickets LEFT JOIN ticket_events on ticket_id. It computes MIN first response and MAX inspection/resolution. Only the fields projected by a KPI affect its value.
- K_ORG_CSAT and K_SUP_CSAT read csat directly. They do not require ticket_events or tickets.
- K_RSP_CSAT joins csat to tickets. A missing parent ticket can remove an otherwise present CSAT row.
- Ticket counts use creation date. A missing file can therefore produce a false zero through a calendar LEFT JOIN.
- Backlogs use created_at <= d at 22:00 and a missing or later response/resolution. Their dependency is a state test, not a one-day event count.
- Daily damage rate joins the known daily delivered-order denominator to ticket counts by ticket creation date. COALESCE can hide a missing numerator as zero.
- Category damage rate joins tickets to orders, then uses an inclusive seven-day window for each category. A missing ticket created on day t can affect output dates t through t+6 when a denominator group exists.
- Event-date medians and rates group by first response, inspection, or resolution date. Delivery date determines availability, not the output business date.
- MIN/MAX facts can move an entity between groups after later events arrive. A general invalidation policy must follow fact fields and entity joins. A date-only rule is insufficient.

All 55 definitions are covered by this source map:

| KPI | Direct relations | Value source tables | Support dependency |
| --- | --- | --- | --- |
| K_ORG_NET_REV | revenue_daily | cal, crm_lead_events, crm_leads, order_events, orders | no |
| K_ORG_REV_MTD_ATTAIN | cal, monthly_targets, revenue_daily | cal, crm_lead_events, crm_leads, monthly_targets, order_events, orders | no |
| K_ORG_ONTIME | order_fact | order_events, orders | no |
| K_ORG_CSAT | csat | csat | yes |
| K_ORG_FRT_MED | ticket_fact | ticket_events, tickets | yes |
| K_ORG_ORDERS | cal, orders | cal, orders | no |
| K_WF1_SLA | order_fact | order_events, orders | no |
| K_WF2_SLA | ticket_fact | ticket_events, tickets | yes |
| K_WF3_SLA_7D | cal, lead_fact | cal, crm_lead_events, crm_leads | no |
| K_SAL_B2C_REV | revenue_daily | cal, order_events, orders | no |
| K_SAL_CONV | orders, web_sessions | orders, web_sessions | no |
| K_SAL_PAYFAIL | order_fact | order_events, orders | no |
| K_SAL_PAYFAIL_BY_CH | order_fact | order_events, orders | no |
| K_ENT_FC_SLA | lead_fact | crm_lead_events, crm_leads | no |
| K_ENT_WINRATE_30D | cal, lead_fact | cal, crm_lead_events, crm_leads | no |
| K_ENT_PIPELINE | cal, lead_fact | cal, crm_lead_events, crm_leads | no |
| K_ENT_CONTRACT_MTD | cal, revenue_daily | cal, crm_leads, crm_lead_events | no |
| K_TASK_OVERDUE_T_ENT | cal, task_fact | cal, task_events, tasks | no |
| K_DIG_LEADS | mkt_daily | mkt_daily | no |
| K_DIG_CPL_7D | cal, mkt_daily | cal, mkt_daily | no |
| K_DIG_SPEND | mkt_daily | mkt_daily | no |
| K_TASK_OVERDUE_T_DIG | cal, task_fact | cal, task_events, tasks | no |
| K_MKT_ORDERS | orders | orders | no |
| K_MKT_REV | revenue_daily | cal, order_events, orders | no |
| K_TASK_OVERDUE_T_MKT | cal, task_fact | cal, task_events, tasks | no |
| K_OPS_ONTIME | order_fact | order_events, orders | no |
| K_OPS_PICK_MED | order_fact | order_events, orders | no |
| K_WH_PICK_MED | order_fact | order_events, orders | no |
| K_WH_PICK_12H_PCT | order_fact | order_events, orders | no |
| K_WH_BACKLOG | cal, order_fact | cal, order_events, orders | no |
| K_WH_DAMAGE_RATE | cal, order_fact, tickets | cal, order_events, orders, tickets | yes |
| K_WH_DAMAGE_BY_CAT_7D | cal, order_fact, orders, tickets | cal, order_events, orders, tickets | yes |
| K_WH_INSPECT_MED | ticket_fact | ticket_events, tickets | yes |
| K_TASK_OVERDUE_T_WH | cal, task_fact | cal, task_events, tasks | no |
| K_SHP_HANDOVER_MED | order_fact | order_events, orders | no |
| K_SHP_ONTIME | order_fact | order_events, orders | no |
| K_SHP_ONTIME_BY_CITY | order_fact | order_events, orders | no |
| K_SHP_DELIV_DAYS_MED | order_fact | order_events, orders | no |
| K_TASK_OVERDUE_T_SHP | cal, task_fact | cal, task_events, tasks | no |
| K_SUP_FRT_MED | ticket_fact | ticket_events, tickets | yes |
| K_SUP_CSAT | csat | csat | yes |
| K_SUP_TICKETS | cal, tickets | cal, tickets | yes |
| K_SUP_BACKLOG | cal, ticket_fact | cal, ticket_events, tickets | yes |
| K_RSP_FRT_MED | ticket_fact | ticket_events, tickets | yes |
| K_RSP_FRT_2H_PCT | ticket_fact | ticket_events, tickets | yes |
| K_RSP_TICKETS | cal, tickets | cal, tickets | yes |
| K_RSP_TICKETS_BY_CAT | tickets | tickets | yes |
| K_RSP_BACKLOG | cal, ticket_fact | cal, ticket_events, tickets | yes |
| K_RSP_CSAT | csat, tickets | csat, tickets | yes |
| K_TASK_OVERDUE_T_RSP | cal, task_fact | cal, task_events, tasks | no |
| K_CMP_RES_48H_PCT | ticket_fact | ticket_events, tickets | yes |
| K_CMP_RES_MED | ticket_fact | ticket_events, tickets | yes |
| K_CMP_TICKETS | cal, tickets | cal, tickets | yes |
| K_CMP_BACKLOG | cal, ticket_fact | cal, ticket_events, tickets | yes |
| K_TASK_OVERDUE_T_CMP | cal, task_fact | cal, task_events, tasks | no |

The task KPIs assigned to support teams still depend on tasks and task_events. Their team names do not make them dependent on missing ticket files. The calendar is present. Its presence does not certify the support sources.

## 3. Morning 67 availability analysis

Real morning 67 permits only drops 000–066. [Day 066 manifest](../../DataSet/arka_dataset/drops/day_066/manifest.json) and its directory omit tickets.csv, ticket_events.csv, and csat.csv. No support row from day 067 was admitted to the real calculation.

The primary comparison domain contains all reference output keys through business day 066. It includes 40 initial CRM history dates where the original KPI returns them. The unit is one KPI/business-date/dimension key. RAW and DEDUP agree at these cutoffs and are counted once. Repeated KPI definitions are separate definitions, as in the dictionary.

| Classification, morning 67 | Output keys | Numeric results | No SQL row |
| --- | --- | --- | --- |
| Definitely changed by observed late support | 32 | 17 | 15 |
| Demonstrably independent of missing support | 2746 | 2602 | 144 |
| Demonstrably independent no-row gates | 7 | 0 | 7 |
| Unresolved | 1809 | 1733 | 76 |
| Total | 4594 | 4352 | 242 |

The table is an exclusive partition: 32 + 2,746 + 7 + 1,809 = 4,594 keys. The 32 affected keys contain 17 existing numbers and 15 absent query rows that later appear. Do not describe all 32 as existing numeric values at morning 67.

“Demonstrably independent” means independent of these missing support sources. It is not a guarantee against all other data-quality issues. The 1,809 unresolved keys contain 1,733 numeric query results and 76 absent query rows.

The existing query values are retained in reference_sql_result. The illustrative reportable_value column uses a strict evidence standard. It is empty for affected or unresolved support results. This is a review annotation, not an approved production policy. candidate_snapshot_value retains the exact real snapshot value for a possible qualified reporting option.

Unknown missing rows need not have day 066 event dates. The README permits late arrivals without a maximum delay. The supplied files contain no source-closure watermark or independent expected total. Therefore, a rule such as “all dates before day 066 are complete” is not supported.

Seven older events provide direct evidence against a day-066-only hold. They are dated day 065 and arrive in day 067. Their source coordinates are lines 2–8 of [day 067 ticket_events.csv](../../DataSet/arka_dataset/drops/day_067/ticket_events.csv). They comprise two first responses, four resolutions, and one inspection.

These later records show a result change. They do not establish the intended delivery schedule of every record. The files do not independently distinguish outage backfill from ordinary late arrival.

## 4. Morning 68 recovery analysis

Real morning 68 permits drops 000–067. [Day 067 manifest](../../DataSet/arka_dataset/drops/day_067/manifest.json) matches the actual source file counts.

| Day 067 file | Dated day 065 | Dated day 066 | Dated day 067 | Total |
| --- | --- | --- | --- | --- |
| tickets.csv | 0 | 104 | 117 | 221 |
| ticket_events.csv | 7 | 229 | 223 | 459 |
| csat.csv | 0 | 25 | 33 | 58 |
| Total | 7 | 358 | 373 | 738 |

There are 358 records dated day 066, plus seven earlier events: 365 support rows dated through day 066. The remaining 373 support records are dated day 067. The files contain 738 support rows in total.

To isolate source effects, the analysis runs these scenarios:

| Scenario | Non-support cutoff | Extra support | Historical support keys changed from REAL M67 |
| --- | --- | --- | --- |
| REAL_M67 | 066 | none | 0 |
| COUNTERFACTUAL_D066_SUPPORT_IN_M67 | 066 | 358 day 067 rows dated day 066 | 25 |
| COUNTERFACTUAL_EARLIER_SUPPORT_IN_M67 | 066 | 365 day 067 rows dated through day 066 | 32 |
| COUNTERFACTUAL_ALL_D067_SUPPORT_IN_M67 | 066 | all 738 day 067 support rows | 32 |
| REAL_M68 | 067 | real delivery through 067 | 32 |

Every scenario that admits day 067 support into a simulated morning 67 is explicitly COUNTERFACTUAL. Its reportable_value is empty. Its maximum source delivery day is 67 even though the simulated report morning is 67. No counterfactual value is presented as available in real morning 67.

Adding only day 066 records changes 25 keys, all dated day 066. Adding the seven earlier events produces seven more changes on day 065. Adding the normal day 067 support records produces no further change to the historical keys in this dataset. This equality is an observed result, not a general guarantee.

Real morning 68 has these classifications, including its new day 067 output keys:

| Classification, morning 68 | Output keys | Numeric results | No SQL row |
| --- | --- | --- | --- |
| Historical keys changed by observed late support | 32 | 32 | 0 |
| Demonstrably independent of missing support | 2787 | 2641 | 146 |
| Demonstrably independent no-row gates | 7 | 0 | 7 |
| Unresolved | 1837 | 1761 | 76 |
| Total | 4663 | 4434 | 229 |

The 4,663 keys include 69 new-date keys beyond the morning 67 domain. The common historical domain remains 4,594 keys. Within it, the 32 support changes match the isolated earlier-record supplement.

The complete real morning 68 calculation also changes two historical order-payment outputs:

| Unrelated KPI | Business date | Dimension | Morning 67 SQL | Morning 68 SQL |
| --- | --- | --- | --- | --- |
| K_SAL_PAYFAIL | 2026-09-26 | none | 3.36 | 3.52 |
| K_SAL_PAYFAIL_BY_CH | 2026-09-26 | app | 3.8 | 4.11 |

These two changes are independent of support. They are absent from the support-only counterfactuals. Thus, comparing two mornings without source isolation would misattribute 34 historical changes to the support incident.

Backfill is observed. Full source recovery is not proved. A matching day 067 manifest establishes what was delivered, not what should have existed in the missing source. No expected source total was invented.

## 5. KPI-level and business-date-level impacts

The table contains all 32 historical support changes between the two real mornings. “NO SQL ROW” is distinct from SQL NULL and zero. Real morning 68 values are reference calculations on delivered data. They are not completeness certificates.

| KPI | Business date | Dimension | REAL morning 67 SQL | REAL morning 68 SQL | Reference unit |
| --- | --- | --- | --- | --- | --- |
| K_ORG_CSAT | 2026-09-26 | none | NO SQL ROW | 3.84 | از ۵ |
| K_ORG_FRT_MED | 2026-09-25 | none | 13.79 | 14.15 | ساعت |
| K_ORG_FRT_MED | 2026-09-26 | none | NO SQL ROW | 16.98 | ساعت |
| K_WF2_SLA | 2026-09-26 | none | NO SQL ROW | 94.7 | % |
| K_WH_DAMAGE_RATE | 2026-09-26 | none | 0 | 0.94 | % |
| K_WH_DAMAGE_BY_CAT_7D | 2026-09-26 | موبایل و لوازم جانبی | 1.09 | 1.41 | % |
| K_WH_DAMAGE_BY_CAT_7D | 2026-09-26 | پوشاک | 0.81 | 1.14 | % |
| K_WH_DAMAGE_BY_CAT_7D | 2026-09-26 | کتاب و لوازم تحریر | 0.55 | 0.83 | % |
| K_WH_INSPECT_MED | 2026-09-25 | none | 6.5 | 6 | ساعت |
| K_WH_INSPECT_MED | 2026-09-26 | none | NO SQL ROW | 11.5 | ساعت |
| K_SUP_FRT_MED | 2026-09-25 | none | 13.79 | 14.15 | ساعت |
| K_SUP_FRT_MED | 2026-09-26 | none | NO SQL ROW | 16.98 | ساعت |
| K_SUP_CSAT | 2026-09-26 | none | NO SQL ROW | 3.84 | از ۵ |
| K_SUP_TICKETS | 2026-09-26 | none | 0 | 104 | عدد |
| K_SUP_BACKLOG | 2026-09-25 | none | 97 | 94 | عدد |
| K_SUP_BACKLOG | 2026-09-26 | none | 97 | 94 | عدد |
| K_RSP_FRT_MED | 2026-09-25 | none | 13.79 | 14.15 | ساعت |
| K_RSP_FRT_MED | 2026-09-26 | none | NO SQL ROW | 16.98 | ساعت |
| K_RSP_FRT_2H_PCT | 2026-09-26 | none | NO SQL ROW | 0 | % |
| K_RSP_TICKETS | 2026-09-26 | none | 0 | 81 | عدد |
| K_RSP_TICKETS_BY_CAT | 2026-09-26 | سؤال عمومی | NO SQL ROW | 43 | عدد |
| K_RSP_TICKETS_BY_CAT | 2026-09-26 | پرداخت | NO SQL ROW | 6 | عدد |
| K_RSP_TICKETS_BY_CAT | 2026-09-26 | پیگیری سفارش | NO SQL ROW | 16 | عدد |
| K_RSP_TICKETS_BY_CAT | 2026-09-26 | کد تخفیف | NO SQL ROW | 16 | عدد |
| K_RSP_BACKLOG | 2026-09-25 | none | 44 | 42 | عدد |
| K_RSP_BACKLOG | 2026-09-26 | none | 49 | 37 | عدد |
| K_RSP_CSAT | 2026-09-26 | none | NO SQL ROW | 3.82 | از ۵ |
| K_CMP_RES_48H_PCT | 2026-09-26 | none | NO SQL ROW | 94.7 | % |
| K_CMP_RES_MED | 2026-09-25 | none | 25.9 | 25.22 | ساعت |
| K_CMP_RES_MED | 2026-09-26 | none | NO SQL ROW | 28.08 | ساعت |
| K_CMP_TICKETS | 2026-09-26 | none | 0 | 23 | عدد |
| K_CMP_BACKLOG | 2026-09-26 | none | 25 | 33 | عدد |

Each of the 20 support KPIs appears at least once. The seven earlier changes occur in first-response medians, inspection median, complaint resolution median, and the support/response backlogs.

The analysis also compares contributing source populations. It finds 35 changed contributor groups. Three have unchanged rounded output:

| KPI, day 065 | Contributors before | Contributors after | Rounded output changed |
| --- | --- | --- | --- |
| K_WF2_SLA | 14 | 15 | No |
| K_RSP_FRT_2H_PCT | 82 | 84 | No |
| K_CMP_RES_48H_PCT | 14 | 15 | No |

For K_WF2_SLA and K_CMP_RES_48H_PCT, the complaint resolution sample increases from 14 to 15. For K_RSP_FRT_2H_PCT, the response sample increases from 82 to 84. Their unchanged percentages do not show complete inputs.

The seven-day damage window has a wider possible future effect than its current historical differences. Day 066 ticket rows can remain relevant through day 072. Future business dates are not reportable in morning 67. The current experiment does not use them to claim a real historical value.

The impact CSV has 23,039 rows across five scenarios. It contains the source dependency, required timestamps, calendar and lookback fields, reference result, row-presence flag, reportable review value, status, reason, morning, and business date. It also records the prior broad mask and the observed contributor-change flag.

## 6. Cases unnecessarily masked in KPI-VAL-001

The previous validation withheld 1,848 support keys at morning 67. The evidence supports this review:

| Review of prior masked support keys | Exact count |
| --- | --- |
| Changed by the observed historical supplement | 32 |
| Same reference output under that supplement | 1,816 |
| Of the unchanged keys, proved independent no-row states | 7 |
| Other unchanged keys with unresolved completeness | 1,809 |
| Existing numeric outputs among unchanged keys | 1,733 |
| Keys before day 065 unchanged under the observed supplement | 1,792 |
| Numeric values proved unnecessarily withheld | **0** |

The seven no-row states are K_WH_DAMAGE_RATE on 2026-07-23 and K_WH_DAMAGE_BY_CAT_7D on that date for six categories. The known order-derived delivered denominator has no group. Missing ticket rows cannot create an order denominator group.

These states should be described as no reference result row, rather than unavailable support values. They are not seven numeric values to restore. They cannot be replaced with zero without changing output semantics.

The 1,792 earlier keys are unchanged under the selected observed records. Their dates are before day 065. No closed-source rule proves them unaffected by every possible undelivered record. Presenting them as verified complete would overstate the evidence.

The count of zero proved unnecessary numeric holds is not a claim that every old number was invalid. It states that this task lacks sufficient evidence to approve their release as complete values.

## 7. Cases correctly marked unavailable

Morning 67 must not use the day 067 records. The observed late supplement changes 32 support output keys. Withholding these keys was justified.

Examples include:

- Day 066 support ticket count is zero in reference SQL, then 104 after recovery. The initial zero is not proof of no tickets.
- Day 066 warehouse damage rate is 0.00%, then 0.94%. COALESCE made a missing numerator look like zero.
- Day 065 first-response median changes from 13.79 to 14.15 hours. An earlier business date is not sufficient protection.
- Fifteen day 066 query rows are absent in morning 67 and appear in morning 68. Their absence is not a measured zero.

The remaining unresolved support keys were held as a precaution. Their incompleteness is not individually proved. The seven structural no-row states were over-classified as unavailable. The review therefore separates justified holds, unresolved holds, and wrong state labels.

## 8. Missing-data state definitions

| State | Meaning | Reference SQL behavior | Availability handling |
| --- | --- | --- | --- |
| Missing source file | Expected source delivery is absent. | Queries over remaining rows may still return numbers or zeros. | Record the source incident. Assess affected dependency keys. Do not infer a zero from absence. |
| Empty but present file | The source exists with a valid header and zero declared/actual rows. | Aggregates depend on query shape. | It is distinct from an absent file. It is not proof of upstream completeness without a source contract. |
| Valid zero | The calculation returns numeric zero on an eligible known input set. | COUNT or another expression can return 0. | Retain zero with its source status. Do not serialize it as NULL. |
| SQL NULL | SQL returns a row whose value is NULL. | Empty scalar AVG/median or undefined arithmetic can yield NULL. | Keep row presence true and value NULL. |
| No SQL result row | The query returns no group/key. | Empty GROUP BY or an absent inner-join denominator can remove a row. | Keep row presence false. Do not invent zero or a returned NULL row. |
| Late-arriving data | Event/business time precedes delivery time. | Later snapshots may change earlier date outputs. | Use delivery cutoff for availability. Preserve event time for the business bucket. |
| Incomplete or unverified source | Rows exist, but closure/completeness is not established. | Results can be fully reproducible and numerically unchanged. | State the uncertainty. A qualified snapshot value requires accepted reporting semantics. |
| COUNTERFACTUAL | A diagnostic intentionally admits data unavailable at the real cutoff. | Produces a simulated result. | Label it explicitly and never place it in the real reportable column. |

No delivered support file is empty in the supplied source inventory. The empty-file state was tested only as an isolated synthetic diagnostic.

In the state tests, an empty relation returns COUNT(*) = 0, COUNT(x) = 0, SUM/AVG/median = NULL, and no grouped row. An all-NULL row returns COUNT(*) = 1 and a grouped row containing NULL. A numeric-zero row returns a real zero. These are different states.

The CSV uses empty numeric cells for NULL or withheld values. Read reference_row_present, availability_status, and reason to distinguish them. A real zero remains numeric 0.

## 9. Evidence-backed policy options

No option below is selected or implemented.

**P1 — Strict evidence-only review.** Report real results that are independent of the missing support sources. Retain proved no-row states. Hold changed and unresolved support results. The reportable_value column illustrates this option. It does not prescribe a production rule.

**P2 — Qualified delivered-snapshot reporting.** If accepted, show the exact real snapshot result with an explicit incomplete/unverified-source label. candidate_snapshot_value records the candidate value. This option must not describe it as complete. It must never use a counterfactual result.

**P3 — Closure-backed dependency release.** Obtain a source-owned completion signal or a documented lateness/closure contract. Then use field, entity, join, date, and window dependencies to release only closed result keys. The present evidence cannot supply the missing contract.

Evidence-backed rules for an approved design are:

1. Apply the manifest delivery cutoff before building facts and running KPI SQL.
2. Track source presence separately from row count. Keep missing, empty, NULL, no row, zero, and unverified source states distinct.
3. Propagate an incident only through relevant value dependencies. A missing csat file does not invalidate a task KPI.
4. Evaluate output gates first. A known absent order denominator can prove that a damage query has no row regardless of missing tickets.
5. Recompute affected fact fields and entity joins when late rows arrive. Account for MIN/MAX effects and the 22:00 backlog predicates.
6. Use the full lookback interval. A single business-date source issue can affect several rolling output dates.
7. Compare contributor sets as well as rounded results. Equality cannot close a source interval.
8. Preserve old report inputs and statuses. A morning 68 recovery must not be inserted into the real morning 67 record.

A dependency-aware policy can replace the single broad label with these precise states now. Releasing the 1,733 unchanged historical numbers as complete requires additional evidence or an explicitly accepted qualified-value policy.

## 10. Engineering decisions requiring approval

| ID | Decision | Options and evidence |
| --- | --- | --- |
| E1 | Approve the dependency and structural gate model for implementation. | Separate full view execution sources from projected value dependencies. Validate entity joins, event fields, time predicates, and no-row gates. |
| E2 | Approve the source availability state model and historical invalidation scope. | Hold unresolved keys, or release only source-closed dependency intervals. Preserve missing/empty/zero/NULL/no-row distinctions. |
| E3 | Approve any qualified delivered-snapshot reporting method. | Use NULL and a data issue, or show an accepted qualified real snapshot value. Never imply completeness or admit counterfactual data. |

These are proposed implementation choices. No production pipeline, KPI definition, threshold, or previous report was changed.

## 11. Questions genuinely requiring project support

**Q1: What source-owned completion signal or maximum-lateness/closure contract defines when the missing support delivery and its historical dates are complete?**

Also specify whether a clearly qualified delivered-snapshot value is acceptable while completeness is unverified. The README requires NULL when data is unavailable. It does not define a closure signal or the acceptance semantics for incomplete-but-reproducible calculations.

This is a source/acceptance requirement. It cannot be resolved by an engineer choosing a shorter date window. The supplied files contain no independent expected recovery total. None is inferred.

No support question is needed for the verified 20-KPI list, exact SQL predicates, observed seven older events, source counts, or actual result changes. They are resolved by the records and experiments.

## 12. Remaining uncertainties

- The observed recovery is not proof that every missing source record arrived.
- No maximum lateness bound proves every earlier support date closed.
- Source rows do not carry an intended delivery day. The exact division between outage recovery and ordinary lateness is not independently proved.
- An unchanged rounded result can contain a changed contributor set.
- Current equality between the two support-only supplements does not guarantee the same behavior for future records or repeated event types.
- Incident-independent results are independent of this support gap, not certified against every other source-quality issue.
- No production policy option, engineer decision, or acceptance rule has been approved.

Verified effects, unresolved completeness, and proposed options remain separate in the CSV and JSON. The investigation stops with these three outputs. No implementation was made.

