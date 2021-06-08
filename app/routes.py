from flask import Flask, Blueprint, render_template, redirect
import os
from app.forms import AppointmentForm
import psycopg2
from datetime import datetime


bp = Blueprint("main", __name__, "/")

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}


@bp.route("/", methods=['GET', 'POST'])
def main_page():
    form = AppointmentForm()
    # print(form)
    if form.validate_on_submit():
        new_appt = {
            'name': form.data['name'],
            'start_datetime': datetime.combine(form.data['start_date'], form.data['start_time']),
            'end_datetime':  datetime.combine(form.data['end_date'], form.data['end_time']),
            'description': form.data['description'],
            'private': form.data['private']
        }
        with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
                    VALUES 
                    (%(name)s, %(start_datetime)s , %(end_datetime)s, %(description)s, %(private)s );""", new_appt)

        return redirect('/')

    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute(
                "SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;")
            rows = curs.fetchall()
            # print("*************", rows)
    return render_template('main.html', rows=rows, form=form)
# (%(new_appt[name])s, %(new_appt.start_date)s %(new_appt.start_time)s, %(new_appt.end_date)s %(new_appt.end_time)s, %(new_appt.description)s, %(new_appt.private)s );""", new_appt)
