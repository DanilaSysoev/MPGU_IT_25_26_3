using EventsDemo;

Notifier notifier = new Notifier(0, 5);

Handler h1 = new Handler(1, notifier);
Handler h2 = new Handler(2);

notifier.Value = 5;
Console.WriteLine();

notifier.ValueIsInterecting += h2.NotifierValueIsInterecting;
notifier.Value = 5;
Console.WriteLine();

notifier.ValueIsInterecting -= h1.NotifierValueIsInterecting;
notifier.Value = 5;
Console.WriteLine();

notifier.Value = 100;

notifier.CustomValueIsInterecting += h2.NotifierValueIsInterecting;