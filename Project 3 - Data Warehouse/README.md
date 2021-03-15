# Project: Data Warehouse

## Introduction
Sparkify is a music streaming company and they've been collecting songs and user activities. Analytics team in Sparkify is interested in understanding what songs users are listening to. As their business is growing, they need to move their business to cloud. And their current JSON logs resides on AWS S3.  

## Purpose of the project: 
1. Design the table and select best key(sort key/dist key) for fast data processing
2. Build the ETL process  

## Schema Design

### Staging Tables
**1. staging_events** - serve as the staging table for Sparkify user activity log data

| Column Name   | Type      | Constraint  | Explanation |
| ---           | ---       | ---         | ---         |
| artist        | VARCHAR   | ---         | ---         |
| auth          | VARCHAR   | ---         | ---         |
| firstName     | VARCHAR   | ---         | ---         |
| gender        | VARCHAR   | ---         | ---         |
| itemInSession | INTEGER   | ---         | ---         |
| lastName      | VARCHAR   | ---         | ---         |
| length        | NUMERIC   | ---         | ---         |
| level         | VARCHAR   | ---         | ---         |
| location      | VARCHAR   | ---         | ---         |
| method        | VARCHAR   | ---         | ---         |
| page          | VARCHAR   | ---         | ---         |
| registration  | VARCHAR   | ---         | ---         |
| sessionId     | INTEGER   | ---         | ---         |
| song          | VARCHAR   | ---         | ---         |
| status        | INTEGER   | ---         | ---         |
| ts            | TIMESTAMP | ---         | ---         |
| userAgent     | VARCHAR   | ---         | ---         |
| userId        | INTEGER   | ---         | ---         |

**2. staging_songs** - serve as the staging table for Sparkify songs database 

| Column Name      | Type      | Constraint  | Explanation |
| ---              | ---       | ---         | ---         |
| num_songs        | INTEGER   | ---         | ---         |
| artist_id        | VARCHAR   | ---         | ---         |
| artist_latitude  | NUMERIC   | ---         | ---         |
| artist_longitude | NUMERIC   | ---         | ---         |
| artist_location  | VARCHAR   | ---         | ---         |
| artist_name      | VARCHAR   | ---         | ---         |
| song_id          | VARCHAR   | ---         | ---         |
| title            | VARCHAR   | ---         | ---         |
| duration         | NUMERIC   | ---         | ---         |
| year             | INTEGER   | ---         | ---         |

### Fact Table  

**3. songplays** - records in log data associated with songplays

| Column Name | Type           | Constraint                | Explanation                          |
| ---         | ---            | ---                       | ---                                  |
| songplay_id | IDENTITY(0,1)  | PRIMARY KEY               | PK + Needs auto-increment            |
| start_time  | TIMESTAMP      | REFERENCES time SORTKEY   | Frequent range filtering required    |
| user_id     | VARCHAR        | REFERENCES users DISTKEY  | Often used to join with other tables |
| level       | VARCHAR        |                           |                                      |
| song_id     | VARCHAR        | REFERENCES songs UNIQUE   |                                      |
| artist_id   | VARCHAR        | REFERENCES artists UNIQUE |                                      |
| session_id  | VARCHAR        | NOT NULL                  | Songplay should have a session       |
| location    | VARCHAR        |                           |                                      |
| user_agent  | VARCHAR        |                           |                                      |

### Dimension Tables

**4. users**  - app users
| Column Name | Type    | Constraint          | Explanation                   |
| ---         | ---     | ---                 | ---                           |
| user_id     | VARCHAR | PRIMARY KEY DISTKEY | PK + Frequent JOIN OPERATIONS |
| first_name  | VARCHAR |                     |                               |
| last_name   | VARCHAR |                     |                               |
| gender      | VARCHAR |                     |                               |
| level       | VARCHAR |                     |                               |

**5. songs** - musics in the database
| Column Name | Type    | Constraint          | Explanation                   |
| ---         | ---     | ---                 | ---                           |
| song_id     | VARCHAR | PRIMARY KEY SORTKEY | PK + Frequent range filtering |
| title       | VARCHAR | NOT NULL            | Song should have title        |
| artist_id   | VARCHAR | NOT NULL            | Song should have an artist    |
| year        | INTEGER |                     |                               |
| duration    | NUMERIC |                     | Have decimals                 |

**6. artists** - artists of music in the database
| Column Name     | Type    | Constraint          | Explanation                   |
| ---             | ---     | ---                 | ---                           |
| artist_id       | VARCHAR | PRIMARY KEY SORTKEY | PK + Frequent range filtering |
| artist_name     | VARCHAR | NOT NULL            | Artist should have name       |
| artist_location | VARCHAR |                     |                               |
| artist_location | NUMERIC |                     | Have decimals                 |
| artist_location | NUMERIC |                     | Have decimals                 |

**7. time** - timestamps of records in **songplays** 
| Column Name | Type      | Constraint          | Explanation                   |
| ---         | ---       | ---                 | ---                           |
| start_time  | TIMESTAMP | PRIMARY KEY SORTKEY | PK + Frequent range filtering |
| hour        | INTEGER   | NOT NULL            |                               |
| day         | INTEGER   | NOT NULL            |                               |
| week        | INTEGER   | NOT NULL            |                               |
| month       | INTEGER   | NOT NULL            |                               |
| year        | INTEGER   | NOT NULL            |                               |
| workday     | INTEGER   | NOT NULL            |                               |

## ETL pipeline

1. Data stored in S3 is first loaded into AWS Redshift database for intermediate storage
2. Fact Table is loaded with information by joining staging_events and staging_songs directly instead of multiple joins from Dimension Table
3. Dimension Table is loaded with information in staging_events and staging_songs as well as fact table

## Sample Query

Sample Query is tested in the test.ipynb jupyter notebook

### User with most songplay
SELECT U.first_name, U.last_name, COUNT(1) as songplay_num  
FROM songplays SP JOIN users U ON SP.user_id = U.user_id 
GROUP BY SP.user_id, U.first_name, U.last_name 
ORDER BY songplay_num DESC 
LIMIT 1;

### Location with most artists
SELECT artist_location, COUNT(*) AS artist_num 
FROM artists 
WHERE TRIM(artist_location) IS NOT NULL 
GROUP BY artist_location 
ORDER BY artist_num DESC LIMIT 1; 
