from . import pos_bp
import decorators
from flask import render_template


@pos_bp.route('/pos', methods=['GET'])
@decorators.user_login_checker
@decorators.handle_errors
def pos():
    return render_template('pos.html')

