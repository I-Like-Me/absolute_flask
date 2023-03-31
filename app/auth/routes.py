from flask import render_template, redirect, url_for, request, session
from app import db, Config
from app.auth import bp
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from duo_universal.client import Client, DuoException
import traceback

duo_client = Client(Config.client_id, Config.client_secret, Config.api_host, Config.redirect_uri)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        try:
            duo_client.health_check()
        except DuoException:
            traceback.print_exc()
            if Config.duo_failmode.upper() == "OPEN":
                return render_template("auth/login.html", message="Login 'Successful', 2FA Not Performed.")
            else:
                return render_template("auth/login.html", message="2FA Unavailable.")
        state = duo_client.generate_state()
        session['state'] = state
        session['username'] = username
        prompt_uri = duo_client.create_auth_url(username, state)
        return redirect(prompt_uri)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route("/duo-callback", methods=['GET', 'POST'])
def duo_callback():
    state = request.args.get('state')
    form = LoginForm()
    if 'state' in session and 'username' in session:
        saved_state = session['state']
        username = session['username']
    else:
        return render_template("auth/login.html", message="No saved state", title='Login', form=form)
    if state != saved_state:
        return render_template("auth/login.html", message="Duo state != saved state", title='Login', form=form)
    user = User.query.filter_by(username=username).first()
    login_user(user)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('main.index')
    return redirect(next_page)

@bp.route('/logout')
def logout():
    my_requests = current_user.get_my_requests()
    for request in my_requests:
        db.session.delete(request)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.index'))