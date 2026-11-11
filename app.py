import os
from flask import Flask, render_template, request, redirect, url_for
from cs50 import SQL
from werkzeug.utils import secure_filename


app = Flask(__name__)


db = SQL("sqlite:///employees.db")


db_folder = 'databases'
allowed_extensions = {'db'}
app.config['db_folder'] = db_folder


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


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


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file.filename == '':
        return redirect("/")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        os.makedirs(app.config['db_folder'], exist_ok=True)
        
        file.save(os.path.join(app.config['db_folder'], filename))

        db = SQL(f"sqlite:///databases/{filename}")
        
        return redirect("/")
    
    return redirect("/")