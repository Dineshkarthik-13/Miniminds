import os
import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
from flask import request, jsonify, g, current_app
from applications.models import User
from applications import db

# Initialize Firebase Admin SDK
cred_path = cred_path = "D:\\iit madras\\mad-i-project\\Miniminds\\firebase_key.json"


if os.path.exists(cred_path):
    try:
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
else:
    print(f"Firebase credentials not found at {cred_path}.")


def get_current_user():
    """Get current user from the request"""
    return getattr(g, 'user', None)

def verify_firebase_token(id_token):
    """Verify Firebase ID token and return user information"""
    try:
        if not firebase_app:
            return None
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        current_app.logger.error(f"Error verifying Firebase token: {e}")
        return None

def auth_required(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid authorization header"}), 401

        id_token = auth_header.split('Bearer ')[1]
        user_info = verify_firebase_token(id_token)

        if not user_info:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Check if user exists
        user = User.query.filter_by(firebase_uid=user_info['uid']).first()

        if not user:
            # Create a new user
            email = user_info.get('email', '')
            name = user_info.get('name', '')
            username = email.split('@')[0] if email else f"user_{user_info['uid'][:8]}"

            user = User(
                username=username,
                email=email,
                name=name,
                firebase_uid=user_info['uid']
            )
            db.session.add(user)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Error creating user: {e}")
                return jsonify({"error": "Failed to create user account"}), 500

        g.user = user
        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    """Decorator for routes that require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        if not getattr(user, 'is_admin', False):
            return jsonify({"error": "Admin privileges required"}), 403
        return f(*args, **kwargs)
    return decorated_function
