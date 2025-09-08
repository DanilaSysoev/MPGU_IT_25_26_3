class Teacher:
    def __init__(self, name: str):
        self.name: str = name
    
    def __str__(self) -> str:
        return self.name
    

class Student:
    def __init__(self, name: str):
        self.name: str = name
    
    def __str__(self) -> str:
        return self.name
    

class Group:
    def __init__(self, name: str):
        self.name: str = name
        self.students: list[Student] = []
    
    def add_student(self, student: Student) -> None:
        if student not in self.students:
            self.students.append(student)
    
    def remove_student(self, student: Student) -> None:
        if student in self.students:
            self.students.remove(student)
            
    def count_of_students(self) -> int:
        return len(self.students)
    
    def get_student(self, index: int) -> Student:
        if 0 <= index < len(self.students):
            return self.students[index]
        else:
            raise IndexError()

    def get_students(self) -> list[Student]:
        return list(self.students)
    
    def __str__(self) -> str:
        return f"{self.name}, число студентов: {len(self.students)}"
    

class Course:
    def __init__(self, name: str):
        self.name: str = name
        self.groups: list[Group] = []
        self.teachers: list[Teacher] = []
        
    def add_group(self, group: Group) -> None:
        if group not in self.groups:
            self.groups.append(group)
            
    def add_teacher(self, teacher: Teacher) -> None:
        if teacher not in self.teachers:
            self.teachers.append(teacher)
            
    def remove_group(self, group: Group) -> None:
        if group in self.groups:
            self.groups.remove(group)
            
    def remove_teacher(self, teacher: Teacher) -> None:
        if teacher in self.teachers:
            self.teachers.remove(teacher)
            
    def get_groups(self) -> list[Group]:
        return list(self.groups)

    def get_teachers(self) -> list[Teacher]:
        return list(self.teachers)
    
    def get_description(self) -> str:
        lines = [f"Курс: {self.name}", "Группы:"]

        for group in self.groups:
            lines.append(f"  {group.name}:")
            for student in group.students:
                lines.append(f"    {student}")

        lines.append("Преподаватели:")
        for teacher in self.teachers:
            if teacher:
                lines.append(f"  {teacher}")

        return "\n".join(lines)
        
    
    def __str__(self) -> str:
        return self.name


def main():
    g1 = Group('101')
    g2 = Group('102')
    
    g1.add_student(Student('Иван'))
    g1.add_student(Student('Петр'))
    g1.add_student(Student('Наталья'))
    
    g2.add_student(Student('Татьяна'))
    g2.add_student(Student('Ирина'))
    g2.add_student(Student('Алексей'))
    g2.add_student(Student('Александр'))
    
    t1 = Teacher('Иванов Иван Иванович')
    
    c1 = Course('Математика')
    c1.add_group(g1)
    c1.add_group(g2)
    c1.add_teacher(t1)
    
    print(c1.get_description())


if __name__ == "__main__":
    main()
