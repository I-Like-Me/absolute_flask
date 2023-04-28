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
    all_logs = Log_Entry.query.all()
    return render_template('index.html', title='Home', all_logs=all_logs)


@bp.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    form = RequestForm()
    device_results = Abs_Actions.abs_device_get(keyword_choice=request.args.get('s_keyword'), keyword_type_choice=request.args.get('s_type'))
    app_results = Abs_Actions.abs_app_get(keyword_choice=request.args.get('s_keyword'))
    results_dict = Abs_Actions.prepare_data(device_results, app_results)
    if form.validate_on_submit():
        raw_keyword = form.keyword.data
        if form.types.data == 'username':
            form.keyword.data = "AD%5C" + form.keyword.data
        results = Abs_Actions.abs_device_get(keyword_choice=form.keyword.data, keyword_type_choice=form.types.data)
        if results['data'] == []: 
            flash('Try different keyword.')
            return redirect(url_for('main.requests'))
        Log_Entry.record_action(tech_name=current_user, a_type=form.types.data, a_keyword=raw_keyword)
        return redirect(url_for('main.requests', s_type=f"{form.types.data}", s_keyword=f"{form.keyword.data}"))
    return render_template('requests.html', title='Requests', form=form, device_results=device_results, results_dict=results_dict, app_results=app_results, s_type=request.args.get('s_type'), s_keyword=request.args.get('s_keyword'))

@bp.route('/space_check', methods=['GET', 'POST'])
@login_required
def space_check():
    full_device_dict = Abs_Actions.abs_all_devices()
    space_dict = Abs_Actions.build_space_list(full_device_dict)
    return render_template('space_check.html', title='Space Checker', full_device_dict=full_device_dict, space_dict=space_dict)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)