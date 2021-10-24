from flask import Flask, render_template, session, flash, redirect, request
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.warehouse import Warehouse
from flask_app.models.planning import Planning
from flask_app.models.item import Item
from flask_app.models.quantity import Quantity
bcrypt = Bcrypt(app)

@app.route("/newWarehouse", methods=["POST"])
def add_warehouse():
    if(session["logged_in"]):
        data ={}
        for key in request.form:
            data[key] = request.form[key]
        if Warehouse.validate_warehouse(data):
            data["updated_by"] = session["user_id"]
            warehouse_id = Warehouse.save_warehouse(data)
            return redirect("/addRecords")
        else:
            return redirect("/addRecords")
    else:
        return redirect("/")

@app.route("/warehouses/show/<int:id>")
def show_warehouse(id):
    if(session["logged_in"]):
        data = {'id': id}
        warehouse = Warehouse.find_by_id(data)
        print(warehouse)
        return render_template("showWarehouse.html", warehouse=warehouse)
    else:
        return redirect("/")

@app.route("/warehouses/<int:id>/addPlanning", methods=["POST"])
def add_to_warehouse(id):
    if(session["logged_in"]):
        data = {}
        for key in request.form:
            data[key] = request.form[key]
        data["warehouse_id"] = id
        data["updated_by"] = session["user_id"]
        data["on_hand"] = 0
        if Item.find_by_itemnumber_exact(request.form):
            data["item_id"] = Item.find_by_itemnumber_exact(request.form).id
        if Planning.validate_planning(data):
            Planning.save_planning(data)
            Quantity.save_quantity(data)

            return redirect(f"/warehouses/show/{id}")
        else:
            return redirect(f"/warehouses/show/{id}")
    else:
        return redirect("/")
