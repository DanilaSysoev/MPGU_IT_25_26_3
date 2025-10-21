namespace EventsDemo;


public delegate void ValueIsInterecting(Notifier sender);


public class Notifier
{
    public event ValueIsInterecting? ValueIsInterecting;

    public event ValueIsInterecting? CustomValueIsInterecting
    {
        add
        {
            customValueIsInterecting += value;
            if(value is not null)
                Console.WriteLine(
                    "[INFO] {0} subscribed to custom event with {1}",
                    value.Target?.GetType().Name,
                    value.Method.Name
                );
        }
        remove
        {
            if (customValueIsInterecting != null)
            {
                customValueIsInterecting -= value;
            }
        }
    }

    public event EventHandler<int>? StandartEvent;

    public int Value
    {
        get => value;
        set
        {
            this.value = value;
            if (value == InterestingValue)
                ValueIsInterecting?.Invoke(this);
        }
    }
    public int InterestingValue { get; init; }

    public Notifier(int value, int interestingValue)
    {
        InterestingValue = interestingValue;
        Value = value;
    }

    public void StandartEventOn()
    {
        StandartEvent?.Invoke(this, value);
    }

    private int value;
    private ValueIsInterecting? customValueIsInterecting;
}
