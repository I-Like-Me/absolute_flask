from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Cass'}
    actions = [
        {
            'tech': {'username': 'Steve'},
            'details': 'Ran computer name check.'
        },
        {
            'tech': {'username': 'Christian'},
            'details': 'Ran netID check.'
        }
    ]
    return render_template('index.html', title='Home', user=user, actions=actions)