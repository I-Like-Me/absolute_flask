from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from app.main.forms import RequestForm, AppVerForm
from flask_login import current_user, login_required
from app.models import User, App, Version
from app.main.absolute_api import Abs_Actions
from app.main.tool_box import Jsonizers, Dict_Builder, Data_fillers, Translators as Tlr
from app.main import bp
import pandas as pd
from bokeh.embed import server_document



@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Workbench')

@bp.route('/requests', methods=['GET', 'POST'])
def requests():
    return render_template('requests.html', title='Requests')

@bp.route('/requests/data')
def requests_data():
    full_device_dict = Abs_Actions.abs_all_devices("pageSize=500&agentStatus=A")
    cortex_dict = Abs_Actions.abs_all_apps("filter=(appNameContains eq 'Cortex')&select=deviceName, appName&pageSize=500&agentStatus=A")
    rapid_dict = Abs_Actions.abs_all_apps("filter=(appNameContains eq 'Rapid7')&select=deviceName, appName&pageSize=500&agentStatus=A")
    request_dict = Dict_Builder.build_request_dict(full_device_dict, cortex_dict, rapid_dict)
    return {'data': [Jsonizers.request_json(key, value) for key, value in request_dict.items()]}

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
    appverforms.version.choices = [(version.id, version.fake_key)for version in Version.query.filter_by(app_id='1').order_by(Version.fake_key.desc()).all()]
    filtered_version_dict = None
    if request.method == 'POST':
        chosen_version = Version.query.filter_by(id=appverforms.version.data).first()
        chosen_app = App.query.filter_by(id=appverforms.app.data).first()
        chosen_operator = appverforms.operator.data
        appverforms.version.choices = [(version.id, version.fake_key)for version in Version.query.filter_by(app_id=str(chosen_app.id)).order_by(Version.fake_key.desc()).all()]
        app_data_all = Abs_Actions.app_version_get(Tlr.app_select_tlr(chosen_app.name)[0], Tlr.app_select_tlr(chosen_app.name)[1])
        all_app_versions = Version.query.filter_by(app_id=chosen_app.id).all()
        clean_version_dict = Dict_Builder.build_version_dict(chosen_app, app_data_all, all_app_versions) 
        filtered_version_dict = Tlr.opt_select_tlr(chosen_operator, chosen_version, clean_version_dict)
        return render_template('version_check.html', title='Version Checker', appverforms=appverforms, filtered_version_dict=filtered_version_dict)
    return render_template('version_check.html', title='Version Checker', appverforms=appverforms, filtered_version_dict=filtered_version_dict)

@bp.route('/version_check/version/<app>')
def version(app):
    versions = Version.query.filter_by(app_id=app).order_by(Version.fake_key.desc()).all()
    versionList = []
    for version in versions:
        versionObj = {}
        versionObj['id'] = version.id
        versionObj['fake_key'] = version.fake_key
        versionList.append(versionObj)
    return jsonify({'versions' : versionList})

@bp.route('/graphs/', methods=['GET', 'POST'])
@login_required
def graphs():
    #script = server_document('http://127.0.0.1:5006/absolute_bokeh')
    script = server_document(url=r'/bokeh/absolute_bokeh', relative_urls=True)
    return render_template('graphs.html', title='Graphs', script=script, template="Flask")


