from . import auth_bp
import decorators
from flask import render_template, request, session, redirect, url_for
import auth_backend


@auth_bp.route('/', methods=['GET', 'POST'])
@decorators.user_login_checker
@decorators.handle_errors
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result_set = auth_backend.user_login(username, password)
        if result_set:
            session['logged_in'] = True
            return redirect(url_for('analytics.dashboard'))
        return render_template('authentication/index.html')
    else:
        return render_template('authentication/index.html')


@auth_bp.route('/', methods=['GET', 'POST'])
@decorators.user_login_checker
@decorators.handle_errors
def session_update():
    if request.method == 'POST':
        password = request.form['password']
        result_set = auth_backend.session_update_section(password)
    else:
        return render_template('session-update.html')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    # clear everything from session except for the session id and update the user type to 100
    auth_backend.user_logout(session['bms_id'])
    session.clear()
    return redirect(url_for('authentication.login'))
