import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop tables if any table exists
    
    Parameters:
    cur: cursor of the connection to the database
    conn: connection obejct to the database
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create tables for the database 
    
    Parameters:
    cur: cursor of the connection to the database
    conn: connection obejct to the database
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Complete table creation process
    
    Load database configuration and connect to database. Then drop existing table and create new tables.
    
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()