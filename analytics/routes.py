from . import analytics_bp
import decorators
from flask import render_template


@analytics_bp.route('/marketplace', methods=['GET'])
@decorators.user_login_checker
@decorators.handle_errors
def index():
    return render_template('index.html')
