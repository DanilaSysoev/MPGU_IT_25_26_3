namespace RecordDemo;

// public record class Student
// {
//     public string Name { get; init; }
//     public int Age { get; init; }
//     public float MeanGrade { get; init; }

//     public Student(string name, int age, float meanGrade)
//     {
//         Name = name;
//         Age = age;
//         MeanGrade = meanGrade;
//     }

//     public void Deconstruct(out string name, out int age, out float meanGrade)
//     {
//         name = Name;
//         age = Age;
//         meanGrade = MeanGrade;
//     }
// }

public record Student(string Name, int Age, float MeanGrade);