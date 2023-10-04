import os,sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
from src.components import *
from src.utils.main_utils import MainUtils
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from typing import Generator,Tuple,List
from sklearn.metrics import accuracy_score


from xgboost import XGBClassifier
from sklearn.svm import SVC
from dataclasses import dataclass


@dataclass

class ModelTrainingConfig:
    artifacts_folder = os.path.join(artifacts_folder)
    training_model_path = os.path.join(artifacts_folder,"model.pkl")
    expected_accuracy = 0.45
    model_config_file_path = os.psth.join('config','model.yaml')


    

class ModelTraining:
    
  
    def __init__(self):

        self.model_training_config = ModelTrainingConfig()

        self.utils = MainUtils()

        self.models = {
            "XGBOOST":XGBClassifier(),
            "GRADIENTBOOST":GradientBoostingClassifier(),
            "RANDOMFOREST":RandomForestClassifier(),
            "SVC":SVC()

        }


    
    def eval_model(self,X,y,models):
        try:

            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42)

            report = {}
            for i in range(len(list(models))):
                model = list(models.values())[i]
                model.fit(X_train,y_train)
                ypred = model.predict(X_test)

                accuracy_score = accuracy_score(y_test,ypred)

                report[list(models.keys())[i]] = accuracy_score

            return report 

        except Exception as e:
            raise CustomException(e,sys)
        


    def get_best_model(self,X_train:np.array,
        X_test:np.array,
        y_test:np.array,
        y_train:np.array):

        try:

            model_report:dict =self.eval_model(self,X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=self.models)

            print(model_report)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]


            best_model_obj = self.models[best_model_name]

            return best_model_name,best_model_score,best_model_obj

        except Exception as e:
            raise CustomException(e,sys)
        

    def finetuning(self,best_model_obj:object,best_model_name,X_train,y_train)->object:

        try:

            model_param_grid = self.utils.read_yaml_file(ModelTrainingConfig.model_config_file_path)["model_selection"][best_model_name]["search_param_grid"]

            grid_search = GridSearchCV(best_model_obj,model_param_grid=model_param_grid,cv=5,verbose=1,n_jobs=1)
            grid_search.fit(X_train,y_train)

            best_param = grid_search.best_params_
            print(f"best Parameters : {best_param}")
            fine_tuned_model = best_model_obj.set_params(**best_param)

            return fine_tuned_model



        except Exception as e:
            raise CustomException(e,sys)
        


    
    def initiate_model_traing(self,train_arr,test_arr):
        try:

            logging.info("spliting data into train and test")

            X_train,X_test,y_train,y_test =(
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]

            )


            logging.info(f"Extracting model config file path")

            model_report = self.eval_model(X_train,X_test,self.models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_name)
                ]
            
            best_model = self.models[best_model_name]

            
            best_model = self.finetuning(
                best_model_name= best_model_name,
                best_model_object= best_model,
                X_train= X_train,
                y_train= y_train
            )



            best_model.fit(X_train,y_train)
            y_pred = best_model.predict(X_test)
            best_model_score = accuracy_score(y_pred,y_test)
                
            print(f"best model name {best_model_name} and best score {best_model_score}")

            if best_model_score<0.5:

                raise Exception("No best model found with an accuracy greater than the threshold 0.6")
            
            logging.info(f"Best found model training dataset")

            

            logging.info(f"saving the model path {self.model_training_config.training_model_path}")
            os.makedirs(os.path.dirname(self.model_training_config.training_model_path),exist_ok=True)

            self.utils.save_obj(file_path=self.model_training_config.training_model_path,
                                obj=best_model)
            return self.model_training_config.training_model_path


        except Exception as e:
            raise CustomException(e,sys)




        
