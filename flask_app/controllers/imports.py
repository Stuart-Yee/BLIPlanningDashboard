from flask import Flask, render_template, session, flash, redirect, request
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.item import Item
from flask_app.models.warehouse import Warehouse
from flask_app.models.quantity import Quantity
from flask_app.models.planning import Planning
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

        # spreadsheet columns will be:
        #   mappings[0] = Warehouse Code
        #   mappings[1] = Warehouse Name
        #   mappings[2] = Warehouse Description

        wb = load_workbook(uploaded_file)
        sheet = wb.active
        if request.form.get("ignore_first_row") == "on":
            start = 2
        else:
            start = 1
        end = sheet.max_row + 1

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
                flash(log_row, "import_successful")
            else:
                log_row += f" Import failed: {validation[1]}"
                flash(log_row, "import_fail")
            print(log_row)
        return redirect("/import/result")


@app.route("/import/items", methods=["POST"])
def import_items():
    if session.get("logged_in") != True or request.method != "POST":
        return redirect("/")
    else:
        uploaded_file = request.files["item_imports"]
        mappings = [request.form["item_number"],
                    request.form["item_description"]]
        # mappings[0] = item number
        # mappings[1] = item description

        wb = load_workbook(uploaded_file)
        sheet = wb.active
        end = sheet.max_row+1
        if request.form.get("ignore_first_row") == "on":
            start = 2
        else:
            start = 1
        for i in range(start, end):
            item = {"item_number": sheet[f"{mappings[0]}{i}"].value, "description": sheet[f"{mappings[1]}{i}"].value}
            for key in item:
                if item[key] == None:
                    item[key] = ""
            log_row = item["item_number"] + " " + item["description"]
            validation = Item.validate_item(item, imported=True)
            if validation[0]:
                log_row += " Import successful!"
                flash(log_row, "import_successful")
                Item.save_item(item)
            else:
                for error in validation[1]:
                    log_row += (" " + error)
                flash(log_row, "import_fail")
        return redirect("/import/result")

@app.route("/import/warehouse_items", methods=["POST"])
def import_warehouse_items():
    return redirect("/import/result")

@app.route("/import/quantities", methods=["POST"])
def import_counts():
    mappings = [request.form["count_item"],
                request.form["count_warehouse"],
                request.form["item_qty"]]

    file = request.files["item_count"]
    excel = load_workbook(file)
    sheet = excel.active

    if request.form["ignore_first_row"] == "on":
        start = 2
    else:
        start = 1

    end = sheet.max_row + 1

    for i in range(start, end):
        data = {
            "code": sheet[f"{mappings[1]}{i}"].value,
            "item_number": sheet[f"{mappings[0]}{i}"].value,
            "on_hand": sheet[f"{mappings[2]}{i}"].value,
            "updated_by": session.get("user_id")
        }
        for key in data:
            if data[key] is None:
                data[key] = ""
        result = Quantity.update_by_warehouse_item(data)

        if result:
            flash(
                f"Updated count for {data['item_number']} in "
                f"{data['code']} to {data['on_hand']}",
            "import_successful")
        else:
            flash(
                f"Could not update count for {data['item_number']} "
                f"in {data['code']}",
                "import_fail"
            )

    # ### TESTING quantity methods
    # data = {"code": mappings[1],
    #         "item_number": mappings[0],
    #         "on_hand": mappings[2],
    #         "updated_by": session.get("user_id")}
    # result = Quantity.update_by_warehouse_item(data)
    # flash(result, "import_successful")
    # #### END TEST ####

    return redirect("/import/result")

@app.route("/import/result")
def show_import_result():
    return render_template("import_finish.html")
