from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
from flask_app import app
from flask_app.models import warehouse, item

SCHEMA = "blistock"

class Quantity:

    def __init__(self, data):
        self.id = data["id"]
        self.on_hand = data["on_hand"]
        self.warehouse = data["warehouse_id"]
        self.item = data["item_id"]
        self.updated_by = data["updated_by"] # This must be the user's id
        self.updated_at = data["updated_at"]
        self.created_at = data["created_at"]

    @classmethod
    def save_quantity(cls, data):
        query = "INSERT INTO quantities (on_hand, warehouse_id, item_id, updated_by, created_at, updated_at) VALUES " \
                "(%(on_hand)s, %(warehouse_id)s, %(item_id)s, %(updated_by)s, now(), now());"
        return connectToMySQL(SCHEMA).query_db(query, data)




