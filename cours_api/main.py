from fastapi import FastAPI, Query # pour pouvoir lancer dans le terminal  : 'pip install "fastapi[standard]"' puis 'fastapi dev main.py' ou 'uvicorn main:app --reload'
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from typing import Any
from base_models import User, Car, ReplaceNAN, NewColumnName, DeleteRow
from car_controler import router as cars_router
from car_mongo_controler import router as cars_mongo_router


app = FastAPI()
# app.include_router(cars_router)
app.include_router(cars_mongo_router)


data = pd.read_csv("train.csv", index_col=None)


# class BaseModel():
#     def __init__(self):
#         self.nom:str = Query(default="Nom", min_length=3, max_length=20, pattern="^[A-Z]")
#         self.prenom:str = Query(default="Prenom", min_length=3, max_length=20, pattern="^[A-Z]")
#         self.mdp:str = Query(min_length=8, max_length=20)


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/say_hello_by_name")   # query parameter
# def hello_name(name:str = Query(default="World", 
#                                 min_length=3, 
#                                 max_length=20, 
#                                 pattern="^[A-Z]" # regex : vérifie name commence par majuscule
#                                 )
#                             ): 
#     if name:
#         return f"Hello {name} !"
#     else:
#         return "Hello !"
    

# @app.get("/add_two_numbers")            # query parameters : on ajoute '?nb1=0&nb2=0' à l'url, faire varier les valeurs de nb1 et nb2 pour résultats différents
# def sum_numbers(nb1: int, nb2: int):
#     return nb1+nb2


# @app.post("/users")
# def add_user(new_account: User):
#     new_user = {
#         "nom":new_account.nom,
#         "prenom":new_account.prenom,
#         "password":new_account.mdp
#     }
#     return new_user


# @app.get("/say_hello_by_name2/{name}")   # path parameter : on ajoute la valeur du paramètre après un '/' dans notre route
# def hello_name(name: str):
#     return f"Hello {name} !"

@app.get("/get_columns")
def get_columns():
    print(data.columns)
    return list(data.columns)



@app.get("/get_head/{number}")
def get_head(number: int):
    print(data.head(number).to_dict())
    return data.head(number).to_dict()


@app.get("/get_column_type")
def get_column_type(column_name: str):
    if column_name in list(data.columns):
        col_type = str(data[column_name].dtype)
        print(data[column_name].dtype)
        if col_type=="float" or col_type=="int" or col_type=="float64" or col_type=="int64":
            minimum = data[column_name].min()
            print(minimum)
            maximum = data[column_name].max()
            print(maximum)
            return [str(col_type), str(minimum), str(maximum)]
        else:
            unique_values = data[column_name].unique()
            print(unique_values)
            return [str(col_type), unique_values.tolist()]
    else:
        return "Colonne introuvable"



@app.post("/replace_nan")
def replace_nan(replace_nan: ReplaceNAN):
    global data
    if replace_nan.column_name not in list(data.columns):
        return "Colonne introuvable"

    nan_count = int(data[replace_nan.column_name].isna().sum())

    if nan_count == 0:
        return "Pas de NaN dans la colonne"

    col = data[replace_nan.column_name]
    new_val = replace_nan.new_value

    type_compatible = (
        (pd.api.types.is_integer_dtype(col) and isinstance(new_val, int)) or
        (pd.api.types.is_float_dtype(col) and isinstance(new_val, float)) or
        (pd.api.types.is_bool_dtype(col) and isinstance(new_val, bool)) or
        (pd.api.types.is_string_dtype(col) and isinstance(new_val, str)) or
        (pd.api.types.is_object_dtype(col) and isinstance(new_val, str))
    )

    if not type_compatible:
        return "La valeur donnée n'est pas du bon type"

    data[replace_nan.column_name] = col.fillna(new_val)
    return f"Nombre de NaN remplacés : {nan_count}"


@app.put("/rename_column")
def rename_column(rename_col:NewColumnName):
    global data
    if rename_col.column_name in list(data.columns):
        data = data.rename(columns={rename_col.column_name : rename_col.new_column_name})
        return f"{rename_col.column_name} renommé en {rename_col.new_column_name}"

    else:
        return "Colonne introuvable"


