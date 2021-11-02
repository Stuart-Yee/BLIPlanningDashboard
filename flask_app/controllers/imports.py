from flask import Flask, render_template, session, flash, redirect, request
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.item import Item
from flask_app.models.warehouse import Warehouse
from openpyxl import workbook, worksheet, load_workbook, writer

#  TODO module for being able to accept CSV

@app.route("/import")
def import_files():
    if session.get("logged_in") == True:
        return render_template("import.html")
    else:
        return redirect("/")

@app.route("/import/warehouses", methods=["POST"])
def import_warehouses():
    if session.get("logged_in") != True or request.method != "POST":
        return redirect("/")
    else:
        uploaded_file = request.files["warehouse_imports"]
        mappings = [request.form["warehouse_code"],
                    request.form["warehouse_name"],
                    request.form["warehouse_description"]]

        #spreasheet columns will be:
        #   mappings[0] = Warehouse Code
        #   mappings[1] = Warehouse Name
        #   mappings[2] = Warehouse Description

        if request.form.get("ignore_first_row") == "on":
            ignore_first = True
        else:
            ignore_first = False

        wb = load_workbook(uploaded_file)
        sheet = wb.active
        if ignore_first:
            start = 2
        else:
            start = 1
        end = sheet.max_row + 1
        print(f"Importing {end - start} rows")
        for i in range(start, end):
            warehouse = {
                "code": sheet[f"{mappings[0]}{i}"].value,
                "warehouse_name": sheet[f"{mappings[1]}{i}"].value,
                "description": sheet[f"{mappings[2]}{i}"].value,
                "updated_by": session["user_id"]
            }
            for key in warehouse:
                if warehouse[key] is None:
                    warehouse[key] = ""
            log_row = warehouse["code"] + " " + warehouse["warehouse_name"]
            validation = Warehouse.validate_warehouse(warehouse, imported=True)
            if validation[0]:
                Warehouse.save_warehouse(warehouse)
                log_row += " Import successful!"
                flash(log_row, "warehouse_import_successful")
            else:
                log_row += f" Import failed: {validation[1]}"
                flash(log_row, "warehouse_import_fail")
            print(log_row)
        return redirect("/import/warehouses/result")

@app.route("/import/warehouses/result")
def show_whs_import_result():
    return render_template("importResultTest.html")