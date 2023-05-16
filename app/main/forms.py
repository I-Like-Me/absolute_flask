from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired

class RequestForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    types = RadioField('Keyword Type', choices=[('deviceName','device name'),('username','user name'),('serialNumber','serial number')], default='deviceName')
    submit = SubmitField('Search')

class SpaceForm(FlaskForm):
    sort = SelectField('Sort By', choices=["Name: A to Z", "Name: Z to A", "Size: High to Low", "Size: Low to High"])

class AppVerForm(FlaskForm):
    app = SelectField('Application', choices=[])
    version = SelectField('Version', choices=[])
    operator = SelectField('Comparison Operator', choices=["is", "not", "less than", "greater than", "is not", "is or less than", "is or greater than"])
   
