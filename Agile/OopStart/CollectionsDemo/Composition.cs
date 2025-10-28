namespace CollectionsDemo;

public class Child
{
    public int Value { get; set; }
    public Child(int value)
    {
        Value = value;
    }

    public override string ToString()
    {
        return $"Value: {Value}";
    }
}

public class Parent
{
    public IReadOnlyList<Child> Children => children;

    public void AddChild(Child child)
    {
        children.Add(child);
    }
    public void RemoveChild(Child child)
    {
        children.Remove(child);
    }

    private readonly List<Child> children = new List<Child>();
}