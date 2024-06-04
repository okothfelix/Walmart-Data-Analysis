from . import auth_bp
import decorators
from flask import render_template, request, session, redirect, url_for
import authentication


@auth_bp.route('/', methods=['GET', 'POST'])
@decorators.user_login_checker
@decorators.handle_errors
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result_set = authentication.user_login(username, password)
        if result_set:
            session['logged_in'] = True
            return redirect(url_for('analytics.dashboard'))
        return render_template('authentication/index.html')
    else:
        return render_template('authentication/index.html')



