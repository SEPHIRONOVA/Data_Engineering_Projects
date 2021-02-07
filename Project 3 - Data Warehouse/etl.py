import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Load data stored in AWS S3 into AWS redshift
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
        

def insert_tables(cur, conn):
    """
    Insert data from AWS redshift into postgre SQL database
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    ETL process for Sparkify Music Streaming Database
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    print('Connected to the server')
    
    load_staging_tables(cur, conn)
    print('Finished Loading Staging Tables.')
    
    insert_tables(cur, conn)
    print('Finished Inserting data into tables.')

    conn.close()


if __name__ == "__main__":
    main()