import numpy as np
from pydantic import BaseModel, Field
from typing import Any, Optional, List


class User(BaseModel):
    nom: str = Field(default="Nom", min_length=3, max_length=20, pattern="^[A-Z]")
    prenom:str = Field(default="Prenom", min_length=3, max_length=20, pattern="^[A-Z]")
    mdp:str = Field(default="12345678", min_length=8, max_length=20)


class Car(BaseModel):
    Name: str
    Location: str
    Year: int
    Kilometers_Driven: int
    Fuel_Type: str
    Transmission: str
    Owner_Type: str
    Mileage: str
    Engine: str
    Power: str
    Seats: float
    New_Price: str
    Price: float

class Cars(BaseModel):
    message : str = "cars loaded"
    cars : List[Car]
    


class ReplaceNAN(BaseModel):
    column_name: str
    new_value: Any


class NewColumnName(BaseModel):
    column_name: str
    new_column_name: str


class DeleteRow(BaseModel):
    row_index: int


class RenameCar(BaseModel):
    new_name: str


class CarYear(BaseModel): # Pas utilisagle dans un get
    operator: str
    year: int