CREATE TABLE IF NOT EXISTS temperatures (
    id serial PRIMARY KEY,
    date date NOT NULL DEFAULT current_date,
    temperature real NOT NULL
);

INSERT INTO temperatures
    (date, temperature)
VALUES
    ('2025-11-01', 4.0),
    ('2025-11-02', 2.3),
    ('2025-11-03', 8.1),
    ('2025-11-04', 0.0),
    ('2025-11-05', -1.2),
    ('2025-11-06', -3.7),
    ('2025-11-07', 1.4);