import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Load data into staging table
    
    Parameters:
    cur: cursor of the connection to the database
    conn: connection obejct to the database
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Insert data from staging tables
    
    Parameters:
    cur: cursor of the connection to the database
    conn: connection obejct to the database
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Complete etl process
    
    Load database configuration and connect to database. Then load staging table and insert data.
    
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    print('Connected to database')

    load_staging_tables(cur, conn)
    print('Loaded Staging Tables')

    insert_tables(cur, conn)
    print('Inserted data from staging tables')
    conn.close()

if __name__ == "__main__":
    main()