from flask import Blueprint

pos_bp = Blueprint('pos', __name__)

from . import routes
