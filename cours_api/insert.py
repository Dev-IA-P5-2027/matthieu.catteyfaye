import pandas as pd
from pymongo import MongoClient, AsyncMongoClient, InsertOne

url = 'mongodb://matthieu:mdp@localhost:27017/?authSource=admin'

conn = MongoClient(url)
print(conn.list_database_names())
mydb = conn["data-cars"]

mycol = mydb["cars"]

df = pd.read_csv(r"train_droped_nan.csv")

data_cars = df.to_dict(orient='records')

x = mycol.insert_many(data_cars)

print(conn.list_database_names())
print(mydb.list_collection_names())