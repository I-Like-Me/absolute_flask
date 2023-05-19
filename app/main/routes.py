from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, session
from app import db
from app.main.forms import RequestForm, AppVerForm
from flask_login import current_user, login_required
from app.models import User, App, Version
from app.main.absolute_api import Abs_Actions
from app.main.tool_box import Jsonizers, Dict_Builder, Translators as Tlr
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
    results_dict = Dict_Builder.build_machine_dict(device_results, app_results)
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
    return render_template('space_check.html', title='Space Checker')

@bp.route('/space/data')
def space_data():
    full_device_dict = Abs_Actions.abs_all_devices("pageSize=500&agentStatus=A")
    space_dict = Dict_Builder.build_space_dict(full_device_dict)
    return {'data': [Jsonizers.space_json(key, value) for key, value in space_dict.items()]}

@bp.route('/version_check', methods=['GET', 'POST'])
@login_required
def version_check():
    appverforms = AppVerForm()
    appverforms.app.choices = [(app.id, app.name)for app in App.query.all()]
    appverforms.version.choices = [(version.id, version.key)for version in Version.query.filter_by(app_id='1').all()]
    clean_version_dict = None
    if request.method == 'POST':
        chosen_version = Version.query.filter_by(id=appverforms.version.data).first()
        chosen_app = App.query.filter_by(id=appverforms.app.data).first()
        app_data_all = Abs_Actions.app_version_get(Tlr.app_select_tlr(chosen_app.name)[0], Tlr.app_select_tlr(chosen_app.name)[1])
        clean_version_dict = Dict_Builder.build_version_dict(chosen_app.name, app_data_all)
        return render_template('version_check.html', title='Version Checker', appverforms=appverforms, clean_version_dict=clean_version_dict)
    return render_template('version_check.html', title='Version Checker', appverforms=appverforms, clean_version_dict=clean_version_dict)

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

@bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    
    return render_template('feedback.html', title='Feedback')