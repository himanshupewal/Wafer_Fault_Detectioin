import pandas as pd
import numpy as np
import sys,os
from pymongo import MongoClient
from src.logger import logging
from zipfile import Path
from src.exception import CustomException
from src.constant import *
from dataclasses import dataclass  ## provide direct contact with fuction without using constuctor __init__.
from utils.main_utils import MainUtils

@dataclass

class DataIngestionconfig:
   
   artifacts_folder:str = os.path.join(artifacts_folder)

   """ train_data_path  = os.path.join("arifacts","train.csv")
    test_data_path  =os.path.join("artifacts","test.csv")
    raw_data_path = os.path.join("artifacts","raw.csv")"""




class DataIngestion:

    def __init__(self):
        self.ingestion_config = DataIngestionconfig()
        self.utils = MainUtils()

    


    def export_data_as_dataframe(self,collection_name,db_name):
        try:
            mongo_client = MongoClient(MONGO_DB_URL)
            collection = mongo_client[db_name][collection_name]

            df =pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=['_id'],axis=1)

            df.replace({"na",np.nan},inplace=True)

            return df
        
        except Exception as e:
            raise CustomException(e,sys)


    def export_data_into_feature_store(self):
            try:
                logging.info("exporting has stated")

                raw_file_path = self.ingestion_config.artifacts_folder
                os.makedirs(raw_file_path,exist_ok=True)
                sensor_data = self.export_data_as_dataframe(collection_name=COLLECTION_NAME,
                                                            db_name=DATABASE_NAME)
                

                logging.info(f"Saving to the path{raw_file_path}")
                feature_store_file_path = os.path.join(raw_file_path,"water_fault.csv")
                sensor_data.to_csv(feature_store_file_path,index=False)

                return feature_store_file_path
            except Exception as e:
                raise CustomException(e,sys)   


        


    def initiating_data_ingestion(self)-> Path:

        logging.info(" Initiating Ingestion")

        try:
            features_store_file_path = self.export_data_into_feature_store()

            logging.info("Data has been collected from mongo")

            logging.info("initiating proccess is completed")

            return features_store_file_path

        except Exception as e:
            raise CustomException(e,sys)




