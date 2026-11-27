using System.Text.Json;
using OrgPilot.BackendApi.Modules.Configuration;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Modules.Kpi;
using OrgPilot.BackgroundWorker.Modules.Snapshots;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.Acceptance;

/// <summary>
/// Regression checks for the supplied development dataset, independent of PostgreSQL.
/// These are not a substitute for the normal PostgreSQL/SQLite parity receipt path.
/// </summary>
internal static class DevDatasetChecks
{
    public static async Task<int> RunAsync(string dataDirectory, string archiveDirectory)
    {
        var failures = 0;
        void Check(string name, bool passed)
        {
            Console.WriteLine($"{(passed ? "PASS" : "FAIL")} {name}");
            if (!passed) failures++;
        }

        var archive = new FileSystemArchive(archiveDirectory);
        var intake = new IngestionCoordinator(archive);
        await IntakeFixtureChecks.RunAsync(archiveDirectory, Check);
        var cutoff = new DateOnly(2026, 10, 20);
        var sources = await SnapshotInputReferences.PinAsync(dataDirectory, archive);
        var definitions = await KpiDefinitionReader.ReadAsync(archive, sources.KpiDictionary);
        PinnedVersions Pins(int day) => SnapshotVersionPinning.Create(day, sources, definitions,
            ConfigurationVersionReader.References(ConfigurationVersionReader.Select(day, [])));
        var batches = new List<IngestionBatch>();
        for (var day = 0; day <= 90; day++)
            batches.Add(await intake.ReadAsync(dataDirectory, day, cutoff));

        var repeat = await intake.ReadAsync(dataDirectory, 1, new DateOnly(2026, 7, 23));
        Check("Repeated drop with a different admissible cutoff", repeat.Id == batches[1].Id &&
            IntakeFingerprint.Of(repeat) == IntakeFingerprint.Of(batches[1]));
        var initialRepeat = await intake.ReadAsync(dataDirectory, 0, new DateOnly(2026, 7, 23));
        Check("Repeated initial load", initialRepeat.Id == batches[0].Id);
        Check("All manifest-listed rows normalize", batches.All(batch =>
            batch.Facts.Count == batch.Drop.Sources.Sum(source => source.ExpectedRowCount ?? 0)));
        Check("No invalid development records", batches.SelectMany(batch => batch.Issues).All(issue => issue.Type != "invalid"));
        Check("Known alias schema versions", batches[82].Drop.Sources
            .Where(source => source.Source is "tickets" or "ticket_events")
            .All(source => source.SchemaVersion == "baseline-v2" &&
                source.Status == SourceReadStatus.ReadyForNormalization));
        Check("Unknown headers remain rejected", SourceSchemaRegistry.Select("tickets", ["unknown"]) is null);

        DailySnapshot Snapshot(int reportDay) => SnapshotBuilder.Build(reportDay,
            batches[reportDay - 1].Drop.BusinessDate!.Value, Pins(reportDay), batches.Take(reportDay));
        var missing = Snapshot(67);
        var arrived = Snapshot(68);
        var later = Snapshot(69);
        Check("Three missing sources on morning 67", missing.ReportIssues.Count(issue => issue.Type == "missing") == 3);
        Check("Three late arrivals on morning 68", arrived.ReportIssues.Count(issue => issue.Type == "late_arrival") == 3 &&
            !arrived.ReportIssues.Any(issue => issue.Type == "missing"));
        Check("No repeated late-arrival notice", !later.ReportIssues.Any(issue => issue.Type == "late_arrival"));
        var partialArrival = batches[67] with
        {
            Id = IntakeFingerprint.Of(new { batches[67].Id, Fixture = "partial-late-arrival" }),
            Issues = batches[67].Issues.Append(new IntakeIssue("tickets", "invalid", 67,
                batches[66].Drop.BusinessDate, "invalid_record", 1)).ToArray()
        };
        var incomplete = SnapshotBuilder.Build(68, arrived.Cutoff, Pins(68),
            batches.Take(67).Append(partialArrival));
        Check("Invalid late source does not clear missing evidence", incomplete.ReportIssues.Any(issue =>
            issue.Source == "tickets" && issue.Type == "missing") && !incomplete.ReportIssues.Any(issue =>
            issue.Source == "tickets" && issue.Type == "late_arrival"));
        var duplicate = Snapshot(77);
        Check("Duplicate order notice on morning 77", duplicate.ReportIssues.Count(issue =>
            issue.Source == "orders" && issue.Type == "duplicate") == 1);
        Check("Duplicate is historical evidence, not a repeated notice", Snapshot(78).ReportIssues.All(issue =>
            issue.Source != "orders" || issue.Type != "duplicate"));
        Check("Unique canonical keys", duplicate.Facts.GroupBy(fact => (fact.Source, fact.Key)).All(group => group.Count() == 1));
        var correction = batches[70].Facts.FirstOrDefault(fact => fact.Source == "crm_lead_events" &&
            fact.ValuesJson.Contains("\"value_corrected\"", StringComparison.Ordinal));
        Check("CRM correction is preserved at decimal precision", correction is not null &&
            !Snapshot(70).Facts.Any(fact => fact.Key == correction.Key && fact.Source == correction.Source) &&
            Snapshot(71).Facts.Any(fact => fact.Key == correction.Key && fact.Source == correction.Source));

        var snapshot = Snapshot(91);
        var rebuilt = SnapshotBuilder.Build(91, cutoff, Pins(91), batches.AsEnumerable().Reverse());
        Check("Deterministic snapshot", snapshot.Id == rebuilt.Id &&
            IntakeFingerprint.Of(snapshot.Facts) == IntakeFingerprint.Of(rebuilt.Facts));
        Check("No future facts", snapshot.Facts.All(fact => fact.EffectiveDate <= cutoff));
        // Exercise exactly the serialized reference stored by SnapshotStore, without a database.
        var stored = new SnapshotReference(snapshot.Id, snapshot.ReportDay, snapshot.Cutoff, snapshot.Versions, snapshot.BatchIds);
        var restoredReference = JsonSerializer.Deserialize<SnapshotReference>(JsonSerializer.Serialize(stored))!;
        var restoredSources = restoredReference.Versions.Sources!;
        var restored = SnapshotBuilder.Build(restoredReference.ReportDay, restoredReference.Cutoff,
            restoredReference.Versions, batches);
        Check("Stored snapshot reference retains all pinned archive addresses", restored.Id == snapshot.Id &&
            restoredSources == sources);
        var archiveReferences = new[] { restoredSources.Calendar, restoredSources.MonthlyTargets,
            restoredSources.KpiDictionary, restoredSources.ReferenceViews, restoredSources.EscalationRules,
            restoredSources.WorkflowDefinitions, restoredSources.Units, restoredSources.Teams,
            restoredSources.Managers, restoredSources.Staff, restoredSources.AccessMatrix };
        var reopened = 0;
        foreach (var reference in archiveReferences)
        {
            await using var archived = await archive.OpenVerifiedAsync(reference);
            if (archived.Length == reference.Size) reopened++;
        }
        Check("Historical snapshot reopens all eleven inputs from archive", reopened == archiveReferences.Length);
        using var changedPolicy = new MemoryStream("fixture policy revision"u8.ToArray());
        var revisedSources = sources with { WorkflowDefinitions = await archive.StoreAsync(changedPolicy) };
        var revisedPins = SnapshotVersionPinning.Create(91, revisedSources, definitions,
            ConfigurationVersionReader.References(ConfigurationVersionReader.Select(91, [])));
        var revisedSnapshot = SnapshotBuilder.Build(91, cutoff, revisedPins, batches);
        Check("Policy change creates a distinct snapshot with original policy still pinned", revisedSnapshot.Id != snapshot.Id &&
            revisedPins.Policy != snapshot.Versions.Policy && restoredSources.WorkflowDefinitions == sources.WorkflowDefinitions);
        var mismatchRejected = false;
        try
        {
            SnapshotBuilder.Build(91, cutoff, snapshot.Versions with { Sources = revisedSources }, batches);
        }
        catch (InvalidDataException)
        {
            mismatchRejected = true;
        }
        Check("Snapshot rejects archive references inconsistent with pinned versions", mismatchRejected);
        Check("All 55 baseline definitions", definitions.Count == 55);
        var baselineKpi = definitions[0];
        var revisedKpi = baselineKpi with { Id = "", EscalateAfterDays = baselineKpi.EscalateAfterDays + 1 };
        revisedKpi = revisedKpi with { Id = IntakeFingerprint.Of(revisedKpi) };
        ConfigurationCandidate Candidate<T>(CandidateKind kind, string key, T payload)
        {
            var candidate = new ConfigurationCandidate("", kind, key, 75, 76, "fixture-actor",
                "fixture-" + kind, JsonSerializer.Serialize(payload));
            return candidate with { Id = ConfigurationFingerprint.Of(candidate) };
        }
        var changes = new[]
        {
            Candidate(CandidateKind.KpiDefinition, baselineKpi.KpiId,
                new KpiChange(baselineKpi.KpiId, revisedKpi.Id, "fixture-receipt")),
            Candidate(CandidateKind.Organization, "ORG", new OrganizationRevision([], [], [], [])),
            Candidate(CandidateKind.ManagerPriority, "M01", new ManagerPriority("M01", [baselineKpi.KpiId]))
        };
        PinnedVersions ChangedPins(int day) => SnapshotVersionPinning.Create(day, sources, definitions,
            ConfigurationVersionReader.References(ConfigurationVersionReader.Select(day, changes)));
        var sameDay = ChangedPins(75);
        var tomorrow = ChangedPins(76);
        Check("Configuration selections are unchanged on submission day", sameDay == Pins(75) ||
            IntakeFingerprint.Of(sameDay) == IntakeFingerprint.Of(Pins(75)));
        Check("D+1 pins only the active revision of each kind", tomorrow.Organization == changes[1].Id &&
            tomorrow.KpiVersions!.Contains(new OrgPilot.Foundation.Configuration.KpiVersionReference(
                baselineKpi.KpiId, revisedKpi.Id)) &&
            !tomorrow.KpiVersions!.Any(v => v.DefinitionId == baselineKpi.Id) &&
            tomorrow.ActiveConfiguration!.ManagerPriorities.Single().CandidateId == changes[2].Id);
        Check("Manager priority is separate from KPI dictionary", tomorrow.KpiDictionary == sources.KpiDictionary.Sha256 &&
            tomorrow.ManagerPriority != Pins(76).ManagerPriority && tomorrow.MonthlyTargets == sources.MonthlyTargets.Sha256);
        var activeSnapshot = SnapshotBuilder.Build(76, batches[75].Drop.BusinessDate!.Value, tomorrow, batches.Take(76));
        Check("New configuration creates a new immutable snapshot", activeSnapshot.Id != Snapshot(76).Id &&
            IntakeFingerprint.Of(activeSnapshot.Facts) == IntakeFingerprint.Of(Snapshot(76).Facts));
        var missingProjection = await ProjectionData.CreateAsync(missing, archive);
        var missingDay = new DateOnly(2026, 9, 26);
        var ticketKpi = definitions.Single(definition => definition.KpiId == "K_SUP_TICKETS");
        var unavailable = KpiQuery.CreateRun(missingProjection, ticketKpi, [new KpiPoint(missingDay, null, 0)]);
        Check("Missing source produces null instead of zero", unavailable.Points.Any(point =>
            point.Date == missingDay && point.Value is null && point.Status == "data_unavailable"));

        var projection = await ProjectionData.CreateAsync(restored, archive);
        Check("Deterministic projection", projection.Hash ==
            (await ProjectionData.CreateAsync(rebuilt, archive)).Hash);
        await using var stream = await archive.OpenVerifiedAsync(restoredSources.ReferenceViews);
        using var reader = new StreamReader(stream);
        await using var oracle = new SqliteReferenceOracle();
        await oracle.InitializeAsync(projection, await reader.ReadToEndAsync());
        foreach (var definition in definitions)
        {
            try
            {
                var first = await oracle.QueryAsync(definition, cutoff);
                var second = await oracle.QueryAsync(definition, cutoff);
                Check($"SQLite reference {definition.KpiId} ({first.Count} rows)",
                    IntakeFingerprint.Of(first) == IntakeFingerprint.Of(second));
            }
            catch (Exception ex)
            {
                Check($"SQLite reference {definition.KpiId}: {ex.GetType().Name}", false);
            }
        }

        var metric = definitions[0];
        var point = new KpiPoint(cutoff, null, 100m);
        Check("Parity accepts exactly one percent", ParityCheck.Compare(projection, metric, [point], [point with { Value = 101m }]).Passed);
        Check("Parity rejects more than one percent", !ParityCheck.Compare(projection, metric, [point], [point with { Value = 101.01m }]).Passed);
        Check("Parity rejects null mismatch", !ParityCheck.Compare(projection, metric, [point with { Value = null }], [point with { Value = 0m }]).Passed);
        Check("Parity rejects row population mismatch", !ParityCheck.Compare(projection, metric, [point], []).Passed);
        Console.WriteLine($"Development regression checks: {failures} failures; {snapshot.Facts.Count} canonical facts.");
        return failures == 0 ? 0 : 1;
    }
}
