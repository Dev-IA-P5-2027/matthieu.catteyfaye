import pandas as pd
from fastapi import APIRouter
from base_models import Car, ReplaceNAN, NewColumnName, DeleteRow, RenameCar, CarYear, Cars

from car_service import CarService

carservice = CarService()

router = APIRouter(tags=["Car"])

# data = pd.read_csv("train_droped_nan.csv", index_col=None)



@router.get("/cars", response_model=Cars)
def get_all_cars():

    cars = carservice.get_all_cars()

    return Cars(cars=cars)



@router.get("/cars/year", response_model=Cars)
def get_cars_by_year(year: int, operator: str):

    cars = carservice.get_cars_by_year(year, operator)

    try:    
        return Cars(cars=cars)
    
    except:
        print(' /!\ ')



@router.get("/cars/location", response_model=Cars)
def get_cars_ordered_by_locations(ascending: bool):
    
    cars = carservice.get_cars_ordered_by_locations(ascending)

    return Cars(cars=cars)



@router.post("/cars")
def create_car(new_car: Car):

    car_row = carservice.create_car(new_car)

    return car_row



@router.delete("/cars/{car_id}")
def delete_car(car_id:int):
    
    msg = carservice.delete_car(car_id)

    return msg



@router.put("/cars/{car_id}")
def rename_car(car_id:int, new_name:RenameCar):
    
    msg = carservice.rename_car(car_id, new_name)

    return msg