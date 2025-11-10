SELECT economy, COUNT(*) AS count FROM settlements
GROUP BY economy;

SELECT economy, category, COUNT(*) AS count FROM settlements
GROUP BY economy, category
ORDER BY count DESC;

SELECT category, SUM(population) AS total_population FROM settlements
GROUP BY category
ORDER BY total_population DESC;

SELECT
    category,
    SUM(population) AS total_population,
    COUNT(economy) FILTER (WHERE economy = 'сельское хозяйство') AS count_farmers
FROM settlements
GROUP BY category
ORDER BY total_population DESC;

SELECT
    category,
    SUM(population) AS total_population
FROM settlements
GROUP BY category
HAVING SUM(population) > 10000
ORDER BY total_population DESC;
