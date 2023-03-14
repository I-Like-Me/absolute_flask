from flask import render_template, flash, redirect, url_for, request
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RequestForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Log_Entry
from app.absolute_api import Abs_Actions


@app.route('/')
@app.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', actions=actions)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    form = RequestForm()
    if form.validate_on_submit():
        results = Abs_Actions.Abs_get(keyword_choice=form.keyword.data, keyword_type_choice=form.types.data)
        if results['data'] == []: 
            flash('Try different keyword.')
            return redirect(url_for('requests'))
        flash(f'{results["data"][0][f"{form.types.data}"]}')
        flash(f'{results}')
        #'username'
        #'systemModel'
        #'serialNumber'
        #flash(f'You search {form.keyword.data} as a {form.types.data}.')
    return render_template('requests.html', title='Requests', form=form, results=results)
    