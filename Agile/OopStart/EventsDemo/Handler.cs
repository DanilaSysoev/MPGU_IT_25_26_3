namespace EventsDemo;

public class Handler
{
    public int Id { get; init; }

    public Handler(int id)
    {
        Id = id;
    }

    public Handler(int id, Notifier notifier)
    {
        Id = id;
        notifier.ValueIsInterecting += NotifierValueIsInterecting;
    }

    public void NotifierValueIsInterecting(Notifier sender)
    {
        Console.WriteLine("Handle event: handler {0}", Id);
    }
}
