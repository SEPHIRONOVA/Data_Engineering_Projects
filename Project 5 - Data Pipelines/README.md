# Project: Data Pipelines with Airflow

## Introduction
Sparkify is a music streaming company and they've been collecting songs and user activities. Now the company decided to automate their data warehouse ETL pipelines. Apache Airflow will be the main tool used to implement the project. AWS S3 and redshift will be used to store the source and output data.

## Purpose of the project:
1. Construct data pipeline with JSON source data located in AWS S3 and move into AWS redshift
2. Automate pipeline with Apache Airflow

## Project Setup - run locally
1. Install Airflow, create variable AIRFLOW_HOME and AIRFLOW_CONFIG with appropriate paths and place dags and plugins on airflow_home directory
	'pip install apache-airflow'
    airflow db init
2. Initialize Airflow with 'airflow db init' and open webserver with 'airflow webserver'
3. Access server with default port 'http://localhost:8080' 
4. Create Connections(required both local and on cloud):

**AWS Connection**
Conn Id: Enter aws_credentials.
Conn Type: Enter Amazon Web Services.
Login: Enter your Access key ID from the IAM User credentials you downloaded earlier.
Password: Enter your Secret access key from the IAM User credentials you downloaded earlier.

**Redshift Connection**
Conn Id: Enter redshift.
Conn Type: Enter Postgres.
Host: Enter the endpoint of your Redshift cluster, excluding the port at the end. 
Schema: Enter dev. This is the Redshift database you want to connect to.
Login: Enter awsuser.
Password: Enter the password you created when launching your Redshift cluster.
Port: Enter 5439.

## Data Source ##
* Log data: `s3://udacity-dend/log_data`
* Song data: `s3://udacity-dend/song_data`

## Pipeline Design

## DAG ##
Default Parameters
  * The DAG does not have dependencies on past runs (depends_on_past)
  * DAG has schedule interval set to hourly
  * On failure, the task are retried 3 times (Retries)
  * Retries happen every 5 minutes (Retry_delay)
  * Catchup is turned off (catchup)
  * Email are not sent on retry
  * Start Time
  * Owner

Task Dependecies
![/images/task_dependencies.png](/images/task_dependencies.png)

## Operators

* Create Table Operator
It create tables in AWS Redshift to store fact & dimension table. It takes following parameters:
  **conn_id** : AWS Redshift connection id
  **create_query_list** : list of CREATE TABLE queries

* Stage Operator
Stage operator loads data in JSON format from AWS S3 to Redshift. It creates a parametric COPY statement based on following parameters:
  **table** : the table to load into
  
  **conn_id** : AWS Redshift connection id
  
  **aws_credentials_id** : AWS username and password
  
  **s3_bucket** : S3 bucket
  
  **s3_key** : S3 bucket key
  
  **region** : region of server
  
  **file_format** : format of source file(e.g. JSON)
  
  **optional_path** : optional file contains json folder

* Fact & Dimension Operator
Fact & Dimension Operators process and load data in staging table into fact & dimension table. It establish a connection with AWS Hook and insert with sql query based on following parameters:

  **table** : the table to load into
  
  **conn_id** : AWS Redshift connection id
  
  **sql_statement** : sql_query
  
  **reset_table** : option to determine reset table
  
* Data Quality Operator
Quality check on data loaded in the facts & dimension table if the table:
1. Table has value after insert statement
2. Data value has more than 0 rows

It needs following parameters:
   **conn_id** : AWS Redshift connection id
	
   **tables[]** : A list contains table need to be checked 

## Helpers
* create_table_queries
A collection of SQL queries for creating table in Redshift

* sql_queries
It is a class contain all the SQL insert statements for data loading.
