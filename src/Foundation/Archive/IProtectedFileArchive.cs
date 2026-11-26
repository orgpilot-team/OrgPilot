namespace OrgPilot.Foundation.Archive;

public sealed record ArchiveReference(string Sha256, long Size);

public interface IProtectedFileArchive
{
    Task<ArchiveReference> StoreAsync(Stream content, CancellationToken cancellationToken = default);

    // The caller owns the returned stream. The archive verifies its hash before returning it.
    Task<Stream> OpenVerifiedAsync(ArchiveReference reference, CancellationToken cancellationToken = default);
}
