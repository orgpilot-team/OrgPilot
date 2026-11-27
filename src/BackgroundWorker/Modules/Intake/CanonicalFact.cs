using System.Text.Json;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.BackgroundWorker.Modules.Intake;

public sealed record CanonicalFact(string Source, string Key, DateOnly EffectiveDate,
    int DropDay, string SchemaVersion, ArchiveReference Archive, int RecordNumber, string ValuesJson);

public sealed record IntakeIssue(string Source, string Type, int DropDay, DateOnly? EffectiveDate,
    string Code, int? RecordNumber = null);

public sealed record IngestionBatch(string Id, DropRead Drop,
    IReadOnlyList<CanonicalFact> Facts, IReadOnlyList<IntakeIssue> Issues);

public static class IntakeFingerprint
{
    public static string Of<T>(T value) =>
        Convert.ToHexStringLower(System.Security.Cryptography.SHA256.HashData(JsonSerializer.SerializeToUtf8Bytes(value)));
}
