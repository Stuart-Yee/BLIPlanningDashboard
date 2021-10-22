from flask_app.config.mysqlconnection import connectToMySQL
SCHEMA = "[database name goes here]"

class item:

    def __init__(self, data):
        self.id = data["id"]
        self.number = data["number"]
        self.description = data["description"]

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
