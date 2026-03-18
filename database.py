import os
import psycopg2
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
import time

class VendingDatabase:
    def __init__(self):
        self.config = {
            "dbname": os.getenv("DATABASE_NAME"),
            "user": os.getenv("DATABASE_USER"),
            "password": os.getenv("DATABASE_PASSWORD"),
            "host": os.getenv("DATABASE_HOST"),
            "port": os.getenv("DATABASE_PORT")
        }

    def get_connection(self):
        retries = 5
        while retries > 0:
            try:
                return psycopg2.connect(**self.config)
            except psycopg2.OperationalError as e:
                print(f"Database connection failed: {e}. Retrying in 5 seconds...")
                retries -= 1
                time.sleep(5)
        raise Exception("Could not connect to the database after multiple attempts.")

    def create_tables(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                price INTEGER NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

    def get_all_products(self):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM products")
                return cur.fetchall()
            
    def add_item(self, name, price):
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
                    conn.commit()
        except errors.UniqueViolation:
            raise Exception(f"Product with name '{name}' already exists.")

    def delete_item(self, name):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM products WHERE name = %s", (name,))
                conn.commit()

    def update_item_price(self, name, new_price):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE products SET price = %s WHERE name = %s", (new_price, name))
                conn.commit()
