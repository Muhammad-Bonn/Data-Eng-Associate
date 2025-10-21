# create_tables.py
import psycopg2
from psycopg2 import OperationalError
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    Creates (or recreates) the sparkifydb database and returns a cursor and connection.
    Automatically terminates existing connections if any are open.
    """
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="1234"
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        # Terminate any connections to sparkifydb before dropping
        cur.execute("""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = 'sparkifydb';
        """)

        # Drop and recreate the database
        cur.execute("DROP DATABASE IF EXISTS sparkifydb;")
        cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0;")

        # Close initial connection
        cur.close()
        conn.close()

        # Connect to the new sparkifydb
        conn = psycopg2.connect(
            host="localhost",
            dbname="sparkifydb",
            user="postgres",
            password="1234"
        )
        cur = conn.cursor()

        print("Database 'sparkifydb' created successfully.")
        return cur, conn

    except OperationalError as e:
        print(f"Database creation failed: {e}")
        raise


def drop_tables(cur, conn):
    """Drops all existing tables."""
    print("Dropping existing tables...")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    print("All tables dropped successfully.")


def create_tables(cur, conn):
    """Creates all tables from sql_queries.py."""
    print("Creating tables...")
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
    print("All tables created successfully.")


def main():
    """Main workflow for setting up Sparkify database."""
    cur, conn = None, None
    try:
        cur, conn = create_database()
        drop_tables(cur, conn)
        create_tables(cur, conn)
    except Exception as e:
        print(f"Error during setup: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
