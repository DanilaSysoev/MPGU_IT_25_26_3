namespace CollectionsDemo;

public static class Demos
{
    public static void ListDemo()
    {
        Random random = new Random(100);

        List<int> data1 = new List<int>();

        for (int i = 0; i < 10; i++)
            data1.Add(random.Next(100));

        for (int i = 0; i < data1.Count; i++)
            Console.Write("{0} ", data1[i]);
        Console.WriteLine();

        int[] tmpData = { 1, 2, 3 };
        data1.AddRange(tmpData);
        data1.Sort();

        for (int i = 0; i < data1.Count; i++)
            Console.Write("{0} ", data1[i]);
        Console.WriteLine();

        for (int i = 1; i <= data1.Count; i++)
            Console.Write("{0} ", data1[^i]);
        Console.WriteLine();

        var slice = data1[1..4];
        for (int i = 0; i < slice.Count; i++)
            Console.Write("{0} ", slice[i]);
        Console.WriteLine();

        List<int> data2 = new List<int>() { 1, 2, 3 };
        for (int i = 0; i < data2.Count; i++)   
            Console.Write("{0} ", data2[i]);
        Console.WriteLine();
    }

    public static void DirectoryDemo()
    {
        var dict = new Dictionary<string, int>()
        {
            { "one", 1 },
            { "two", 2 },
            { "three", 3 }
        };
        PrintDict(dict);

        dict.Add("four", 4);
        PrintDict(dict);

        dict.Remove("three");
        PrintDict(dict);

        dict.Remove("ten");
        PrintDict(dict);

        foreach (var key in dict.Keys)
            Console.WriteLine(key);
        foreach (var value in dict.Values)
            Console.WriteLine(value);

        dict["one"] = 10;
        PrintDict(dict);
    }

    public static void OwnEnumerableDemo()
    {
        EnumerableDemo demo = new EnumerableDemo([2, 5, 1, 3, 8]);

        foreach (var item in demo)
            Console.Write("{0} ", item);
        Console.WriteLine();
    }

    public static void GeneratorDemo()
    {
        var generator = new GeneratorDemo();

        foreach (var item in generator)
            Console.Write("{0} ", item);
        Console.WriteLine();
    }

    public static void ReadoblyDemo()
    {
        var parent = new Parent();
        parent.AddChild(new Child(1));
        parent.AddChild(new Child(2));
        parent.AddChild(new Child(3));
        parent.AddChild(new Child(4));

        for (int i = 0; i < parent.Children.Count; i++)
            Console.WriteLine(parent.Children[i]);
    }

    public static void IndexatorDemo()
    {
        var indexator = new IndexatorDemo();

        Console.WriteLine(indexator[1]);
        Console.WriteLine(indexator[1000]);
        indexator[100] = 1234;
        Console.WriteLine(indexator[12]);

        Console.WriteLine(indexator[10, 12]);
    }

    private static void PrintDict<TKey, TValue>(Dictionary<TKey, TValue> dict)
        where TKey : notnull
    {
        foreach (var item in dict)
            Console.WriteLine("{0}: {1}", item.Key, item.Value);
    }
}
