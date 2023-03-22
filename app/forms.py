from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RequestForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    types = RadioField('Keyword Type', choices=[('deviceName','device name'),('username','user name'),('serialNumber','serial number')], default='deviceName')
    submit = SubmitField('Search')