# Project: Data Warehouse

## Introduction
Sparkify is a music streaming company and they've been collecting songs and user activities. Analytics team in Sparkify is interested in understanding what songs users are listening to. As their business is growing, they need to move their business to cloud. And their current JSON logs resides on AWS S3. They need to process them in Spark and load back to AWS S3.

## Purpose of the project: 
1. Design the table for fast data processing
2. Build the ETL process on cloud with Spark and load back to AWS S3

## Schema Design

### Fact Table  

**1. songplays** - records in log data associated with songplays

| Column Name | Type                           | Explanation                          |
| ---         | ---                            | ---                                  |
| songplay_id | monotonically_increasing_id()  | Need auto-increment                  |
| start_time  | TIMESTAMP                      |                                      |
| user_id     | INT                            |                                      |
| level       | TEXT                           |                                      |
| song_id     | TEXT                           |                                      |
| artist_id   | TEXT                           |                                      |
| session_id  | INT                            |                                      |
| location    | TEXT                           |                                      |
| user_agent  | TEXT                           |                                      |
| month       | TEXT                           | Partition key                        |
| year        | TEXT                           | Partition key                        |


### Dimension Tables

**2. users**  - app users
| Column Name | Type    | Explanation                   |
| ---         | ---     | ---                           |
| user_id     | INT     |                               |
| first_name  | TEXT    |                               |
| last_name   | TEXT    |                               |
| gender      | TEXT    |                               |
| level       | TEXT    |                               |

**3. songs** - musics in the database
| Column Name | Type    | Explanation                   |
| ---         | ---     | ---                           |
| song_id     | TEXT    |                               |
| title       | TEXT    |                               |
| artist_id   | TEXT    |                               |
| year        | TEXT    |                               |
| duration    | NUMERIC | Have decimals                 |

**4. artists** - artists of music in the database
| Column Name        | Type    | Explanation                   |
| ---                | ---     | ---                           |
| artist_id          | TEXT    |                               |
| artist_name        | TEXT    |                               |
| artist_location    | TEXT    |                               |
| artist_lattitude   | NUMERIC | Have decimals                 |
| artist_longitude   | NUMERIC | Have decimals                 |

**5. time** - timestamps of records in **songplays** 
| Column Name | Type      | Explanation                   |
| ---         | ---       | ---                           |
| start_time  | DATE      |                               |
| hour        | INT       |                               |
| day         | INT       |                               |
| week        | INT       |                               |
| month       | INT       | Partition key                 |
| year        | INT       | Partition key                 |
| workday     | TEXT      |                               |

## ETL pipeline

1. Raw Data in json format is loaded from AWS S3
2. Data loaded is processed and transformed with Spark into Fact table and Dimension table
3. Processed data is loaded back to AWS S3 with partition in parquet format
