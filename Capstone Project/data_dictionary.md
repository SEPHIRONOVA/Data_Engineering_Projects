# ETF Research Capstone Project

# **Data Dictionary**

## Dimension Table

### Index List
1. index_name: Name of the index (VARCHAR)
2. symbol: Current symbol used to extract from quandl(VARCHAR) - Primary Key
3. old_symbol: Previously used symbol to extract from quandl. It may used when new symbol is not working(VARCHAR) 

### Index Value
1. date: Date in mm/dd/yyyy format (DATE) - Primary Key
2. dataset_code: Database code. One database may contain multiple dataset. (VARCHAR) - Primary Key & Foreign Key (Reference index_list(symbol))
3. database_code: Dataset code specifically for the dataset - represent a index (VARCHAR)
4. index_value: Close value of index given date (NUMERIC)
5. total_market_value: Market value of index given the date(NUMERIC)
6. dividend_market_value: Equalivant Dividend received for Index in the given day(NUMERIC)

### Economic Indicator List
1. code: Dataset code within FRED database(VARCHAR) - Primary Key
2. indicator_name: The name of Economic Indicator (VARCHAR)
3. type: Type of Economic indicator (VARCHAR)

### Economic Indicator Value
1. date: Date in mm/dd/yyyy format (DATE) - Primary Key
2. database_code: Database code. One database may contain multiple dataset. (VARCHAR)  - Primary Key & Foreign Key(Reference eco_indicator_list(code))
3. dataset_code: Dataset code specifically for the dataset - represent a type of indicator (VARCHAR)
4. indicator_value: Value of the indicator (NUMERIC)

## Fact Tables

### Index Value Fact Table
1. index_name: Name of the index (VARCHAR)
2. date: Date in mm/dd/yyyy format (DATE)
3. dataset_code: Database code. One database may contain multiple dataset. (VARCHAR)
4. index_value: Close value of index given date (NUMERIC)
5. total_market_value: Market value of index given the date(NUMERIC)
6. dividend_market_value: Equalivant Dividend received for Index in the given day(NUMERIC)

### Economic Indicator Fact Table
1. indicator_name: The name of Economic Indicator (VARCHAR)
2. date: Date in mm/dd/yyyy format (DATE)
3. code: Dataset code specifically for the dataset - represent a type of indicator (VARCHAR)
4. value: Value of the indicator (NUMERIC)
5. type: Type of Economic indicator (VARCHAR)
