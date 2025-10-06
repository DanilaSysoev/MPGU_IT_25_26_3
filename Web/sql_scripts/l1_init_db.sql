CREATE SCHEMA IF NOT EXISTS demo_1;

CREATE TABLE IF NOT EXISTS demo_1.fruits (
    id serial PRIMARY KEY,
    name text NOT NULL,
    price integer NOT NULL
);

/*
Целочисленные типы данных:
------------------------------------------------------------------------------
integer (int) - 4 bytes, signed                | 123, -5
biginteger (bigint) - 8 bytes, signed          | 123, -5
serial - 4 bytes, unsigned, autoincrement      | -
bigserial - 8 bytes, unsigned, autoincrement   | -
smallint - 2 bytes, signed                     | 123, -5
smallserial - 2 bytes, unsigned, autoincrement | 123, -5

numeric (decimal) - accurate floating point    | 2.5, -0.89
real - 4 bytes floating point                  | 2.5, -0.89
double precision - 8 bytes floating point      | 2.5, -0.89

Текстовые типы данных:
------------------------------------------------------------------------------
text - variable-length string                              | 'Hello, world!' 
varchar(n) - fixed-length string of n characters           | 'Hello, world!' 
char(n) - fixed-length string of n characters (add spaces) | 'Hello, world!' 

Типы для дат и времени:
------------------------------------------------------------------------------
date - date                                 | '2025-10-06' '20251006'
timestamp - date and time                   | '2025-10-06 12:00:00'
interval - time span                        | '1 day 2 hours' '30 minutes'
timestamptz - date and time with time zone  | '2025-10-06 12:00:00+03'

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