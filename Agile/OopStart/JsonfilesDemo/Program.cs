using JsonfilesDemo;

namespace JsonFileIoDemo;

static class Program
{
    public static void Main(string[] args)
    {
        for(int i = 0; i < args.Length; ++i)
        {
            var path = Path.Join("./data", args[i]);
            if(!File.Exists(path))
            {
                Console.WriteLine($"File {path} not exists");
            }
            else
            {
                using StreamReader reader = new StreamReader(path);
                Console.WriteLine($"File {path}:");
                while (!reader.EndOfStream)
                {
                    Console.WriteLine($"> {reader.ReadLine()}");
                }
            }
        }

        {
            using StreamWriter writer = new StreamWriter("./data/result.txt");
            writer.WriteLine("Hello");
        }

        CoreJsonDemo.ReadJson(Path.Join(".", "data", "data.json"));
        Console.WriteLine();
        NewtonsoftDemo.ReadJson(Path.Join(".", "data", "data.json"));
        Console.WriteLine();

        CoreJsonDemo.WriteJson(Path.Join(".", "data", "data2.json"));
        NewtonsoftDemo.WriteJson(Path.Join(".", "data", "data3.json"));        
    }
}
