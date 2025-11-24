-- ========== SCHEMA: libraries_example ==========
-- Скрипт создания таблиц: authors, books, libraries, readers,
-- связи many-to-many с доп. атрибутами и таблица выдач.

-- Убедимся, что старые версии таблиц удалены (для повторного запуска)
DROP TABLE IF EXISTS issuances CASCADE;
DROP TABLE IF EXISTS libraries_books CASCADE;
DROP TABLE IF EXISTS readers_libraries CASCADE;
DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS authors CASCADE;
DROP TABLE IF EXISTS libraries CASCADE;
DROP TABLE IF EXISTS readers CASCADE;

-- -------------------------
-- Таблица авторов
-- -------------------------
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_year INT
);

-- -------------------------
-- Таблица книг
-- -------------------------
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    authors_id INT REFERENCES authors(id) ON DELETE RESTRICT,
    year_published INT,
    isbn VARCHAR(20) UNIQUE,
    annotation TEXT
);

-- -------------------------
-- Таблица библиотек
-- -------------------------
CREATE TABLE libraries (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    year_founded INT
);

-- -------------------------
-- Таблица читателей
-- -------------------------
CREATE TABLE readers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- -------------------------
-- MtM: читатель <-> библиотека с атрибутом "номер читательского билета"
-- readers_libraries: хранит у какой библиотеки какой читатель и его номер билета
-- Composite unique: (libraries_id, card_number) — номер билета уникален внутри библиотеки
-- Composite unique: (libraries_id, readers_id) — один читатель не может иметь несколько записей в одной библиотеке
-- -------------------------
CREATE TABLE readers_libraries (
    libraries_id INT NOT NULL REFERENCES libraries(id) ON DELETE CASCADE,
    readers_id INT NOT NULL REFERENCES readers(id) ON DELETE CASCADE,
    card_number TEXT NOT NULL,
    membership_started DATE DEFAULT CURRENT_DATE,
    membership_ends DATE,
    PRIMARY KEY (libraries_id, readers_id),
    CONSTRAINT uniq_card_per_libraries UNIQUE (libraries_id, card_number)
);

-- -------------------------
-- MtM: книга <-> библиотека с атрибутом "количество"
-- libraries_books: сколько экземпляров данной книги в библиотеке
-- -------------------------
CREATE TABLE libraries_books (
    libraries_id INT NOT NULL REFERENCES libraries(id) ON DELETE CASCADE,
    books_id INT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    quantity INT NOT NULL CHECK (quantity >= 0),
    shelf TEXT,
    PRIMARY KEY (libraries_id, books_id)
);

-- -------------------------
-- Таблица выдач
-- Поля:
--   id
--   libraries_id -> библиотека, где выдана книга
--   card_number -> номер читательского билета (ссылаемся на readers_libraries.libraries_id + card_number)
--   books_id -> какая книга (FK)
--   term_days -> срок в днях (целое, >0)
--   issued_at -> дата выдачи
-- Дополнительно создаём FOREIGN KEY (libraries_id, card_number) -> readers_libraries(libraries_id, card_number)
-- -------------------------
CREATE TABLE issuances (
    id SERIAL PRIMARY KEY,
    libraries_id INT NOT NULL REFERENCES libraries(id) ON DELETE CASCADE,
    card_number TEXT NOT NULL,
    books_id INT NOT NULL REFERENCES books(id) ON DELETE RESTRICT,
    term_days INT NOT NULL CHECK (term_days > 0),
    issued_at DATE NOT NULL DEFAULT CURRENT_DATE,
    returned_at DATE,
    CONSTRAINT fk_readers_card FOREIGN KEY (libraries_id, card_number)
        REFERENCES readers_libraries (libraries_id, card_number)
        ON DELETE RESTRICT
);

-- Индексы для ускорения поиска выдач по читателю / книге
CREATE INDEX idx_issuances_card ON issuances(libraries_id, card_number);
CREATE INDEX idx_issuances_books ON issuances(books_id);

-- -------------------------
-- Наполнение данными (пример)
-- -------------------------

-- Авторы
INSERT INTO authors (name, birth_year) VALUES
('Фёдор Достоевский', 1821),
('Лев Толстой', 1828),
('Маргарет Этвуд', 1939),
('Джордж Оруэлл', 1903),
('Харуки Мураками', 1949);

-- Книги
INSERT INTO books (title, authors_id, year_published, isbn, annotation) VALUES
('Преступление и наказание', 1, 1866, '978-5-17-118366-1', 'Классика русской литературы. Роман о моральных дилеммах.'),
('Война и мир', 2, 1869, '978-5-17-084875-6', 'Эпопея о России эпохи Наполеоновских войн.'),
('Рассказ служанки', 3, 1985, '978-0-241-12239-1', 'Антиутопия о тоталитарном обществе.'),
('1984', 4, 1949, '978-0-452-28423-4', 'Антиутопия про тоталитарный контроль и манипуляцию правдой.'),
('Норвежский лес', 5, 1987, '978-0-670-80752-0', 'Роман о взрослении и потерях.'),
('Идиот', 1, 1869, '978-5-17-089565-5', 'Роман о человеке с необычной добротой в жестоком мире.'),
('Анна Каренина', 2, 1877, '978-5-699-98973-4', 'Трагедия любви и общества.'),
('Хор любимых женщин', 5, 2013, '978-0-316-25280-9', 'Сборник рассказов и эссе.');

-- Библиотеки
INSERT INTO libraries (name, year_founded) VALUES
('Центральная городская библиотека', 1952),
('Библиотека на Тихой улице', 1998);

-- Читатели
INSERT INTO readers (name) VALUES
('Алексей Иванов'),
('Мария Смирнова'),
('Ольга Петрова'),
('Игорь Кузнецов');

-- Связи читатель <-> библиотека (readers_libraries) с номерами чит. билетов
-- Предполагаем, что номера билетов уникальны внутри библиотеки, например 'C-0001'
INSERT INTO readers_libraries (libraries_id, readers_id, card_number, membership_started) VALUES
(1, 1, 'C-0001', '2020-02-10'),
(1, 2, 'C-0002', '2021-06-15'),
(2, 3, 'T-1001', '2022-01-05'),
(2, 4, 'T-1002', '2023-09-20'),
-- читатель 1 также в библиотеке 2 (например, переехал)
(2, 1, 'T-2001', '2024-03-01');

-- Книжный фонд: книга <-> библиотека с количеством экземпляров
INSERT INTO libraries_books (libraries_id, books_id, quantity, shelf) VALUES
(1, 1, 3, 'A-1'),
(1, 2, 1, 'A-2'),
(1, 4, 2, 'B-1'),
(1, 6, 1, 'A-3'),
(2, 3, 4, 'C-1'),
(2, 5, 2, 'C-2'),
(2, 7, 1, 'C-3'),
(2, 8, 2, 'C-4'),
(1, 5, 1, 'B-2'); -- Мураками есть в обеих библиотеках

-- Выдачи (issuances)
-- выдача из Центральной библиотеки (libraries_id = 1)
INSERT INTO issuances (libraries_id, card_number, books_id, term_days, issued_at) VALUES
(1, 'C-0001', 1, 21, '2025-11-01'),  -- Алексей взял "Преступление и наказание"
(1, 'C-0002', 4, 14, '2025-10-28'),  -- Мария взяла "1984"
(1, 'C-0001', 6, 30, '2025-09-15');  -- Алексей взял "Идиот"

-- выдача из библиотеки на Тихой улице (libraries_id = 2)
INSERT INTO issuances (libraries_id, card_number, books_id, term_days, issued_at) VALUES
(2, 'T-1001', 3, 14, '2025-11-10'), -- Ольга взяла "Рассказ служанки"
(2, 'T-1002', 5, 21, '2025-11-05'), -- Игорь взял "Норвежский лес"
(2, 'T-2001', 8, 14, '2025-10-20'); -- Алексей (в библиотеке 2) взял сборник Мураками

-- ========== Примеры запросов (комментарии) ==========
-- Посмотреть все книги и их авторов:
-- SELECT b.id, b.title, a.name AS authors, b.year_published FROM books b JOIN authors a USING (id) -- (ошибка: пример)
-- Правильно:
-- SELECT b.id, b.title, a.name AS authors, b.year_published
-- FROM books b
-- JOIN authors a ON b.authors_id = a.id;

-- Проверить текущие активные выдачи читателя по его id:
-- SELECT i.* FROM issuances i
-- JOIN readers_libraries rl ON (i.libraries_id = rl.libraries_id AND i.card_number = rl.card_number)
-- WHERE rl.readers_id = 1;

-- Снижение количества при выдаче и проверка наличия можно реализовать в триггерах/транзакциях при необходимости.

-- ============================================
-- ДОПОЛНИТЕЛЬНЫЕ ДАННЫЕ ДЛЯ ДЕМОНСТРАЦИИ JOIN
-- ============================================

-- 1. Дополнительные авторы
INSERT INTO authors (name, birth_year) VALUES
('Неизвестный автор', NULL),          -- для LEFT JOIN (книга без автора)
('Джон Смит', 1975),
('Эмили Браун', 1982),
('Иван Иванов', 1991);

-- 2. Дополнительные книги
INSERT INTO books (title, authors_id, year_published, isbn, annotation) VALUES
('Загадочная книга', 6, 2000, NULL, 'Книга без ISBN и почти без автора.'),
('Путешествие в горы', 7, 2010, '111-1111111111', 'Приключенческая книга.'),
('Тайные сны', 8, 2018, '222-2222222222', 'Романтическая проза.'),
('Книга без автора', NULL, 2020, '333-3333333333', 'Осознанно оставлена без автора — для LEFT JOIN.'),
('Редкая рукопись', NULL, NULL, NULL, 'Нет года, нет автора — идеальна для FULL JOIN.');

-- 3. Дополнительные библиотеки
INSERT INTO libraries (name, year_founded) VALUES
('Библиотека на холме', 2005),
('Старая районная библиотека', NULL),
('Маленький читалый клуб', 2023);

-- 4. Дополнительные читатели
INSERT INTO readers (name) VALUES
('Читатель без библиотеки'),
('Ветеран чтения'),
('Постоянный посетитель'),
('Гость');

-- 5. readers_libraries — некоторые читатели ни в одной библиотеке не состоят
INSERT INTO readers_libraries (libraries_id, readers_id, card_number, membership_started) VALUES
(1, 5, 'C-0100', '2024-05-10'),
(3, 6, 'H-2001', '2023-01-01'),
(4, 7, 'O-3001', '2024-12-01'),
(5, 4, 'M-5001', '2025-02-20'); -- читатель 4 состоит в библиотеке 5

-- НЕ добавляем читателя 8 — он остаётся без библиотек для демонстрации LEFT/RIGHT JOIN

-- 6. libraries_books — добавим книги в новые библиотеки
INSERT INTO libraries_books (libraries_id, books_id, quantity, shelf) VALUES
(3, 7, 2, 'D-1'),
(3, 8, 1, 'D-2'),
(4, 9, 3, 'E-1'),
(5, 10, 1, 'F-1'),
(5, 11, 2, 'F-2'),
(5, 12, 1, 'F-3'),
(3, 13, 1, 'D-3');  -- редкая рукопись есть только в 1 библиотеке

-- 7. issuances — много разных комбинаций
INSERT INTO issuances (libraries_id, card_number, books_id, term_days, issued_at) VALUES
(3, 'H-2001', 9, 14, '2025-11-01'),
(3, 'H-2001', 10, 30, '2025-11-05'),
(4, 'O-3001', 11, 21, '2025-11-10'),
(5, 'M-5001', 12, 7, '2025-11-05'),
(5, 'M-5001', 13, 14, '2025-11-12');
