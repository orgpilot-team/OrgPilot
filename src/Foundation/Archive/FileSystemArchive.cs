using System.Security.Cryptography;

namespace OrgPilot.Foundation.Archive;

public sealed class FileSystemArchive(string rootPath) : IProtectedFileArchive
{
    private readonly string _root = Path.GetFullPath(rootPath);

    public async Task<ArchiveReference> StoreAsync(Stream content, CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(content);
        Directory.CreateDirectory(_root);
        var temporary = Path.Combine(_root, $".{Guid.NewGuid():N}.tmp");
        try
        {
            ArchiveReference reference;
            await using (var output = new FileStream(temporary, FileMode.CreateNew, FileAccess.ReadWrite,
                FileShare.None, 81920, FileOptions.Asynchronous | FileOptions.SequentialScan))
            {
                await content.CopyToAsync(output, cancellationToken);
                await output.FlushAsync(cancellationToken);
                output.Position = 0;
                var digest = await SHA256.HashDataAsync(output, cancellationToken);
                reference = new ArchiveReference(Convert.ToHexStringLower(digest), output.Length);
            }

            cancellationToken.ThrowIfCancellationRequested();
            var destination = PathFor(reference);
            try
            {
                File.Move(temporary, destination, overwrite: false);
            }
            catch (IOException) when (File.Exists(destination))
            {
                // An identical concurrent store is safe only if the existing object is intact.
                await using var existing = await OpenVerifiedAsync(reference, cancellationToken);
            }

            return reference;
        }
        finally
        {
            File.Delete(temporary);
        }
    }

    public async Task<Stream> OpenVerifiedAsync(ArchiveReference reference, CancellationToken cancellationToken = default)
    {
        var stream = new FileStream(PathFor(reference), FileMode.Open, FileAccess.Read,
            FileShare.Read, 81920, FileOptions.Asynchronous | FileOptions.SequentialScan);
        try
        {
            var digest = await SHA256.HashDataAsync(stream, cancellationToken);
            if (stream.Length != reference.Size || Convert.ToHexStringLower(digest) != reference.Sha256)
                throw new InvalidDataException("Archived object failed integrity verification.");
            stream.Position = 0;
            return stream;
        }
        catch
        {
            await stream.DisposeAsync();
            throw;
        }
    }

    private string PathFor(ArchiveReference reference)
    {
        ArgumentNullException.ThrowIfNull(reference);
        if (reference.Size < 0 || reference.Sha256 is not { Length: 64 } ||
            !reference.Sha256.All(c => c is >= '0' and <= '9' or >= 'a' and <= 'f'))
            throw new ArgumentException("Invalid archive reference.", nameof(reference));
        return Path.Combine(_root, reference.Sha256);
    }
}
