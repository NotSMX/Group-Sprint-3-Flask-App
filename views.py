from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

main_blueprint = Blueprint('main', __name__)

@main_blueprint.get("/")
def landing():
    return render_template("base.html")

@main_blueprint.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.home"))
        else:
            flash("Invalid email or password.", "error")
            return render_template("login.html"), 401

    return render_template("login.html")

@main_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = (request.form.get("user") or "").strip()
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""
        role = (request.form.get("role") or "").strip()

        if not user or not email or not password or not role:
            flash("Please fill in all fields.", "error")
            return render_template("register.html"), 400

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
            return render_template("register.html"), 400

        new_user = User(name=user, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")

@main_blueprint.get("/schedule")
@login_required
def schedule():
    return render_template("schedule.html", user=current_user)

# Profile
@main_blueprint.get("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

# Settings
@main_blueprint.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        role = (request.form.get("role") or "").strip()
        photo = (request.form.get("profile_pic_url") or "").strip()
        new_password = request.form.get("new_password") or ""
        confirm_password = request.form.get("confirm_password") or ""

        if name:
            current_user.name = name
        if role:
            current_user.role = role
        if photo:
            current_user.profile_pic_url = photo

        if new_password or confirm_password:
            if new_password != confirm_password:
                flash("Passwords do not match.", "error")
                return render_template("settings.html", user=current_user), 400
            if len(new_password) < 6:
                flash("Password must be at least 6 characters.", "error")
                return render_template("settings.html", user=current_user), 400
            current_user.set_password(new_password)

        db.session.commit()
        flash("Settings updated.", "success")
        return redirect(url_for("main.settings"))

    return render_template("settings.html", user=current_user)

@main_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for("main.login"))
