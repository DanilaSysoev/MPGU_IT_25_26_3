namespace Composition;

public class Student
{
    public string Name { get; init; }

    public Student(string name)
    {
        Name = name;
    }

    public override string ToString()
    {
        return Name;
    }
}
