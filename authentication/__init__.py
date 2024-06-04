from flask import Blueprint

auth_bp = Blueprint('authentication', __name__)

from . import routes
