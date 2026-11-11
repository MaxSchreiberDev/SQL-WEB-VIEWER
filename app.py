import os
from flask import Flask, render_template, request
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///newDB.db")

@app.route("/", methods=["POST", "GET"])
def index():
    try:
        tables = db.execute("SELECT DISTINCT name FROM sqlite_master WHERE type = 'table'")
    except:
        raise Exception("No Database")

    promt = request.args.get("sql")

    if promt == None or promt == "?" or promt == "?sql=" or promt == "":
        return render_template("index.html", tables = tables, promt = promt)

    try:
        response = db.execute(promt)

    except RuntimeError:
        return render_template("index.html", error = "Runtime Error: Check SQL statment!", tables = tables, promt = promt)

    return render_template("index.html", response = response, tables = tables, promt = promt)