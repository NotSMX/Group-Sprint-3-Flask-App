from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return render_template('base.html')

@main_blueprint.route('/login')
def login():
    return render_template('login.html')

@main_blueprint.route('/register')
def register():
    return render_template('register.html')

