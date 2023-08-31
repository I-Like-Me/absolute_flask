from flask_wtf import FlaskForm
from wtforms import SelectField

# SelectFeild used for Version Checker.
class AppVerForm(FlaskForm):
    app = SelectField('Application', choices=[])
    version = SelectField('Version', choices=[])
    operator = SelectField('Comparison Operator', choices=["is", "not", "less than", "greater than", "is or less than", "is or greater than"])
   
