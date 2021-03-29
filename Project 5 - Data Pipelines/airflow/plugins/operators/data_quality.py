from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 conn_id,
                 tables=[],
                 *args, **kwargs):
        """
        Construct of Data Quality Operator
        
        Args:
        tables: a list of table need to be checked
        redshift_conn_id
        """
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.tables = tables

    def execute(self, context):
        """
        Execute the DataQualityOperator instance
        
        Args:
        context: Context for the operator
        """
        
        redshift_hook = PostgresHook(self.conn_id)
        
        for table in self.tables:
            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {table} returned no results")
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check failed. {table} contained 0 rows")
 
            logging.info(f"Data quality on table {table} check passed with {records[0][0]} records")    
    
        logging.info(f"All Data quality checks passed!")    
        