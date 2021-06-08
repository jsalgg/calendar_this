from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField
)
from wtforms.widgets.html5 import DateInput, TimeInput
from wtforms.validators import DataRequired


class AppointmentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[
                           DataRequired()], widget=DateInput())
    start_time = TimeField("Start Time", validators=[
                           DataRequired()], widget=TimeInput())
    end_date = DateField("End Date", validators=[
                         DataRequired()], widget=DateInput())
    end_time = TimeField("End Time", validators=[
                         DataRequired()], widget=TimeInput())
    description = TextAreaField('Description', validators=[DataRequired()])
    private = BooleanField('Private')
    submit = SubmitField("Submit")
