CREATE SCHEMA IF NOT EXISTS demo_1;

CREATE TABLE IF NOT EXISTS demo_1.fruits (
    id serial PRIMARY KEY,
    name text NOT NULL,
    price integer NOT NULL
);

/*
Целочисленные типы данных:
------------------------------------------------------------------------------
integer (int) - 4 bytes, signed
biginteger (bigint) - 8 bytes, signed
serial - 4 bytes, unsigned, autoincrement
bigserial - 8 bytes, unsigned, autoincrement
smallint - 2 bytes, signed
smallserial - 2 bytes, unsigned, autoincrement

numeric (decimal) - accurate floating point
real - 4 bytes floating point
double precision - 8 bytes floating point

Текстовые типы данных:
------------------------------------------------------------------------------
text - variable-length string
varchar(n) - fixed-length string of n characters
char(n) - fixed-length string of n characters (add spaces)

Типы для дат и времени:
------------------------------------------------------------------------------
date - date
timestamp - date and time
interval - time span
timestamptz - date and time with time zone

Дополнтельные типы данных:
------------------------------------------------------------------------------
boolean - true/false
json - JSON data
jsonb - JSON data with binary support
*/

/*
Constraints:
------------------------------------------------------------------------------
NOT NULL - column cannot be null
UNIQUE - column must be unique
PRIMARY KEY - column acts as primary key
DEFAULT - default value
*/