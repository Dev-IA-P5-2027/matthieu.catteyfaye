from base_models import Car, ReplaceNAN, NewColumnName, DeleteRow, RenameCar, CarYear
from pymongo import MongoClient

url = 'mongodb://matthieu:mdp@localhost:27017/?authSource=admin'

conn = MongoClient(url)

db = conn["data-cars"]

collection = db["cars"]


class CarService():
    def __init__(self):
        pass


    def get_all_cars(self):

        cars = list(collection.find({}, {"_id":0}))

        return cars
    

    def get_cars_by_year(self, year: int, operator: str):

        if operator=='>':
            return list(collection.find({}, {"_id":0}))
        
        elif operator=='<':
            return list(collection.find({}, {"_id":0}))
        
        elif operator=='=':
            return list(collection.find({}, {"_id":0}))
        
        else:
            return list(collection.find({}, {"_id":0}))