import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Create the spark session
    :return: a Spark Session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    This function read the song data from S3 and extract required column for songs and artists table and load back to S3
    
    :param spark: the spark session to read data
    :param input_data: input file path
    :param output_data: output file path
    """
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data).drop_duplicates()

    # extract columns to create songs table
    songs_table = df.select(['song_id', 'title', 'artist_id', 'year', 'duration'])
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id").parquet(output_data + 'songs/', mode = 'overwrite')

    # extract columns to create artists table
    artists_table = df.select("artist_id","artist_name","artist_location","artist_latitude","artist_longitude").drop_duplicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + 'artists/', mode = 'overwrite')


def process_log_data(spark, input_data, output_data):
    """
    This function read the log data from S3 and extract required information for song_play, users and time table and load them back to S3 
    
    :param spark: the spark session to read data
    :param input_data: input file path
    :param output_data: output file path
    """
    # get filepath to log data file
    log_data = input_data + 'log_data/*.json'

    # read log data file
    df = spark.read.json(log_data).drop_duplicates()
    
    # filter by actions for song plays
    df = df.where(df.page == 'NextSong')
    
    # Reanme column name to match required time
    df = df.withColumnRenamed('userID','user_id') \
            .withColumnRenamed('firstName','first_name') \
            .withColumnRenamed('lastName','last_name') \
            .withColumnRenamed('sessionId', 'session_id') \
            .withColumnRenamed('userAgent', 'user_agent') \
            .drop_duplicates() 
    
    # extract columns for users table    
    user_table = df.select(['user_id','first_name','last_name','gender','level']).drop_duplicates()

    # write users table to parquet files
    user_table.write.parquet(output_data + 'users/', mode = 'overwrite')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: datetime.fromtimestamp(int(x)/1000), TimestampType())
    df = df.withColumn('start_time', get_timestamp('ts'))
    
    # extract columns to create time table
    time_table = df.withColumn('hour', hour(col('start_time'))).withColumn('day', dayofmonth(col('start_time'))) \
                    .withColumn('week', weekofyear(col('start_time'))).withColumn('month', month(col('start_time'))) \
                    .withColumn('year', year(col("start_time"))).withColumn("weekday", date_format(col("start_time"), 'E')) \
                    .select('ts','start_time','hour','day','week','month','year','weekday') \
                    .dropDuplicates() 
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet(output_data + 'timetable/', mode = 'overwrite')

    # read in artist data to use for songplays table
    artist_df = spark.read.parquet(output_data + 'artists/*')
    
    songplays_table = df.join(artist_df, (df.artist == artist_df.artist_name), 'left').drop_duplicates()
    
    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data + "songs/*/*/*")
    
    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = songplays_table.join(song_df, (songplays_table.song == song_df.title), 'inner') \
                        .withColumn("songplay_id", monotonically_increasing_id()) \
                        .select('songplay_id', 'start_time', 'user_id', 'level', 'song_id', 'artist_id', 'session_id', 'location','user_agent') \
                        .drop_duplicates()
    
    # need to join time_table to get year and month
    songplays_table = songplays_table.join(time_table, songplays_table.start_time == time_table.start_time) \
                        .drop_duplicates() \
                        .select('songplay_id', songplays_table.start_time, 'user_id','level','song_id','artist_id','session_id','location','user_agent', 'year', 'month') 
                                                               
    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet(output_data + 'songplays/', mode = 'overwrite')


def main():
    """
    The main function to execute all the ETL processes
    """
    spark = create_spark_session()
    input_data = "data/"
    output_data = "output/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
