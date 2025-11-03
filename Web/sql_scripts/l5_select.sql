-- SELECT * FROM humans;
-- SELECT * FROM drive_licenses;

-- SELECT * FROM humans
-- WHERE city_id = 1;

SELECT * FROM students, students_disciplines
WHERE students_disciplines.student_id = students.id AND
      students_disciplines.discipline_id = 1;
