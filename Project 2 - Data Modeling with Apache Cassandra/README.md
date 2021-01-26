# Project: Data Modeling with Apache Cassandra

## Introduction
Sparkify is a music streaming company and they've been collecting songs and user activities. Analytics team in Sparkify is interested in understanding what songs users are listening to. They need a data pipeline to load data for user behavior and songs analysis. 

## Purpose of the project: 
Modeling data table to satisfy the specific needs from analytics team with high frequency and fast read.

## Database Table design:

### Query 1:
**Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4**

This type of query is to answer analysts' interest in particular session and particular song.

| Column Name   | Type    | Constraint        | Explanation                   |
| ---           | ---     | ---               | ---                           |
| sessionID     | INT     | PARTITION KEY     | search based on session       |
| itemInSession | INT     | PARTITION KEY     | search also need item info    |
| artist        | TEXT    | ---               | artist name is required info  |
| song          | TEXT    | ---               | song name is required info    |
| length        | DECIMAL | ---               | length of song is required    |

### Query 2:
**Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182**

This type of query is to get information on particular user's one completed session ordered by 'itemInSession'

| Column Name   | Type    | Constraint        | Explanation                    |
| ---           | ---     | ---               | ---                            |
| userID        | INT     | PARTITION KEY     | search based on user           |
| sessionID     | INT     | PARTITION KEY     | search based on session        |
| itemInSession | INT     | CLUSTERING COLUMN | determine order of output      |
| artist        | TEXT    | ---               | artist name is required info   |
| song          | TEXT    | ---               | song name is required info     |
| user          | TEXT    | ---               | fisrt and last name combined   |

### Query 3:
**Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'**

This type of query is to get information on particular song, and help analyze user protrait for people who listen to this type of songs

| Column Name   | Type    | Constraint        | Explanation                            |
| ---           | ---     | ---               | ---                                    |
| song          | TEXT    | PARTITION KEY     | song name is required info             |
| userID        | INT     | CLUSTERING COLUMN | more info is required for PRIMARY KEY  |
| user          | TEXT    | ---               | fisrt and last name combined           |