-- UPDATE goods SET
--     count = count + 100;

-- UPDATE goods SET
--     price = (price * 1.1)
-- WHERE
--     supplier ILIKE '%ферма%';

UPDATE goods SET
    count = 0,
    price = 0
WHERE supplier = 'Рога и копыта';
