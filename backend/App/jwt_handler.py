import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps

def encode_jwt_token(user_id: int, is_admin: bool) -> str:
    with current_app.app_context():
        expiration = datetime.utcnow() + timedelta(hours=1)  # Short-lived access token
        return jwt.encode({'user_id': user_id, 'is_admin': is_admin, 'exp': expiration}, current_app.config['SECRET_KEY'], algorithm='HS256')

def encode_refresh_token(user_id: int) -> str:
    with current_app.app_context():
        expiration = datetime.utcnow() + timedelta(days=7)  # Longer-lived refresh token
        return jwt.encode({'user_id': user_id, 'exp': expiration}, current_app.config['REFRESH_SECRET_KEY'], algorithm='HS256')

def decode_jwt_token(token: str) -> dict:
    with current_app.app_context():
        try:
            return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise Exception('Access token has expired')
        except jwt.InvalidTokenError:
            raise Exception('Invalid access token')

def decode_refresh_token(token: str) -> dict:
    with current_app.app_context():
        try:
            return jwt.decode(token, current_app.config['REFRESH_SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise Exception('Refresh token has expired')
        except jwt.InvalidTokenError:
            raise Exception('Invalid refresh token')

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        
        try:
            decoded = decode_jwt_token(token)
            request.user_id = decoded['user_id']
            request.is_admin = decoded.get('is_admin', False)
        except Exception as e:
            return jsonify({"message": str(e)}), 403

        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        
        try:
            decoded = decode_jwt_token(token)
            if not decoded.get('is_admin', False):
                return jsonify({"message": "Admin access required"}), 403
        except Exception as e:
            return jsonify({"message": str(e)}), 403

        return f(*args, **kwargs)
    return decorated_function