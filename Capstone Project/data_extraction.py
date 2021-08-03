import quandl
import pandas as pd
import configparser
import os

config = configparser.ConfigParser()
config.read('credential.cfg')

quandl.ApiConfig.api_key = config['QUANDL']['QUANDL_API_KEY']

INDEX_DATABASE_CODE = 'NASDAQOMX'

# Index Data Extraction

index_list = pd.read_csv('datasets/indexes_list.csv')

# Filter Out Canadian Dollar Based Index
cad_index_list = index_list.loc[index_list['#NAME'].apply(lambda x: x.find('CAD') != -1)]

# Filter out Canada Exposure Index
na_index_list = cad_index_list.loc[cad_index_list['#NAME'].apply(lambda x: x.find('Canada') != -1 or x.find('US') != -1)]

# Total Return Index(TR only not NTR)
na_tr_index_list = na_index_list.loc[na_index_list['#NAME'].apply(lambda x: x.find('TR') != -1 & x.find('NTR') == -1)]

index_data = pd.DataFrame(columns = ['DATABASE_CODE', 'DATASET_CODE'] + ['Index Value','High','Low','Total Market Value','Dividend Market Value'])

for index in na_tr_index_list['SYMBOL']:   

       temp_id = INDEX_DATABASE_CODE + '/' + index
       try:
              temp = quandl.get(temp_id)

              temp['DATABASE_CODE'] = DATABASE_CODE
              temp['DATASET_CODE'] = index
            
              index_data = index_data.append(temp)
       except:
              # Check which index are not able to fetch
              print(index)
              
index_data.reset_index(inplace=True)

index_data = index_data.rename(columns = {'index':'Date'})

index_data.to_csv('datasets/north_america_index.csv', index = False)


# Economic Data Extraction

economic_indicator_list = pd.read_csv('datasets/economic indicator schema.csv')

ECONOMIC_DB_CODE = 'FRED'

economic_data = pd.DataFrame(columns = ['DATABASE_CODE', 'DATASET_CODE', 'Value'])

for indicator in economic_indicator_list['CODE']:   

       temp_id = ECONOMIC_DB_CODE + '/' + indicator
       try:
              temp = quandl.get(temp_id)

              temp['DATABASE_CODE'] = ECONOMIC_DB_CODE
              temp['DATASET_CODE'] = indicator
              
              economic_data = economic_data.append(temp)
       except:
              # Check which economic indicator is not able to fetch
              print(indicator)
              
economic_data.reset_index(inplace=True)

economic_data = economic_data.rename(columns = {'index':'Date'})

economic_data.to_csv('datasets/economic_indicator_value.csv', index = False)
