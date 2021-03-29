from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 conn_id,
                 table,
                 sql_query,
                 reset_table,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.table = table
        self.sql_query = sql_query
        self.reset_table = reset_table

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id = self.conn_id)
        
        # To delete the content of database
        if self.reset_table:
            reset_sql = "TRUNCATE TABLE {}".format(self.table)
            redshift.run(reset_sql)
            
        sql = """
            INSERT INTO {}
            {};
            """.format(self.table, self.sql_query)
        redshift.run(sql)
        
        self.log.info('Finished loading staging table {}'.format(self.table))

