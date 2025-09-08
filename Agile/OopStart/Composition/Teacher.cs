namespace Composition;

public class Teacher
{
    public string Name { get; init; }

    public Teacher(string name)
    {
        Name = name;
    }

    public override string ToString()
    {
        return Name;
    }
}
