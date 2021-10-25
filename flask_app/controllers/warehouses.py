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
        return render_template("showWarehouse.html", warehouse=warehouse)
    else:
        return redirect("/")

@app.route("/warehouses/<int:id>/addPlanning", methods=["POST"])
def add_to_warehouse(id):
    if session["logged_in"]:
        data = {}
        for key in request.form:
            data[key] = request.form[key]
        data["warehouse_id"] = id
        data["updated_by"] = session["user_id"]
        data["on_hand"] = int(request.form["quantity"])
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

@app.route("/warehouses/plannings/<int:planning_id>", methods=["GET", "POST"])
def update_planning(planning_id):
    if not session["logged_in"]:
        return  redirect("/")
    else:
        if request.method == "GET":
            data = {'id': planning_id} #id corresponds to planning
            display_objects = Planning.find_planning_by_whs(data)
            display_planning = display_objects[0]
            display_item = display_objects[1]
            display_warehouse = display_objects[2]
            return render_template("planning.html",
                           display_planning=display_planning,
                           display_item=display_item,
                           display_warehouse=display_warehouse)
        else:
            warehouse_id = request.form["warehouse_id"]
            data = {
                "id": planning_id,
                "min": request.form["min"],
                "max": request.form["max"],
                "updated_by": session["user_id"]
            }
            if Planning.validate_update(data):
                Planning.update_planning(data)
                return redirect(f"/warehouses/show/{warehouse_id}")
            else:
                return redirect(f"/warehouses/plannings/{planning_id}")

@app.route("/warehouses/quantities/<int:qty_id>", methods=["POST"])
def update_quantity(qty_id):
    if not session["logged_in"] == True:
        return redirect("/")
    else:
        print("logged in!")
        data = {
            "id": qty_id,
            "on_hand": request.form["quantity"],
            "updated_by": session["user_id"]
        }
        warehouse = request.form["warehouse_id"]
        Quantity.update_quantity(data)
        return redirect(f"/warehouses/show/{warehouse}")
