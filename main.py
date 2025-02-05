import webbrowser
import threading
import re
import bleach
import html
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import bcrypt
import sqlite3 as sql
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import userManagement as dbHandler
import diaryManagement as logHandler

database = ".databaseFiles/database.db"

app = Flask(__name__)
app.secret_key = "_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)

logging.basicConfig(filename="security_log.log", encoding="utf-8", level=logging.DEBUG,
                    format="%(asctime)s %(message)s")

logging.basicConfig(filename='failed_logins.log', level=logging.WARNING,
                    format='%(asctime)s - %(ip)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

@app.route("/index")
@app.route("/index.htm")
@app.route("/index.asp")
@app.route("/index.php")
@app.route("/index.html")

def root():
    return redirect("/", 302)

@app.route("/", methods=["GET", "POST"])
@csp_header({
    "base-uri": "'self'",
    "default-src": "'self'",
    "style-src": "'self'",
    "script-src": "'self'",
    "img-src": "'self' data:",
    "media-src": "'self'",
    "font-src": "'self'",
    "object-src": "'self'",
    "child-src": "'self'",
    "connect-src": "'self'",
    "worker-src": "'self'",
    "report-uri": "/csp_report",
    "frame-ancestors": "'none'",
    "form-action": "'self'",
    "frame-src": "'none'",
})
def index():
    return render_template("index.html")

def validate_devtag(devtag):
    return re.match(r"^[a-zA-Z0-9_]{3,20}$", devtag)

def validate_password(password):
    return len(password) >= 8 and bool(re.search(r"[A-Za-z0-9@#$%^&+=]", password))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        devtag = bleach.clean(request.form["devtag"]).strip()
        password = request.form["password"].strip()
        if not validate_devtag(devtag) or not validate_password(password):
            flash("Invalid input format.", "danger")
            return redirect(url_for("login"))
        login_result = dbHandler.checkUser(devtag, password)
        if login_result == "locked":
            flash("Too many failed attempts. Please try again later.", logging.warning(f"Locked out {request.remote_addr}"))
            return redirect(url_for("login"))
        if login_result:
            session["user"] = devtag
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", logging.warning(f"Failed login attempt from {request.remote_addr}"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        devtag = bleach.clean(request.form["devtag"]).strip()
        password = request.form["password"].strip()
        if not validate_devtag(devtag) or not validate_password(password):
            flash("Invalid input format. Ensure username is 3-20 characters (letters, numbers, _ only) and password is at least 8 characters.", logging.warning(f"Invalid input format from {request.remote_addr}"))
            return redirect(url_for("signup"))

        if dbHandler.addUser(devtag, password):
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("User already exists", "danger")
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=html.escape(session["user"]))

class DiaryEntryForm(FlaskForm):
    devtag = StringField('Devtag', validators=[DataRequired(), Length(min=3, max=20)])
    project = StringField('Project', validators=[DataRequired(), Length(min=2, max=50)])
    repo = StringField('Repo', validators=[DataRequired(), Length(min=2, max=100)])
    starttime = StringField('Start Time', validators=[DataRequired(), Length(min=5, max=20)])
    endtime = StringField('End Time', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Submit')

@app.route("/form", methods=["GET", "POST"])
def insertEntry():
    if "user" not in session:
        return redirect(url_for("login"))
    form = DiaryEntryForm()
    if form.validate_on_submit():
        devtag = bleach.clean(form.devtag.data.strip())
        project = bleach.clean(form.project.data.strip())
        repo = bleach.clean(form.repo.data.strip())
        starttime = bleach.clean(form.starttime.data.strip())
        endtime = bleach.clean(form.endtime.data.strip())
        logHandler.new_entry(devtag, project, repo, starttime, endtime)
        flash("Entry added successfully", "success")
        return redirect(url_for("showEntry"))
    flash("Please fill in all fields", logging.warning(f"Empty fields from {request.remote_addr}"))
    return render_template("form.html", form=form)

@app.route("/entries", methods=["GET"])
def showEntry():
    if "user" not in session:
        return redirect(url_for("login"))
    entries = logHandler.entries()
    return render_template("entries.html", entries=entries)

@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("index"))

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
    app.run(debug=True)
