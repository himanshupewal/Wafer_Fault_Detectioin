import os,sys
from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTraining

class TrainingPipeline:

    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion()
            features_store_file_path = data_ingestion.export_data_into_feature_store
            return features_store_file_path

        except Exception as e:
            raise CustomException(e,sys)
        


class Transfoemation_Pipeline:

    def start_data_transformation(self,features_store_file_path):
        try:

            data_transformation = DataTransformation(feature_store_path=features_store_file_path)
            train_arr,test_arr,preprocessor_path = data_transformation.initate_data_transformation()
            return train_arr,test_arr,preprocessor_path

        
        except Exception as e:
            raise CustomException(e,sys)
        


class Model_training_pipeline:

    def start_data_model(self,train_arr,test_arr):
        try:
            model_trainer = ModelTraining()
            model_score = model_trainer.initiate_model_traing(
                train_arr,test_arr
            )
            return model_score
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def run_pipeline(self):

        try:

            feature_store_file_path = self.start_data_ingestion()
            train_arr,test_arr,preprocessor_path = self.start_data_transformation(feature_store_file_path)
            accuracy_score = self.start_data_model(train_arr,test_arr)

            
            print("training completed. Trained model score : ", accuracy_score)



        
        except Exception as e:
            raise CustomException(e,sys)