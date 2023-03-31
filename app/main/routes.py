from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.main.forms import RequestForm
from flask_login import current_user, login_required
from app.models import User, Log_Entry, Request
from app.main.absolute_api import Abs_Actions
from app.main import bp


@bp.route('/')
@bp.route('/index')
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

@bp.route('/requests', methods=['GET', 'POST'])
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
            return redirect(url_for('main.requests'))
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
        return redirect(url_for('main.requests'))
    page = request.args.get('page', 1, type=int)
    my_requests = current_user.get_my_requests().paginate(page=page, per_page=current_app.config['RESULTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.requests', page=my_requests.next_num) \
        if my_requests.has_next else None
    prev_url = url_for('main.requests', page=my_requests.prev_num) \
        if my_requests.has_prev else None
    return render_template('requests.html', title='Requests', form=form, my_requests=my_requests.items, next_url=next_url, prev_url=prev_url)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)