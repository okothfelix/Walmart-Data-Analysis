from . import pos_bp
import decorators
from flask import render_template


@pos_bp.route('/', methods=['GET'])
@decorators.user_login_checker
@decorators.handle_errors
def pos():
    return render_template('pos/index.html')


@pos_bp.route('/posApp', methods=['GET'])
@decorators.user_login_checker
@decorators.handle_errors
def pos_app():
    return render_template('pos/pos-app.html')


