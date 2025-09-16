namespace ExceptionsDemo;

public class Program
{
    public static void Main()
    {
        try
        {
            F();
        }
        catch (MyOwnException e)
        {
            Console.WriteLine(e.Message);
        }
        finally
        {
            Console.WriteLine("Always run in Main");
        }

        Console.WriteLine("Main catch exception");
    }

    public static void F()
    {
        try
        {
            G();
        }
        catch (InvalidOperationException e)
        {
            Console.WriteLine(e.Message);
        }
        finally
        {
            Console.WriteLine("Always run in F");
        }

        Console.WriteLine("F catch exception");
    }

    public static void G()
    {
        var line = Console.ReadLine();

        if (line == "own")
            throw new MyOwnException("Own exception");
        else if (line == "argument")
            throw new ArgumentException("Argument exception");
        else if (line != "not exception")
            throw new InvalidOperationException("Other exception");
        
        Console.WriteLine("I am alive!");
    }
}