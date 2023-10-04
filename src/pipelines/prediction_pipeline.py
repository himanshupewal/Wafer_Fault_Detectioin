import os,sys
import shutil
from src.exception import CustomException
from src.components.data_transformation import *
from src.logger import logging
from src.utils.main_utils import MainUtils
from src.constant import *
from flask import request
import pickle
from dataclasses import dataclass

@dataclass

class PredictionPipelineConfig:
    
    pred_output_dirname:str= "Prediction"
    pre_file_name:str = "Predicted_fiel.csv"
    model_file_path: str= os.path.join(artifacts_folder,"model.pkl")
    preprocessor_file_path:str = os.path.join(artifacts_folder,"preprocessor")
    prediction_file_path:str = os.path.join(pred_output_dirname,pre_file_name)








class PredictionPipeline:


    def __init__(self,request):

        self.request = request
        self.utils= MainUtils()
        self.Prediction_pipeline_config = PendingDeprecationWarning()



    def save_input_file(self)->str:

        try:


            pred_input_file_dic = "prediction_artifacts"

            os.makedirs(pred_input_file_dic,exist_ok=True)

            input_csv_file = self.request.file["file"]

            pred_input_file_path = os.path.join(pred_input_file_dic,input_csv_file.filename)

            input_csv_file.save(pred_input_file_path)



            return pred_input_file_path
        
        except Exception as e:
            raise CustomException(e,sys)
            




    def start_prediction_pipeline(self,features):
        try:
            model = self.utils.load_object(self.Prediction_pipeline_config.model_file_path)
            preprocessor = self.utils.load_object(self.Prediction_pipeline_config.preprocessor_file_path)

            tranformed_x = preprocessor.transform(features)

            pred = model.predict(tranformed_x)

            return pred




        except Exception as e:
            raise CustomException(e,sys)
        

    def get_predicted_dataframe(self,input_csv_file_path:pd.DataFrame):
        try:
            prediction_col_name :str = TARGET_COLUMN
            input_dataframe : pd.read_csv = pd.read_csv(input_csv_file_path)
            input_dataframe = input_dataframe.drop(columns="Unnamed: 0",axis=1) if "Unnamed: 0" in input_dataframe else input_dataframe

            prediction = self.start_prediction_pipeline(input_dataframe)
            input_dataframe[prediction_col_name] = [ pred for pred in prediction]

            target_col_mapping = {1:"Good",0:"Bad"}

            input_csv_file_path[prediction_col_name] = input_dataframe[prediction_col_name].map(target_col_mapping)

            os.makedirs(self.Prediction_pipeline_config.pred_output_dirname,exist_ok=True)
            input_dataframe.to_csv(self.Prediction_pipeline_config.prediction_file_path,index=False)

            logging.info("Prediction completed")

        except Exception as e:
            raise CustomException(e,sys)
        


    def run_pipeline(self):
        try:
            input_csv_path = self.save_input_file()
            self.get_predicted_dataframe(input_csv_path)
            return self.Prediction_pipeline_config

        except Exception as e:
            raise CustomException(e,sys)






