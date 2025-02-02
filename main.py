import webbrowser
import threading
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
<<<<<<< HEAD
import bcrypt
=======
>>>>>>> 70add9764a6100db9b4b6602f1acc04963d29da6
import userManagement as dbHandler

app = Flask(__name__)
app.secret_key = "_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)

logging.basicConfig(filename="security_log.log", encoding="utf-8", level=logging.DEBUG,
                    format="%(asctime)s %(message)s")

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        devtag = request.form["devtag"]
        password = request.form["password"]
        if dbHandler.checkUser(devtag, password):
            session["user"] = devtag
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        devtag = request.form["devtag"]
        password = request.form["password"]
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
    return render_template("dashboard.html", user=session["user"])

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
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)
