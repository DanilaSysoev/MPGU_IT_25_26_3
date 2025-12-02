using System.Text.Json.Nodes;
using Newtonsoft.Json;

namespace JsonfilesDemo;

public static class NewtonsoftDemo
{
    public static void ReadJson(string filename)
    {        
        var json = File.ReadAllText(filename);
        var data = JsonNode.Parse(json);
        Console.WriteLine(data);

        Console.WriteLine(data!["Name"]!.GetValue<string>());
        Console.WriteLine(data!["Value"]!.GetValue<int>());
        Console.WriteLine(data!["Data"]!.AsArray());
    }

    public static void WriteJson(string filename)
    {        
        var data = new {
            Name = "Test",
            Value = 10,
            Data = new List<int> { 1, 2, 3 },
            Addition = 20.5,
        };
        var json = JsonConvert.SerializeObject(data);
        File.WriteAllText(filename, json);
    }
}
