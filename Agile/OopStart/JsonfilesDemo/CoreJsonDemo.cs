using System.Text.Json;

namespace JsonfilesDemo;

class JsonData
{
    public string Name { get; set; } = "";
    public int Value { get; set; }
    public List<string> Data { get; set; } = new();

    public override string ToString()
    {
        return $"{Name}: {Value}, Data: {Data}";
    }
}

public static class CoreJsonDemo
{
    public static void ReadJson(string filename)
    {        
        var json = File.ReadAllText(filename);
        var data = JsonSerializer.Deserialize<JsonData>(json);
        Console.WriteLine(data);
    }

    public static void WriteJson(string filename)
    {   
        var data = new JsonData { Name = "Test", Value = 10, Data = new() { "1", "2", "3" } };
        var json = JsonSerializer.Serialize(data);
        File.WriteAllText(filename, json);
    }
}
