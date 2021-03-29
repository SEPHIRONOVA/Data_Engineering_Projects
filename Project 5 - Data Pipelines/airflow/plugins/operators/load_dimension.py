from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 conn_id,
                 table,
                 sql_query,
                 reset_table,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.table = table
        self.sql_query = sql_query
        self.reset_table = reset_table


    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id = self.conn_id)
        
        if self.reset_table:
            reset_sql = "TRUNCATE TABLE {}".format(self.table)
            redshift.run(reset_sql)
        
        sql = """
            INSERT INTO {}
            {};
            """.format(self.table, self.sql_query)
        redshift.run(sql)
        
        self.log.info('Finished loading dimension {}'.format(self.table))
