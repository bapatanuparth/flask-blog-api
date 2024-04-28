import jwt
import datetime
from flask import current_app
from app.models.token import Token  # Import the Token model
from flask import request, jsonify
from functools import wraps
from app.extensions import mongo

def generate_token(user_id):
    """
    Generate a JWT token and save it to the database using the Token model.
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Token expires in 1 day
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_id)
        }
        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],  
            algorithm='HS256'
        )
       
        if Token(user_id=user_id, token=token, expires=payload['exp']).save():
            return token
        else:
            return None
    except Exception as e:
        return None

def extract_token_from_header(auth_header):
    """
    Clean the header to extract token
    """
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header[7:]  # Skip the first 7 characters to get rid of "Bearer "
    return None

def verify_token(token):
    """
    Verify the provided JWT token and check its validity against the database.
    """
    try:
        token_data = Token.find_by_token(token)
        if not token_data:
            return {'status': 'error', 'message': 'Token not found'}
        if token_data['expires'] < datetime.datetime.utcnow():
            Token.delete(token)
            return {'status': 'error', 'message': 'Token has expired'}
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        print(payload)
        return {'status': 'success', 'message': 'Token is valid', 'user_id': payload['sub']}
    except jwt.ExpiredSignatureError:
        Token.delete(token)  
        return {'status': 'error', 'message': 'Token has expired (JWT check)'}
    except jwt.InvalidTokenError:
        return {'status': 'error', 'message': 'Invalid token'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def delete_token(auth_token):
    token = extract_token_from_header(auth_token)
    result = mongo.db.tokens.delete_one({'token': token})
    if result.deleted_count > 0:
        return {'status': 'success', 'message': 'Successfully logged out'}
    else:
        return {'status': 'error', 'message': 'Invalid or expired token, logout failed'}


def token_required(f):
    """
    Decorator to verify the token before proceeding with the request
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        token = extract_token_from_header(token)
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        verification_result = verify_token(token)
        
        if verification_result['status'] == 'error':
            return jsonify({'error': verification_result['message']}), 401 if verification_result['message'] == 'Invalid token' else 403
        request.user_id = verification_result.get('user_id', None)
        return f(*args, **kwargs)
    return decorated_function