from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
from flask_app import app
from flask_app.models import planning, item, quantity
SCHEMA = "blistock"

class Warehouse:

    def __init__(self, data):
        self.id = data["id"]
        self.warehouse_name = data["warehouse_name"]
        self.code = data["code"]
        self.description = data["description"]
        self.updated_by = data["updated_by"] # This must be the user's id
        self.warehouse_items = []

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
        query = "SELECT * FROM warehouses " \
              "LEFT JOIN plannings on plannings.warehouse_id = warehouses.id " \
              "LEFT JOIN items on items.id = plannings.item_id " \
              "LEFT JOIN quantities on items.id = quantities.item_id " \
              "LEFT JOIN users on users.id = plannings.updated_by " \
              "WHERE warehouses.id = %(id)s"
        result = connectToMySQL(SCHEMA).query_db(query, data)
        if len(result) > 0:
            warehouse = cls(result[0])
            for row in result:
                warehouse_item_data = {
                    "item_number": row['item_number'],
                    "description": row['items.description'],
                    "warehouse": row['code'],
                    "warehouse_min": row['min'],
                    "warehouse_max": row['max'],
                    "warehouse_qty": row['on_hand'],
                    "planning_updated_on": row['plannings.updated_at'],
                    "quantity_updated_on": row['updated_at'],
                    "quantity_id": row["quantities.id"],
                    "planning_id": row["plannings.id"],
                    "quantity_updated_by": ""
                }
                if row['first_name'] is None or row['last_name'] is None:
                    warehouse_item_data["planning_updated_by"] = None
                else:
                    warehouse_item_data["planning_updated_by"] = row['first_name'] + " " + row['last_name']
                this_item = item.WarehouseItem(warehouse_item_data)
                warehouse.warehouse_items.append(this_item)
            return warehouse
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
