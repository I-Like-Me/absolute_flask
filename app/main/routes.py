from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from app import db
from app.main.forms import RequestForm, AppVerForm
from flask_login import current_user, login_required
from app.models import User, App, Version
from app.main.absolute_api import Abs_Actions
from app.main.tool_box import Jsonizers, Dict_Builder, MDG, Data_fillers, List_builders, Translators as Tlr
from app.main.d3_tools import Pie_Tool, Bar_Tool
from app.main import bp
import pandas as pd

data_df = pd.read_csv("app/static/data/test_data.csv")
viz_data_df = data_df[(data_df['Churn']=="Yes").notnull()] 

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
    bitkey = Abs_Actions.abs_device_bitkey(device_results['data'][0]['deviceUid'])
    results_dict = Dict_Builder.build_machine_dict(device_results, app_results, bitkey)
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

@bp.route('/graphs', methods=['GET', 'POST'])
@login_required
def graphs():
    #full_device_dict = Abs_Actions.abs_device_get('deviceName', 'MC214DW20')
    full_device_dict = Abs_Actions.abs_all_devices("pageSize=500&select=deviceName,localIp,volumes,espInfo.encryptionStatus,systemManufacturer,operatingSystem&agentStatus=A")
    raw_citrix_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'receiver' or appNameContains eq 'workspace')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A")
    raw_zoom_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Zoom')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A")
    raw_cortex_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Cortex')&select=deviceName&pageSize=500&agentStatus=A")
    raw_insightvm_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Rapid7')&select=deviceName&pageSize=500&agentStatus=A")    
    all_device_dicts = Data_fillers.fill_device_series(full_device_dict, raw_citrix_data, raw_zoom_data, raw_cortex_data, raw_insightvm_data)
    all_dept_dicts = Data_fillers.fill_dept_series(all_device_dicts)
    return render_template('graphs.html', title='Graphs', all_device_dicts=all_device_dicts, full_device_dict=full_device_dict)

@bp.route('/get_piechart_data')
def get_piechart_data():
    piechart_data = Pie_Tool.piechart_data(viz_data_df)
    return jsonify(piechart_data)

@bp.route('/get_barchart_data')
def get_barchart_data():
    barchart_data = Bar_Tool.barchart_data(viz_data_df)
    return jsonify(barchart_data)