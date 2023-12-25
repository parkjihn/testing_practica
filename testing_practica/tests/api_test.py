
import os
import json
import logging
from faker import Faker


log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'logs_api.log')

def configure_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

base_logger = configure_logger('base_request_logger', log_file)


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

class Product:
    def __init__(self, product_id, name, price, category_id):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category_id = category_id

class Order:
    def __init__(self, order_id, user_id, product_id, quantity):
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

class Category:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

class Review:
    def __init__(self, review_id, user_id, product_id, rating, comment):
        self.review_id = review_id
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment


class JSONHandler:
    def __init__(self, filename):
        self.filename = filename

    def read_data(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def write_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)


class CRUD:
    def __init__(self, entity_name, file_handler):
        self.entity_name = entity_name
        self.file_handler = file_handler

    def create(self, entity_id, entity):
        data = self.file_handler.read_data()
        if entity_id not in data[self.entity_name]:
            data[self.entity_name][entity_id] = entity.__dict__
            self.file_handler.write_data(data)
            base_logger.debug(f'Создан {self.entity_name[:-1]}: {entity_id}')
            return True
        base_logger.warning(f'{self.entity_name[:-1]} {entity_id} уже существует')
        return False

    def read(self, entity_id):
        data = self.file_handler.read_data()
        return data[self.entity_name].get(entity_id)

    def update(self, entity_id, new_data):
        data = self.file_handler.read_data()
        if entity_id in data[self.entity_name]:
            data[self.entity_name][entity_id].update(new_data)
            self.file_handler.write_data(data)
            base_logger.debug(f'Обновлен {self.entity_name[:-1]}: {entity_id}')
            return True
        base_logger.warning(f'{self.entity_name[:-1]} {entity_id} не существует')
        return False

    def delete(self, entity_id):
        data = self.file_handler.read_data()
        if entity_id in data[self.entity_name]:
            del data[self.entity_name][entity_id]
            self.file_handler.write_data(data)
            base_logger.debug(f'Удален {self.entity_name[:-1]}: {entity_id}')
            return True
        base_logger.warning(f'{self.entity_name[:-1]} {entity_id} не существует')
        return False




faker = Faker()

file_handler = JSONHandler('../db.json')

user_crud = CRUD('users', file_handler)
product_crud = CRUD('products', file_handler)
order_crud = CRUD('orders', file_handler)
category_crud = CRUD('categories', file_handler)
review_crud = CRUD('reviews', file_handler)


for _ in range(5):
    user_id = faker.uuid4()
    user = User(user_id, faker.name(), faker.email())
    user_crud.create(user_id, user)


user_id = list(file_handler.read_data()['users'].keys())[0]
user_crud.update(user_id, {'name': 'Обновленное имя'})
user_crud.delete(user_id)


for _ in range(5):
    product_id = faker.uuid4()
    product = Product(product_id, faker.word(), faker.random_number(digits=3), faker.uuid4())
    product_crud.create(product_id, product)


product_id = list(file_handler.read_data()['products'].keys())[0]
product_crud.update(product_id, {'name': 'Обновленное название продукта', 'price': 999})
product_crud.delete(product_id)


for _ in range(5):
    order_id = faker.uuid4()
    order = Order(order_id, faker.uuid4(), faker.uuid4(), faker.random_digit())
    order_crud.create(order_id, order)


order_id = list(file_handler.read_data()['orders'].keys())[0]
order_crud.update(order_id, {'quantity': 10})
order_crud.delete(order_id)


for _ in range(5):
    category_id = faker.uuid4()
    category = Category(category_id, faker.word())
    category_crud.create(category_id, category)


category_id = list(file_handler.read_data()['categories'].keys())[0]
category_crud.update(category_id, {'name': 'Обновленное название категории'})
category_crud.delete(category_id)


for _ in range(5):
    review_id = faker.uuid4()
    review = Review(review_id, faker.uuid4(), faker.uuid4(), faker.random_digit(), faker.sentence())
    review_crud.create(review_id, review)


review_id = list(file_handler.read_data()['reviews'].keys())[0]
review_crud.update(review_id, {'rating': 5, 'comment': 'Обновленный комментарий'})
review_crud.delete(review_id)