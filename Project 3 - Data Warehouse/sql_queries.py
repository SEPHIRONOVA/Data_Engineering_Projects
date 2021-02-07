import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get('S3','LOG_DATA')
LOG_JSON_DATA = config.get('S3','LOG_JSONPATH')
SONG_DATA = config.get('S3','SONG_DATA')
ARN = config.get('IAM_ROLE','ARN')
REGION = config.get('GEOGRAPHIC','REGION')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS events CASCADE;"
staging_songs_table_drop = "DROP TABLE IF EXISTS songs CASCADE;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay CASCADE;"
user_table_drop = "DROP TABLE IF EXISTS users CASCADE;"
song_table_drop = "DROP TABLE IF EXISTS songs CASCADE;"
artist_table_drop = "DROP TABLE IF EXISTS artists CASCADE;"
time_table_drop = "DROP TABLE IF EXISTS time CASCADE;"

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
                            title VARCHAR, 
                            artist_id VARCHAR, 
                            year INTEGER, 
                            duration NUMERIC);""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
                            artist_id VARCHAR SORTKEY PRIMARY KEY, 
                            artist_name VARCHAR, 
                            artist_location VARCHAR, 
                            artist_latitude NUMERIC, 
                            artist_longitude NUMERIC); """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                            start_time TIMESTAMP SORTKEY PRIMARY KEY, 
                            hour INT, 
                            day INT, 
                            week INT, 
                            month INT, 
                            year INT, 
                            workday INT); """)

# STAGING TABLES

staging_events_copy = ("""
copy staging_events 
    FROM {}
    iam_role {}
    region {}
    FORMAT AS json {}
    TIMEFORMAT 'epochmillisecs'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;""").format(LOG_DATA, ARN, REGION, LOG_JSON_DATA) # Need to format the timestamp as millisecs and format json with json log file

staging_songs_copy = ("""
copy staging_songs 
    FROM {}
    iam_role {}
    region {}
    FORMAT AS json 'auto'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;""").format(SONG_DATA, ARN, REGION) # Need to format JSON file

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
                                   SELECT se.ts, se.userId, se.level, se.location, ss.song_id, ss.artist_id, se.sessionId, se.userAgent
                                   FROM staging_events se JOIN staging_songs ss ON se.song = ss.title AND se.artist = ss.artist_name
                                   WHERE se.page = 'NextSong'
                                ON CONFLICT (song_id, artist_id)
                                   DO NOTHING;
                           """)

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) 
                              SELECT se.userId, se.firstName, se.lastName, se.gender, se.level
                              FROM staging_events se
                              WHERE se.page = 'NextSong'
                            ON CONFLICT (user_id) 
                                DO UPDATE SET level = EXCLUDED.level; """)

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) 
                            SELECT DISTINCT(ss.song_id), ss.title, ss.artist_id, ss.year, ss.duration
                            FROM staging_songs ss
                      ON CONFLICT (song_id)  
                          DO NOTHING""")

artist_table_insert = ("""INSERT INTO artists (artist_id, artist_name, artist_location, artist_latitude, artist_longitude) 
                              SELECT DISTINCT(ss.artist_id), ss.artist_name, ss.artist_location, ss.artist_latitude, ss.artist_longitude
                              FROM staging_songs ss 
                          ON CONFLICT(artist_id) 
                              DO NOTHING;""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, workday) 
                              SELECT DISTINCT(se.ts), EXTRACT(HOUR FROM se.ts), EXTRACT(DAY FROM se.ts), EXTRACT(WEEK FROM se.ts), EXTRACT(MONTH FROM se.ts), EXTRACT(YEAR FROM se.ts), EXTRACT(WORKDAY FROM se.ts)
                              FROM staging_events se
                              WHERE se.page = 'NextSong'
                         ON CONFLICT (start_time) 
                            DO NOTHING;""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
