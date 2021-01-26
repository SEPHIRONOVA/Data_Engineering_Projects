# Import Python packages 
import os
import glob
import csv

def get_path_lists(path):
    """
    Get all directories in the path and store them in a list
    :path: the directory path to walk through
    :return: list of arraies that contain all paths in the directory
    """
    filepath = os.getcwd() + '/event_data'
    
    for root, dirs, files in os.walk(filepath):
        # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root,'*'))
        
    return file_path_list

def process_raw_data(file_path_list, output_path):
    """
    Go through all file paths and write them into a csv file 
    :file_path_list: list of arraies that contain all paths in the directory
    :return: None
    """
    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = [] 

    # for every filepath in the file path list 
    for f in file_path_list:

    # reading csv file 
        with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            next(csvreader)

     # extracting each data row one by one and append it        
            for line in csvreader:
                full_data_rows_list.append(line) 

    # creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
    # Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                    'level','location','sessionId','song','userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))
            
def check_output(output_path):
    """
    Check number of rows loaded into the output file:
    output_path: the path for output file
    """
    with open(output_path, 'r', encoding = 'utf8') as f:
        print('Total number of records is %d \n' % (sum(1 for line in f)))
        