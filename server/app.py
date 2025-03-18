#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods = ["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_dict = [
        {
            "id": restaurant.id, 
            "name": restaurant.name, 
            "address": restaurant.address
        }
        for restaurant in restaurants
    ]   
    return jsonify(restaurant_dict), 200

@app.route("/restaurants/<int:id>", methods = ["GET"])
def get_restaurants_by_id(id):
    restaurant = Restaurant.query.filter_by(id = id).first()

    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict()), 200

@app.route("/restaurants/<int:id>", methods = ["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id = id).first()

    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404
    
    db.session.delete(restaurant)
    db.session.commit()

    return "", 204

@app.route("/pizzas", methods = ["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_dict = [
        {
            "id": pizza.id, 
            "name": pizza.name, 
            "ingredients": pizza.ingredients
        }
        for pizza in pizzas
    ]   
    return jsonify(pizza_dict), 200

@app.route("/restaurant_pizzas", methods = ["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        new_restaurant_pizza = RestaurantPizza(
            price = data["price"],
            pizza_id = data["pizza_id"],
            restaurant_id = data["restaurant_id"]
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        return jsonify(new_restaurant_pizza.to_dict()), 201
    
    except ValueError:
        return jsonify({"errors": ["validation errors"]}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400
    

if __name__ == "__main__":
    app.run(port=5555, debug=True)


# an instance of a class is called an object