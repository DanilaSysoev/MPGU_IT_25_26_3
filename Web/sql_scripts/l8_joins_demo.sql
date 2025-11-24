-- SELECT * FROM authors;
-- SELECT * FROM readers;

-- SELECT a.name, r.name
-- FROM authors AS a
-- CROSS JOIN readers AS r;

-- SELECT a.name, r.name
-- FROM authors AS a, readers AS r;

-- SELECT a1.name, a2.name
-- FROM authors AS a1, authors AS a2;

-- SELECT r.name, rl.card_number
-- FROM readers AS r
-- JOIN readers_libraries AS rl ON r.id = rl.readers_id
-- ORDER BY r.name;

-- SELECT r.name, COUNT(rl.card_number)
-- FROM readers AS r
-- JOIN readers_libraries AS rl ON r.id = rl.readers_id
-- GROUP BY r.name
-- ORDER BY r.name;

-- SELECT r.name, COUNT(rl.card_number)
-- FROM readers AS r
-- INNER JOIN readers_libraries AS rl ON r.id = rl.readers_id
-- GROUP BY r.name
-- ORDER BY r.name;

-- SELECT a.name, COUNT(b.title)
-- FROM authors AS a
-- LEFT JOIN books AS b ON a.id = b.authors_id
-- GROUP BY a.name;

-- SELECT a.name, COUNT(b.title)
-- FROM authors AS a
-- RIGHT JOIN books AS b ON a.id = b.authors_id
-- GROUP BY a.name;

-- SELECT a.name, COUNT(b.title)
-- FROM authors AS a
-- FULL JOIN books AS b ON a.id = b.authors_id
-- GROUP BY a.name;


-- SELECT a.name, COUNT(b.title)
-- FROM authors AS a
-- LEFT OUTER JOIN books AS b ON a.id = b.authors_id
-- GROUP BY a.name;

-- SELECT a.name, COUNT(b.title)
-- FROM authors AS a
-- RIGHT OUTER JOIN books AS b ON a.id = b.authors_id
-- GROUP BY a.name;

-- SELECT a.name, COUNT(b.title)
-- FROM authors AS a
-- FULL OUTER JOIN books AS b ON a.id = b.authors_id
-- GROUP BY a.name;

-- SELECT r.name, rl.card_number, l.name
-- FROM readers AS r
-- LEFT JOIN readers_libraries AS rl ON r.id = rl.readers_id
-- JOIN libraries AS l ON rl.libraries_id = l.id
-- ORDER BY l.name;

-- SELECT r.name, i.*
-- FROM readers r
-- LEFT JOIN LATERAL (
--     SELECT i.*
--     FROM issuances i
--     JOIN readers_libraries rl
--       ON rl.libraries_id = i.libraries_id
--      AND rl.card_number = i.card_number
--     WHERE rl.readers_id = r.id
--     ORDER BY i.issued_at DESC
--     LIMIT 1
-- ) i ON true;

SELECT r.name, i.*
FROM readers r
JOIN LATERAL (
    SELECT i.*
    FROM issuances i
    JOIN readers_libraries rl
      ON rl.libraries_id = i.libraries_id
     AND rl.card_number = i.card_number
    WHERE rl.readers_id = r.id
    ORDER BY i.issued_at DESC
    LIMIT 1
) i ON true;
