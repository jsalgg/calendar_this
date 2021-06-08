from flask import Flask, Blueprint, render_template
import os
from app.forms import AppointmentForm
import psycopg2


bp = Blueprint("main", __name__, "/")

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}


@bp.route("/")
def main_page():
    form = AppointmentForm()
    print(form)
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute(
                "SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;")
            rows = curs.fetchall()
            print("*************", rows)
    return render_template('main.html', rows=rows, form=form)
