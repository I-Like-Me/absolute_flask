from app import app, db
from app.models import User, Log_Entry
#from app.absolute_api import Abs_Actions

#Abs_Actions.Abs_get(keyword_type_choice="username", keyword_choice="AD%5Ccg155")
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Log_Entry': Log_Entry}