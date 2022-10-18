import datetime
import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False

db = SQLAlchemy(app)


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        user_data = db.session.query(User).all()
        return jsonify([user.to_dict() for user in user_data])
    elif request.method == "POST":
        try:
            user = json.loads(request.data)
            new_user_obj = User(
                id=user["id"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                age=user["age"],
                email=user["email"],
                role=user["role"],
                phone=user["phone"]
            )
            with db.session.begin():
                db.session.add(new_user_obj)
                return "Пользователь создан в базе данных", 200
        except Exception as e:
            print(e)


@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def user_one(user_id):
    if request.method == "GET":
        user_data = db.session.query(User).get(user_id)
        if user_data is None:
            return "Не найдено"
        else:
            return jsonify(user_data.to_dict())
    elif request.method == "PUT":
        with db.session.begin():
            user_data = json.loads(request.data)
            user = db.session.query(User).get(user_id)
            if user is None:
                return "Пользователь не найден!", 404
            user.first_name = user_data["first_name"]
            user.last_name = user_data["last_name"]
            user.age = user_data["age"]
            user.email = user_data["email"]
            user.role = user_data["role"]
            user.phone = user_data["phone"]

            db.session.add(user)
            return f"Пользователь с id {user_id} успешно изменён!", 200
    elif request.method == "DELETE":
        with db.session.begin():
            user = db.session.query(User).get(user_id)
            if user is None:
                return "Пользователь не найден!", 404

            db.session.delete(user)
            return f"Пользователь с id {user_id} успешно удалён!", 200


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        order_data = db.session.query(Order).all()
        return jsonify([order.to_dict() for order in order_data])
    elif request.method == "POST":
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = [int(_) for _ in order['start_date'].split("/")]
            month_end, day_end, year_end = [int(_) for _ in order['end_date'].split("/")]
            new_order_obj = Order(
                id=order["id"],
                name=order["name"],
                description=order["description"],
                start_date=datetime.date(month=month_start, day=day_start, year=year_start),
                end_date=datetime.date(month=month_end, day=day_end, year=year_end),
                address=order["address"],
                price=order["price"],
                customer_id=order["customer_id"],
                executor_id=order["executor_id"]
            )
            with db.session.begin():
                db.session.add(new_order_obj)
                return "Заказ создан в базе данных", 200
        except Exception as e:
            print(e)


@app.route("/orders/<int:order_id>", methods=["GET", "PUT", "DELETE"])
def order_one(order_id):
    if request.method == "GET":
        order_data = db.session.query(Order).get(order_id)
        if order_data is None:
            return "Не найдено"
        else:
            return jsonify(order_data.to_dict())
    elif request.method == "PUT":
        with db.session.begin():
            order_data = json.loads(request.data)
            order = db.session.query(Order).get(order_id)
            month_start, day_start, year_start = [int(_) for _ in order_data['start_date'].split("/")]
            month_end, day_end, year_end = [int(_) for _ in order_data['end_date'].split("/")]
            if order is None:
                return "Заказ не найден!", 404
            order.name = order_data["name"]
            order.description = order_data["description"]
            order.start_date = datetime.date(month=month_start, day=day_start, year=year_start)
            order.end_date = datetime.date(month=month_end, day=day_end, year=year_end)
            order.address = order_data["address"]
            order.price = order_data["price"]
            order.customer_id = order_data["customer_id"]
            order.executor_id = order_data["executor_id"]

            db.session.add(order)
            return f"Заказ с id {order_id} успешно изменён!", 200
    elif request.method == "DELETE":
        with db.session.begin():
            order = db.session.query(Order).get(order_id)
            if order is None:
                return "Заказ не найден!", 404

            db.session.delete(order)
            return f"Заказ с id {order_id} успешно удалён!", 200


@app.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "GET":
        offer_data = db.session.query(Offer).all()
        return jsonify([offer.to_dict() for offer in offer_data])
    elif request.method == "POST":
        try:
            offer = json.loads(request.data)
            new_offer_obj = Offer(
                id=offer["id"],
                order_id=offer["order_id"],
                executor_id=offer["executor_id"]
            )
            with db.session.begin():
                db.session.add(new_offer_obj)
                return "Предложение создано в базе данных", 200
        except Exception as e:
            print(e)


@app.route("/offers/<int:offer_id>", methods=["GET", "PUT", "DELETE"])
def offer_one(offer_id):
    if request.method == "GET":
        offer_data = db.session.query(Offer).get(offer_id)
        if offer_data is None:
            return "Не найдено"
        else:
            return jsonify(offer_data.to_dict())
    elif request.method == "PUT":
        with db.session.begin():
            offer_data = json.loads(request.data)
            offer = db.session.query(Offer).get(offer_id)
            if offer is None:
                return "Предложение не найдено!", 404
            offer.order_id = offer_data["order_id"]
            offer.executor_id = offer_data["executor_id"]

            db.session.add(offer)
            return f"Предложение с id {offer_id} успешно изменёно!", 200
    elif request.method == "DELETE":
        with db.session.begin():
            offer = db.session.query(Offer).get(offer_id)
            if offer is None:
                return "Предложение не найдено!", 404

            db.session.delete(offer)
            return f"Предложение с id {offer_id} успешно удалёно!", 200


if __name__ == "__main__":
    app.run(debug=True)
