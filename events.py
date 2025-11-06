from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Event, Session
from datetime import time

events_blueprint = Blueprint('events', __name__)

@events_blueprint.route('/eventcreate', methods=['GET'])
@login_required
def eventcreate():
    return render_template('eventcreate.html', user=current_user)

@events_blueprint.route('/eventcreate', methods=['POST'])
@login_required
def create_event():
    # Collect form data
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

    new_event = Event(
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
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('events.eventlist'))

@events_blueprint.route('/eventlist', methods=['GET'])
@login_required
def eventlist():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('eventlist.html', user=current_user, events=events)

@events_blueprint.route('/event/submit/<int:event_id>', methods=['POST'])
@login_required
def submit_event(event_id):
    event = Event.query.get_or_404(event_id)

    existing_session = Session.query.filter_by(submission_id=event.id).first()
    if existing_session:
        flash(f'Event "{event.session_title}" has already been submitted.', 'info')
        return redirect(url_for('events.eventlist'))

    new_session = Session(
        user_id=current_user.id,
        submission_id=event.id,
        room_id=1,
        start_time=time(0, 0),
        end_time=time(1, 0)
    )
    db.session.add(new_session)
    db.session.commit()

    flash(f'Event "{event.session_title}" submitted successfully!', 'success')
    return redirect(url_for('events.eventlist'))
