from app import db
from classes.json_read import JsonRead
from models import User, Order, Offer

import datetime

users_json = JsonRead("data/users.json")
orders_json = JsonRead("data/orders.json")
offers_json = JsonRead("data/offers.json")

db.drop_all()
db.create_all()

for user in users_json.load_data():
    with db.session.begin():
        db.session.add(User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        ))

for order in orders_json.load_data():
    month_start, day_start, year_start = [int(_) for _ in order['start_date'].split("/")]
    month_end, day_end, year_end = [int(_) for _ in order['end_date'].split("/")]
    with db.session.begin():
        db.session.add(Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(month=month_start, day=day_start, year=year_start),
            end_date=datetime.date(month=month_end, day=day_end, year=year_end),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        ))

for offer in offers_json.load_data():
    with db.session.begin():
        db.session.add(Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        ))
