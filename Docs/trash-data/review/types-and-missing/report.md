# Data type and missing value check

The source files need type conversion and consistent column names before analysis.
The checked nonempty numeric and Gregorian date fields have no format errors.
This result does not prove that each business value is correct.

Scope: all 1,093 CSV files and 95 JSON files under dataset. The CSV files contain 224,067 rows in 26 tables.
Counts include all deliveries, repeated rows, reference tables, and the uploaded CSV.
Source files and analysis.ipynb were not changed.

## Missing values

The CSV files contain 190,185 empty cells out of 1,287,636 cells (14.77%).
A total of 188,928 rows have at least one empty cell. These are cell and row counts, respectively.
There are no CSV text values that equal null, none, nan, na, n/a, <na>, or nat after case and space changes.
There is one JSON null. It is decision_card in output_contract/example_brief.json. This is an output example.

| Table | Column | Empty cells | Percent of table rows |
| --- | --- | ---: | ---: |
| calendar/events_calendar.csv | end_date | 3 | 42.86% |
| config/kpi_dictionary.csv | target | 13 | 23.64% |
| config/kpi_dictionary.csv | warn | 13 | 23.64% |
| config/kpi_dictionary.csv | crit | 13 | 23.64% |
| config/kpi_dictionary.csv | dim | 51 | 92.73% |
| config/workflow_definitions.csv | sla_hours | 1 | 8.33% |
| config/workflow_definitions.csv | stage_target_median_h | 1 | 8.33% |
| crm_lead_events.csv | contract_value_toman | 5,893 | 94.93% |
| order_events.csv | amount_toman | 143,345 | 98.84% |
| orders.csv | campaign_id | 31,206 | 82.44% |
| orders.csv | promised_by | 1,475 | 3.90% |
| tasks.csv | blocker_fa | 1,584 | 93.45% |
| ticket_events.csv | staff_id | 1,539 | 9.94% |
| tickets.csv | order_id | 5,017 | 71.62% |
| org/access_matrix.csv | individual_level_data_team | 4 | 36.36% |
| org/staff.csv | effective_to_day | 26 | 100.00% |
| org/units.csv | parent_id | 1 | 25.00% |

Do not replace all empty cells with zero or delete all rows with empty cells.
All 1,677 refund events have an amount. Other order events have no amount in this field.
All 314 won events and the one value correction have a contract value. Other CRM events have no contract value.
An empty parent_id is expected for ORG. An empty effective_to_day can indicate no end date.
An empty campaign_id can indicate no campaign. An empty blocker_fa can indicate no blocker.
Confirm the business meaning before you fill other empty fields.
The 1,475 empty promised_by values and 1,539 empty staff_id values need explicit rules.
An empty access field must not grant access.

## Data types

CSV files have no declared data types. The notebook uses dtype="string" and keep_default_na=False for most source loads.
This retains empty cells as empty strings. A direct isna() count will not detect them.
Use a copy for conversion. First replace empty strings with pd.NA.

| Fields | Type to use |
| --- | --- |
| IDs, codes, names, category values, jdate, jmonth | string |
| Counts, day numbers, score, direction | nullable Int64 |
| Money | nullable Int64 for whole toman values; DECIMAL for exact decimal values |
| Thresholds and fractional durations | nullable Float64 or DECIMAL |
| created_at, at, answered_at, promised_by | datetime |
| date, due_date, effective_from_date | date |
| is_holiday | boolean after a 0/1 check |

effective_to_day has 26 empty values and no populated values. Use nullable Int64 because it is a day number.
Its intended type cannot be inferred from its values alone.
sla_hours has ten numeric values, one empty value, and the text promised_by.
Keep this source field. In a derived table, use a numeric duration and a separate deadline field reference.
Do not convert promised_by to an unreported missing number.
The Gregorian date checks do not validate the Jalali calendar. Keep jdate and jmonth as strings.
The source timestamps have no time zone. Confirm the source time zone before conversion to UTC.

## Normalization

Data cleaning is necessary. Apply the following changes in a derived data layer:

1. Map tickets.create_time to created_at and ticket_events.event_time to at. The names change on day 082.
2. Convert empty cells to nullable values and apply an explicit type for each column.
3. Remove 262 exact repeated order rows from the analysis copy. Keep the source records and delivery details.
4. Keep a missing delivery separate from empty cells. Day 066 has no tickets, ticket_events, or csat file.

Numeric scaling, such as Min-Max or Z-score, is not required for the supplied KPI SQL.
Keep amounts, durations, and counts in their specified units. If an ML model is added, assess scaling for that model.
For a distance-based or gradient-based model, fit a scaler on training data only.
For database normalization, separate multi-value fields when they are needed for joins or access checks.
Examples are access_matrix.visible_entities and workflow_definitions.units.
A full database redesign is not required to run the supplied KPI queries.

## Evidence

Run: .venv/Scripts/python.exe review/check_types_and_missing.py
See evidence.json for counts, column name changes, conversion checks, and delivery gaps.
See column-checks.csv for all 137 columns after the two column name mappings.
