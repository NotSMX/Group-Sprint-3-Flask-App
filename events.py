from flask import Blueprint, request, render_template, flash, redirect, url_for, request
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

    action = request.form.get('action')
    status = 'submitted' if action == 'submit' else 'draft'

    if status == 'submitted':
        required_fields = [
            clas_type, format, department, course_number, course_title,
            session_title, session_length, individual_entry_length
        ]
        if any(f is None or f == '' for f in required_fields):
                flash("All fields must be filled to submit the event. Please double check you have filled out all the required fields. Or, you can save this as a draft and come back to it later.")
                return redirect(url_for('events.eventcreate'))

    # Create and save event
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
        special_request=special_request,
        status=status
    )

    db.session.add(new_event)
    db.session.commit()
    if status == 'draft':
        flash(f'Draft "{session_title}" saved successfully!')
    else:
        flash(f'Event "{session_title}" submitted successfully!')
    return redirect(url_for('events.eventlist'))  # Redirect to list after creating

@events_blueprint.route('/eventlist', methods=['GET'])
@login_required
def eventlist():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('eventlist.html', user=current_user, events=events)

@events_blueprint.route('/event/submit/<int:event_id>', methods=['POST'])
@login_required
def submit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if session already exists for this event
    if event.status == 'submitted':
        flash(f'Event "{event.session_title}" has already been submitted.')
        return redirect(url_for('events.eventlist'))
    
    required_fields = [
        event.clas_type, event.format, event.department, event.course_number,
        event.course_title, event.num_entries, event.num_students,
        event.session_title, event.session_length, event.individual_entry_length
    ]
    if any(f is None or f == '' for f in required_fields):
        flash("All fields must be filled to submit the event. Please double check you have filled out all the required fields. Or, you can save this as a draft and come back to it later.")
        return render_template('eventedit.html', user=current_user, event=event)

    event.status = 'submitted'
    db.session.commit()
    
    flash(f'Event "{event.session_title}" submitted successfully!')
    return redirect(url_for('events.eventlist'))

@events_blueprint.route('/event/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        flash("You don't have permission to edit this event.")
        return redirect(url_for('events.eventlist'))

    if request.method == 'POST':
        action = request.form.get('action')

        event.clas_type = request.form.get('clas_type', event.clas_type)
        event.format = request.form.get('format', event.format)
        event.department = request.form.get('department', event.department)
        event.course_number = request.form.get('course_number', event.course_number)
        event.course_title = request.form.get('course_title', event.course_title)
        event.num_entries = request.form.get('num_entries', type=int) or event.num_entries
        event.num_students = request.form.get('num_students', type=int) or event.num_students
        event.session_title = request.form.get('session_title', event.session_title)
        event.session_length = request.form.get('session_length', event.session_length)
        event.individual_entry_length = request.form.get('individual_entry_length', event.individual_entry_length)
        event.room_request = request.form.get('room_request', event.room_request)
        event.special_request = request.form.get('special_request', event.special_request)

        if action == 'draft':
            event.status = 'draft'
            db.session.commit()
            flash(f'Draft "{event.session_title}" saved successfully!')
            return redirect(url_for('events.eventlist'))

        if action == 'submit':
            required_fields = [
                event.clas_type, event.format, event.department, event.course_number,
                event.course_title, event.num_entries, event.num_students,
                event.session_title, event.session_length, event.individual_entry_length
            ]
            if any(f is None or f == '' for f in required_fields):
                flash("All fields must be filled to submit the event. Please double check you have filled out all the required fields. Or, you can save this as a draft and come back to it later.")
                return render_template('eventedit.html', user=current_user, event=event)

            event.status = 'submitted'
            db.session.commit()
            flash(f'Event "{event.session_title}" submitted successfully!')
            return redirect(url_for('events.eventlist'))

    return render_template('eventedit.html', user=current_user, event=event)


@events_blueprint.route('/event/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        flash("You don't have permission to delete this event.")
        return redirect(url_for('events.eventlist'))

    db.session.delete(event)
    db.session.commit()
    flash(f'Event "{event.session_title}" deleted successfully!')
    return redirect(url_for('events.eventlist'))