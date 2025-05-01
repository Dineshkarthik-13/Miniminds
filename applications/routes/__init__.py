from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
datasets_bp = Blueprint('datasets', __name__, url_prefix='/datasets')
competitions_bp = Blueprint('competitions', __name__, url_prefix='/competitions')


