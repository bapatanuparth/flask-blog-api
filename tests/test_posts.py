import pytest
from app import create_app
from app.config import TestingConfig
from bson import ObjectId
from flask import json

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

@pytest.fixture
def headers():
    # Simulate obtaining a valid token
    return {'Authorization': 'Bearer valid_token'}


@pytest.fixture(autouse=True)
def mock_verify_token(monkeypatch):
    def verify(token):
        return {'status': 'success', 'message': 'Token is valid', 'user_id': 'some_user_id'}
    monkeypatch.setattr('app.token.jwt_util.verify_token', verify)

################ CREATE POST ####################
def test_create_post(client, headers):
    """Test creating a new blog post after logging in a user."""

    login_data = {'email': 'login@example.com', 'password': 'loginpassword'}
    login_response = client.post('/auth/login', json=login_data)
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    assert 'userID' in login_data 
    user_id = login_data['userID']

    """Test creating a new blog post."""
    post_data = {'title': 'New Post', 'content': 'Content of the new post', 'author_id': user_id}
    response = client.post('/blogpost', json=post_data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Post created successfully'
    assert 'post' in data

def test_create_post_missing_fields(client, headers):
    """Test creating a new blog post with missing required fields."""
    
    post_data = {'content': 'Content of the new post', 'author_id': 'some_user_id'}
    response = client.post('/blogpost', json=post_data, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Missing required fields'

def test_create_post_no_data(client, headers):
    """Test creating a new blog post without sending any data."""
    response = client.post('/blogpost', json={}, headers=headers) 
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No data provided'

############# GET POSTS BY USER ################
def test_get_posts_by_user(client, headers):
    """Test retrieving all blog posts by userID after login"""

    login_data = {'email': 'login@example.com', 'password': 'loginpassword'}
    login_response = client.post('/auth/login', json=login_data)
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    assert 'userID' in login_data  
    user_id = login_data['userID']

    """Test retrieving posts for a specific user."""
    response = client.get(f'/allPosts/{user_id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'posts' in data 

def test_get_posts_by_nonexistent_user(client, headers):
    """Test retrieving posts for a non-existent user."""
    # Generate a random or specific user ID that is unlikely to exist
    nonexistent_user_id = '12345'  

    response = client.get(f'/allPosts/{nonexistent_user_id}', headers=headers)
    assert response.status_code == 404  
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No posts found for the user'

############# GET POST BY ID ############
def test_get_post_by_id(client, headers):
    """Test creating a new blog post after logging in a user."""
  
    login_data = {'email': 'login@example.com', 'password': 'loginpassword'}
    login_response = client.post('/auth/login', json=login_data)
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    assert 'userID' in login_data  
    user_id = login_data['userID']

    """Test creating a new blog post."""
    post_data = {'title': 'New Post for second test', 'content': 'Content of the new post', 'author_id': user_id}
    response = client.post('/blogpost', json=post_data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Post created successfully'
    assert 'post' in data
    post_id = data['post']['_id']

    """Test retrieving a single post by ID.""" 
    retrieve_response = client.get(f'/blogpost/{post_id}', headers=headers)
    assert retrieve_response.status_code == 200
    retrieve_data = retrieve_response.get_json()
    assert 'title' in retrieve_data and retrieve_data['title'] == post_data['title']
    assert 'content' in retrieve_data and retrieve_data['content'] == post_data['content']
    assert 'author_id' in retrieve_data and retrieve_data['author_id'] == post_data['author_id']

def test_get_post_by_nonexisting_id(client, headers):
    post_id=ObjectId()
    """Test retrieving a single post by ID.""" 
    retrieve_response = client.get(f'/blogpost/{post_id}', headers=headers)
    assert retrieve_response.status_code == 404



############### UPDATE ########################
def test_update_post_by_id(client, headers):
    """Test creating a new blog post after logging in a user."""
    # First, log in the user to get a valid user ID
    login_data = {'email': 'login@example.com', 'password': 'loginpassword'}
    login_response = client.post('/auth/login', json=login_data)
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    assert 'userID' in login_data  # Ensure that login response has 'userID'
    user_id = login_data['userID']

    """Test creating a new blog post."""
    post_data = {'title': 'New Post for second test', 'content': 'Content of the new post', 'author_id': user_id}
    response = client.post('/blogpost', json=post_data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Post created successfully'
    assert 'post' in data
    post_id = data['post']['_id']

    """Test updating an existing post."""
    update_data = {'title': 'Updated Title', 'content': 'Updated content'}
    response = client.put(f'/blogpost/{post_id}', json=update_data, headers=headers)
    assert response.status_code == 200
    retrieve_data = response.get_json()
    assert 'title' in retrieve_data and retrieve_data['title'] == update_data['title']
    assert 'content' in retrieve_data and retrieve_data['content'] == update_data['content']

def test_update_post_no_data(client, headers):
    """Test creating a new blog post after logging in a user."""

    login_data = {'email': 'login@example.com', 'password': 'loginpassword'}
    login_response = client.post('/auth/login', json=login_data)
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    assert 'userID' in login_data  
    user_id = login_data['userID']

    """Test creating a new blog post."""
    post_data = {'title': 'New Post for second test', 'content': 'Content of the new post', 'author_id': user_id}
    response = client.post('/blogpost', json=post_data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Post created successfully'
    assert 'post' in data
    post_id = data['post']['_id']

    """Test updating an existing post with no data provided."""
    response = client.put(f'/blogpost/{post_id}', json={}, headers=headers) 
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No data provided'

def test_update_nonexistent_post(client, headers):
    """Test updating a non-existent post."""
    post_id = str(ObjectId())  
    update_data = {'title': 'New Title', 'content': 'New content'}
    response = client.put(f'/blogpost/{post_id}', json=update_data, headers=headers)
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Post not found or no changes to update'

############### DELETE ###########################
def test_delete_existing_post(client, headers):
    """Test deleting an existing post."""
   
    post_data = {'title': 'Post to Delete', 'content': 'Content of the post to delete', 'author_id': str(ObjectId())}
    create_response = client.post('/blogpost', json=post_data, headers=headers)
    assert create_response.status_code == 201  
    post_id = create_response.get_json()['post']['_id']

    delete_response = client.delete(f'/blogpost/{post_id}', headers=headers)
    assert delete_response.status_code == 200
    delete_data = delete_response.get_json()
    assert delete_data['message'] == 'Post deleted successfully'

def test_delete_nonexistent_post(client, headers):
    """Test attempting to delete a post that does not exist."""
    nonexistent_post_id = str(ObjectId())  # Generate a valid but non-existent ObjectId
    response = client.delete(f'/blogpost/{nonexistent_post_id}', headers=headers)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Post not found'
