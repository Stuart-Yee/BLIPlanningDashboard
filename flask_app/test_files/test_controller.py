from flask import Flask, render_template, session, flash, redirect, request
from flask_app import app
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_app.models.warehouse import Warehouse
from flask_app.models.planning import Planning
from flask_app.models.item import Item
from flask_app.models.quantity import Quantity
from openpyxl import workbook, worksheet, load_workbook, writer

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx'}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/testupload", methods=["GET", "POST"])
def testing_upload():
    if request.method == "GET":
        return render_template("testxlupload.html")
    else:
        for key in request.files:
            print(key)
        workbook_bytes = request.files["newExcel"]
        workbook = load_workbook(workbook_bytes)
        sheet = workbook.active
        print(sheet["A1"].value)
        filename = secure_filename(workbook_bytes.filename)
        workbook_bytes.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return redirect("/testupload")