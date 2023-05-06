from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from app import db
from app.main.forms import RequestForm, AppVerForm
from flask_login import current_user, login_required
from app.models import User, App, Version
from app.main.absolute_api import Abs_Actions
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Workbench')


@bp.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    form = RequestForm()
    device_results = Abs_Actions.abs_device_get(keyword_choice=request.args.get('s_keyword'), keyword_type_choice=request.args.get('s_type'))
    app_results = Abs_Actions.abs_app_get(keyword_choice=request.args.get('s_keyword'))
    results_dict = Abs_Actions.prepare_data(device_results, app_results)
    if form.validate_on_submit():
        if form.types.data == 'username':
            form.keyword.data = "AD%5C" + form.keyword.data
        results = Abs_Actions.abs_device_get(keyword_choice=form.keyword.data, keyword_type_choice=form.types.data)
        if results['data'] == []: 
            flash('Try different keyword.')
            return redirect(url_for('main.requests'))
        return redirect(url_for('main.requests', s_type=f"{form.types.data}", s_keyword=f"{form.keyword.data}"))
    return render_template('requests.html', title='Requests', form=form, device_results=device_results, results_dict=results_dict, app_results=app_results, s_type=request.args.get('s_type'), s_keyword=request.args.get('s_keyword'))

@bp.route('/space_check', methods=['GET', 'POST'])
@login_required
def space_check():
    full_device_dict = Abs_Actions.abs_all_devices("pageSize=500&agentStatus=A")
    space_dict = Abs_Actions.build_space_list(full_device_dict)
    return render_template('space_check.html', title='Space Checker', full_device_dict=full_device_dict, space_dict=space_dict)

@bp.route('/version_check', methods=['GET', 'POST'])
@login_required
def version_check():
    appverforms = AppVerForm()
    appverforms.app.choices = [(app.id, app.name)for app in App.query.all()]
    appverforms.version.choices = [(version.id, version.key)for version in Version.query.filter_by(app_id='1').all()]
    
    if request.method == 'POST':
        version = Version.query.filter_by(id=appverforms.version.data).first()
        return f'<h1>App: {appverforms.app.data}, Version: {version.key}</h1>'

    return render_template('version_check.html', title='Version Checker', appverforms=appverforms)

@bp.route('/version_check/version/<app>')
def version(app):
    versions = Version.query.filter_by(app_id=app).all()
    
    versionList = []

    for version in versions:
        versionObj = {}
        versionObj['id'] = version.id
        versionObj['key'] = version.key
        versionList.append(versionObj)
    
    return jsonify({'versions' : versionList})

@bp.route('/graphs', methods=['GET', 'POST'])
@login_required
def graphs():
    
    return render_template('graphs.html', title='Graphs')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)