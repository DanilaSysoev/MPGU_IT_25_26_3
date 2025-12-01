import psycopg
import random
from time import time

CONN_STRING = "postgresql://danila:super_secret@localhost:5430/lesson_9"


def create_database():
    conn = psycopg.connect(
        CONN_STRING
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS index_demos (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            int_value INT NOT NULL
        );
    """)
    conn.commit()
    
    cursor.close()
    conn.close()


def add_rows(cnt):
    conn = psycopg.connect(
        CONN_STRING
    )
    cursor = conn.cursor()
    
    for _ in range(cnt):
        value = random.randint(0, 1_000_000_000)
        cursor.execute(
            "INSERT INTO index_demos (name, int_value) VALUES (%s, %s)",
            (f"Row {value}", value)
        )
    
    conn.commit()
    
    cursor.close()
    conn.close()


def select():
    conn = psycopg.connect(
        CONN_STRING
    )
    cursor = conn.cursor()
    start = time()
    ssum = 0
    for _ in range(1000):
        treschold = random.randint(0, 1_000_000_000)
        cursor.execute(
            "SELECT MIN(int_value) FROM index_demos WHERE int_value > %s",
            (treschold,)
        )
        ssum += cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()
    print(f"Total selected: {ssum}, time: {time() - start:.2f} s")


def main():
    create_database()
    # add_rows(1000000)
    select()
    

if __name__ == "__main__":
    main()
