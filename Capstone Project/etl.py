import configparser
import psycopg2
import pandas as pd
from sql_queries import index_list_insert, index_value_insert, eco_list_insert, eco_value_insert, insert_dimension_table_queries, insert_fact_table_queries
    
def data_transform_index_list():
    """
    Transform index list data (reorder the column)
    
    """
    index_list = pd.read_csv('output/index_list_updated.csv')
    index_list = index_list.rename(columns = {'SYMBOL':'symbol', '#NAME':'index_name', 'OLD SYMBOL':'old_symbol'})
    index_list = index_list[['symbol','index_name','old_symbol']]
    
    return index_list

def data_transform_index_value():
    """
    Transform index value data (rename the column)
    
    """
    index_value = pd.read_csv('output/index_value_updated.csv')
    index_value = index_value.rename(columns = {'Date':'date', 'DATABASE_CODE':'database_code', 'DATASET_CODE':'dataset_code', 'Index Value': 'index_value', 'Total Market Value': 'total_market_value', 'Dividend Market Value': 'dividend_market_value'})
    index_value = index_value[['date','database_code','dataset_code','index_value','total_market_value','dividend_market_value']]
    
    return index_value

def data_transform_eco_list():
    """
    Transform economic indicator list data (rename the column)
    
    """
    eco_list = pd.read_csv('output/eco_indicator_mapping.csv')
    eco_list = eco_list.rename(columns = {'CODE':'code', 'INDICATOR':'indicator_name', 'TYPE':'type'})
    
    return eco_list    

def data_transform_eco_value():
    """
    Transform economic indicator list data (rename the column)
    
    """
    eco_value = pd.read_csv('output/eco_indicator_value.csv')
    eco_value = eco_value.rename(columns = {'Date':'date', 'DATABASE_CODE':'database_code', 'DATASET_CODE':'dataset_code', 'Value': 'indicator_value'})
    eco_value = eco_value[['date','database_code','dataset_code','indicator_value']]
    
    return eco_value   

def load_dimension_tables(cur, conn, insert_query, df_to_insert, schema_name):
    """
    Load data into dimension table
    
    Parameters:
    cur: cursor of the connection to the database
    conn: connection obejct to the database
    df_to_insert: the DataFrame that contains data to insert into destination table
    insert_query: INSERT statement for specific table
    schema_name: Name of schema for displaying progress
    """
    # Insert into tables
    print("Started loading {}".format(schema_name))
    count = 0 
    total_rows = len(df_to_insert)
    for row in df_to_insert.itertuples(index = False):
        cur.execute(insert_query, row)
        count += 1
        if count % 50 == 0:
            print('{current} out of {total} are loaded'.format(current = str(count), total = str(total_rows))) 
        
        # Limit rows to insert to 1000 for testing purpose
        #if count == 1000:
        #    break
        
    conn.commit()  

def load_fact_tables(cur, conn):
    """
    Insert data from dimension tables
    
    Parameters:
    cur: cursor of the connection to the database
    conn: connection obejct to the database
    """
    for query in insert_fact_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Complete etl process
    
    Load database configuration and connect to database. Then load staging table and insert data.
    
    """
    config = configparser.ConfigParser()
    config.read('credential.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    print('Connected to database')
    
    # Transform Raw Data
    index_list = data_transform_index_list()
    index_value = data_transform_index_value()
    eco_list = data_transform_eco_list()
    eco_value = data_transform_eco_value()
    
    # Load Staging tables
    load_dimension_tables(cur, conn, index_list_insert, index_list, 'Index List')
    load_dimension_tables(cur, conn, index_value_insert, index_value, 'Index Value')
    load_dimension_tables(cur, conn, eco_list_insert, eco_list, 'Economic Indicator List')
    load_dimension_tables(cur, conn, eco_value_insert, eco_value, 'Economic Indicator  Value')
    print('Loaded Dimension Tables')

    load_fact_tables(cur, conn)
    print('Inserted fact tables')
    conn.close()

if __name__ == "__main__":
    main()