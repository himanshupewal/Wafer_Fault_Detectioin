import os,sys
from src.logger import logging
from typing import Dict,Tuple
import numpy as np
import pandas as pd
import pickle
from src.exception import CustomException
import yaml


class MainUtils:
    def __init__(self):
        pass


    def read_yaml_file(self,filename:str)->dict:
        try:
            with open(filename,'rb') as yaml_file:
                return yaml.safe_load(yaml_file)
            
        except Exception as e:
            raise CustomException(e,sys)
        

    def read_schema_config_file(self)->dict:
        try:
            schema_config = self.read_yaml_file(os.apth.join("config","schema.yaml"))
            return schema_config
        
        except Exception as e:
            raise CustomException(e,sys) from e

        



def save_obj(file_path,obj):

    try:

        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys) from e
    


@staticmethod
def load_object(file_path:str)->object:
    logging.info("Entered the load_obj method of MainUttils")

    try:
        

        with open(file_path,"rb") as file_obj:
            obj = pickle.load(file_obj)

            
        logging.info("Existing the load_obj of MainUtils")

        return obj

    except Exception as e:
        raise CustomException(e,sys) from e
    

@staticmethod
def load_object(file_path):
        try:
            with open(file_path,'rb') as file_obj:
                return pickle.load(file_obj)
        except Exception as e:
            logging.info('Exception Occured in load_object function utils')
            raise CustomException(e,sys)
    