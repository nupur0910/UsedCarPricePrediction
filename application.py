from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

model = pickle.load(open('LinearRegModel.pkl', 'rb'))
car = pd.read_csv("car data.csv")


@app.route('/')
def index():
    car_name = sorted(car['Car_Name'].unique())
    year = sorted(car['Year'].unique(), reverse=True)
    fuel_type = car['Fuel_Type'].unique()
    seller_type = sorted(car['Seller_Type'].unique())
    transmission = sorted(car['Transmission'].unique())
    car_name.insert(0,"Select Car Name")
    return render_template("index.html", car_name=car_name, years=year, fuel_types=fuel_type, seller_types=seller_type,
                           trans=transmission)


@app.route("/predict", methods=['POST'])
def predict():
    year = request.form.get('year')
    price = request.form.get('curr_price')
    driven = request.form.get('kilo_driven')
    fuel_type = request.form.get('fuel_type')
    seller_type = request.form.get('seller_type')
    trans = request.form.get('trans')
    owner = request.form.get('owner')
    if (fuel_type == "Petrol"):
        fuel_type = 0
    if (fuel_type == "Diesel"):
        fuel_type = 1
    if (fuel_type == "CNG"):
        fuel_type = 2

    if (seller_type == "Dealer"):
        seller_type = 0
    if (seller_type == "Individual"):
        seller_type = 1

    if (trans == "Manual"):
        trans = 0
    if (trans == "Automatic"):
        trans = 1
    prediction = model.predict(
        pd.DataFrame(columns=['Year', 'Present_Price', 'Kms_driven', 'Fuel_type', 'Seller_Type', 'Transmission', 'Owner'],
                     data=np.array([year, price, driven, fuel_type, seller_type, trans, owner]).reshape(1, 7)))
    print(prediction)

    return str(np.round(prediction[0], 2))


if __name__ == "__main__":
    app.run(debug=True)
