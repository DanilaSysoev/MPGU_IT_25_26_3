CREATE TABLE IF NOT EXISTS animals (
    id serial PRIMARY KEY,
    name text NOT NULL,
    age int NOT NULL CHECK(age BETWEEN 0 AND 40),
    species text NOT NULL CHECK(species IN ('Кот', 'Кошка', 'Собака')),
    owner_name text DEFAULT NULL,
    aa int NOT NULL,
    bb int NOT NULL,
    cc int NOT NULL CHECK(cc = aa + bb)
);

-- INSERT INTO animals
--     (name, age, species, owner_name)
-- VALUES
--     ('Барсик', 3, 'Кот', 'Василий Петрович');

-- INSERT INTO animals
--     (name, age, species)
-- VALUES
--     ('Барбос', 2, 'Собака');

-- -- Invalid

-- -- INSERT INTO animals
-- --     (age, species)
-- -- VALUES
-- --     (2, 'Собака');

-- INSERT INTO animals
--     (name, age, species, owner_name)
-- VALUES
--     ('Мурзик', 1, 'Кот', 'Иван Иванович'),
--     ('Бобик', 12, 'Собака', 'Сергей Петрович'),
--     ('Маруся', 5, 'Кошка', 'Татьяна Петровна'),
--     ('Маркиз', 6, 'Кот', NULL),
--     ('Буль-буль', 50, 'Рыбка', 'Татьяна Петровна');

INSERT INTO animals
    (name, age, species, owner_name, aa, bb, cc)
VALUES
    ('Барсик', 3, 'Кот', 'Василий Петрович', 1, 2, 5);
