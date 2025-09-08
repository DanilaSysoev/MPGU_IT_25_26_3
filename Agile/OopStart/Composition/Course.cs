using System.Collections.Generic;

namespace Composition;

public class Course
{
    public string Name { get; init; }
    public Teacher Teacher { get; set; }
    public IEnumerable<Group> Groups => groups;

    public Course(string name, Teacher teacher)
    {
        Name = name;
        Teacher = teacher;
        groups = new List<Group>();
    }

    public void AddGroup(Group group)
    {
        groups.Add(group);
    }
    public void RemoveGroup(Group group)
    {
        groups.Remove(group);
    }

    public override string ToString()
    {
        return Name;
    }


    private readonly List<Group> groups;
}
