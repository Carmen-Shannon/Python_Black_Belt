from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL as connect
import re
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)


class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owned_paintings = []

    @staticmethod
    def validate(user):
        is_valid = True
        data = {'email': user['email_register']}
        email_exists = User.get_user_by_email(data)
        print(email_exists)
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(user['first_name']) < 2 or user['first_name'] == '':
            flash('First name must be at least 2 characters', 'reg')
            is_valid = False
        if len(user['last_name']) < 2 or user['last_name'] == '':
            flash('Last name must be at least 2 characters', 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(user['email_register']) or user['email_register'] == '':
            flash('Invalid email', 'reg')
            is_valid = False
        if email_exists:
            flash('Email already exists', 'reg')
            is_valid = False
        if user['password_register'] != user['confirm_password']:
            flash('Passwords do not match', 'reg')
            is_valid = False
        if len(user['password_register']) < 8 or user['password_register'] == '' or user['password_register'].isalpha():
            flash(
                'Passwords must be at least 8 characters and contain a number or special character', 'reg')
        return is_valid

    @classmethod
    def add_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        return connect('paintings').query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connect('paintings').query_db(query, data)

        if result == False or len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM USERS;'
        results = connect('paintings').query_db(query)
        users = []

        for user in results:
            users.append(cls(user))

        if results == False or len(results) < 1:
            return False

        return users

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connect('paintings').query_db(query, data)

        if result == False or len(result) < 1:
            return False

        return cls(result[0])

    def add_painting(self, painting):
        self.owned_paintings.append(painting)
