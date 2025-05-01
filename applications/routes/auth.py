from flask import Blueprint, request, jsonify
from applications.firebase_auth import auth_required, get_current_user

# Rename the blueprint name from 'auth' to 'auth_bp'
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if 'idToken' not in data:
        return jsonify({"error": "Missing ID token"}), 400

    return jsonify({"success": True}), 200

@auth_bp.route('/user', methods=['GET'])
@auth_required
def get_user():
    current_user = get_current_user()
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "name": current_user.name,
        "is_admin": current_user.is_admin
    })
