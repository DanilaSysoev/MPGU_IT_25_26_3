SELECT * FROM temperatures;

SELECT
    date,
    CASE
        WHEN temperature < 0 THEN 'Negative'
        ELSE 'Positive or zero'
    END AS temperature_class,
    temperature
FROM temperatures
ORDER BY date;

SELECT
    date,
    CASE
        WHEN temperature < 0 THEN 'Negative'
        WHEN temperature > 0 THEN 'Positive'
        ELSE 'Zero'
    END AS temperature_class,
    temperature
FROM temperatures
ORDER BY date;

SELECT
    date,
    temperature
FROM temperatures
WHERE
    CASE
        WHEN temperature > 4 THEN 'Too High'
        ELSE 'Normal'
    END = 'Normal'
ORDER BY date;
