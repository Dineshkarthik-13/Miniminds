from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/ping')
def ping():
    return {'message': 'pong'}
