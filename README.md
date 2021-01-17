# Project: Data Modeling with Postgres

## Introduction
Sparkify is a startup company building music streaming app. They have been collecting user activities log and songs. Analytics Team need a database based on postgre to expand their analytical capability. As a startup company, Sparkify will have more songs, users and new songs added to their database. Flexibility is a key in database design.
 
## Purpose of the project: 
The key functionalities required for the database included:
1. Design and implement a star schema to store user streaming logs with flexibility  
   1.1 Create Dimension Tables to store user, songs, artist of songs, and playtime
   1.2 Create Fact Table to record log data with song play data
2. Build ETL pipeline to load streaming log and music data in JSON format into designed database
3. Support analytical applications for Sparkify Analytics Team to understand user behaviors

## Database Schema design:
All SQL query are stored in **sql_queries.py** with following 3 functionalities:
1. DROP table if they exists before updating table
2. CREATE new table
3. INSERT new rows into the table
4. Extract information from **songs** and **artists** for **songplays** table 

### The Star Schema I created consists of following tables:

#### Fact Table  

**1. songplays** - records in log data associated with songplays

| Column Name | Type    | Constraint  | Explanation                 |
| ---         | ---     | ---         | ---                         |
| songplay_id | SERIAL  | PRIMARY KEY | PK + Needs auto-increment   |
| start_time  | BIGINT  | NOT NULL    | echos in millionsecond      |
| user_id     | VARCHAR | NOT NULL    | song must be played by user |
| level       | VARCHAR |             | new type users may added    |
| song_id     | VARCHAR | UNIQUE      | Unique with artist_id       |
| artist_id   | VARCHAR | UNIQUE      | Unique with song_id         |
| session_id  | VARCHAR |             |                             |
| location    | VARCHAR |             |                             |
| user_agent  | VARCHAR |             |                             |

#### Dimension Tables

**2. users**  - app users
| Column Name | Type    | Constraint  | Explanation                               |
| ---         | ---     | ---         | ---                                       |
| user_id     | VARCHAR | PRIMARY KEY | PK                                        |
| first_name  | VARCHAR |             |                                           |
| last_name   | VARCHAR |             |                                           |
| gender      | VARCHAR |             |                                           |
| level       | VARCHAR |             | type may switch and new type may added    |

**3. songs** - musics in the database
| Column Name | Type    | Constraint  | Explanation                 |
| ---         | ---     | ---         | ---                         |
| song_id     | VARCHAR | PRIMARY KEY | PK                          |
| title       | VARCHAR |             |                             |
| artist_id   | VARCHAR |             |                             |
| year        | INT     |             |                             |
| duration    | NUMERIC |             | Have decimals               |

**4. artists** - artists of music in the database
| Column Name     | Type    | Constraint  | Explanation                 |
| ---             | ---     | ---         | ---                         |
| artist_id       | VARCHAR | PRIMARY KEY | PK                          |
| artist_name     | VARCHAR |             |                             |
| artist_location | VARCHAR |             |                             |
| artist_location | NUMERIC |             | Have decimals               |
| artist_location | NUMERIC |             | Have decimals               |

**5. time** - timestamps of records in **songplays** 
| Column Name | Type      | Constraint  | Explanation                 |
| ---         | ---       | ---         | ---                         |
| start_time  | TIMESTAMP | PRIMARY KEY | PK                          |
| hour        | INT       |             |                             |
| day         | INT       |             |                             |
| week        | INT       |             |                             |
| month       | INT       |             |                             |
| year        | INT       |             |                             |
| workday     | INT       |             |                             |

## ETL pipeline design:
### create_table.py
It execute SQL queries in sql_queries.py to create table.

### etl.ipynb
This is an exploratory ipython notebook to construct pipeline for loading data from single JSON file(song_data and log_data seperately):
1. Connect to database created with **create_table.py**
2. Process song_data
    2.1 Select and flatten required information for songs and insert into database
    2.2 Select and flatten required information for artists and insert into database
3. Process log_data
    3.1 Process time table
        3.1.1 Select only Songplay data by filtering with **page == 'NextSong'**
        3.1.2 Convert column 'ts' to datetime
        3.1.3 Extract hour, day, week, month, year, and weekday from 'ts'
        3.1.4 Insert them into the database
    3.2 Process users table
        3.2.1 Select required information from log_data 
        3.2.2 Insert into database
    3.3 Process songplays table
        3.3.1 Extract information from the songs and artists table
        3.3.2 Combine with song_id and artist_id from logfile
        3.3.3 Insert into the database
    

### test.ipynb
This is to test whether the data has been inserted into the table. 

### etl.py
It add functionalities of reading all files under a file name in addition to **etl.ipynb** to load all data into the database

## Sample Query

### User with most songplay
'SELECT U.first_name, U.last_name, COUNT(1) as songplay_num  
 FROM songplays SP JOIN users U ON SP.user_id = U.user_id 
 GROUP BY SP.user_id, U.first_name, U.last_name 
 ORDER BY songplay_num DESC 
 LIMIT 1;'

### Location with most artists
'SELECT artist_location, COUNT(*) AS artist_num 
 FROM artists 
 WHERE TRIM(artist_location) IS NOT NULL 
 GROUP BY artist_location 
 HAVING COUNT(*) <> 27 
 ORDER BY artist_num DESC LIMIT 1; '
 
Note: Theoretically, we don't need HAVING clause. This having clause is need to remove the white-space like artist_location which is not removable by "IS NOT NULL" or TRIM().