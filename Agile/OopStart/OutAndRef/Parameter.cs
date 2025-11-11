namespace OutAndRef;

public class Parameter
{
    public string Name { get; set; } = "";
    public int Value { get; set; }

    public override string ToString()
    {
        return $"{Name}: {Value}";
    }
}
