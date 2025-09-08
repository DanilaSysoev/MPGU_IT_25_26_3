using Composition;


var g1 = new Group("Group 1");
g1.AddStudent(new Student("Ivan"));
g1.AddStudent(new Student("Petr"));
g1.AddStudent(new Student("Irina"));

var g2 = new Group("Group 2");
g2.AddStudent(new Student("Tatyana"));
g2.AddStudent(new Student("Olga"));
g2.AddStudent(new Student("Anrey"));
g2.AddStudent(new Student("Alexander"));

var course = new Course("OOP", new Teacher("Ivanov"));
course.AddGroup(g1);
course.AddGroup(g2);

Console.WriteLine(course);
foreach (var group in course.Groups)
{
    Console.WriteLine($"  {group}:");
    for (int i = 0; i < group.GetStudentsCount(); i++)
    {
        Console.WriteLine($"    {group.GetStudent(i)}");
    }
}
Console.WriteLine($"  Teacher: {course.Teacher}");
