from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
from flask_app import app
SCHEMA = "blistock"

class Item:

    def __init__(self, data):
        self.id = data["id"]
        self.number = data["number"]
        self.description = data["description"]

    @classmethod
    def save_item(cls, data):
        query = "INSERT INTO items (item_number, description, created_at, updated_at) VALUES " \
                "(%(item_number)s, %(description)s, now(), now());"
        return connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items;"
        results = connectToMySQL(SCHEMA).query_db(query)
        items = []
        for item in results:
            items.append(cls(item))
        return items

    @classmethod
    def find_by_id(cls, data):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        result = connectToMySQL(SCHEMA).query_db(query, data)
        return cls(result[0])

    @classmethod
    def find_by_itemnumber(cls, data):
        query = "SELECT * FROM items WHERE itemnumber = %(itemnumber)s;"
        result = connectToMySQL(SCHEMA).query_db(query, data)
        return cls(result[0])

    @staticmethod
    def validate_item(item):
        valid_item = True
        if len(item["item_number"]) < 1:
            flash("Please enter item number", "item_number")
            valid_item = False
        if len(item["description"]) < 1:
            flash("Please enter an item description")
            valid_item = False
        return valid_item
