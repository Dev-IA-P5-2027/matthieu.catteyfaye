import pandas as pd
from base_models import Car, ReplaceNAN, NewColumnName, DeleteRow, RenameCar, CarYear

data = pd.read_csv("train_droped_nan.csv", index_col=None)

class CarService():
    def __init__(self):
        pass


    def get_all_cars(self):

        return [Car(**datum) for datum in data.to_dict(orient="records")]


    def get_cars_by_year(self, year: int, operator: str):

        if operator=='>':
            # print(data[data["Year"].astype(int)>year].values.tolist())
            return [Car(**datum) for datum in data[data['Year'].astype(int)>year].to_dict(orient="records")]
            # return data[data["Year"].astype(int)>year].values.tolist()

        elif operator=='<':
            # print(data[data["Year"].astype(int)<year].values.tolist())
            return [Car(**datum) for datum in data[data['Year'].astype(int)<year].to_dict(orient="records")]
            # return data[data["Year"].astype(int)<year].values.tolist()

        elif operator=='=':
            # print(data[data["Year"].astype(int)==year].values.tolist())
            return [Car(**datum) for datum in data[data['Year'].astype(int)==year].to_dict(orient="records")]
            # return data[data["Year"].astype(int)==year].values.tolist()

        else:
            return "Erreur de saisie"


    def get_cars_ordered_by_locations(self, ascending: bool):

        return [Car(**datum) for datum in data.sort_values("Location", ascending=ascending).to_dict(orient="records")]
        # return data.sort_values("Location", ascending=ascending).values.tolist()


    def create_car(self, new_car: Car):

        car = {
            "Name":[new_car.name],
            "Location":[new_car.location],
            "Year":[new_car.year],
            "Kilometers_Driven":[new_car.kilometers_driven],
            "Fuel_Type":[new_car.fuel_type],
            "Transmission":[new_car.transmission],
            "Owner_Type":[new_car.owner_type],
            "Mileage":[new_car.mileage],
            "Engine":[new_car.engine],
            "Power":[new_car.power],
            "Seats":[new_car.seats],
            "New_Price":[new_car.new_price],
            "Price":[new_car.price]
        }

        car_row = pd.DataFrame(data=car)
        # print(car_row)
        data = pd.concat([data, car_row], ignore_index=True)
        return list(car_row)


    def delete_car(self, car_id:int):

        try:
            data.drop(car_id)
            return f"Ligne d'index '{car_id}' supprimée"
        except:
            return "Suppression impossible"


    def rename_car(self, car_id:int, new_name:RenameCar):

        try:
            data["Name"].iloc[[car_id]] = new_name.new_name
            return f"Voiture renommée en {new_name.new_name}"
        except:
            return "Impossible de renommer"