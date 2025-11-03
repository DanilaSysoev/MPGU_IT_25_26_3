UPDATE humans SET city_id = 1
WHERE city_id IS NULL;

DELETE FROM humans
WHERE id = 1;