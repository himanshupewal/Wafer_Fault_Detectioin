import pandas as pd
from pymongo.mongo_client import MongoClient
import json

url = "mongodb+srv://himanshupewal:ABCabc123@cluster1.t9c5vaf.mongodb.net/?retryWrites=true&w=majority"

clinet = MongoClient(url)

DATABASE_NAME= "Wafer"
COLLECTION_NAME="Waferfault"

df=pd.read_csv("C:/Users/himan/OneDrive/Desktop/Wafer_sensor_project/Notebook/Data/wafer_23012020_041211.csv")
df=df.drop("Unnamed: 0",axis=1)

json_recods = list(json.loads(df.T.to_json()).values())
clinet[DATABASE_NAME][COLLECTION_NAME].insert_many(json_recods)