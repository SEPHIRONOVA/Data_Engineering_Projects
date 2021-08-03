import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('credential.cfg')

# CREATE TABLES

# Dimension Tables

index_list_table_create = ("""CREATE TABLE IF NOT EXISTS index_list (
                            symbol VARCHAR PRIMARY KEY,
                            index_name VARCHAR,
                            old_symbol VARCHAR);""")

index_value_table_create = ("""CREATE TABLE IF NOT EXISTS index_value (
                            date DISTKEY DATE,
                            database_code VARCHAR,
                            dataset_code VARCHAR REFERENCES index_list(symbol), 
                            index_value NUMERIC,
                            total_market_value NUMERIC,
                            dividend_market_value NUMERIC,
                            PRIMARY KEY(date, dataset_code));""")

eco_list_table_create = ("""CREATE TABLE IF NOT EXISTS eco_list (
                            code VARCHAR PRIMARY KEY,
                            indicator_name VARCHAR,
                            type VARCHAR);""")

eco_value_table_create = ("""CREATE TABLE IF NOT EXISTS eco_value (
                            date DATE DISTKEY PRIMARY KEY ,
                            database_code VARCHAR,
                            dataset_code VARCHAR REFERENCES eco_list(code) SORTKEY, 
                            indicator_value NUMERIC);""")

# Fact Tables

index_fact_table_create = ("""CREATE TABLE IF NOT EXISTS index_fact (
                            index_name VARCHAR,
                            date DATE DISTKEY,
                            dataset_code VARCHAR SORTKEY,
                            index_value NUMERIC,
                            total_market_value NUMERIC,
                            dividend_market_value NUMERIC,
                            PRIMARY KEY(date, dataset_code));""")

eco_fact_table_create = ("""CREATE TABLE IF NOT EXISTS eco_fact (
                            indicator_name VARCHAR SORTKEY,
                            date DATE DISTKEY,
                            code VARCHAR,
                            indicator_value NUMERIC,
                            type VARCHAR,
                            PRIMARY KEY(date, code));""")

# DROP TABLES

index_value_table_drop = "DROP TABLE IF EXISTS index_value CASCADE"

index_list_table_drop = "DROP TABLE IF EXISTS index_list CASCADE"

eco_value_table_drop = "DROP TABLE IF EXISTS eco_value CASCADE"

eco_list_table_drop = "DROP TABLE IF EXISTS eco_list CASCADE"

index_fact_table_drop = "DROP TABLE IF EXISTS index_fact CASCADE"

eco_fact_table_drop = "DROP TABLE IF EXISTS eco_fact CASCADE"

# INSERT TABLES
index_list_insert = """INSERT INTO index_list (symbol, index_name, old_symbol) 
                       VALUES (%s, %s, %s);"""

index_value_insert = """INSERT INTO index_value (date, database_code, dataset_code, index_value, total_market_value, dividend_market_value)
                         VALUES (%s, %s, %s, %s, %s, %s);"""

eco_list_insert = """INSERT INTO eco_list (code, indicator_name, type)
                      VALUES (%s, %s, %s);"""

eco_value_insert = """INSERT INTO eco_value (date, database_code, dataset_code,  indicator_value)
                       VALUES (%s, %s, %s, %s);"""

index_fact_insert = """INSERT INTO index_fact (index_name, date, dataset_code, index_value, total_market_value, dividend_market_value)
                            SELECT il.index_name, iv.date, iv.dataset_code, iv.index_value, iv.total_market_value, iv.dividend_market_value
                            FROM index_list il JOIN index_value iv ON il.symbol = iv.dataset_code;"""

eco_fact_insert = """INSERT INTO eco_fact (indicator_name, date, code, indicator_value, type)
                            SELECT el.indicator_name, ev.date, el.code, ev.indicator_value, el.type
                            FROM eco_list el JOIN eco_value ev ON el.code = ev.dataset_code;"""

# UPDATE TABLES 
index_list_update = ("""""")

index_value_update = ("""""")

eco_list_update = ("""""")

eco_value_update = ("""""")

index_fact_update = ("""""")

eco_fact_update = ("""""")

# QUERY LISTS
create_table_queries = [index_list_table_create, index_value_table_create, eco_list_table_create, eco_value_table_create, index_fact_table_create, eco_fact_table_create]
drop_table_queries = [index_value_table_drop, index_list_table_drop, eco_value_table_drop, eco_list_table_drop, index_fact_table_drop, eco_fact_table_drop]
insert_dimension_table_queries = [index_list_table_create, index_value_table_create, eco_list_table_create, eco_value_table_create]
insert_fact_table_queries = [index_fact_insert, eco_fact_insert]
update_table_queries = [index_list_update, index_value_update, eco_list_update, eco_value_update, index_fact_update, eco_fact_update]