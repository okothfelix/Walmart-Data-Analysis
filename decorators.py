from functools import wraps
from flask import request, redirect, url_for, session
import generators
import secrets


def admin_login_checker(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'analytics_id' in session:
            result_set = generators.session_details_section(session['analytics_id'])
            if result_set[0]:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('session_update', next=request.url))
        else:
            return redirect(url_for('login', next=request.url))

    return wrap


def user_login_checker(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'analytics_id' in session:
            analytics_id = session['analytics_id']
        else:
            analytics_id = session['analytics_id'] = secrets.token_hex(10)

        result_set = generators.user_details_section(analytics_id)
        if result_set is None:
            return redirect(url_for('error_log'))
        if result_set[0] == 0:
            return redirect(url_for('user_dashboard'))
        elif result_set[0] == 3:
            return redirect(url_for('admin_dashboard'))
        else:
            return f(*args, **kwargs)

    return wrap


def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return redirect(url_for('error_log'))

    return decorated_function
