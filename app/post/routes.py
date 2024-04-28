from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from . import post_bp 
from bson import ObjectId
from bson import json_util
from bson.json_util import dumps
from flask import jsonify, request, current_app, Response
import bcrypt
from app.extensions import mongo
from app.models.post import Post  
from app.token.jwt_util import generate_token, verify_token, token_required 
from . import post_bp
import json

from flask import request, jsonify
from functools import wraps


@post_bp.route('/blogpost', methods=['POST'])
@token_required
def create_post():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title')
    content = data.get('content')
    author_id = data.get('author_id')  

    if not title or not content or not author_id:
        return jsonify({'error': 'Missing required fields'}), 400

    new_post = Post(title=title, content=content, author_id=author_id)
    result = mongo.db.posts.insert_one(new_post.__dict__)
    
    if result.inserted_id:
        return jsonify({'message': 'Post created successfully', 'post': new_post.to_dict()}), 201
    else:
        return jsonify({'error': 'Failed to create post'}), 500
   


@post_bp.route('/allPosts/<user_id>', methods=['GET'])
@token_required
def get_posts_by_user(user_id):
    posts_ = mongo.db.posts.find({'author_id': user_id})
    posts = list(posts_)
    if posts:
       
        encoded_data = json.dumps({'posts': posts}, cls=current_app.json_encoder)
        return Response(encoded_data, mimetype='application/json')
    else:
        return jsonify({'error': 'No posts found for the user'}), 404


@post_bp.route('/blogpost/<post_id>', methods=['GET'])
@token_required
def get_post_by_id(post_id):
    
    post = mongo.db.posts.find_one({'_id': ObjectId(post_id)})
   
    if post:
        encoded_data = json.dumps(post, cls=current_app.json_encoder)
        return Response(encoded_data, mimetype='application/json')
    else:
        return jsonify({'error': 'Post not found'}), 404


@post_bp.route('/blogpost/<post_id>', methods=['PUT'])
@token_required
def update_post_by_id(post_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title')
    content = data.get('content')

    if not title and not content:
        return jsonify({'error': 'Nothing to update'}), 400

    update_data = {}
    if title:
        update_data['title'] = title
    if content:
        update_data['content'] = content

    result = mongo.db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': update_data})

    if result.modified_count > 0:
        updated_post = mongo.db.posts.find_one({'_id': ObjectId(post_id)})
        if updated_post:
          
            encoded_data = json.dumps(updated_post, cls=current_app.json_encoder)
            return Response(encoded_data, mimetype='application/json')
        else:
           
            return jsonify({'error': 'Updated post could not be fetched'}), 500
       
    else:
        return jsonify({'error': 'Post not found or no changes to update'}), 404


@post_bp.route('/blogpost/<post_id>', methods=['DELETE'])
@token_required
def delete_post_by_id(post_id):
    result = mongo.db.posts.delete_one({'_id': ObjectId(post_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Post deleted successfully'}), 200
    else:
        return jsonify({'error': 'Post not found'}), 404

