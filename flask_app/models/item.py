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
        query = "SELECT * FROM items " \
                "ORDER BY items.item_number;"
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
        query = "SELECT * FROM items WHERE item_number = %(item_number)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return False

    @staticmethod
    def validate_item(item, imported=False):
        valid_item = True
        errors = []  # for imports, will return a list of error messages
        if len(item["item_number"]) < 1 or item["item_number"] == None:
            errors.append("Item number missing")
            flash("Please enter item number", "item_number")
            valid_item = False
        if len(item["description"]) < 1 or item["description"] == None:
            errors.append("Description missing")
            flash("Please enter an item description", "description")
            valid_item = False
        if Item.find_by_itemnumber_exact(item):
            errors.append("Item number already exists")
            flash("Item number already exists", "item_number")
            valid_item = False
        if imported:
            return [valid_item, errors]  # for imports, returns boolean value and error messages
        return valid_item

class WarehouseItem:

    def __init__(self, data):
        self.item_number = data["item_number"]
        self.description = data["description"]
        self.warehouse = data["warehouse"]  # not persisted, particular to warehouse
        self.whs_min = data["warehouse_min"]  # not persisted, particular to warehouse
        self.whs_max = data["warehouse_max"]  # not persisted, particular to warehouse
        self.whs_qty = data["warehouse_qty"]  # not persisted, particular to warehouse
        self.plan_updated_by_name = data["planning_updated_by"]  # not persisted, particular to warehouse
        self.plan_updated_date = data["planning_updated_on"]  # not persisted, particular to warehouse
        self.qty_updated_by = data["quantity_updated_by"]  # not persisted, particular to warehouse
        self.qty_updated_on = data["quantity_updated_on"]  # not persisted, particular to warehouse
        self.quantity_id = data["quantity_id"]
        self.planning_id = data["planning_id"]


