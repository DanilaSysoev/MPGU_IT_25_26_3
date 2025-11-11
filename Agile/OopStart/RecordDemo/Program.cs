using RecordDemo;

Student student = new Student("Иван", 22, 3.8f);

(string studentName, int studentAge, float studentMeanGrade) = student;

Student student2 = student with { Name = "Алексей" };
Student student3 = student with { };