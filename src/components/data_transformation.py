import os,sys
import pandas as pd
import numpy as np
from src.logger import logging
from sklearn.preprocessing import StandardScaler,RobustScaler,FunctionTransformer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.constant import * 
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
from src.exception import CustomException


@dataclass 

class DataTransformationConfig:
    artifacts_dir = os.path.join(artifacts_folder)
    transformaed_train_file_path = os.path.join(artifacts_dir,"train.npy")
    transformed_test_file_path=os.path.join(artifacts_dir,'test.npy')
    transformaed_obj_file_path = os.path.join(artifacts_dir,"preprocessor.pkl")




class DataTransformation:

    def __init__(self,feature_store_path):
        self.feature_store_path = feature_store_path
        self.data_transformation_config = DataTransformationConfig()
        self.utils = MainUtils()


@staticmethod

def get_data(feature_store_path:str)->pd.DataFrame:
    try:

        data = pd.read_csv(feature_store_path)

        data.rename(columns={"Good/Bad":TARGET_COLUMN},inplace=True)

        return data
    
    except Exception as e:
        raise CustomException(e,sys)


@staticmethod

def get_data_transformed(self):
    try:
        imputer = ("imputer",SimpleImputer(strategy='constant',fill_value=0))
        scaler = ("scaler",RobustScaler())

        preprocessor = Pipeline(
            steps=[("imputation of missing values with constant value",imputer),
                   ('scaling the features',scaler)]
        )
        return preprocessor
    

    

    except Exception as e:
        raise CustomException(e,sys)

@staticmethod

def initate_data_transformation(self):
    logging.info(
            "Entered initiate_data_transformation method of Data_Transformation class"
        )

    try:
        dataframe = self.get_data(feature_store_path=feature_store_path)

        X = dataframe.drop(columns=TARGET_COLUMN)
        y = np.where(dataframe[TARGET_COLUMN]==-1,0,1)
        logging.info("data splited into X,y now runinig in train test split")

        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42)

        preprocessor = self.get_data_transformed()

        X_train_scaled = preprocessor.fit_transform(X_train)
        X_test_scaled = preprocessor.transform(X_test)


        preprocessor_path = self.data_transformation_config.transformaed_obj_file_path
        os.makedirs(os.path.dirname(preprocessor_path),exist_ok=True)
        self.utils.save_obj(preprocessor_path,preprocessor)


        train_arr = np.c_[X_train_scaled,np.array(y_train)]
        test_arr = np.c_[X_test_scaled,np.array(y_test)]

        return (train_arr,test_arr,preprocessor_path)


        

    except Exception as e:
        raise CustomException(e,sys)




