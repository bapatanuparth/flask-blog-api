from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from . import auth_bp 
from bson import ObjectId
from flask import jsonify, request
import bcrypt
from app.extensions import mongo
from app.models.user import User  
from app.token.jwt_util import *  

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing data'}), 400
    
    existing_user = mongo.db.users.find_one({'email': data['email']})
    if existing_user:
        return jsonify({'error': 'Email already in use'}), 409

    # Hash password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    user = User(data['username'], data['email'], hashed_password.decode('utf-8'))
    result = mongo.db.users.insert_one(user.__dict__)
    uID=str(result.inserted_id)
    # Generate token
    token = generate_token(str(result.inserted_id))


    return jsonify({'user': "user registered",'userID':uID, 'token': token}), 201



@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400

    user = mongo.db.users.find_one({'email': data['email']})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    print(user)
    user['_id'] = str(user['_id'])
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
     
        token = generate_token(str(user['_id']))
        return jsonify({'message': 'Login successful', 'userID':user['_id'], 'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    

@auth_bp.route('/logout', methods=['POST'])
@token_required  
def logout_user():
    auth_token = request.headers.get('Authorization')
    if auth_token:
        result = delete_token(auth_token)
        if result['status'] == 'success':
            return jsonify({'message': result['message']}), 200
        else:
            return jsonify({'error': result['message']}), 400
    else:
        return jsonify({'error': 'No token provided'}), 403

