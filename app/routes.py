from flask import Flask, Blueprint, render_template, redirect, url_for
import os
from app.forms import AppointmentForm
import psycopg2
from datetime import datetime, timedelta


bp = Blueprint("main", __name__, "/")

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}

@bp.route("/<int:year>/<int:month>/<int:day>")
def daily(year,month,day, methods=['GET','POST']):
    day = datetime(year,month,day)
    next_day = day+ timedelta(days=1)
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
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute(
                "SELECT id, name, start_datetime, end_datetime FROM appointments WHERE start_datetime BETWEEN %(day)s AND %(next_day)s ORDER BY start_datetime;",{'day':day,'next_day':next_day})
            rows = curs.fetchall()
    return render_template('main.html', rows=rows, form=form)


@bp.route("/", methods=['GET', 'POST'])
def main_page():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))
