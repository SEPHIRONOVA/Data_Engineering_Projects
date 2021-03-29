from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    template_fields = ("s3_key",)
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID  '{}'
        SECRET_ACCESS_KEY '{}'
        REGION '{}'
        FORMAT AS {} '{}'
        TIMEFORMAT 'epochmillisecs'
        TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    """
    
    @apply_defaults
    def __init__(self, 
                 table="",
                 conn_id="",
                 aws_credentials_id="",
                 s3_bucket="",
                 s3_key="",
                 region="",
                 file_format="",
                 optional_path="",
                 *args, **kwargs
                ):
        """
        Initialize the StageToRedshiftOperator
        
        Args:
        table: redshift cluster table name
        conn_id: connection id 
        aws_credentials_id: AWS credentials for connection
        s3_bucket: S3 bucket name
        s3_key: S3 key files 
        region: region of the server
        format: the format of file to load
        optional_path: an optional path contains all paths for file
        """
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.conn_id = conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region
        self.file_format = file_format
        self.path = optional_path

    def execute(self, context):
        """
        Copy data from S3 to redshift 
        """        
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.conn_id)
        
        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))
        
        self.log.info("Copying data from S3 to Redshift")
        s3_path = "s3://{}/{}".format(self.s3_bucket, self.s3_key)
        
        # If no path contain all json files given, it will use auto formatting
        if self.path == '':
            self.path = 'auto'
        
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.file_format,
            self.path
        )
        
        redshift.run(formatted_sql)
        
        self.info.logging("Successfully loaded {} data to redshift".format(self.table))



