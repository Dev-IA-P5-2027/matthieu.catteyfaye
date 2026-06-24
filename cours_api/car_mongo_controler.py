from fastapi import APIRouter
from base_models import Car, ReplaceNAN, NewColumnName, DeleteRow, RenameCar, CarYear, Cars
from pymongo import MongoClient

from car_mongo_service import CarService

carservice = CarService()

# url = 'mongodb://matthieu:mdp@localhost:27017/?authSource=admin'

# conn = MongoClient(url)

# db = conn["data-cars"]

# collection = db["cars"]

router = APIRouter(tags=["Cars"])

@router.get("/cars", response_model=Cars)
def get_all_cars():

    cars = carservice.get_all_cars()

    return Cars(cars=cars)


@router.get("/cars/year", response_model=Cars)
def get_cars_by_year(year: int, operator: str):

    cars = carservice.get_cars_by_year(year, operator)

    return Cars(cars=cars)