using System.Security.Cryptography;

namespace OrgPilot.Foundation.Archive;

// An explicit infrastructure check over synthetic bytes in an isolated directory on the archive volume.
public static class ArchiveSmokeCheck
{
    public static async Task RunAsync(string archiveRoot, CancellationToken cancellationToken = default)
    {
        var root = Directory.CreateDirectory(Path.Combine(archiveRoot, $".smoke-{Guid.NewGuid():N}")).FullName;
        try
        {
            var archive = new FileSystemArchive(root);
            var sample = "OrgPilot Stage 1 archive smoke check"u8.ToArray();
            var expected = Convert.ToHexStringLower(SHA256.HashData(sample));
            var original = await archive.StoreAsync(new MemoryStream(sample), cancellationToken);
            var repeated = await archive.StoreAsync(new MemoryStream(sample), cancellationToken);
            if (original != repeated || original.Sha256 != expected || original.Size != sample.Length)
                throw new InvalidDataException("Archive write or idempotency check failed.");

            await using var stored = await archive.OpenVerifiedAsync(original, cancellationToken);
            using var output = new MemoryStream();
            await stored.CopyToAsync(output, cancellationToken);
            if (!sample.AsSpan().SequenceEqual(output.ToArray()))
                throw new InvalidDataException("Archive round-trip check failed.");
        }
        finally
        {
            Directory.Delete(root, recursive: true);
        }
    }
}
