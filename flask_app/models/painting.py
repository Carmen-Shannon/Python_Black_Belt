from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL as connect
from flask_app.models import user


class Painting:

    author = None
    amount_purchased = 0

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.created_by = data['created_by']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.amount_purchased = data['amount_purchased']

    @staticmethod
    def validate(painting):
        is_valid = True
        if len(painting['title']) < 2 or painting['title'] == '':
            flash('Title must be at least two characters', 'add_painting')
            is_valid = False
        if len(painting['description']) < 10 or painting['description'] == '':
            flash('Description must be at least 10 characters', 'add_painting')
            is_valid = False
        if painting['price'] == '' or int(painting['price']) <= 0:
            flash('Price can not be less than 1', 'add_painting')
            is_valid = False
        if painting['quantity'] == '' or int(painting['quantity']) <= 0:
            flash('Can not have less than 1 painting made', 'add_painting')
            is_valid = False
        return is_valid

    @classmethod
    def add_painting(cls, data):
        query = 'INSERT INTO paintings (title, description, price, quantity, created_by, created_at, updated_at, amount_purchased) VALUES (%(title)s, %(description)s, %(price)s, %(quantity)s, %(created_by)s, NOW(), NOW(), 0);'
        return connect('paintings').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM paintings;'
        results = connect('paintings').query_db(query)
        paintings = []
        if results == False or len(results) < 1:
            return False

        for painting in results:
            paintings.append(cls(painting))

        return paintings

    @classmethod
    def get_painting_by_id(cls, data):
        query = 'SELECT * FROM paintings WHERE id = %(id)s;'
        result = connect('paintings').query_db(query, data)

        if result == False or len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def update_quantity(cls, data):
        query = 'UPDATE paintings SET quantity = %(quantity)s, amount_purchased = %(amount_purchased)s WHERE id = %(id)s;'
        return connect('paintings').query_db(query, data)

    @classmethod
    def delete_painting(cls, data):
        query = 'DELETE FROM paintings WHERE id = %(id)s;'
        return connect('paintings').query_db(query, data)

    @classmethod
    def update_painting(cls, data):
        query = 'UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s, updated_at = NOW() WHERE id = %(id)s;'
        return connect('paintings').query_db(query, data)

    @classmethod
    def create_purchase(cls, data):
        query = 'INSERT INTO owned_paintings (user_id, painting_id, created_at, updated_at) VALUES (%(user_id)s, %(painting_id)s, NOW(), NOW());'
        return connect('paintings').query_db(query, data)

    @classmethod
    def get_paintings_by_purchased(cls, data):
        query = 'SELECT painting_id AS id, paintings.title AS title, paintings.description AS description, paintings.price AS price, paintings.quantity AS quantity, paintings.created_by AS created_by, paintings.created_at AS created_at, paintings.updated_at AS updated_at, paintings.amount_purchased AS amount_purchased FROM owned_paintings LEFT JOIN users ON users.id = user_id LEFT JOIN paintings ON paintings.id = painting_id WHERE user_id = %(id)s;'
        paintings = []
        results = connect('paintings').query_db(query, data)

        if results == False or len(results) < 1:
            return False

        for painting in results:
            paintings.append(cls(painting))

        return paintings
