from data_extraction import *
from database_connection import *

def data_processing(path, output_path):
    """
    This function process all event_data and saved into a new csv file
    """
    file_path_list = get_path_lists(path)
    process_raw_data(file_path_list, output_path) 
    check_output(output_path)

def main():
    """
    It create an etl process to process event_data and load them into the sparkify database and test database with 3 query
    """
    path = os.getcwd() + '/event_data'
    output_path = os.getcwd() + '/event_datafile_new.csv'
    
    data_processing(path, output_path)
    
    ip = ['127.0.0.1']
    replication_class = 'SimpleStrategy'
    replication_factor = 1
    key_space = 'sparkify'
    
    #Create Database
    sparkify_db = CassandraDatabase(ip, replication_class, replication_factor, key_space)

    session = sparkify_db.connect()
    
    # Testing Query 1: Give me the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession  = 4
    table1 = 'song_info_session_item'
    columns1_type = ['sessionId int', 'itemInSession int', 'artist text', 'song text', 'length decimal']
    columns1 = ['sessionId', 'itemInSession', 'artist', 'song', 'length']
    keys1 = '(sessionId, itemInSession)'
    
    ### Create table for Query 1
    sparkify_db.create_table(session, table1, columns1_type, keys1)
    
    ### Insert data for Table 1
    with open(output_path, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            value = [int(line[8]), int(line[3]), line[0], line[9], float(line[5])]
            sparkify_db.insert_data(session, table1, columns1, value)
    
    print('\nInserted data for Query 1\n')
    
    ### Testing result for Query 1
    test_query1 = "SELECT artist, song, length FROM %s WHERE sessionId = 338 AND itemInSession = 4" % (table1)
    result1 = sparkify_db.test_table(session, table1, test_query1)
    print('The result for Query 1:')
    for row in result1:
        print("\t", "ArtistName: ", row.artist, "\t", "Song: ", row.song, "\t", "Duration: ", row.length)
    
    # Testing Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
    table2 = 'song_playlist_session'
    columns2_type = ['userId int', 'sessionId int', 'itemInSession int', 'artist text', 'song text', 'user text']
    columns2 = ['userId', 'sessionId', 'itemInSession', 'artist', 'song', 'user']
    keys2 = '((userId, sessionid), itemInSession)'
    
    ### Create table for Query 2
    sparkify_db.create_table(session, table2, columns2_type, keys2)
    
    ### Insert data for Table 2
    with open(output_path, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for line in csvreader:
            user = line[1] + " " + line[4]
            value = [int(line[10]), int(line[8]), int(line[3]), line[0], line[9], user]
            sparkify_db.insert_data(session, table2, columns2, value)
    
    print('\nInserted data for Query 2\n')
    
    ### Testing result for Query 2
    test_query2 = "SELECT artist, song, user FROM %s WHERE userId = 10 AND sessionId = 182 ORDER BY itemInSession ASC" % (table2)
    result2 = sparkify_db.test_table(session, table2, test_query2)
    print('The result for Query 2:')
    for row in result2:
        print("ArtistName: ", row.artist, "\t", "Song: ", row.song, "\t", "User: ", row.user)
    
    # Testing Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
    table3 = 'user_song'
    columns3_type = ['song text', 'userId int', 'user text']
    columns3 = ['song', 'userId', 'user']
    keys3 = '((song), userId)'
    
    ### Create table for Query 3
    sparkify_db.create_table(session, table3, columns3_type, keys3)
    
    ### Insert data for Table 3
    with open(output_path, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for line in csvreader:
            user = line[1] + " " + line[4]
            value = [line[9], int(line[10]), user]
            sparkify_db.insert_data(session, table3, columns3, value)
    
    print('Inserted data for Query 3\n')
    
    ### Testing result for Query 3
    test_query3 = "SELECT song, user FROM %s WHERE song = 'All Hands Against His Own'" % (table3)
    result3 = sparkify_db.test_table(session, table3, test_query3)
    print('The result for Query 3:')
    for row in result3:
        print("User: ", row.user, "\t", "Song: ", row.song)
    
    # Drop tables 
    sparkify_db.drop_table(session, table1)
    sparkify_db.drop_table(session, table2)
    sparkify_db.drop_table(session, table3)
    print('\nDropped all tables')
    
    # Disconnect tables
    sparkify_db.disconnect(session)
    print('\nShut down all sessions\n')
    
if __name__ == "__main__":
    main()