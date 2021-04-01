from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CreateTablesOperator(BaseOperator):
    """
    Initialize the CreateTablesOperator

    Args:
        conn_id: connection id 
        create_query_list: a list of create_table query
        
    Returns: None
    """
    ui_color = '#85BC9F'
    
    @apply_defaults
    def __init__(self,
                 conn_id,
                 create_query_list,
                 *args, **kwargs):

        super(CreateTablesOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.create_query_list = create_query_list

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id = self.conn_id)
        
        for create_query in self.create_query_list:
            redshift.run(create_query)
 
        self.log.info('Finished creating tables')
