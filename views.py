from flask import Blueprint, render_template, flash, redirect, url_for, request

main_blueprint = Blueprint('main', __name__)

@main_blueprint.get("/")
def landing():
    return render_template("base.html")

@main_blueprint.route('/home')
def home():
    return render_template('home.html')

@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash("logged in", "success")
        return redirect(url_for("main.home"))
    return render_template("login.html")

## still need authentication

@main_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = (request.form.get("username") or "").strip()
        p = request.form.get("password") or ""
        if not u or not p:
            flash("you need to provide a username and password!!", "error")
            return render_template("register.html"), 400
        flash("Nice! Your account has been created", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html")

## need to add user to database

@main_blueprint.get("/schedule")
def schedule():
    return render_template("schedule.html")