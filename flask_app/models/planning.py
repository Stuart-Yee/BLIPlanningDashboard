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

    @classmethod
    def find_by_id(cls, data):
        query = "SELECT * FROM plannings WHERE plannings.id = %(id)"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return False

    @classmethod
    def find_planning_by_whs(cls, data):
        query = "SELECT * FROM plannings " \
                "LEFT JOIN warehouses ON warehouses.id = plannings.warehouse_id " \
                "LEFT JOIN items ON items.id = plannings.item_id " \
                "WHERE plannings.id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if len(results) > 0:
            this_planning = cls(results[0])
            item_data = {
                "id": results[0]["items.id"],
                "item_number": results[0]["item_number"],
                "description": results[0]["items.description"]
            }
            whs_data = {
                "id": results[0]["warehouses.id"],
                "warehouse_name": results[0]["warehouse_name"],
                "code": results[0]["code"],
                "description": results[0]["description"],
                "updated_by": results[0]["warehouses.updated_by"],
            }
            this_item = item.Item(item_data)
            this_warehouse = warehouse.Warehouse(whs_data)
            objects = [this_planning, this_item, this_warehouse]
            return objects
        else:
            return False

    @classmethod
    def find_with_whs_and_item(cls, data):
        query = "SELECT * FROM plannings " \
                "LEFT JOIN items on items.id = plannings.item_id " \
                "WHERE plannings.warehouse_id = %(warehouse_id)s AND " \
                "items.item_number = %(item_number)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return False

    @classmethod
    def update_planning(cls, data):
        query = "UPDATE plannings SET min = %(min)s, " \
                "max = %(max)s, "\
                "updated_by = %(updated_by)s, " \
                "updated_at = now() "\
                "WHERE plannings.id = %(id)s;"
        connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def update_from_whs_item(cls, data):
        planning_id = Planning.find_with_whs_and_item(data)
        if planning_id:
            data["id"] = planning_id.id
            Planning.update_planning(data)
            return planning_id
        else:
            return False


    @staticmethod
    def validate_planning(data, imported=False, update=False):
        data["id"] = data["warehouse_id"]
        valid_planning = True
        errors = []
        if not warehouse.Warehouse.find_by_id(data):
            error = "Could not find warehouse"
            valid_planning = False
            if imported:
                errors.append(error)
            else:
                flash(error, "warehouse")

        if not item.Item.find_by_itemnumber_exact(data):
            error = f"Could not find item {data['item_number']}"
            valid_planning = False
            if imported:
                errors.append(error)
            else:
                flash(error, "item")

        if int(data["min"]) > int(data["max"]):
            valid_planning = False
            error = "Min must be less than Max"
            if imported:
                errors.append(error)
            else:
                flash(error, "item")
        if not update:
            if Planning.find_with_whs_and_item(data):
                valid_planning = False
                error = "Item already added to this warehouse"
                if imported:
                    errors.append(error)
                else:
                    flash(error, "item")

        return [valid_planning, errors]

    @staticmethod
    def validate_update(data):
        valid_planning = True
        if int(data["min"]) > int(data["max"]):
            flash("Min must be less than Max", "item")
            valid_planning = False
        return valid_planning
