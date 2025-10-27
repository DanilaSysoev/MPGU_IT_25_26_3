-- SELECT * FROM goods;

-- SELECT name, price FROM goods;

-- SELECT name AS "Название товара", price AS "Цена товара" FROM goods;

-- SELECT name, price * count AS total_cost FROM goods;

-- SELECT name, price, article, 'На складе' AS status FROM goods;

-- SELECT * FROM goods
-- WHERE price > 500;

-- SELECT name, article, price FROM goods
-- WHERE price > 500 OR price < 100;

-- SELECT * FROM goods
-- WHERE EXTRACT(YEAR FROM created_at) = 2025;

-- SELECT * FROM goods
-- WHERE EXTRACT(YEAR FROM created_at) BETWEEN 2020 AND 2024;

-- SELECT * FROM goods
-- WHERE description LIKE '%Акция%';

-- SELECT * FROM goods
-- WHERE description ILIKE '%акция%';

-- SELECT * FROM goods
-- WHERE supplier ILIKE '%ферм%';

-- SELECT * FROM goods
-- WHERE article LIKE '1234_';

-- SELECT * FROM goods;

-- SELECT * FROM goods
-- WHERE price > 0
-- ORDER BY price;

-- SELECT * FROM goods
-- WHERE price > 0
-- ORDER BY price DESC;

-- SELECT name, supplier, price FROM goods
-- WHERE price > 0
-- ORDER BY supplier ASC, price DESC;

SELECT * FROM goods
WHERE price > 0
ORDER BY price DESC
LIMIT 5;
