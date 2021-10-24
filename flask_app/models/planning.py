from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
from flask_app import app
from flask_app.models import warehouse, item
SCHEMA = "blistock"

class Planning:

    def __init__(self, data):
        self.id = data["id"]
        self.min = data["min"]
        self.max = data["max"]
        self.warehouse = data["warehouse_id"]
        self.item = data["item_id"]
        self.updated_by = data["updated_by"] # This must be the user's id

    @classmethod
    def save_planning(cls, data):
        query = "INSERT INTO plannings (min, max, warehouse_id, item_id, updated_by, created_at, updated_at) VALUES " \
                "(%(min)s, %(max)s, %(warehouse_id)s, %(item_id)s, %(updated_by)s, now(), now());"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # @classmethod
    # def find_by_warehouse(cls, data):
    #     query = "SELECT * FROM plannings " \
    #             "JOIN warehouses ON warehouses.id = warehouse_id " \
    #             "JOIN items on items.id = item_id " \
    #             "WHERE warehouse_id = %(id)s;"
    #     results = connectToMySQL(SCHEMA).query_db(query, data)
    #     print(results)
    #     if len(results) > 0:
    #         plannings = []
    #         for planning in results:
    #             print(planning)
    #             plannings.append(cls(planning))
    #         return plannings
    #     else:
    #         return False

    @staticmethod
    def validate_planning(data):
        print("Validating:")
        print(data)
        data["id"] = data["warehouse_id"]
        valid_planning = True
        if not warehouse.Warehouse.find_by_id(data):
            flash("Could not find warehouse", "warehouse")
            valid_planning = False
        if not item.Item.find_by_itemnumber_exact(data):
            flash(f"Could not find item {data['item_number']}", "item")
            valid_planning = False
        if data["min"] > data["max"]:
            flash("Min must be less than Max", "item")
            valid_planning = False
        print(valid_planning)
        return valid_planning
