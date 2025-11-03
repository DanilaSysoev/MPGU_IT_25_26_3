-- OTO
CREATE TABLE IF NOT EXISTS humans (
    id serial PRIMARY KEY,
    name text NOT NULL,
    age integer NOT NULL CHECK(age >= 0)
);

CREATE TABLE IF NOT EXISTS drive_licenses (
    id serial PRIMARY KEY,
    serial text NOT NULL,
    number text NOT NULL,
    human_id integer REFERENCES humans(id) ON DELETE CASCADE ON UPDATE CASCADE
);

ALTER TABLE humans
    ADD COLUMN IF NOT EXISTS
        drive_license_id integer REFERENCES drive_licenses(id) ON DELETE SET NULL ON UPDATE CASCADE;

INSERT INTO humans
    (name, age)
VALUES
    ('Иван', 25),
    ('Петр', 30),
    ('Сидор', 35);

INSERT INTO drive_licenses
    (serial, number, human_id)
VALUES
    ('AAA', '123456', 1);

UPDATE humans SET drive_license_id = 1 WHERE id = 1;

-- OTM

CREATE TABLE IF NOT EXISTS cities (
    id serial PRIMARY KEY,
    name text NOT NULL,
    foundaton_year integer NOT NULL CHECK(foundaton_year >= 0)
);

INSERT INTO cities
    (name, foundaton_year)
VALUES
    ('Москва', 1147),
    ('Санкт-Петербург', 1703),
    ('Воронеж', 1586);

ALTER TABLE humans
    ADD COLUMN IF NOT EXISTS
        city_id integer REFERENCES cities(id) ON DELETE SET NULL ON UPDATE CASCADE;

INSERT INTO humans
    (name, age, city_id)
VALUES
    ('Сергей', 25, 2),
    ('Алексей', 30, 3);

-- MTM

CREATE TABLE students (
    id serial PRIMARY KEY,
    name text NOT NULL,
    admissin_year integer NOT NULL CHECK(admissin_year >= 1800),
    age integer NOT NULL CHECK(age >= 6)
);

CREATE TABLE disciplines (
    id serial PRIMARY KEY,
    name text NOT NULL UNIQUE,
    teacher text NOT NULL
);

CREATE TABLE students_disciplines (
    student_id integer REFERENCES students(id) ON DELETE CASCADE ON UPDATE CASCADE,
    discipline_id integer REFERENCES disciplines(id) ON DELETE CASCADE ON UPDATE CASCADE,
    grade integer NOT NULL CHECK(grade >= 0 AND grade <= 100) DEFAULT 0,
    taking_year int NOT NULL CHECK(taking_year > 1800),
    PRIMARY KEY (student_id, discipline_id)
);

INSERT INTO students
    (name, admissin_year, age)
VALUES
    ('Иванов Иван Иванович', 2018, 18),
    ('Петров Петр Петрович', 2019, 19),
    ('Сидоров Сидор Сидорович', 2020, 20),
    ('Алексеев Алексей Алексеевич', 2021, 21);

INSERT INTO disciplines
    (name, teacher)
VALUES
    ('Физика', 'Иванов И.И.'),
    ('Математика', 'Петров П.П.'),
    ('Информатика', 'Сидоров С.С.');

INSERT INTO students_disciplines
    (student_id, discipline_id, taking_year)
VALUES
    (1, 1, 2023),
    (1, 2, 2023),
    (2, 2, 2023),
    (2, 3, 2024),
    (3, 1, 2024),
    (3, 3, 2021);
