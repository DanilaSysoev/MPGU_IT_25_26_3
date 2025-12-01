-- CREATE DATABASE lesson_9;
-- SELECT COUNT(*) FROM index_demos;

-- CREATE INDEX IF NOT EXISTS int_value_idx ON index_demos(int_value);
-- DROP INDEX IF EXISTS int_value_idx;

EXPLAIN SELECT MIN(int_value) FROM index_demos WHERE int_value > 500000000;