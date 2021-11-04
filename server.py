from flask_app.controllers import users, items, warehouses, imports
from flask_app import app
if __name__=="__main__":
	app.run(debug=True)