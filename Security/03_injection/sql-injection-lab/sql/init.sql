DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS goods CASCADE;
DROP TABLE IF EXISTS tokens CASCADE;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  password_hash TEXT NOT NULL
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE goods (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  order_id INTEGER NOT NULL REFERENCES orders(id),
  count INTEGER NOT NULL,
  price NUMERIC NOT NULL
);

CREATE TABLE tokens (
  id SERIAL PRIMARY KEY,
  value TEXT NOT NULL,
  user_id INTEGER NOT NULL REFERENCES users(id),
  is_valid BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO users (id, name, password_hash) VALUES
  (1, 'alice', 'e6d21a69daa4a8ebca755c1d5808b85b'),
  (2, 'bob', '530c81a25a362791fff683c511c2edd8'),
  (3, 'eva', 'f8c87688d560489d977c7414ca146d37');

INSERT INTO orders (id, user_id) VALUES (1, 1);
INSERT INTO orders (id, user_id) VALUES (2, 2);
INSERT INTO orders (id, user_id) VALUES (3, 3);
INSERT INTO orders (id, user_id) VALUES (4, 1);

INSERT INTO goods (id, name, order_id, count, price) VALUES (1, 'widget', 1, 3, 9.99);
INSERT INTO goods (id, name, order_id, count, price) VALUES (2, 'widget', 1, 4, 10.99);
INSERT INTO goods (id, name, order_id, count, price) VALUES (3, 'widget', 2, 5, 1.99);
INSERT INTO goods (id, name, order_id, count, price) VALUES (4, 'widget', 2, 6, 2.99);
INSERT INTO goods (id, name, order_id, count, price) VALUES (5, 'widget', 3, 1, 3.99);
INSERT INTO goods (id, name, order_id, count, price) VALUES (6, 'widget', 3, 2, 4.99);
INSERT INTO goods (id, name, order_id, count, price) VALUES (7, 'widget', 4, 3, 5.99);
INSERT INTO goods (id, name, order_id, count, price) VALUES (8, 'widget', 4, 4, 6.99);

INSERT INTO tokens (value, user_id, is_valid) VALUES ('secrettokenAlice', 1, true);
INSERT INTO tokens (value, user_id, is_valid) VALUES ('secrettokenBob', 2, true);
INSERT INTO tokens (value, user_id, is_valid) VALUES ('secrettokenEva', 3, true);
