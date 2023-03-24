from flask import render_template, flash, redirect, url_for, request, session
from app import app, db, Config
from werkzeug.urls import url_parse
from app.forms import LoginForm, RequestForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Log_Entry, Request
from app.absolute_api import Abs_Actions
from duo_universal.client import Client, DuoException
from flask_paginate import Pagination, get_page_parameter
import traceback

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
                return render_template("login.html", message="Login 'Successful', 2FA Not Performed.")
            else:
                return render_template("login.html", message="2FA Unavailable.")
        state = duo_client.generate_state()
        session['state'] = state
        session['username'] = username
        prompt_uri = duo_client.create_auth_url(username, state)
        return redirect(prompt_uri)
    return render_template('login.html', title='Sign In', form=form)

@app.route("/duo-callback", methods=['GET', 'POST'])
def duo_callback():
    state = request.args.get('state')
    form = LoginForm()
    if 'state' in session and 'username' in session:
        saved_state = session['state']
        username = session['username']
    else:
        return render_template("login.html", message="No saved state", title='Login', form=form)
    if state != saved_state:
        return render_template("login.html", message="Duo state != saved state", title='Login', form=form)
    user = User.query.filter_by(username=username).first()
    login_user(user)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return redirect(next_page)

@app.route('/logout')
def logout():
    my_requests = current_user.get_my_requests()
    for request in my_requests:
        db.session.delete(request)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))

@app.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    form = RequestForm()
    raw_keyword = form.keyword.data
    if form.validate_on_submit():
        my_requests = current_user.get_my_requests()
        for my_request in my_requests:
            db.session.delete(my_request)
        db.session.commit()
        if form.types.data == 'username':
            form.keyword.data = "AD%5C" + form.keyword.data
        results = Abs_Actions.Abs_get(keyword_choice=form.keyword.data, keyword_type_choice=form.types.data)
        form.keyword.data = raw_keyword
        if results['data'] == []: 
            flash('Try different keyword.')
            return redirect(url_for('requests'))
        for machine in results["data"]:
            device = Request(deviceName=machine["deviceName"],
                             username=machine["username"],
                             serialNumber=machine["serialNumber"],
                             localIp=machine["localIp"],
                             systemModel=machine["systemModel"],
                             systemManufacturer=machine["systemManufacturer"],
                             keyTypeUsed=form.types.data,
                             caller=current_user
                             )
            db.session.add(device)
            db.session.commit()
    page = request.args.get('page', 1, type=int)
    my_requests = current_user.get_my_requests().paginate(page=page, per_page=app.config['RESULTS_PER_PAGE'], error_out=False)
    next_url = url_for('requests', page=my_requests.next_num) \
        if my_requests.has_next else None
    prev_url = url_for('requests', page=my_requests.prev_num) \
        if my_requests.has_prev else None
    return render_template('requests.html', title='Requests', form=form, my_requests=my_requests.items, next_url=next_url, prev_url=prev_url)