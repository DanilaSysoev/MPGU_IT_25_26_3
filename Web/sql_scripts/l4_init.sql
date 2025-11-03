CREATE TABLE IF NOT EXISTS students (
    id serial PRIMARY KEY,
    name text NOT NULL,
    admission_year int NOT NULL CHECK(admission_year > 1800),
    faculty text NOT NULL
);

INSERT INTO students
    (name, admission_year, faculty)
VALUES
    ('Иванов Иван Иванович', 2024, 'ПММ'),
    ('Петров Петр Петрович', 2023, 'ИМО'),
    ('Сидоров Сидор Сидорович', 2022, 'Информатика'),
    ('Алексеев Алексей Алексеевич', 2021, 'ИнЯз');
