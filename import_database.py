from operator import index
from pickle import FALSE
import pandas as pd
from sqlalchemy import false
import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from msrest import ServiceClient

# path_folder = '21_07_2022'
# path_file   = 'data_21_07_2022_13_14_03'


def load_database(storage_account_name, storage_account_key,path_folder, path_file):
    
    path = f'C:\\Users\\Trieu.Nguyen\\Downloads\\WareHouse_Solution\\upload\\{path_folder}\\{path_file}.xlsx'
    path_parquet = f'C:\\Users\\Trieu.Nguyen\\Downloads\\WareHouse_Solution\\upload\\{path_folder}\\{path_file}.parquet'
    df  =  pd.read_excel(path)
    df.to_parquet(path_parquet, index =  FALSE)    
    try:  
        global service_client
        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)

        global file_system_client
        file_system_client = service_client.get_file_system_client(file_system="my-file-system")
        directory_client = file_system_client.get_directory_client("my-directory\\test")

        file_client = directory_client.get_file_client(f'{path_file}.parquet')

        local_file = open(path_parquet,'rb')
        file_contents = local_file.read()
        file_client.upload_data(file_contents, overwrite=True)

    except Exception as e:
        print(e.__str__())
        print("333333333333333333333333333")

# load_database(path_folder, path_file, storage_account_name, storage_account_key)