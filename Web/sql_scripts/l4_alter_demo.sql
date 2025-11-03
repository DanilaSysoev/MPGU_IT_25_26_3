-- ALTER TABLE students ADD COLUMN IF NOT EXISTS age int CHECK(age > 6);

-- ALTER TABLE students ADD CHECK(faculty in ('ПММ', 'Информатика', 'ИнЯз', 'ИМО', 'Экономика'));

-- ALTER TABLE students ALTER COLUMN name TYPE varchar(128);

-- ALTER TABLE students RENAME COLUMN name TO fio;

-- ALTER TABLE students ADD COLUMN IF NOT EXISTS test text;

ALTER TABLE students DROP COLUMN test;