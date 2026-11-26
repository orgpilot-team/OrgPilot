namespace OrgPilot.Foundation.Time;

/// <summary>Business dates are supplied by the run, never derived from the host clock.</summary>
public interface IBusinessClock
{
    DateOnly BusinessDate { get; }
    DateTimeOffset Cutoff { get; }
}
