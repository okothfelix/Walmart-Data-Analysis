from . import analytics_bp
import decorators
from flask import render_template, request, redirect, url_for, session
import generators
import analytics_backend


@analytics_bp.route('/dashboard', methods=['GET'])
@decorators.user_login_checker
@decorators.handle_errors
def index():
    return render_template('index.html')


@analytics_bp.route('/sales', methods=['GET'])
@decorators.user_login_checker
@decorators.handle_errors
def sales():
    return render_template('analytics/sales.html')


@analytics_bp.route('/product-list', methods=['GET'])
@decorators.user_login_checker
@decorators.handle_errors
def product_list():
    return render_template('analytics/product-list.html')


@analytics_bp.route('/profile', methods=['GET', 'POST'])
@decorators.user_login_checker
@decorators.handle_errors
def profile():
    cur_user = generators.cur_user_details(session['analytics_id'])
    if request.method == 'POST':
        f_name = request.form['first-name']
        l_name = request.form['last-name']
        email = request.form['address']
        number = generators.phone_num_checker(request.form['phone-number'])
        analytics_backend.user_profile_section('POST', cur_user[2], f_name, l_name, email, number)
        session['update-flag'] = True
        return redirect(url_for('analytics.profile'))
    else:
        result_set = analytics_backend.user_profile_section('GET', cur_user[2])
        update_flag = None
        if 'update-flag' in session:
            update_flag = session['update-flag']
            session.pop('update-flag')
        return render_template('analytics/profile.html', admin_name=cur_user[0], admin_details=result_set, update_flag=update_flag)


@analytics_bp.route('/profile/password-update', methods=['POST'])
@decorators.user_login_checker
@decorators.handle_errors
def password_update():
    return redirect(url_for('analytics.profile'))
