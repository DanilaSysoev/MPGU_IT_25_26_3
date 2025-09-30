namespace GameEngine;

static class Program
{
    private static int callsCount = 0;

    public static void Update()
    {
        callsCount += 1;
    }

    public static void Main(string[] args)
    {
        Update();
        Console.WriteLine("Hello: {0}", callsCount);
    }
}
