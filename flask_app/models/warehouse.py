from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
from flask_app import app
SCHEMA = "blistock"

class Warehouse:

    def __init__(self, data):
        self.id = data["id"]
        self.warehouse_name = data["warehouse_name"]
        self.code = data["code"]
        self.description = data["description"]
        self.updated_by = data["updated_by"] # This must be the user's id

    @classmethod
    def save_warehouse(cls, data):
        query = "INSERT INTO warehouses (warehouse_name, code, description, updated_by, created_at, updated_at) VALUES " \
                "(%(warehouse_name)s, %(code)s, %(description)s, %(updated_by)s, now(), now());"
        return connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM warehouses;"
        results = connectToMySQL(SCHEMA).query_db(query)
        warehouses = []
        for warehouse in results:
            warehouses.append(cls(warehouse))
        return warehouses

    @classmethod
    def find_by_id(cls, data):
        query = "SELECT * FROM warehouses WHERE id = %(id)s;"
        result = connectToMySQL(SCHEMA).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return False

    @classmethod
    def find_exact_by_code(cls, data):
        query= "SELECT * FROM warehouses WHERE code = %(code)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return False

    @staticmethod
    def validate_warehouse(warehouse):
        valid_item = True
        if len(warehouse["code"]) < 1:
            flash("Please enter a warehouse designation", "code")
            valid_item = False
        if Warehouse.find_exact_by_code(warehouse):
            flash("That Warehouse designation already exists!", "code")
            valid_item = False
        return valid_item
