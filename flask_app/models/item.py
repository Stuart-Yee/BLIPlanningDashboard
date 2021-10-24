from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
from flask_app import app
SCHEMA = "blistock"

class Item:

    def __init__(self, data):
        self.id = data["id"]
        self.item_number = data["item_number"]
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
    def find_by_itemnumber_exact(cls, data):
        print(data)
        query = "SELECT * FROM items WHERE item_number = %(item_number)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        print("results:", results)
        if len(results) > 0:
            return cls(results[0])
        else:
            return False

    @staticmethod
    def validate_item(item):
        valid_item = True
        if len(item["item_number"]) < 1 or item["item_number"] == None:
            flash("Please enter item number", "item_number")
            valid_item = False
        if len(item["description"]) < 1 or item["description"] == None:
            flash("Please enter an item description", "description")
            valid_item = False
        if Item.find_by_itemnumber_exact(item):
            flash("Item number already exists", "item_number")
            valid_item = False
        return valid_item
