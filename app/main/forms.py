from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
from app.models import User

class RequestForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    types = RadioField('Keyword Type', choices=[('deviceName','device name'),('username','user name'),('serialNumber','serial number')], default='deviceName')
    submit = SubmitField('Search')