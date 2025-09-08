namespace Composition;

public class Group
{
    public string Name { get; init; }

    public Group(string name)
    {
        Name = name;
        students = new Student[MaxGroupSize];
        studentsCount = 0;
    }

    public void AddStudent(Student student)
    {
        if (studentsCount < students.Length)
            students[studentsCount++] = student;
        else
            throw new InvalidOperationException(GroupIsFullError);
    }
    public void RemoveStudent(Student student)
    {
        var index = Array.IndexOf(students, student);

        if (index < 0) return;

        for (var i = index + 1; i < studentsCount; i++)
            students[i - 1] = students[i];
        --studentsCount;
    }
    public int GetStudentsCount()
    {
        return studentsCount;
    }
    public Student GetStudent(int index)
    {
        if (index < studentsCount)
            return students[index];
        else
            throw new InvalidOperationException(StudentNotExistsError);
    }

    public override string ToString()
    {
        return Name;
    }


    private readonly Student[] students;
    private int studentsCount;

    private const int MaxGroupSize = 64;
    private const string GroupIsFullError = "Group is full";
    private const string StudentNotExistsError = "Student not exists";
}
