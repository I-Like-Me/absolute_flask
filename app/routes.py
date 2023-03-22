from flask import render_template, flash, redirect, url_for, request, session
from app import app, db, Config
from werkzeug.urls import url_parse
from app.forms import LoginForm, RequestForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Log_Entry
from app.absolute_api import Abs_Actions
from duo_universal.client import Client, DuoException
import traceback
import json

duo_client = Client(Config.client_id, Config.client_secret, Config.api_host, Config.redirect_uri)

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

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')

        try:
            duo_client.health_check()
        except DuoException:
            traceback.print_exc()
            if Config.duo_failmode.upper() == "OPEN":
                return render_template("login.html",
                                   message="Login 'Successful', but 2FA Not Performed. Confirm Duo client/secret/host values are correct")
            else:
                return render_template("login.html",
                                   message="2FA Unavailable. Confirm Duo client/secret/host values are correct")


        state = duo_client.generate_state()
        session['state'] = state
        session['username'] = username
        prompt_uri = duo_client.create_auth_url(username, state)
 
        return redirect(prompt_uri)
    return render_template('login.html', title='Sign In', form=form)


@app.route("/duo-callback", methods=['GET', 'POST'])
def duo_callback():
    state = request.args.get('state')
    code = request.args.get('duo_code')
    form = LoginForm()

    if 'state' in session and 'username' in session:
        saved_state = session['state']
        username = session['username']
    else:
        return render_template("login.html", message="No saved state please login again", title='Login', form=form)
    
    if state != saved_state:
        return render_template("login.html", message="Duo state does not match saved state", title='Login', form=form)

    decoded_token = duo_client.exchange_authorization_code_for_2fa_result(code, username)
    user = User.query.filter_by(username=username).first()
    login_user(user)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    message=json.dumps(decoded_token)
    return redirect(next_page)
    #return render_template('index.html', message=json.dumps(decoded_token, indent=2, sort_keys=True))
    #return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    form = RequestForm()
    results = None
    if form.validate_on_submit():
        if form.types.data == 'username':
            form.keyword.data = "AD%5C" + form.keyword.data
        results = Abs_Actions.Abs_get(keyword_choice=form.keyword.data, keyword_type_choice=form.types.data)
        if results['data'] == []: 
            flash('Try different keyword.')
            return redirect(url_for('requests'))
    return render_template('requests.html', title='Requests', form=form, results=results)
    