# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (
                                artist VARCHAR,
                                auth VARCHAR,
                                firstName VARCHAR,
                                gender VARCHAR,
                                itemInSession INTEGER,
                                lastName VARCHAR,
                                length NUMERIC,
                                level VARCHAR,
                                location VARCHAR,
                                method VARCHAR,
                                page VARCHAR,
                                registration VARCHAR,
                                sessionId INTEGER,
                                song VARCHAR,
                                status INTEGER,
                                ts TIMESTAMP,
                                userAgent VARCHAR,
                                userId INTEGER);""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (
                                num_songs INTEGER,
                                artist_id VARCHAR,
                                artist_latitude NUMERIC,
                                artist_longitude NUMERIC,
                                artist_location VARCHAR,
                                artist_name VARCHAR,
                                song_id VARCHAR,
                                title VARCHAR,
                                duration NUMERIC,
                                year INTEGER);""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays ( 
                                    songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY, 
                                    start_time TIMESTAMP REFERENCES time(start_time) SORTKEY, 
                                    user_id VARCHAR NOT NULL REFERENCES users(user_id) DISTKEY, 
                                    level VARCHAR, 
                                    song_id VARCHAR REFERENCES songs(song_id), 
                                    artist_id VARCHAR REFERENCES artists(artist_id), 
                                    session_id VARCHAR, 
                                    location VARCHAR, 
                                    user_agent VARCHAR,
                                    UNIQUE(song_id, artist_id));""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users ( 
                                      user_id VARCHAR DISTKEY PRIMARY KEY, 
                                      first_name VARCHAR, 
                                      last_name VARCHAR, 
                                      gender VARCHAR, 
                                      level VARCHAR);""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs ( 
                            song_id VARCHAR SORTKEY PRIMARY KEY, 
                            title VARCHAR NOT NULL, 
                            artist_id VARCHAR NOT NULL, 
                            year INTEGER, 
                            duration NUMERIC);""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
                            artist_id VARCHAR SORTKEY PRIMARY KEY, 
                            artist_name VARCHAR NOT NULL, 
                            artist_location VARCHAR, 
                            artist_latitude NUMERIC, 
                            artist_longitude NUMERIC); """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                            start_time TIMESTAMP SORTKEY PRIMARY KEY, 
                            hour INTEGER NOT NULL, 
                            day INTEGER NOT NULL, 
                            week INTEGER NOT NULL, 
                            month INTEGER NOT NULL, 
                            year INTEGER NOT NULL, 
                            weekday INTEGER NOT NULL); """)

# QUERY LISTS

create_table_queries_list = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]