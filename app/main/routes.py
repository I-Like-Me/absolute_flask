from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.main.forms import RequestForm
from flask_login import current_user, login_required
from app.models import User, Log_Entry
from app.main.absolute_api import Abs_Actions
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    form = RequestForm()
    results = Abs_Actions.Abs_get(keyword_choice=request.args.get('s_keyword'), keyword_type_choice=request.args.get('s_type'))
    if form.validate_on_submit():
        if form.types.data == 'username':
            form.keyword.data = "AD%5C" + form.keyword.data
        results = Abs_Actions.Abs_get(keyword_choice=form.keyword.data, keyword_type_choice=form.types.data)
        if results['data'] == []: 
            flash('Try different keyword.')
            return redirect(url_for('main.requests'))
        return redirect(url_for('main.requests', s_type=f"{form.types.data}", s_keyword=f"{form.keyword.data}"))
    return render_template('requests.html', title='Requests', form=form, results=results, s_type=request.args.get('s_type'), s_keyword=request.args.get('s_keyword'))

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)