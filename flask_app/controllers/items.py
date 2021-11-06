from flask import Flask, render_template, session, flash, redirect, request
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.item import Item
from flask_app.controllers.users import logged_in
bcrypt = Bcrypt(app)

@app.route("/newItem", methods=["POST", "GET"])
@logged_in
def add_item():
    if request.method == "GET":
        return render_template("new_item.html")
    elif request.method == "POST":
        data = {}
        for key in request.form:
            data[key] = request.form[key]
        if(Item.validate_item(data)):
            item_id = Item.save_item(data)
        return redirect("/success")
    else:
        return "Sorry, that request method is not valid"


