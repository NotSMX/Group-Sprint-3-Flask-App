from flask import Flask, render_template, send_from_directory, request
from views import main_blueprint
from flask_login import current_user, login_required, LoginManager
from models import db, User, Submission, Session, Room

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clas_app.db'
app.config["SECRET_KEY"] = "dev"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(main_blueprint)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/submission', methods=['POST'])
@login_required
def create_submission():
    clas_type = request.form['clas_type']
    format = request.form['format']
    department = request.form['department']
    course_number = request.form['course_number']
    course_title = request.form['course_title']
    num_entries = request.form.get('num_entries', type=int)
    num_students = request.form.get('num_students', type=int)
    session_title = request.form['session_title']
    session_length = request.form['session_length']
    individual_entry_length = request.form['individual_entry_length']
    room_request = request.form.get('room_request', '')
    special_request = request.form.get('special_request', '')

    new_submission = Submission(
        user_id=current_user.id,
        clas_type=clas_type,
        format=format,
        department=department,
        course_number=course_number,
        course_title=course_title,
        num_entries=num_entries,
        num_students=num_students,
        session_title=session_title,
        session_length=session_length,
        individual_entry_length=individual_entry_length,
        room_request=room_request,
        special_request=special_request
    )

    db.session.add(new_submission)
    db.session.commit()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

