# ETF Research Data Project

## Project Summary
As a Canadian Passive Investor who wants to invest in North America stocks. As there're thousands ETF available in the market, investor want to start a top-down analysis on different sector in North America. He/she want to do analysis on different sectors in both Canada and US.

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

### Glossary:
* North America: Only include US and Canada
* Passive Investor: Investors who will likely to invest in ETF or Mutual fund tracking certain index
* Benchmark: Benchmark is the standard to evaluate the performance of security, mutual fund, ETF, portfolio manager. Different benchmarks have different focus include different geographic locations, industry sectors, and investment styles, etc. It often constitute different individual securities or other benchmarks.
* NTR Index: Net Total Return Tracks all the capital gain as well as cash distribution income

## 1: Project Scope and Data Collection

All data are collected from Quandl with its Python API. 
Two datasets are used:

### Required packages installation
1. Quandl API
2. Pandas
3. Configparser

Installation for Quandl
'''
!pip install quandl
'''

Usage of Quandl API
'''
import quandl
'''

For more details related to Quandl, please refer to:
[Quandl](https://www.quandl.com/)
[Quandl Python API Installation](https://docs.quandl.com/docs/python-installation)

#### 1.1 Index Past Performance
When selecting industry and location, benchmarks for different industries and location are most suitable to track their past performance. NNASDAQ OMX Global Index Data is used for this project. 

There are two dataset used for Index data:
1. Past Daily Index Data
2. Index list data

##### Index Data Columns:
1. Date: Date in mm/dd/yyyy format
2. DATABASE_CODE: Database code
3. DATASET_CODE: Dataset code 
4. Index Value: Close value of given date
5. High: Highest value of given date
6. Low: Lowest value of given date
7. Total Market Value: Market value of index
8. Dividend Market Value: Total Dividend received

##### Index List Columns:
1. Name: Name of the index
2. SYMBOL: Current symbol
3. OLD SYMBOL: Previously used symbol

Source for Index List: https://www.quandl.com/data/NASDAQOMX-NASDAQ-OMX-Global-Index-Data/documentation

#### 1.2 Federal Reserve Economic Data
Economic data are highly valuable when conducting sector analysis. Traditional industry like consumer staples and consumer discretionary are highly correlated to economic data. Federal Reserve data is collected as well to supplement sector analysis.

There are two dataset used for Economic data:
1. Economic Indicator Schema
2. Economic Indicator with value

##### Economic Indicator Schema Columns:
1. CODE: Dataset code
2. INDICATOR: The name of Indicator
3. TYPE: Type of indicator

Source for Economoic Indicator List: https://www.quandl.com/data/FRED-Federal-Reserve-Economic-Data/documentation

##### Economic Indicator with Value Columns:
1. Date: Date in mm/dd/yyyy format
2. DATABASE_CODE: Database code
3. DATASET_CODE: Dataset code 
4. Value: Value of the indicator

### Expected Outcome
1. Update daily index value when market is open
2. Check if new Federal Reserve data is available and update it
3. Enable investor to conduct analysis with both index and economic data

Note: Quandl is a alternative data platform to provide different dataset for making investment decision.

## 2: Data Exploration and Cleaning

Duplicate Value are found and removed. Please refer to Capstone Project Template.ipynb for detailed process.

## 3: Data Modeling

### 3.1 Data Model Design 

#### Standard SQL Database vs NoSQL

Standard SQL Database is picked over NoSQL database with the following reason:
1. Due to scope of this analysis, only index and economoic indicators will be analyzed. Varieties of data are limited. 
2. Type of query can be varied. If NoSQL database like Cassandra is used, lots of type of query need to be created for analyzing investments and thus not very effective
3. Standard SQL database are more cost-effective for personal projects of small scale

Factors that affects variation of queries:
1. Time-Series - Different Time Period can be selected 
2. Geographical Location - US/Canada
3. For each sector, different economoic indicators combination may be used for analysis.
4. Correlation analysis between sector analysis/ Economoic Indicators

#### Star-Schema
Both economoic indicator and index are selected based on eco_indicator_list and index_list. However, when extracting out data, important information is missing from the 'value' table. Thus, a STAR schema is needed. Information in the list and value table need to combine as a fact table for easier accessible of all required information for research.

### 3.2 Final Conceptual Data Model

#### Schema Design
![../images/ERD.jpg](../images/ERD.jpg)

The graph above shown the fact table component of data modeling. Each table need a fact table to better prepare for analysis.

##### Dimension Tables:

###### index_value:
1. date: Date in mm/dd/yyyy format (DATE) - Primary Key
2. dataset_code: Database code (VARCHAR) - Primary Key & Foreign Key(Reference index_list(symbol))
3. database_code: Dataset code (VARCHAR)
4. index_value: Close value of given date (NUMERIC)
5. total_market_value: Market value of index (NUMERIC)
6. dividend_market_value: Total Dividend received (NUMERIC)

###### index_list:
1. index_name: Name of the index (VARCHAR)
2. symbol: Current symbol (VARCHAR) - Primary Key
3. old_symbol: (VARCHAR) Previously used symbol

###### eco_indicator_list:
1. code: Dataset code (VARCHAR) - Primary Key
2. indicator_name: The name of Indicator (VARCHAR)
3. type: Type of indicator (VARCHAR)

###### eco_indicator_value:
1. date: Date in mm/dd/yyyy format (DATE) - Primary Key
2. database_code: Database code (VARCHAR) - Primary Key & Foreign Key(Reference eco_indicator_list(code))
3. dataset_code: Dataset code (VARCHAR)
4. indicator_value: Value of the indicator (NUMERIC)

##### Fact Tables:

When conducting sector analysis, the actual name of index is needed. It's not clear with only dataset_code. At this moment, only 1 type of index provider is used, we can ignore database_code. However, as index from other provider may be added in the future, database_code is kept to distinguish index data provider.

###### index_fact:
1. index_name 
2. date
3. dataset_code
4. index_value
5. total_market_value
6. dividend_market_value

When we conduct economical analysis, we need the sector information for economic indicators. 'indicator_name' and 'type' are added to the fact table.

###### eco_fact:
1. indicator_name
2. date
3. code
4. value
5. type

### 3.2 Data Pipelines Processes
1. Extract data from API 
2. Transform data to required foramt for schema
3. Create connection to data table 
4. Load initial data into the dimension tables
5. Load initial data into the fact tables with data from dimension table

## 4. Data Pipeline Running

### 4.1 Table Creation and Data Loading

The data pipeline is executed with the following command.

'''
python create_tables.py
'''

'''
python etl.py
'''

### 4.2 Data Quality Checks
Explain the data quality checks you'll perform to ensure the pipeline ran as expected. These could include:
 * Integrity constraints on the relational database (e.g., unique key, data type, etc.)
 * Unit tests for the scripts to ensure they are doing the right thing
 * Source/Count checks to ensure completeness

The data checks are mainly completed through 2 components 
1. Initial duplication and data check(Please refer to part 1)
2. integrity constraints on the relational database during the insert base:
    a. Unique key exists to identify unique value 
    b. Date type is used for all date related columns 
    c. NUMERIC data type are used for all value column and rest are all VARCHAR
    
### 4.3 Data Dictionary
### **Data Dictionary**

### Dimension Table

#### Index List
1. index_name: Name of the index (VARCHAR)
2. symbol: Current symbol used to extract from quandl(VARCHAR) - Primary Key
3. old_symbol: Previously used symbol to extract from quandl. It may used when new symbol is not working(VARCHAR) 

#### Index Value
1. date: Date in mm/dd/yyyy format (DATE) - Primary Key
2. dataset_code: Database code. One database may contain multiple dataset. (VARCHAR) - Primary Key & Foreign Key (Reference index_list(symbol))
3. database_code: Dataset code specifically for the dataset - represent a index (VARCHAR)
4. index_value: Close value of index given date (NUMERIC)
5. total_market_value: Market value of index given the date(NUMERIC)
6. dividend_market_value: Equalivant Dividend received for Index in the given day(NUMERIC)

#### Economic Indicator List
1. code: Dataset code within FRED database(VARCHAR) - Primary Key
2. indicator_name: The name of Economic Indicator (VARCHAR)
3. type: Type of Economic indicator (VARCHAR)

#### Economic Indicator Value
1. date: Date in mm/dd/yyyy format (DATE) - Primary Key
2. database_code: Database code. One database may contain multiple dataset. (VARCHAR)  - Primary Key & Foreign Key(Reference eco_indicator_list(code))
3. dataset_code: Dataset code specifically for the dataset - represent a type of indicator (VARCHAR)
4. indicator_value: Value of the indicator (NUMERIC)

### Fact Tables

#### Index Value Fact Table
1. index_name: Name of the index (VARCHAR)
2. date: Date in mm/dd/yyyy format (DATE)
3. dataset_code: Database code. One database may contain multiple dataset. (VARCHAR)
4. index_value: Close value of index given date (NUMERIC)
5. total_market_value: Market value of index given the date(NUMERIC)
6. dividend_market_value: Equalivant Dividend received for Index in the given day(NUMERIC)

#### Economic Indicator Fact Table
1. indicator_name: The name of Economic Indicator (VARCHAR)
2. date: Date in mm/dd/yyyy format (DATE)
3. code: Dataset code specifically for the dataset - represent a type of indicator (VARCHAR)
4. value: Value of the indicator (NUMERIC)
5. type: Type of Economic indicator (VARCHAR)


## 5. Project Write Up

### 5.1 Tools/Technology Selection: 
1. Data Exploration: 
Python Pandas Dataframe is used for initial exploration of raw data as it is easy to use for this size of data with good I/O compared to Spark.

2. Data Pipeline:
ETL are mainly completed with Python. The raw data are relatively clean after data exploration. Python pandas is more than enough to complete the task. Python also have easy access to connect to AWS Redshift. 

3. Data Storage:
AWS Redshift is the data storage tool selected for the project. It offers flexibility with resize/concurrency scaling feature that allows the database to expand capability. With SORTKEY & DISTKEY setup, the reading speed will be increased when large amount of data is stored in the schema.

### 5.2 Data Update Frequency
It depends on analytics need. To get the most updated everyday, it can set to update everything daily as index value are updated every working day. However, economic indicator value are usually updated at least weekly. Another update strategy will be update everything on weekly when we need the data to do analysis. As a long-term investor, we tend not to do a lot of update on our investment strategy/decision a lot. I believe weekly update is more than enough to serve its purpose effectively.

### 5.3 Plan for future

#### 5.3.1 Data Amount increase by 100x
If stock market in more area are needed to analyze, the data amount will be increased. Current database utilization is less than 1 GB. If the data amount increase by 100x as data accumulate over time and area to analyze expand, current Redshift configuration is still able to hold. If the data amount increases further, the size of REDSHIFT cluster can be resized to cater increasing data size demand.

#### 5.3.2 Data Populates a dashboard that must be updated on a daily basis by 7am everyday
Airflow will be a good choice to schedule everything to run daily basis by 7am as it offers:
1. One platform to have overview of data pipeline processes(DAG)
2. Task dependency easily managed by DAG
3. Easy to use scheduling capabilities including good retry set up
4. Alerting system inform data engineers with emails

The data pipeline for updating the dashboard will likely to include following steps 
1. Check most recent date for each index and economic indicator used(Python)
2. Download data starting after the most recent date(Python)
3. Load downloaded data into cluster (Airflow with Python)
4. Refresh dashboard with the new data

#### 5.3.3 The database needed to be accessed by 100+ people
AWS Redshift has the concurrency scaling feature that allows Redshift to automatically add additional cluster when more cluster capacity is needed as more users are querying the database. It will be able to 100+ users at ease with flexibility to save cost incurred.