# import python packages
from cassandra.cluster import Cluster

class CassandraDatabase:
    """
    Manage Apache Cassandra database
    """
    
    def __init__(self, ip_address, replication_class, replication_factor, key_space):
        """
        Constructor
        :ip: IP address for server
        :replication_class:
        :replication_factor
        """
        self.ip = ip_address
        self.replication_class = replication_class
        self.replication_factor = replication_factor
        self.key_space = key_space
        self.cluster = Cluster(self.ip)
    
    def connect(self):
        """
        Establish a connection to Cassandra Cluster and setup a session
        :return: a connected session
        """
        # To establish connection and begin executing queries, need a session
        session = self.cluster.connect()
        
        cql_query = """
                CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = { 'class': '%s', 'replication_factor': %d}
                """ % (self.key_space, self.replication_class, self.replication_factor)

        try:
            session.execute(cql_query)
        except Exception as e:
                print(e)
            
        try:
            session.set_keyspace(self.key_space)
        except Exception as e:
            print(e)
        
        return session

    def create_table(self, session, table, columns, keys):
        """
        Create table for an query
        :session: session needed to create table
        :table: tablename to create
        """
        create_query = "CREATE TABLE IF NOT EXISTS %s (%s , PRIMARY KEY %s)" %(table, ", ".join(columns), keys)
        try:
            session.execute(create_query)
        except Exception as e:
            print(e)            

    def insert_data(self, session, table, columns, value):
        """
        Insert data into table
        :session: session for table
        :table: table to insert

        """
        insert_query = "INSERT INTO %s (%s)" % (table, ", ".join(columns))
        insert_query = insert_query + "VALUES (" + ", ".join(["%s"] * len(columns)) +")"
        try:
            session.execute(insert_query, (value))
        except Exception as e:
            print(e)

    def test_table(self, session, table, test_query):
        """
        Test table with select statement
        :table: table to test
        :test_query: query to test table
        :return: the result of query
        """
        try:
            result = session.execute(test_query)
        except Exception as e:
            print(e)
            
        return result
    
    def drop_table(self, session, table):
        """
        Drop the table if exists
        """
        query = "DROP TABLE IF EXISTS %s" % table
        try:
            session.execute(query)
        except Exception as e:
            print(e)
        
    
    def disconnect(self, session):
        """
        Shut down the session and cluster
        :param session: the session to shutdown
        """
        session.shutdown()
        self.cluster.shutdown()
        