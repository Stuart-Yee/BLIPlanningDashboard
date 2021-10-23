from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("(?=.*\d)(?=.*[A-Z])")
bcrypt = Bcrypt(app)
DATABASE = "blistock"

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.email = data["email"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (email, first_name, last_name, password, created_at, updated_at) VALUES (%(email)s, %(first_name)s, %(last_name)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        for user in users:
            print(user.email)
        return users

    @classmethod
    def get_all_emails(cls):
        users = User.get_all()
        emails = []
        for user in users:
            emails.append(user.email)
        return emails


    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            user = cls(results[0])
            return user
        else:
            return False

    @staticmethod
    def validate_registration(user):
        valid_user = True
        # make sure email follows format
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email, please try again", "email")
            valid_user = False
        if user["email"] in User.get_all_emails():
            flash("User already registered by that email", "email")
            valid_user = False
            print("duplicate email!")
        if len(user["first_name"]) < 2:
            flash("First name must be at least two characters", "first_name")
            valid_user = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least two characters", "last_name")
            valid_user = False
        if user["password"] != user["password_confirm"]:
            flash("Passwords do not match, please try again!", "password")
            valid_user = False
        if not PASSWORD_REGEX.match(user["password"]):
            flash("Password must have at least one(1) number and one(1) uppercase letter", "password")
            valid_user = False
        return valid_user

    @staticmethod
    def validate_login(user):
        valid_login = True
        if not User.find_by_email(user):
            valid_login = False
        else:
            registered_user = User.find_by_email(user)
            if not bcrypt.check_password_hash(registered_user.password, user["password"]):
                valid_login = False
        if not valid_login:
            print("adding message to flash")
            flash("Invalid email/password combination", "login")
        return valid_login