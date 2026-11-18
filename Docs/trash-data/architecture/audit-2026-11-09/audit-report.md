# Detailed architecture audit report

Review date: 2026-11-09, Asia/Tehran. This is a source-driven documentation audit. It preserves the existing target architecture. It does not certify product correctness or authorize implementation.

## Scope and method

The four numbered documents were reviewed sequentially against the Markdown brief, important/ambiguous PDF passages, README, all five config files, all organization/access files, both output schemas and example, all 23 manager inputs, all 91 manifests and delivered header/count evidence, relevant source fixtures, investigation reports, the recorded 17-question discussion, and the existing Structurizr model. The source records and model remain unchanged.

The PDF has 26 annotations. Current checked pages 8,10,15 agree with the Markdown requirements; the same current PDF was checked on pages 13,16 in the previous review. Highlighting/resaving and byte-hash differences do not establish requirement changes. See [brief evidence](brief-content-check.json).

Requirements come from official sources. Accepted choices come from recorded team/user decisions. Physical mechanisms, algorithms and exact limits remain Proposed or Open unless evidence approves them. Observation is an evidence category. The current user confirms all five accepted boundaries; none was reopened.

## Results and limits

There are 59 audit records: 58 material findings and one verified, retained source observation (AUD-028). Material severity: {'High': 23, 'Medium': 26, 'Low': 9}. Record states: {'Corrected': 56, 'Verified; retained': 1, 'Deferred to model phase': 2}. The two deferred findings concern DSL source/count comments. Model work is reserved for the subsequent visualization phase. Open business/source policies remain in the [Decision Log](../registry/open-issues-registry.md#decision-log); a corrected document does not close them.

The [unit ledger](document-review-ledger.csv) inventories 911 pre-edit headings, paragraphs/list items, table rows, blocks and anchors. Every nonblank line in the four pre-edit documents belongs to a review unit. Each unit has a hash, exact line span, context and relevant findings. Inherited section evidence is review context, not an independent proof of every sentence. Semantic results rest on the detailed issue analysis and [granular traceability](requirements-traceability.md), not link counts.

The [findings CSV](findings.csv) and [JSON](findings.json) preserve every full original claim. Locations below refer to immutable pre-edit bytes in [pre-edit.zip](pre-edit.zip), not shifted current line numbers. The [baseline manifest](pre-edit-manifest.json) identifies the files. Corrected means the documentation issue was addressed; it does not mean an implementation passed a test.

## Findings and the retained source observation

### AUD-001: Incomplete rule enumeration

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 241.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#124; R1 &#124; شروع در &#96;owner_manager_id&#96; و پایین‌ترین سطح مسئول. اگر مالک فعال نباشد، routing issue ثبت شود؛ مالک جدید حدس زده نشود. &#124;
- Source evidence: dataset/config/escalation_rules.csv records R1-R8; brief pp.6-8
- Correction: Replace the partial rule table with all eight rules, inputs, triggers, outcomes, routing, state, and gates.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-002: Obsolete visualization standard

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 111.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#96;&#96;&#96;mermaid
- Source evidence: User audit instruction section 6; workspace.dsl views IntegratedOverview, NightlyReporting, NightlyData, NightlyBrief
- Correction: Remove two active diagram blocks. Cite verified Structurizr view keys.
- Remaining uncertainty: None.

### AUD-003: Ambiguous document identifier

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 1.
- Severity: **Low**. Correction status: **Corrected**.
- Original claim or affected location: # ARCH-001: طرح معماری سیستم ARKA
- Source evidence: The four files share the ARCH-001 prefix; no separate document-ID specification was found.
- Correction: Retain ARCH-001 as the architecture-family label. Add an explicit unique document key; do not migrate stable IDs.
- Remaining uncertainty: None.

### AUD-004: Missing source discovery

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 44.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#124; S01 &#124; &#91;بریف اصلی DIDRAH&#93;(../../Project_berif/بریف%20پروژه%20بوتکمپ%20_%20دستیار%20ایجنتیک%20مدیران%20سازمانی%20_%20دیدراه.pdf) &#124; Current PDF: 19 pages read on 2026-11-09. Pages 13 and 16 also checked as images. Product and acceptance requirements. &#124;
- Source evidence: Project_berif contains the PDF and its Markdown conversion.
- Correction: Add S18 for the Markdown brief. Verify important passages against the PDF.
- Remaining uncertainty: None.

### AUD-005: Misleading source-version emphasis

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 66.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: Current S01 SHA-256: &#96;6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8&#96;. The former listed hash was &#96;fac22a35109e627d90be519e187354a773f57a4d26561311ce90963e3780e747&#96;. It does not match the current file. This does not establish which PDF content changed.
- Source evidence: User confirms highlighting/resave; current PDF pp.8,10,15 agree with corresponding Markdown content.
- Correction: Keep the current hash as provenance. Do not report a requirement conflict from a file hash.
- Remaining uncertainty: None.

### AUD-006: Missing execution and revision contracts

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 172.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#124; &#96;InsightBrief&#96; &#124; &#96;summary, impact, metric_refs, drilldowns, causes, alternatives, options, history, proposed_owner, query_refs&#96;؛ شرط پذیرش هر علت جدا بررسی می‌شود. &#124;
- Source evidence: workspace.dsl requests, documents, queryGateway, modelGateway and InteractiveAssistant/ManagerUpload views
- Correction: Add Proposed execution-grant and interactive-evidence contracts. Map document terms to actual DSL IDs.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-007: Incomplete configuration lifecycle

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 152.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#124; F: &#96;ManagementInputService&#96; &#124; پرسش، تصمیم یا تغییر تنظیم احراز‌شده &#124; input event، config revision یا QA job &#124; متن فایل نمی‌تواند دستور مدیر بسازد. تغییر مجاز از زمان اثر مشخص فعال می‌شود. &#124;
- Source evidence: Brief p.13 configuration; README KPI extension; workspace.dsl managerConfig and ManagerGovernance
- Correction: Document governed goals, thresholds, priorities, organization, and new inactive KPI validation/activation.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-008: Unqualified evidence interpretation

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 277.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: هر علت قابل انتشار باید حداقل دو گروه شاهد مستقل داشته باشد. دو KPI مشتق از یک جمعیت، دو شاهد مستقل نیستند. نمونهٔ مناسب، تغییر صف تیکت و دادهٔ ظرفیت تجمیعی از منبع جداست. استقلال مسیر مشاهده، استقلال آماری یا اثبات علیت نیست؛ S02 تصریح می‌کند که کل داده از یک شبیه‌سازی مشترک ساخته شده است.
- Source evidence: Brief p.9 requires two independent witnesses, confidence, and alternative causes; no independence algorithm is supplied.
- Correction: Keep the requirement. Mark evidence grouping and independence heuristics Proposed.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-009: Unapproved fallback stated as guaranteed behavior

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 302.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: cache شامل snapshot، query/result hash، scope fingerprint، policy، model و prompt version است. cache بدون scope ممنوع است. هنگام کمبود بودجه یا خطای مدل، گزارش با قالب قطعی و عددهای تأییدشده ساخته می‌شود. علت بدون شاهد و گزینهٔ تخمینی حذف می‌شود. افت کیفیت تحلیل در لاگ ثبت می‌شود؛ عبور از سقف هزینه راه جبران نیست.
- Source evidence: S16 Q16 accepts independent publication, while fallback details remain Open; workspace.dsl PartialPublication
- Correction: Label template fallback Proposed. Preserve explicit failure and incomplete-day reporting.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-010: Implementation recommendation presented as scope

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 308.
- Severity: **Low**. Correction status: **Corrected**.
- Original claim or affected location: سه صفحهٔ اصلی فارسی و RTL کافی است: گفتگو و گزارش صبح، داشبورد نقش‌محور و اتاق کنترل Workflow برای مدیر ارشد. صفحهٔ سابقهٔ تصمیم و اقدام، بخشی از همین رابط‌هاست. از هر عدد می‌توان query و شواهد مجاز آن را دید.
- Source evidence: Brief pp.11-12,18 requires three interfaces, not exactly three pages.
- Correction: Distinguish required interfaces from Proposed page layout.
- Remaining uncertainty: None.

### AUD-011: Incomplete report contract

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 318.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: ### ۹.۱. قرارداد خروجی و کنترل پیش از انتشار
- Source evidence: Brief pp.9-11: report item, chart specification, decision card, health, open actions, read/decision/referral state
- Correction: Add complete content requirements and separate internal representation from permissive wire schemas.
- Remaining uncertainty: None.

### AUD-012: Undeclared schema mapping

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 324.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#96;data_issues.source&#96; فقط enumهای قرارداد را دارد: &#96;orders, tickets, crm, tasks, marketing, sessions, availability&#96;. مسئلهٔ &#96;csat&#96; و &#96;ticket_events&#96; به &#96;tickets&#96; نگاشت می‌شود و نام دقیق فایل در detail مجاز می‌آید. حالت‌های داخلی بیشتر، در همین schema با &#96;type=other&#96; و توضیح قابل فهم نشان داده می‌شوند؛ enum منبع تغییر نمی‌کند.
- Source evidence: brief_schema.json data_issues source/type enums; no source-family alias contract supplied
- Correction: List exact enums. Label detailed-file to source-family mapping Proposed.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-013: Unapproved infrastructure exclusion

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 373.
- Severity: **Low**. Correction status: **Corrected**.
- Original claim or affected location: نسخهٔ اول به message broker، Kubernetes، graph database، vector database یا چند agent خودمختار نیاز ندارد. برای این داده، جستجوی SQL و retrieval محدود متن کافی است. افزودن هر زیرساخت پس از اندازه‌گیری نیاز، ADR جدا می‌خواهد.
- Source evidence: S16 Q01 accepts one Agent; no source mandates the other named infrastructure choices.
- Correction: Keep one Agent Accepted. Mark infrastructure deferral Proposed.
- Remaining uncertainty: None.

### AUD-014: Incomplete rule boundary inventory

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 237.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: هر مقایسه فقط از مقادیر مجاز در همان knowledge snapshot استفاده می‌کند. نبود baseline، مقدار صفر مبنا یا دادهٔ نامطمئن به نتیجهٔ عادی یا انحراف نامحدود تبدیل نمی‌شود. جهت انحراف baseline، حداقل تعداد نمونه و تساوی دقیق با آستانه در ADR-07 تعیین می‌شوند.
- Source evidence: R2 explicitly uses more than escalate_after_days and worsening >=20%; R4 does not define its change comparand; R3 can lack a numeric warn.
- Correction: Separate explicit source comparisons from genuinely Open edge cases.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-015: Missing governed KPI extension detail

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 225.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: گردکردن در خود SQL مرجع انجام می‌شود. LLM، رابط و serializer نباید مقدار را دوباره گرد کنند. واحد «میلیون تومان»، «هزار تومان»، «تومان»، «ساعت»، «روز»، درصد و امتیاز از پنج یکسان نیستند. اختلاف دو درصد در توضیح، «واحد درصد» است. هر محاسبهٔ اضافه باید query و تعریف ثبت‌شدهٔ مستقل داشته باشد.
- Source evidence: README permits additions and prohibits changing existing definitions; brief p.13 requires configurable KPIs.
- Correction: Preserve canonical definitions. Describe inactive candidate registration, validation, human approval, and versioned activation as Proposed mechanism.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-016: Incomplete workflow-stage coverage

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 267.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: مالک انتهابه‌انتهای هر Workflow از ستون &#96;owner&#96; در S11 می‌آید. برای انتساب گلوگاه به مرحله، &#96;order_events.actor_team&#96; یا رابطهٔ مجاز staff/team در زمان رخداد بررسی می‌شود. نبود actor معتبر، مجوز حدس‌زدن مالک مرحله نیست؛ mapping تکمیلی stage-to-team در policy catalog تأیید شود. این metadata با مالک KPI موجود جایگزین نمی‌شود.
- Source evidence: workflow_definitions.csv has 12 stages, targets, numeric SLA, deadline reference, and one blank SLA.
- Correction: Add all 12 stage records and distinguish workflow owner, stage owner, median target, SLA, and canonical KPI.
- Remaining uncertainty: See the referenced ADR and Decision Log for unresolved policy details.

### AUD-017: Obsolete and misleading data visualization

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 31.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#96;&#96;&#96;mermaid
- Source evidence: User visualization standard; existing DSL has component/data-flow views, but no entity ERD or row-level lineage view.
- Correction: Replace three active blocks with accurate Structurizr references and explicit data-model/lineage gaps. Do not imply mandatory SourceFile for a missing-source incident.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-018: Incomplete logical entity contracts

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 75.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#124; &#96;ReportVersion&#96; &#124; &#96;report_day + manager_id + run_id + version&#96; &#124; snapshot، JSON/text hashes، Insight refs، policy bundle، validation receipt، &#96;supersedes&#96; و publication mode. &#124;
- Source evidence: The document uses many undefined internal entities; workspace.dsl lists shared Insights, grants, cost, manager outcomes and upload revisions.
- Correction: Define logical grains and boundaries for the referenced entities. Keep physical keys/constraints Proposed.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-019: Mixed and unclear time semantics

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 109.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: S01 ص۱۴ زمان‌های داده را تهران اعلام می‌کند. متن timestamp خام بدون offset حفظ می‌شود. نسخهٔ استاندارد می‌تواند تفسیر &#96;Asia/Tehran&#96; داشته باشد، ولی The PostgreSQL translation must preserve reference time semantics. Keep the raw timestamp text for comparison. تبدیل بی‌دلیل متن به UTC، روز گروه‌بندی و &#96;julianday&#96; را تغییر می‌دهد.
- Source evidence: Brief p.14 Tehran time; README D-1 eligibility; raw timestamps have no offset.
- Correction: Use one clear time contract. Preserve raw time text and reference arithmetic; distinguish operational cutoff from interactive revision.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-020: Observation presented as a universal binding example

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 122.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: ### ۳.۱. مثال الزام‌آور اصلاح قرارداد
- Source evidence: RCA CRM-02 and source L02045 rows are a development fixture. The general cutoff and replacement semantics are authoritative.
- Correction: Label the example Observation. Do not turn a fixed lead ID/date into runtime logic.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-021: Incomplete privacy boundary

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 92.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#124; &#96;staff_availability&#96; &#124; مشاهدهٔ date/staff_id/team_id &#124; استفاده فقط برای ظرفیت؛ وضعیت حضور فرد به گزارش مدیر بالاتر وارد نمی‌شود. &#124;
- Source evidence: Brief pp.6,12-13 prohibits individual attendance monitoring; README permits direct-team capacity purpose, not general disclosure.
- Correction: State that individual attendance/leave status is not a manager display. Capacity formula and small-group inference remain Open.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-022: Count coverage without sufficient per-KPI semantics

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 251.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: ### ۶.۱. کلیدهای خواندن جدول پوشش
- Source evidence: All 55 SQL definitions, five reference views, owner/unit/dimension/rule metadata.
- Correction: Add 55 source-backed semantic contracts with exact SQL/hash, date/window, formula, population/filter, NULL/row and precision semantics, plus gates.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-023: Missing reference-view contract detail

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 321.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: ### ۶.۲. وابستگی عملیاتی هر تعریف
- Source evidence: reference_views.sql views order_fact, ticket_fact, lead_fact, task_fact, revenue_daily
- Correction: Document selected MIN/MAX fields, correction replacement and COALESCE behavior, grouping, join multiplicity, and execution/value dependencies.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-024: Incorrect priority scope

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 435.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: configهای قابل تغییر: threshold، target، escalation، manager preference، source adapter mapping و publication policy. SQL اصلی ۵۵ KPI در طول ارزیابی تغییر نمی‌کند. درخواست تغییر تعریف باید یک revision پیشنهادی بسازد و با مرجع ارزیابی جدا بماند. priority فقط رتبهٔ نمایش را تغییر می‌دهد.
- Source evidence: Brief pp.3,7,10,13; DSL managerConfig, signals, evidence and reportWriter
- Correction: Allow authorized priorities to shape selection, evidence focus, and role emphasis; never formulas, grants, or unsupported facts.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-025: Incomplete independent job outcomes

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 465.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: jobها &#96;pending/running/succeeded/failed&#96;، lease و retry count دارند. crash میان ثبت فایل و batch commit، فایل orphan قابل بازیابی می‌سازد؛ snapshot فقط receipt committed را می‌بیند. crash پس از محاسبه و پیش از انتشار با idempotency key، انتشار دوم ایجاد نمی‌کند.
- Source evidence: Accepted independent publication; DSL jobs/requests/publication; PartialPublication view
- Correction: Separate technical job state, package validation/export outcome, and day coverage. Record pre-draft failure and cancellation without inventing output enums.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-026: Unresolved dimension serialization hidden in a prose note

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 77.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#96;dim_key&#96; در ذخیره‌سازی، نام بعد و مقدار آن را نگه می‌دارد. رشتهٔ خالی خروجی S06 به معنی «بدون بعد» است. NULL واقعی یک مقدار بعد، نباید با «بدون بعد» مخلوط شود. تبدیل آن به schema خروجی نیازمند قاعدهٔ صریح است.
- Source evidence: brief_schema.json number.dim is a string; dictionary has four dimensioned definitions; raw dimensions can have empty/NULL cases.
- Correction: Keep no dimension distinct from a NULL dimension. Record the wire policy and test gap explicitly in the Decision Log.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-027: Incomplete source and schema contract evidence

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 176.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: ### ۴.۲. نسخهٔ schema
- Source evidence: Actual delivered headers, day000/day066/day067/day070/day076/day081/day082 manifests and source rows.
- Correction: Add a reproducible read-only source sample check and all delivered header signatures. Do not infer event IDs or customer/campaign parent registries.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-028: Verified attributed source observation

- Location: `docs/architecture/002-data-architecture.md`, pre-edit line 220.
- Severity: **Low**. Correction status: **Verified; retained**.
- Original claim or affected location: در S10، هفت کلید پشتیبانی به علت نبود گروه denominator سفارش، مستقل و &#96;no_reference_row&#96; بودند. آن‌ها هفت عدد قابل بازگرداندن نیستند. ۱٬۷۳۳ مقدار تاریخی ثابت، از نظر کامل‌بودن همچنان نامعلوم بودند. معماری هیچ‌یک را صرفاً به دلیل ثابت‌ماندن عدد کامل اعلام نمی‌کند.
- Source evidence: DQ report sections 3,5,6: 1809 unresolved keys include 1733 numbers and 76 no-row states.
- Correction: Retain the correctly attributed counts without a substantive correction. They are historical observations, not a new calculation, completeness proof or approved hold policy.
- Remaining uncertainty: Referenced data and publication policies remain Open; no product test result is implied.

### AUD-029: Ambiguous family/document identity

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 1.
- Severity: **Low**. Correction status: **Corrected**.
- Original claim or affected location: # ARCH-001: تصمیم‌ها، ریسک‌ها و مسیر پیاده‌سازی
- Source evidence: Shared prefix in the four files; stable unique filename keys.
- Correction: Keep ARCH-001 as family metadata and add the unique document key.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-030: Incomplete boundary precision

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 151.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: **Status:** Requirement: R1-R8. Open: edge cases. Proposed: named candidate interpretations only.
- Source evidence: escalation_rules.csv R2-R5,R7-R8; brief p.8 controls at three points.
- Correction: Link the complete rule contract. Add missing-warn and R4 reference ambiguities without reopening explicit comparisons.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-031: Invalid enum shorthand

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 182.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: **ورودی هم‌روز:** S07 پرسش manager Q09 را پیش از upload IN07 روز ۸۰ نوشته است. محتوای پرسش به پیوست اشاره دارد، ولی زمان دقیق دریافت آن در روز مشخص نیست. پیشنهاد، ثبت dependency صریح attachment و زمان دریافت است. اگر فایل هنوز مجاز/دریافت‌شده نیست، پاسخ clarification/data_unavailable بدهد؛ صرف وجود آن در filesystem مجوز خواندن زودهنگام نیست.
- Source evidence: qa_answer_schema.json /properties/answer_status/enum
- Correction: Use clarification_requested or data_unavailable; do not publish clarification as a status.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-032: Missing non-question input coverage

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 416.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: ### 7.2. Supplied manager questions
- Source evidence: scripted_inputs.json has 23 events: 16 questions and seven other inputs across five types.
- Correction: Add all seven non-question contracts and all-23 receipt tests, plus close/referral requirements from the brief.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-033: Incomplete acceptance coverage

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 387.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#124; &lt;a id=&quot;at-08&quot;&gt;&lt;/a&gt;AT-08 &#124; recurrence/escalation &#124; کمتر از۱۰٪ تغییر به همان مخاطب new نسازد؛ reason و history تشدید حاضر؛ owner و rule version درست؛ حداکثر پنج مورد. &#124;
- Source evidence: R1-R8, all Workflow stages, report content, KPI lifecycle, execution grants, JSON schema properties.
- Correction: Preserve AT-01..23. Add AT-24..30 for the uncovered contracts. Mark every product gate planned, not passed.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-034: Decision Log lacks exact source and closure evidence

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 480.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: All rows below are &#96;Open&#96;. Options are review inputs, not accepted rules. Listed roles are proposed owners, not assigned people. Close a row only with a source or team decision record and the applicable gate evidence.
- Source evidence: Each DL row relies on distinct brief pages, CSV records, JSON pointers, and recorded decisions.
- Correction: Retain DL-01..16; add source-location and closure-evidence columns. Add missing dimension/content/config decisions.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-035: Obsolete runtime risk wording

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 336.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#124; پیچیدگی دو dialect &#124; خطای مسیر query و هزینهٔ نگهداری &#124; interface واحد، reference result authoritative و ثبت engine هر query. &#124;
- Source evidence: Accepted PostgreSQL-only product engine; ADR-01 permits a separate test oracle.
- Correction: State translation/oracle maintenance risk; do not imply two product query engines.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-036: Proposed fallback stated as mandatory success

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 216.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: **شرط تصویب:** روز پرترافیک با retry و سؤال مدیر از سقف نگذرد. fallback قطعی، گزارش قابل استفاده تولید کند و کیفیت افت‌کرده ثبت شود. هزینهٔ زیرساخت جدا گزارش شود؛ با سقف LLM اشتباه نشود.
- Source evidence: S16 Q16 and ADR-14; failure may precede a draft and remain a failed required report.
- Correction: Condition fallback acceptance on selection and validation. Otherwise retain explicit failure and incomplete day.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-037: Missing stage-contract test

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 276.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: **Gate:** AT-08 and AT-12, including an unmapped stage and a unit actor. Product/data owners must approve the mapping.
- Source evidence: 12 workflow_definitions.csv stages; canonical WF2/WF3 differ from full stage SLA.
- Correction: Add AT-25 and retain Open owner mapping. Do not imply an official missing-owner policy.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-038: Verification scope too broad

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 470.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: The three architecture documents are reconciled with the supplied review record. Document 004 contains the Q01-Q17 mapping, source checks, file changes, and verification limits. The Decision Log below retains unresolved choices. No product code, SQL port, KPI run, security test, performance test, or acceptance result is claimed.
- Source evidence: Previous review checked links/counts; the current audit finds semantic omissions.
- Correction: Replace general completion wording with evidence-linked audit, traceability, and current verification scope.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-039: Mixed requirement and engineering gate authority

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 398.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#124; &lt;a id=&quot;at-19&quot;&gt;&lt;/a&gt;AT-19 &#124; تعمیم و تحویل &#124; data root و تنظیم جدید بدون تغییر کد؛ یک دستور Docker؛ no hardcoded incident days/IDs؛ restart و restore موفق. &#124;
- Source evidence: Brief p.18 requires Docker delivery; backup/restore specifics are engineering proposals.
- Correction: Add an acceptance-basis register. Separate official requirements, Accepted boundaries, and Proposed mechanisms.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-040: Human execution status ambiguity

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 300.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: **Gate:** AT-14. Product owns lifecycle details.
- Source evidence: Brief pp.11-12; existing HumanDecisionFollowUp view records human-reported status, never execution by ARKA.
- Correction: Preserve the target lifecycle, but keep actual confirmation schema/authority Open. No source decision proves execution.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-041: Stale source enumeration

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 5.
- Severity: **Low**. Correction status: **Corrected**.
- Original claim or affected location: Read this document with the &#91;system blueprint&#93;(001-system-blueprint.md), &#91;data architecture&#93;(002-data-architecture.md), and &#91;Q01-Q17 review&#93;(004-reconciliation-review.md#question-map). Sources S01-S17 are listed in document 001. This task changes documentation only. It does not authorize product implementation.
- Source evidence: Discovered Markdown brief S18 and current accepted-decision confirmation.
- Correction: Update the source range and identify the audit request as confirmation, not a replacement requirement specification.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-042: Stale review/delivery scope

- Location: `docs/architecture/003-decisions-and-roadmap.md`, pre-edit line 347.
- Severity: **Low**. Correction status: **Corrected**.
- Original claim or affected location: &#124; P0: review معماری &#124; مرور سه سند، تعیین owner ADRها و ثبت EvaluationProfile &#124; تصمیم‌های پذیرفته/ردشده و پرسش‌های پذیرش &#124; scope و مرزهای امنیت و reference روشن باشد؛ implementation فقط بعد از این مرحله. &#124;
- Source evidence: Current task audits four numbered documents and dependent documentation.
- Correction: Keep the roadmap Proposed; update P0 review and clarify P2 is not complete without required content and workflows.
- Remaining uncertainty: Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.

### AUD-043: Stale audit scope

- Location: `docs/architecture/004-reconciliation-review.md`, pre-edit line 5.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: This review reconciles the three architecture documents with the official brief, dataset contracts, and the supplied Q01-Q17 review record. It changes documentation only. It does not claim product implementation, numerical equivalence, security, performance, or acceptance results.
- Source evidence: Current request requires sequential audit of four numbered documents and dependent documentation.
- Correction: Update the review scope, family/document metadata, and source range.
- Remaining uncertainty: Open architecture/source-contract choices are retained in the central Decision Log.

### AUD-044: Hash difference treated as a review concern without content difference

- Location: `docs/architecture/004-reconciliation-review.md`, pre-edit line 22.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: Document 001 formerly listed a different PDF hash. It does not match the current file. All 19 pages of the current file were read. Pages 13 and 16 were also checked as images. A hash difference alone does not establish a change in requirements. Earlier numerical audit results remain attributed historical evidence.
- Source evidence: User confirms PDF highlighting/resave; PDF pp.8,10,15 match the Markdown passages checked.
- Correction: Report content comparison and provenance. Do not classify a source-version requirement conflict.
- Remaining uncertainty: Open architecture/source-contract choices are retained in the central Decision Log.

### AUD-045: Unsupported semantic completion claim

- Location: `docs/architecture/004-reconciliation-review.md`, pre-edit line 78.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: The architecture review is complete at the documentation level. Product implementation is outside this task. The team must resolve or explicitly approve named temporary policies for these P0 design choices before affected work starts:
- Source evidence: Current source audit finds omitted rules, stage targets, report content, configuration and schema details.
- Correction: Replace broad completion with scoped audit evidence and explicit unresolved gates.
- Remaining uncertainty: Open architecture/source-contract choices are retained in the central Decision Log.

### AUD-046: Obsolete visualization validation criterion

- Location: `docs/architecture/004-reconciliation-review.md`, pre-edit line 113.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: - All 150 local Markdown links in the changed/new Markdown files resolve, including explicit section anchors. All five fenced diagram blocks have closed fences. No graphical Mermaid check is claimed.
- Source evidence: User selects Structurizr and prohibits active architecture diagrams in the retired format.
- Correction: Retire active blocks/previews and map existing view keys; record absent views as gaps.
- Remaining uncertainty: Open architecture/source-contract choices are retained in the central Decision Log.

### AUD-047: Stale verification result

- Location: `docs/architecture/004-reconciliation-review.md`, pre-edit line 112.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: - The set has 17 ADRs and 23 planned acceptance gates. The original 12 ADR IDs and 19 acceptance IDs remain available.
- Source evidence: New semantic audit adds planned gates and a reproducible backup. Earlier link counts cannot validate this run.
- Correction: Replace old current-result counters with the new verification report. Preserve historical evidence in the backup.
- Remaining uncertainty: Open architecture/source-contract choices are retained in the central Decision Log.

### AUD-048: Proposed mechanism promoted in conflict disposition

- Location: `docs/architecture/004-reconciliation-review.md`, pre-edit line 69.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#124; Daily atomic wording versus independent publication &#124; Resolve at the package boundary: one manager&#x27;s text/JSON is atomic; manager outcomes are independent. Incomplete required coverage cannot pass the day. Retry and fallback remain Open. &#124;
- Source evidence: ADR-14 accepts independent publication but marks atomic text/JSON commit Proposed.
- Correction: Keep independent publication Accepted and package commit Proposed; retain incomplete-day coverage.
- Remaining uncertainty: Open architecture/source-contract choices are retained in the central Decision Log.

### AUD-049: Incomplete question-to-rule coverage

- Location: `docs/architecture/004-reconciliation-review.md`, pre-edit line 54.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#124; &lt;a id=&quot;review-q12&quot;&gt;&lt;/a&gt;Q12: signals and escalation &#124; &#96;Requirement&#96;: deterministic detection and R1-R8; S01 pp.6-8,13 and S11. &#96;Proposed&#96;: strict crossing and named unknown states. &#96;Open&#96;: equality, baseline, zero denominator, warning-day count, and reset. &#124; &#91;ADR-07&#93;(003-decisions-and-roadmap.md#adr-07) &#124; &#91;001: signals&#93;(001-system-blueprint.md#system-7), &#91;002: quality&#93;(002-data-architecture.md#data-5) &#124; &#91;AT-08&#93;(003-decisions-and-roadmap.md#at-08), AT-09; DL-09 &#124;
- Source evidence: Complete R1-R8 contract and AT-24; all 12 Workflow stages and AT-25.
- Correction: Add the new granular gates/traceability references to affected question rows.
- Remaining uncertainty: Open architecture/source-contract choices are retained in the central Decision Log.

### AUD-050: Non-reproducible previous comparison reference

- Location: `docs/architecture/004-reconciliation-review.md`, pre-edit line 100.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#124; &#91;Unified diff&#93;(reconciliation.diff) &#124; Compare the changed documents with the saved pre-edit files. Include new documentation. Exclude the diff itself. &#124;
- Source evidence: Previous pre-edit files were outside the workspace; root diff belongs to the earlier task.
- Correction: Keep the prior root diff historical. Supply a new in-workspace backup, manifest, unified diff, and verification procedure.
- Remaining uncertainty: Open architecture/source-contract choices are retained in the central Decision Log.

### AUD-051: Retired visualization presented as active standard

- Location: `docs/architecture/visualizations/README.md`, pre-edit line 13.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#124; &#91;01-source-data-erd.mmd&#93;(01-source-data-erd.mmd) &#124; Observed CSV families and selected relations &#124; Eight &#96;01-source-*-detail.mmd&#96; ERDs; catalog, profiles, and relationship evidence &#124;
- Source evidence: User section 6; actual Structurizr view declarations.
- Correction: Replace the active guide with a verified Structurizr view index. Keep old source artifacts as an archive, not active diagrams.
- Remaining uncertainty: None.

### AUD-052: Obsolete diagram dependency and incomplete contracts

- Location: `docs/architecture/visualizations/proposed-entity-contracts.md`, pre-edit line 3.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: All entities in Diagram B are PROPOSED - NOT IMPLEMENTED. The source is &#96;../002-data-architecture.md&#96;, sections 1 and 2. This file does not approve physical tables or constraints.
- Source evidence: Document 002 logical contracts; existing Structurizr has no entity ERD.
- Correction: Refer to logical contracts and the explicit entity-visualization gap. Preserve Proposed status.
- Remaining uncertainty: None.

### AUD-053: Duplicate status vocabulary

- Location: `docs/architecture/visualizations/open-questions.md`, pre-edit line 5.
- Severity: **Low**. Correction status: **Corrected**.
- Original claim or affected location: UNRESOLVED means Open. PROPOSED means Proposed. CONFIRMED is a legacy evidence label, not proof of team approval.
- Source evidence: Requirement/Accepted/Proposed/Open convention; Observation is evidence.
- Correction: Use Open/Proposed in the active register. Keep VQ identifiers and source restrictions.
- Remaining uncertainty: None.

### AUD-054: Active legacy preview family

- Location: `docs/architecture/visualizations/previews/01-source-data-erd.md`, pre-edit line 1.
- Severity: **Medium**. Correction status: **Corrected**.
- Original claim or affected location: &#96;&#96;&#96;mermaid
- Source evidence: All 26 previews use the retired diagram syntax; user section 6.
- Correction: Retire all 26 rendered previews. Point to verified Structurizr scope views and actual missing-view gaps. Preserve the raw historical files and pre-edit ZIP.
- Remaining uncertainty: None.

### AUD-055: Evidence labels can imply architecture approval

- Location: `docs/architecture/visualizations/security-examples.md`, pre-edit line 7.
- Severity: **Low**. Correction status: **Corrected**.
- Original claim or affected location: CONFIRMED: M07 can see T_WH KPIs and direct-team workload. DERIVED: the minimum workload projection can use &#96;tasks.task_id&#96;, &#96;tasks.team_id&#96;, &#96;tasks.owner_id&#96;, &#96;tasks.created_at&#96;, and &#96;tasks.due_date&#96;. Compute completion from &#96;task_events.task_id&#96;, &#96;task_events.event&#96;, and &#96;task_events.at&#96;, using &#96;task_fact.done_at&#96;. The row condition is &#96;tasks.team_id = &#x27;T_WH&#x27;&#96;. Join &#96;tasks.owner_id = staff.staff_id&#96; and verify that &#96;staff.team_id = &#x27;T_WH&#x27;&#96; at the applicable date. These are candidate query conditions derived from observed keys. The physical enforcement design is PROPOSED. For an as-of date, use the supplied overdue SQL time conditions, or define a separate approved open-work query. Do not count all historical tasks as open.
- Source evidence: Source access matrix and brief restrictions; candidate physical projections are not Accepted.
- Correction: Add the active status/evidence legend and link the central policy decisions. Keep correct examples.
- Remaining uncertainty: None.

### AUD-056: Stale source/authority notes

- Location: `architecture/structurizr/workspace.dsl`, pre-edit line 31.
- Severity: **Medium**. Correction status: **Deferred to model phase**.
- Original claim or affected location:     // A separate original 17-question record was not found in the inspected repository.
- Source evidence: The original review record now exists at docs/architecture/sources/Adr.md; Markdown brief exists beside PDF. Documents have mixed explicit statuses.
- Correction: Later update source notes to actual locations and explicit authority. Preserve accepted boundaries and all existing model work.
- Remaining uncertainty: No DSL edit is authorized in this task.

### AUD-057: Incorrect view inventory

- Location: `architecture/structurizr/workspace.dsl`, pre-edit line 644.
- Severity: **Low**. Correction status: **Deferred to model phase**.
- Original claim or affected location:     // F08 - VIEW SCOPE: all 15 view keys are retained. Short visible descriptions retain
- Source evidence: Actual DSL declarations contain 16 distinct view keys, including IntegratedOverview.
- Correction: Correct the stale count in the later model phase. Do not remove or rename a view to match the comment.
- Remaining uncertainty: No parser/render validation is implied.

### AUD-058: Incomplete confidence-to-number boundary

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 286.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#96;cause_confidence&#96; با &#96;source_completeness&#96; یا صحت عدد یک فیلد نیست. روش امتیازدهی اطمینان باید نسخه‌دار و قابل توضیح باشد؛ عدد ۰ تا ۱ احتمال آماری کالیبره‌شده فرض نمی‌شود. برچسب کم/متوسط/زیاد و دلیل آن در متن بیاید. ادعای اثر تصمیم نیز مشاهدهٔ قبل/بعد است؛ هم‌زمانی، اثبات اثر علّی نیست.
- Source evidence: Brief pp.9,16; brief_schema.json causes.confidence is optional numeric 0..1; DSL F01 requires an approved registered-query scoring path.
- Correction: Use qualitative confidence until an approved numeric scoring definition has a registered-query result. Do not let the model invent a number.
- Remaining uncertainty: Scoring definition and wire mapping remain Open under ADR-09/DL-18.

### AUD-059: Incomplete schema-required and enum enumeration

- Location: `docs/architecture/001-system-blueprint.md`, pre-edit line 320.
- Severity: **High**. Correction status: **Corrected**.
- Original claim or affected location: &#96;submission/briefs/day_XXX/&lt;manager_id&gt;.json&#96; از &#96;brief_schema.json&#96; ساخته می‌شود. &#96;report_day, manager_id, items, numbers, data_issues, text_fa&#96; الزامی‌اند. &#96;items&#96; حداکثر پنج مورد دارد. هر عدد، KPI/entity/dim/date/value و &#96;query_id&#96; قابل ردیابی دارد. اگر schema فیلدی را اختیاری بداند ولی بریف آن را برای ردیابی لازم بداند، Validator داخلی آن را الزامی می‌کند.
- Source evidence: brief_schema.json root/item/number required sets and all enums; qa_answer_schema.json required sets/statuses.
- Correction: Add exact wire required sets, nullable value rule, confidence bound, and all follow-up effect directions. Keep schema and semantic requirements distinct.
- Remaining uncertainty: suppressed mapping, extra-query IDs and complete content mapping remain Open.

## Unresolved matters and implementation limits

The central log retains numerical equivalence/input types and input mode, source closure/release, correction ties, shared-resource/privacy/capacity policy, stage owners, genuinely unspecified rule boundaries, M11/attachment timing, output status/number/dimension mapping, human execution confirmation, model limits, approval roles, retention and official evaluation profile. Full source coverage cannot invent these answers.

The five accepted architecture boundaries remain intact. All55 canonical definitions, all 8 rules, all 12 stages, all 11 access scopes and all 23 supplied inputs have semantic trace records. Exact schema constraints are recorded separately from required report content. All AT gates remain planned. No KPI SQL, PostgreSQL parity, model call, product security, runtime, restore or official acceptance test was executed.

No Structurizr element, relationship, view, style or layout was changed. The [gap report](structurizr-gap-report.md) distinguishes existing coverage from future visualization work. Active legacy rendered previews are retired; original raw files and generators remain historical and must not replace the baseline.
