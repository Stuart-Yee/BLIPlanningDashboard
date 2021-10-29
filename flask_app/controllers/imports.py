from flask import Flask, render_template, session, flash, redirect, request
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.item import Item
from flask_app.models.warehouse import Warehouse
from openpyxl import workbook, worksheet, load_workbook, writer

@app.route("/import")
def import_files():
    if session["logged_in"]:
        return render_template("import.html")
    else:
        return redirect("/")