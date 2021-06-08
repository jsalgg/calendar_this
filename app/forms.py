from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField
)
from wtforms.widgets.html5 import DateInput, TimeInput
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

def validate_end_date(form,field):
        end = datetime.combine(field.data,form.end_time.data)
        start = datetime.combine(form.start_date.data,form.start_time.data)
        if start.date != end.date and start.time >= end.time:
            print('END DATE ERROR')
            msg = " Start and end date must be the same day and end time must come after start time"
            raise ValidationError(msg)

class AppointmentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[
                           DataRequired()], widget=DateInput())
    start_time = TimeField("Start Time", validators=[
                           DataRequired()], widget=TimeInput())
    end_date = DateField("End Date", validators=[
                         DataRequired(),validate_end_date], widget=DateInput())
    end_time = TimeField("End Time", validators=[
                         DataRequired()], widget=TimeInput())
    description = TextAreaField('Description', validators=[DataRequired()])
    private = BooleanField('Private')
    submit = SubmitField("Submit")
